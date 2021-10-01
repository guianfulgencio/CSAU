vlan_ids = []

#Adds 5 vlans to the list with while-loop
vlan = 100

while 5 < len(vlan_ids):
  vlan_ids.append(vlan)
  vlan += 100

print(vlan_ids)

