import argparse
import datetime
import logging
import os
import os.path as osp
import queue
import threading
import time
from typing import Optional, Dict, Union

from fastapi import FastAPI
from serial import Serial

from arizon_usb_apiserver import Config as SensorConfig
from arizon_usb_apiserver import Sensor

app = FastAPI()


class Application:
    logger: logging.Logger
    option: SensorConfig
    start_fifo_ev: threading.Event
    force_data_queue: queue.Queue

    def __init__(self, cfg) -> None:
        if isinstance(cfg, SensorConfig):
            self.option = cfg
        elif isinstance(cfg, str):
            self.option = SensorConfig(cfg)
        elif isinstance(cfg, argparse.Namespace):
            self.option = SensorConfig(cfg.config)
        else:
            raise TypeError(
                "cfg must be SensorConfig, str, or argparse.Namespace"
            )
        if self.option.valid is False:
            raise ValueError("invalid config file")

        self.logger = logging.getLogger("arizon.main")
        self.start_fifo_ev = threading.Event()
        self.start_recording_ev = threading.Event()
        self.force_data_queue = queue.Queue(maxsize=1024)
        self.state = {
            "recording": False
        }
        self.state_lock = threading.Lock()
        self.recording_thread: Optional[threading.Thread] = None

    def start_thread(self):
        self.logger.info(f"start force data collection thread, serial port: {[p.port for p in self.option.serials]}")

        def update_arizon_sensor_thread(sensor_idx: int):
            while True:
                self.start_fifo_ev.wait()

                conn = Serial(self.option.serials[sensor_idx].port, self.option.serials[sensor_idx].baudrate)
                addr = self.option.serials[sensor_idx].addr
                sensor = Sensor(conn)
                sensor.reset()
                while not self.force_data_queue.empty():
                    self.force_data_queue.get_nowait()
                while True:
                    data = sensor.read_once()
                    if data is None:
                        continue
                    while self.force_data_queue.full():
                        self.force_data_queue.get(block=False)
                    self.force_data_queue.put(
                        {
                            "addr": str(data[0]) if addr is None or addr == "" else addr,
                            "f": data[1],
                            "index": data[2],
                            "sys_ts_ns": time.time_ns()
                        },
                        block=False
                    )
                    if not self.start_fifo_ev.is_set():
                        conn.close()
                        break

        for idx, s in enumerate(self.option.serials):
            threading.Thread(target=update_arizon_sensor_thread, args=(idx,),
                             daemon=True).start()

    def shutdown(self):
        return None

    def start_fifo(self) -> Optional[Exception]:
        self.state_lock.acquire()
        if self.state['recording']:
            self.state_lock.release()
            return Exception("already recording")
        else:
            self.logger.info("starting force data collection")
            self.start_fifo_ev.set()
            self.state_lock.release()
            return None

    def stop_fifo(self) -> Optional[Exception]:
        self.state_lock.acquire()
        if self.state['recording']:
            self.state_lock.release()
            return Exception("already recording")
        else:
            self.logger.info("stopping force data collection")
            self.start_fifo_ev.clear()
            self.state_lock.release()
            return None

    def clean_cached_force(self) -> Optional[Exception]:
        for _ in range(self.force_data_queue.qsize()):
            if not self.force_data_queue.empty():
                self.force_data_queue.get(block=False)
        return None

    @property
    def fifo_status(self) -> bool:
        return self.start_fifo_ev.is_set()

    def get(self, recording=False) -> Optional[Dict[str, Union[int, float]]]:
        if self.state['recording'] and not recording:
            return None
        try:
            return self.force_data_queue.get(timeout=1e-2)
        except queue.Empty:
            return None

        except Exception as e:
            self.logger.error(f"error: {e}")
            return None

    def start_recording(self, tag: str) -> Optional[Exception]:
        self.state_lock.acquire()
        if self.state['recording']:
            self.state_lock.release()
            return Exception("already recording")
        self.state["recording"] = True
        self.state_lock.release()

        if tag is None or tag == "":
            tag = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        tagged_path = osp.join(self.option.data_path, tag)
        if not osp.exists(tagged_path):
            os.makedirs(tagged_path)

        self.start_recording_ev.set()
        self.start_fifo_ev.clear()
        time.sleep(1e-2)
        self.clean_cached_force()
        self.start_fifo_ev.set()

        def record_thread():
            self.logger.info(f"starting recording thread, tag: {tag}")
            handles = {
                s.addr: open(osp.join(tagged_path, f"{s.addr}.csv"), "w") for s in self.option.serials
            }
            while True:
                data = self.get(recording=True)
                if data is None:
                    time.sleep(1e-2)
                else:
                    handles[data['addr']].write(f"{data['index']},{data['sys_ts_ns']},{data['addr']},{data['f']}\n")
                if not self.start_recording_ev.is_set():
                    break
            [f.close() for _, f in handles.items()]

        t = threading.Thread(target=record_thread, daemon=True)
        t.start()
        self.recording_thread = t
        return None

    def stop_recording(self) -> Optional[Exception]:
        self.state_lock.acquire()
        if not self.state['recording']:
            self.state_lock.release()
            return Exception("not recording")
        self.start_recording_ev.clear()
        self.recording_thread.join()
        self.state["recording"] = False
        self.state_lock.release()
        return None


if __name__ == '__main__':
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="./arizon_config.yaml")
    run_args = parser.parse_args(sys.argv[1:])

    logging.basicConfig(level=logging.INFO)

    app = Application(run_args)
    app.start_thread()

    app.start_fifo_ev.set()

    try:
        while True:
            print(app.get())

    except KeyboardInterrupt as e:
        app.shutdown()
