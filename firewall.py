#!/usr/bin/python3

import pprint
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
import os

CONF ={}

console = Console()

def gprint(string):
	console.print(Text(string,style="bold green"))

def rprint(string): 
	console.print(Text(string,style="bold red"))

def fw_reload():
	print(os.popen("sudo firewall-cmd --reload").read())

def fw_get_active_zones():
	zone = os.popen("sudo firewall-cmd --get-active-zones").read()
	CONF["ZONE"] = zone.split("\n")[0]
	print(zone)

def fw_activate():
	gprint("Activating the firewall")
	os.popen("sudo systemctl start firewalld").read()

def fw_get_status():
	state = os.popen("sudo firewall-cmd --state").read()
	if state == "running\n":
		gprint("Firewall is active")
	else:
		rprint("Firewall is not active")
	fw_activate()
	fw_get_active_zones()

def get_zone_list():
	zone_lst = os.popen("sudo firewall-cmd --get-zones").read().split(" ")
	zone_lst[-1] = zone_lst[-1][:-1] 
	return zone_lst

def fw_add_port():
	port = Prompt.ask("Enter port number : ")
	proto = Prompt.ask("Enter protocol :", choices=["tcp","udp"],default="tcp")
	fw_get_active_zones()
	zone =  Prompt.ask("Enter zone :", choices=get_zone_list(),default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --add-port="+port+"/"+proto+" --zone="+zone+" --permanent "
	print(os.popen(cmd).read())

def fw_get_services():
	gprint("___________________")
	gprint("Service List:")
	cmd = "sudo firewall-cmd --get-services"
	print(os.popen(cmd).read())
	gprint("___________________")
def zones():
	zone = Prompt.ask('Enter zone:',choices=get_zone_list(),default=CONF['ZONE'])
	return zone
def fw_add_services():
	fw_get_services()
	service = Prompt.ask("Enter service name from above list : ")
	fw_get_active_zones()
	zone =  Prompt.ask("Enter zone :", choices=get_zone_list(),default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --add-service="+service+" --zone="+zone+" --permanent" 
	print(os.popen(cmd).read())
def fw_add_source():
	ip=input("Enter source ip address")
	cmd=f'sudo firewall-cmd - -add-source ={ip}'
	print(os.popen(cmd).read)
def fw_dlt_rule_menu():
	print("\t [1] Remove port")
	print("\t [2] Remove services")
	print("\t [3] Remove sources")
	print("\t [4] Back to main menu ")

def fw_add_rule_menu():
	gprint("\t[1]Add Port")
	gprint("\t[2]Add services")
	gprint("\t[3]Add sources")
	gprint("\t[4]Back to Main menu")

def fw_add_rule():
	fw_add_rule_menu()
	ch = Prompt.ask("Enter your option : ", choices=["1", "2", "3","4"])
	if ch == "1":
		#add port
		fw_add_port()
		pass
	elif ch == "2":
		fw_add_services()
		#add services
	elif ch == "3":
		#add sources
		fw_add_source()
	elif ch == "4":
		pass
	else:
		print("Invalid option")
def fw_dlt_port():
	port = Prompt.ask("Enter port number : ")
	proto = Prompt.ask("Enter protocol :", choices=["tcp","udp"],default="tcp")
	fw_get_active_zones()
	zone =  Prompt.ask("Enter zone :", choices=get_zone_list(),default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --remove-port="+port+"/"+proto+" --zone="+zone+" --permanent "
	print(os.popen(cmd).read())    

def fw_dlt_services():
	fw_get_services()
	service = Prompt.ask("Enter service name from above list : ")
	fw_get_active_zones()
	zone =  Prompt.ask("Enter zone :", choices=get_zone_list(),default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --remove-service="+service+" --zone="+zone+" --permanent" 
	print(os.popen(cmd).read())

def fw_dlt_sources():
	ip = input('Enter source ip address : ')
	cmd = f'sudo firewall-cmd --remove-source ={ip}'
	print(os.popen(cmd).read)        		

def fw_dlt_rule():
	fw_dlt_rule_menu()
	ch=input("Enter choice")
	if ch == "1":
		fw_dlt_port()
	elif ch == "2":
		fw_dlt_service()
	elif ch == "3":
		fw_dlt_source()
	elif ch == "4":
		pass
	else:
		print("Invalid Entry")

def add_menu():
	gprint("[1] Add rules")
	gprint("[2] Delete rules")
	gprint("[3] Get Active Zones")
	gprint("[4] Get Details of Active Zones")
	gprint("[5] Reload firewall")
	gprint("[6] Exit")
def menu():
	print("[1] Display firewall status")
	print("[2] Set Rules")
	print("[3] Delete Rule")
	print("[4] Reload Rule")
	print("[5] Exit")


if __name__ == "__main__":
	while True:
		menu()
		ch = Prompt.ask("Enter your choice : ", choices=["1", "2", "3","4","5"])
		if ch == "1":
		#get status
			fw_get_status()
			
		elif ch == "2":
		#add rules
			fw_add_rule()
		elif ch == "3":
			fw_dlt_rule()
		elif ch == "4":
			fw_reload()
		elif ch == "5":
			break;
		else:
			console.print(Text("Invalid choice",style="bold red"))
