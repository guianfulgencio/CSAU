from netmiko import ConnectHandler

HOST = "csr1kv1"  # Host name
USER = "cisco"  # Username
PASS = "cisco"  # Password for authentication
TYPE = "cisco_xe"  # Device type

device = ConnectHandler(host=HOST, username=USER, password=PASS, device_type=TYPE)

router = HOST
print("Connecting to {}".format(router))

print("Sending SNMP Configurations to {}...".format(router))

file_path = "./configs/{}.cfg".format(router)
device.send_config_from_file(file_path)
print("Commands sent to device...")

print("Verifying Configuration {}...".format(router))

snmp_config = device.send_command("show run | include snmp-server")
print(snmp_config)
print("Disconnecting from {}...".format(router))
