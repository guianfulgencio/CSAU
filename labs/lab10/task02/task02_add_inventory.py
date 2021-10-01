#! /usr/bin/env python

import requests
import json

# Check for module dependencies:
not_installed_modules = []

try:
    from requests.auth import HTTPBasicAuth
except ImportError:
    not_installed_modules.append("requests")
try:
    import yaml
except ImportError:
    not_installed_modules.append("PyYAML")


if not_installed_modules:
    print("Please install following Python modules:")

    for module in not_installed_modules:
        print("  - {module}").format(module=module)

    sys.exit(1)

HTTP_HEADERS = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json",
}

HTTP_AUTH = HTTPBasicAuth("cisco", "cisco")

# Disable Insecure SSL warnings
requests.packages.urllib3.disable_warnings()


def get_inventory():
    pass


def get_serial_data(host):

    url = (
        "https://{host}/restconf/data/Cisco-IOS-XE-native:native"
        "/license/udi/sn".format(host=host)
    )
    response = requests.get(url, headers=HTTP_HEADERS, auth=HTTP_AUTH, verify=False)
    result = json.loads(response.text)
    serial_data = result["Cisco-IOS-XE-native:sn"]
    return serial_data


def get_version_data(host):

    url = "https://{host}/restconf/data/Cisco-IOS-XE-native:native" "/version".format(
        host=host
    )
    response = requests.get(url, headers=HTTP_HEADERS, auth=HTTP_AUTH, verify=False)
    result = json.loads(response.text)
    version_data = result["Cisco-IOS-XE-native:version"]
    return version_data


def get_hostname(host):
    url = "https://{host}/restconf/data/Cisco-IOS-XE-native:native" "/hostname".format(
        host=host
    )
    response = requests.get(url, headers=HTTP_HEADERS, auth=HTTP_AUTH, verify=False)
    result = json.loads(response.text)
    hostname = result.get("Cisco-IOS-XE-native:hostname")

    return hostname


def structure_data():

    devices = {}
    net_inventory = get_inventory()
    for host in net_inventory:
        devices[host] = {}
        devices[host]["os_version"] = get_version_data(host)
        devices[host]["serial_number"] = get_serial_data(host)
        devices[host]["hostname"] = get_hostname(host)

    return devices


def main():

    heading = "|{:^10} | {:^10} | {:^12} | {:^15}|".format(
        "Device", "Hostname", "OS Version", "Serial Number"
    )
    print(len(heading) * "-")
    print(heading)
    print(len(heading) * "-")
    for hostname, details in structure_data().items():

        print(
            "|{:^10} | {:^10} | {:^12} | {:^15}|".format(
                hostname,
                details["hostname"],
                details["os_version"],
                details["serial_number"],
            )
        )
        print(len(heading) * "-")


if __name__ == "__main__":
    main()
