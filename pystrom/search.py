import logging
import socket

from pystrom.device import MyStromDevice

logger = logging.getLogger(__name__)


class MyStromSearch:
    UDP_IP = "0.0.0.0"
    UDP_PORT = 7979

    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))

    @classmethod
    def searchall(cls):
        logger.info("Looking for devices...")

        ipsfound = []
        devicesfound = []

        try:
            while True:
                cls.sock.settimeout(5.0)
                data, addr = cls.sock.recvfrom(1024)  # buffer size is 1024 bytes

                if not addr[0] in ipsfound:
                    x = MyStromDevice.from_announcement(data, addr[0])
                    logger.info("Found device: %s", x)

                    ipsfound.append(addr[0])
                    devicesfound.append(x)
                else:
                    break
        except socket.timeout:
            pass

        logger.info("%s devices found!", len(devicesfound))
        return devicesfound

    @classmethod
    def searchlive(cls):
        logger.info("Looking for devices... (Press Ctrl+C to exit!)")

        try:
            while True:
                try:
                    cls.sock.settimeout(5.0)
                    data, addr = cls.sock.recvfrom(1024)  # buffer size is 1024 bytes

                    x = MyStromDevice.from_announcement(data, addr[0])
                    logger.info("Found device: %s", x)
                except socket.timeout:
                    pass
        except KeyboardInterrupt:
            pass
