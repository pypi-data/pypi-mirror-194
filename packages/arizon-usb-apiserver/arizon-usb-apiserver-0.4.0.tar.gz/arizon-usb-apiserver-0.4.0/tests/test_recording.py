import logging
import time
from arizon_usb_apiserver.apiserver import Application

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    app = Application("./arizon_config.yaml")
    app.start_thread()

    for i in range(3):
        app.start_recording(None)
        time.sleep(10)
        app.stop_recording()
        app.shutdown()