import yaml
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class SerialConfig:
    port: str
    baudrate: int
    addr: str = field(default='')


@dataclass
class Config:
    path: str = './arizon_config.yaml'
    serials: List[SerialConfig] = field(default_factory=list)
    api_port: int = 8080
    api_interface: str = '0.0.0.0'
    debug: bool = False
    valid: bool = field(default=False, init=False)
    data_path: str = field(default='./arizon_data', init=False)

    def __post_init__(self) -> None:
        err = self.load()
        if err is None:
            self.valid = True
        else:
            self.valid = False

    def load(self) -> Optional[Exception]:
        if self.path is not None:
            try:
                cfg_dict = yaml.load(open(self.path, "r"),
                                     Loader=yaml.SafeLoader)
            except Exception as e:
                return e

            try:
                cfg = cfg_dict['arizon_usb_apiserver']
                self.serials = [SerialConfig(**s) for s in cfg['serials']]
                self.api_port = cfg['api']['port']
                self.api_interface = cfg['api']['interface'] if 'interface' in cfg['api'] else '0.0.0.0'
                self.debug = cfg['debug']
                self.data_path = cfg['data_path'] if 'data_path' in cfg else './arizon_data'
                return None

            except Exception as e:
                return e

        else:
            return Exception("Config path is not set")

    def dump(self) -> Optional[Exception]:
        if self.path is not None:
            try:
                with open(self.path, 'w') as f:
                    yaml.dump({
                        "serials": [
                            {
                                "port": s.port,
                                "baudrate": s.baudrate,
                                "addr": s.addr
                            }
                            for s in self.serials
                        ],
                        "api": {
                            "port": self.api_port,
                            "interface": self.api_interface
                        },
                        "data_path": self.data_path
                    }, f)
                    return None
            except:
                return Exception("Failed to dump config")
        else:
            return Exception("Config path is not set")
