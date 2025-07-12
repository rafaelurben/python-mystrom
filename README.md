# python-mystrom aka. pystrom

This is an unofficial Python integration for finding and controlling local MyStrom devices.

Due to the lack of owned devices, some features may not be fully implemented or tested. The project is primarily
developed and tested with the MyStrom Wi-Fi Switch CH.

> [!IMPORTANT]  
> This project is not developed by [MyStrom](https://mystrom.ch) nor affiliated with them in any way.

Official MyStrom API Documentation: [https://api.mystrom.ch/](https://api.mystrom.ch/)

## Installation

Installation requires [Python](https://www.python.org/downloads/)
and [Pip](https://pip.pypa.io/en/stable/installation/) (which usually comes with Python).

`python -m pip install -U pystrom`

## Features

This library provides a simple [CLI](#console-commands) and a [Python API](#python-api).

### Console Commands

| Command                           | Function                                                     |
|-----------------------------------|--------------------------------------------------------------|
| `python -m pystrom search`        | Search for MyStrom devices in the local network              |
| `python -m pystrom search --live` | Continuously search for MyStrom devices in the local network |

### Python API

#### Get device objects

You can use the `MyStromSearch` class to find devices in your local network. It will return a list of `MyStromDevice`
objects or subclasses thereof.

```python
from pystrom.search import MyStromSearch

with MyStromSearch() as searcher:
    devices = searcher.search_all()  # will take 5 seconds
    for device in devices:
        print(device)
```

You can also create a `MyStromDevice` object by using the `MyStromDeviceFactory.from_ip` method, which only requires the
IP address of the device:

```python
from pystrom.device import MyStromDeviceFactory

device = MyStromDeviceFactory.from_ip("192.168.1.220")
print(device)
```

#### Control devices

The following API methods are available for controlling devices:

##### General (`MyStromDevice`)

| Method                | Function                              |
|-----------------------|---------------------------------------|
| `.get_general_info()` | Get general device information        |
| `.get_wifi_list()`    | Get reachable Wi-Fi networks          |
| `.get_help()`         | Get a list of available API endpoints |
| `.get_settings()`     | Get current device settings           |
| `.set_settings()`     | Set or update device settings         |

##### Switch (`MyStromSwitch`)

| Method               | Function                                              |
|----------------------|-------------------------------------------------------|
| `.turn_on()`         | Turn on the switch                                    |
| `.turn_off()`        | Turn off the switch                                   |
| `.toggle()`          | Toggle the switch state and return the new state      |
| `.power_cycle()`     | Power cycle the switch (off, wait, then on)           |
| `.timer()`           | Set the state and reverse it after a specified time   |
| `.get_report()`      | Get a report of the switch's current state            |
| `.get_temperature()` | Get the current temperature reading and configuration |

##### Bulb (`MyStromBulb`)

| Method                      | Function                                                 |
|-----------------------------|----------------------------------------------------------|
| `.turn_on()`                | Turn on the bulb                                         |
| `.turn_off()`               | Turn off the bulb                                        |
| `.toggle()`                 | Toggle the bulb state                                    |
| `.set_options()`            | Set options like color, ramp, mode, and notifyurl        |
| `.get_device_information()` | Get the device information, including current bulb state |

##### Other devices and missing endpoints

Other device types are not yet implemented with specific classes, but you can still interact with them:

To control them, you can use the manuel API methods of the `MyStromDevice` class, which allows you to send HTTP requests
to the device's API endpoints.

| Method        | Function                                         |
|---------------|--------------------------------------------------|
| `.api_get()`  | Send a GET request to the device's API endpoint  |
| `.api_post()` | Send a POST request to the device's API endpoint |
