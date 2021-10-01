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
        print("  - {module}".format(module=module))

    sys.exit(1)

requests.packages.urllib3.disable_warnings()

HTTP_HEADERS = {
    "Content-Type": "application/yang-data+json", 
    "Accept": "application/yang-data+json", 
}

HTTP_AUTH = HTTPBasicAuth("cisco", "cisco")

def get_inventory():
    inventory = {
        "csr1kv1": {"username": "cisco", "password": "cisco"},
        "csr1kv2": {"username": "cisco", "password": "cisco"},
    }

    return inventory

def get_serial_data(host):

    url = "https://{host}/restconf/data/Cisco-IOS-XE-native:native" "/license/udi/sn".format(host=host)
    response = requests.get(url=url, headers=HTTP_HEADERS, auth=HTTP_AUTH, verify=False)

    #print("Status Code: {}".format(response.status_code))
    #print("Returned Data:\n{}".format(response.text))
    #print(type(response.text))

    result = json.loads(response.text)
    #print(type(result))
    serial_data = result["Cisco-IOS-XE-native:sn"]
    return serial_data

def get_version_data(host):

    url = "https://{host}/restconf/data/Cisco-IOS-XE-native:native" "/version".format(host=host)
    response = requests.get(url, headers=HTTP_HEADERS, auth=HTTP_AUTH, verify=False)

    result = response.json()


def get_hostname(host):
    url = "https://{host}/restconf/data/Cisco-IOS-XE-native:native" "/hostname".format(
        host=host
    )
    response = requests.get(url, headers=HTTP_HEADERS, auth=HTTP_AUTH, verify=False)
    result = json.loads(response.text)
    hostname = result.get("Cisco-IOS-XE-native:hostname")

    return hostname
    version_data = result["Cisco-IOS-XE-native:version"]
    return version_data


def structure_data():

    devices = {}
    net_inventory = get_inventory()
    for host in net_inventory:
        devices[host] = {}
        devices[host]["serial_number"] = get_serial_data(host)
        devices[host]["os_version"] = get_version_data(host)
        devices[host]["hostname"] = get_hostname(host)
    return devices


def main():

    structured_data = structure_data()

    heading = "| {:^10} | {:^10} | {:^15} | {:^12} |".format(
        "Device", "Hostname", "Serial Number", "OS Version"
    )
    print(len(heading) * "-")
    print(heading)
    print(len(heading) * "-")
    for hostname, details in structured_data.items():
        print(
            "| {:^10} | {:^10} | {:^15} | {:^12} |".format(
                hostname,
                details["hostname"],
                details["serial_number"],
                details["os_version"],
            )
        )
        print(len(heading) * "-")

if __name__ == "__main__":
    main()
