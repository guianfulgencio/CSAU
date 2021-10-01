from netmiko import ConnectHandler


HOST = "csr1kv1" #Host name
USER = "cisco" #Username to access the router
PASS = "cisco" #Pasword for authentication
TYPE = "cisco_xe" #Device type

#Using Netmiko's ConnectHandler class initiate a connection to the device
r1 = ConnectHandler(host=HOST, username=USER, password=PASS, device_type=TYPE)
