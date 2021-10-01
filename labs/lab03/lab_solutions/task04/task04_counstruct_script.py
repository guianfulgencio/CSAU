from netmiko import ConnectHandler

inventory = {
    "csr1kv1": {
        "ip_addr": "10.254.0.1",
        "username": "cisco",
        "password": "cisco",
        "device_type": "cisco_xe",
    },
    "csr1kv2": {
        "ip_addr": "10.254.0.2",
        "username": "cisco",
        "password": "cisco",
        "device_type": "cisco_xe",
    },
    "csr1kv3": {
        "ip_addr": "10.254.0.3",
        "username": "cisco",
        "password": "cisco",
        "device_type": "cisco_xe",
    },
}

ip_info = {
    "csr1kv1": {
        "Loopback10": {
            "ip": "10.200.10.1",
            "mask": "255.255.255.0",
        }
    },
    "csr1kv2": {
        "Loopback20": {
            "ip": "10.200.20.2",
            "mask": "255.255.255.0",
        }
    },
    "csr1kv3": {
        "Loopback30": {
            "ip": "10.200.30.3",
            "mask": "255.255.255.0",
        }
    },
}

# Templates for interface and IP configuration
show_run_template = "show run {}" 
interface_template = "interface {}"
interface_ip_template = "ip address {} {}"

# Iterating over ip_info dictionary an
for hostname, ip_data in ip_info.items():
    username = inventory[hostname]["username"]  # The hostname is used to obtain the value of username from inventory variable
    password = inventory[hostname]["password"]  # The hostname is used to obtain the value of password from inventory variable
    device_type = inventory[hostname]["device_type"] # The hostname is used to obtain the value of device_type from inventory variable
    print("Establishing connection with {}".format(hostname))
    device = ConnectHandler(
        host=hostname,
        username=username,
        password=password,
        device_type=device_type,
    )  # Initiating a connection to the device
    for interface, details in ip_data.items():
        commands = []
        interface_command = interface_template.format(
            interface
        )
        commands.append(interface_command)
        interface_ip_command = interface_ip_template.format(
            details["ip"], details["mask"]
        )
        commands.append(interface_ip_command)
    print(commands) # print the commands and make sure the format is correct
    print("Applying the configuration")
    device.send_config_set(commands)
    print("Validating if the configuration was successfully applied...")
    show_command = show_run_template.format(commands[0])
    show_run_output = device.send_command(show_command)
    print(show_run_output)
    print("Disconnecting from the {} ".format(hostname))
    device.disconnect()
