import logging
from json import JSONDecodeError

import requests

from pystrom.exceptions import MyStromException

logger = logging.getLogger(__name__)

DEVICE_TYPE_NAME_MAP = {
    101: "Switch CH v1",
    102: "Bulb",
    103: "Button+ 1st gen",
    104: "Button small/simple",
    105: "LED Strip",
    106: "Switch CH v2",
    107: "Switch EU",
    110: "Motion Sensor",
    112: "Gateway",
    113: "modulo® STECCO / CUBO",
    118: "Button+ 2nd gen",
    120: "Switch Zero",
}


class MyStromDevice:
    """Base class for MyStrom devices. All MyStrom devices inherit from this class."""

    def __init__(self, ip: str, mac: str, device_type: int):
        """Do not instantiate this class directly; use MyStromDeviceFactory to create device instances."""
        self.ip: str = ip
        self.mac: str = mac
        self.device_type: int = device_type
        self.settings: dict = {}

    # Properties

    @property
    def type_name(self) -> str:
        """Returns the name of the device type based on the device_type integer."""
        if self.device_type in DEVICE_TYPE_NAME_MAP:
            return DEVICE_TYPE_NAME_MAP[self.device_type]
        else:
            return f"Unknown type: {str(self.device_type)}"

    @property
    def name(self) -> str:
        """Returns the name of the device. Must have fetched settings first."""
        return self.settings.get("name", "Name unknown")

    def __str__(self):
        return f"<{self.__class__.__name__} ({self.type_name}) '{self.name}' {self.mac} @ {self.ip}>"

    # Base API

    def api_request(self, method: str, path: str, **kwargs) -> dict | list | str | None:
        """Sends a request to the device API and returns the response in an appropriate format."""
        protocol = "http"
        url = f"{protocol}://{self.ip}/{path.lstrip('/')}"
        logger.info("Requesting %s %s", method.upper(), url)
        r = requests.request(method, url, **kwargs)
        if r.status_code < 200 or r.status_code >= 300:
            logger.error("Error %d while requesting %s", r.status_code, url)
            raise MyStromException(f"Error {r.status_code} while requesting {url}: {r.text}")
        try:
            return r.json()
        except JSONDecodeError:
            return r.text

    def api_get(self, path, **kwargs) -> dict | list | str:
        """Sends a GET request to the device API and returns the response in an appropriate format."""
        return self.api_request("GET", path, **kwargs)

    def api_post(self, path, **kwargs) -> dict | list | str:
        """Sends a POST request to the device API and returns the response in an appropriate format."""
        return self.api_request("POST", path, **kwargs)

    # General API Endpoints

    def get_general_info(self) -> dict:
        """Returns general device information such as network settings, type, firmware version, etc."""
        return self.api_get("api/v1/info")

    def get_wifi_list(self) -> dict[str, int]:
        """Returns a dictionary of available WiFi networks with their signal strength."""
        data = self.api_get("api/v1/scan")
        networks = {}
        for i in range(len(data) // 2):
            networks[data[i * 2]] = data[i * 2 + 1]
        return networks

    def get_help(self) -> str:
        """Returns a string containing a list of available API endpoints."""
        return self.api_get("help")

    # Common Settings API Endpoints

    def get_settings(self) -> dict:
        """Returns the current settings of the device."""
        self.settings = self.api_get("api/v1/settings")
        return self.settings

    def set_settings(self, settings: dict):
        """Sets/Updates the device settings."""
        self.api_post("api/v1/settings", data=settings)


    # Switch

    def switch_on(self):
        return self.api_get("relay?state=1")

    def switch_off(self):
        return self.api_get("relay?state=0")

    def switch_toggle(self):
        return self.api_get("toggle")

    def switch_report(self):
        return self.api_get("report")


class MyStromDeviceFactory:
    all_devices: dict[str, MyStromDevice] = {}

    @classmethod
    def _get_or_create_device(cls, mac: str, ip: str, device_type: int) -> MyStromDevice:
        if mac not in cls.all_devices:
            device = MyStromDevice(ip=ip, mac=mac, device_type=device_type)
            cls.all_devices[mac] = device
            return device
        else:
            return cls.all_devices[mac]

    @classmethod
    def from_announcement(cls, data: bytes, ip: str) -> "MyStromDevice":
        mac = data[:6].hex()
        device_type = data[6]
        # flags = data[7]

        return cls._get_or_create_device(mac=mac, ip=ip, device_type=device_type)

    @classmethod
    def from_ip(cls, ip: str) -> "MyStromDevice":
        r = requests.get(f"http://{ip}/api/v1/info")
        if r.status_code != 200:
            raise ConnectionError(f"Could not connect to device at {ip}")
        data = r.json()
        mac = data.get("mac")
        device_type = data.get("type")
        if not mac or not device_type:
            raise ValueError("Invalid device data received from the API")

        return cls._get_or_create_device(mac=mac, ip=ip, device_type=device_type)
