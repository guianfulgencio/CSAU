from netmiko import ConnectHandler


HOST = "" #Host name
USER = "" #Username to access the router
PASS = "" #Pasword for authentication
TYPE = "" #Device type

#Using Netmiko's ConnectHandler class initiate a connection to the device
r1 = ConnectHandler(host=HOST, username=USER, password=PASS, device_type=TYPE)
