config_data = {
    "csr1kv1": {
        "banner": "This Device is being monitored 24/7.",
        "mgmt_ip": "10.254.0.1",
        "interface_data": [
            {
                "if_name": "GigabitEthernet1",
                "state": "no shutdown",
                "mode": "access",
                "config": "10",
            },
            {
                "if_name": "GigabitEthernet2",
                "state": "up",
                "mode": "routing",
                "config": "10.12.0.1",
            },
            {
                "if_name": "GigabitEthernet3",
                "state": "up",
                "mode": "routing",
                "config": "10.13.0.1",
            },
        ],
    },
    "csr1kv2": {
        "banner": "This Device is being monitored 24/7.",
        "mgmt_ip": "10.254.0.2",
        "interface_data": [
            {
                "if_name": "GigabitEthernet1",
                "state": "up",
                "mode": "routing",
                "config": "10.12.0.2",
            },
            {
                "if_name": "GigabitEthernet2",
                "state": "shutdown",
                "mode": "access",
                "config": "20",
            },
            {
                "if_name": "GigabitEthernet3",
                "state": "up",
                "mode": "routing",
                "config": "10.23.0.2",
            },
        ],
    },
    "csr1kv3": {
        "banner": "This Device is being monitored 24/7.",
        "mgmt_ip": "10.254.0.3",
        "interface_data": [
            {
                "if_name": "GigabitEthernet1",
                "state": "up",
                "mode": "routing",
                "config": "10.13.0.3",
            },
            {
                "if_name": "GigabitEthernet2",
                "state": "up",
                "mode": "routing",
                "config": "10.23.0.3",
            },
            {
                "if_name": "GigabitEthernet3",
                "state": "shutdown",
                "mode": "trunk",
                "config": "30",
            },
        ],
    },
}


for device, config in config_data.items():
    print("Generating configuration for {}".format(device))
    print("#" * 22 + device + "#" * 22)
    print("banner + {} +".format(config["banner"]))
    print("interface GigabitEthernet4")
    print("ip address {} 255.255.255.0".format(config["mgmt_ip"]))
    for interface in config["interface_data"]:
        print("!")
        print("interface {}".format(interface["if_name"]))
        if interface["state"] == "shutdown":
            print("shutdown")
        elif interface["state"] == "up":
            print("no shutdown")
        else:
            print("!INTERFACE STATE UNKNOWN")
        if interface["mode"] == "access":
            print("switctport mode access")
            print("switchport access vlan {}".format(interface["config"]))
        elif interface["mode"] == "routing":
            print("ip address {} 255.255.255.0".format(interface["config"]))
        elif interface["mode"] == "trunk":
            print("switchport mode trunk")
            print("switchport trunk native vlan {}".format(interface["config"]))
    print("#" * 50)
