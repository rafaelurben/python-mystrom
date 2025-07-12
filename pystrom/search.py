import logging
import socket

from pystrom.device import MyStromDevice, MyStromDeviceFactory

logger = logging.getLogger(__name__)


class MyStromSearch:
    """
    Search for MyStrom devices on the local network by listening for UDP broadcasts.

    Usage:

        with MyStromSearch() as searcher:
            devices = searcher.search_all()
            for device in devices:
                print(device)
    """

    def __init__(self, ip: str = "0.0.0.0", port: int = 7979):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet (IPv4) / UDP
        self.ip = ip
        self.port = port

    def __enter__(self):
        self.sock.bind((self.ip, self.port))
        logger.debug("Socket bound to %s:%s", self.ip, self.port)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.close()
        logger.debug("Socket closed")

    def search_all(self) -> list[MyStromDevice]:
        logger.info("Looking for devices...")

        ips_found = []
        devices_found = []

        try:
            while True:
                self.sock.settimeout(5.0)
                data, (ip, port) = self.sock.recvfrom(1024)  # buffer size is 1024 bytes

                if ip not in ips_found:
                    x = MyStromDeviceFactory.from_announcement(data, ip)
                    logger.info("Found device: %s", x)

                    ips_found.append(ip)
                    devices_found.append(x)
                else:
                    break
        except socket.timeout:
            pass

        logger.info("%s devices found!", len(devices_found))
        return devices_found

    def search_live(self):
        logger.info("Looking for devices... (Press Ctrl+C to exit!)")

        try:
            while True:
                try:
                    self.sock.settimeout(5.0)
                    data, (ip, port) = self.sock.recvfrom(1024)  # buffer size is 1024 bytes

                    x = MyStromDeviceFactory.from_announcement(data, ip)
                    logger.info("Found device: %s", x)
                except socket.timeout:
                    pass
        except KeyboardInterrupt:
            pass
