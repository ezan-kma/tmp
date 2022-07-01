import csv
import netmiko
import logging
##import pandas as pd
import platform
import subprocess
from netmiko import ConnectHandler
from operator import index


#Liste IP des clusters#

"""ip_list = ['192.168.100.200', '10.75.54.80', '10.94.51.80','10.91.50.80', '10.41.50.80', '10.92.50.80', '10.14.50.80', '10.81.51.80', '10.95.50.80', '10.76.50.80', '10.42.50.80', 
		   '10.13.51.80', '10.6.50.80', '10.59.50.80', '10.94.50.80', '10.30.50.80', '10.76.51.80', '10.76.52.80', '10.69.50.80', '192.168.28.80', '10.13.50.80', '10.13.56.80',
		   '10.81.50.80', '10.57.1.80', '10.34.50.80', '10.68.50.80', '10.54.50.80', '10.59.51.80', '10.45.50.80', '10.75.50.80', '10.75.52.80', '10.66.50.80', '10.42.51.80', 
		   '10.93.50.80', '10.76.54.80', '10.69.1.80', '10.77.50.80', '10.74.50.80', '10.78.50.80', '10.67.50.80', '10.69.52.80', '10.31.50.80', '10.27.50.80', '10.38.50.80']
"""
"""
ip_list = ['10.75.50.80', '192.168.100.200']

for ip in ip_list:

	net_device = {
	'device_type': 'aruba_os',
	'ip': ip,
	'username': 'admin',
	'password': 'Arub@2015',
	'port':22,
	}
"""
def myping(row):
	parameter = '-n' if platform.system().lower()=='windows' else '-c'

	command = ['ping', parameter, '1', row['IP']]
	response = subprocess.call(command)

	if response == 0:
		return True
	else:
		return False

#print(myping)



########
########
device_list = []
with open("List_iap.csv", encoding='utf-8-sig') as f:
	for row in csv.DictReader(f):
		device_dict = {
			'ip' : row['IP'],
			'device_type' : row['device_type'],
			'username' : row['USERNAME'],
			'password' : row['PASSWORD'],
			'port' : row['SSH PORT'],
		}
		if myping(row) == True :
			device_list.append(device_dict)
		else:
			continue


		logging.basicConfig(filename='iap.log', level=logging.DEBUG)
		logger = logging.getLogger("netmiko")

	#net_connect = netmiko.ConnectHandler(**net_device)
		net_connect = netmiko.ConnectHandler(**device_dict)

	#output = net_connect.send_command("show run | include virtual-controller-ip ")
	#print(output)
		
		print("Adresse IP :", row['IP'])

########
		## Modèle & version de l'équipement
		output2 = net_connect.send_command("show ver | include Ver")
		#print(output2)

		## output2 contient les 2 informations séparées par une virgule.
		## On les enrégistre donc dans 2 variables différentes(model et version)
		model = output2.split(", ")[0]
		
		print("Modèle : ", model)
		version = output2.split(", ")[1]
		
		print("Version : ", version)

########
		## Nom de l'équipement
		output3 = net_connect.send_command("show ru | include name")
		#print(output3)
		#On récupère uniquement la 1ère ligne du resultat de la commande
		name = output3.split("\n")[0]
		#On supprime le mot "name" au début de la ligne
		name = output3.split()[1]
		
		print("Nom : ", name)

########
		## Format de la ligne
		data = [name, row['IP'], model, version]

		with open("List1.csv", "a", newline='') as file: 

	# Créer l'objet file

			obj = csv.writer(file, delimiter =" ",quoting=csv.QUOTE_MINIMAL)
			obj.writerow(data)
			#file.close()

		net_connect.disconnect()