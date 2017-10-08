import json
import requests
import time
from pprint import pprint
import threading
from termcolor import colored
import os
import configparser
from util import *


class vultr:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.cfg")
        self.api_key = config.get('API','api') # put your api key in here
        self.end_point = config.get('END_POINT', 'end_point') # endpoint, usually "https://api.vultr.com/v1/"
        self.VPSPLANID= config.get('ID', 'VPSPLANID') # your sever plan id
        self.SCRIPTID = config.get('SCRIPT_ID', 'script_id') # your start script id if you have one
        self.OSID = config.get('ID', 'OSID') #Ubuntu 14.04 X64 your operation system id
        ###self.location = location # your server location
        self.DCID = config.get('ID','DCID') # your location Id
        self.SUBID = []  # need it when destroying servers
        self.ips = [] # to store all the ip address of your server
        self.proxy_list = [] # store the proxy list


    def info(self):
        # get
        # params more get method while data used in post method
        append = "account/info"
        url = self.end_point + append
        params = {"api_key": self.api_key}
        r = requests.get(url=url,params=params)
        for key, value in r.items():
            print("{} : {}".format(key, green(value)))

    def check_ips(self):
        # get, api
        append = "server/list"
        url = self.end_point + append
        params = {
            "api_key": self.api_key,
        }
        r = requests.get(url=url, params=params)
        # now we retrive all the ips
        self.ips = []
        self.SUBID = []
        for key in r:
            self.ips.append(r_json[key]['main_ip'])
            self.SUBID.append(r_json[key]['SUBID'])

    def region_list(self):
        # get, no auth
        append = "regions/list?"
        url = self.end_point + append
        r = requests.get(url=url)
        num = 0
        for key, value in r.items():
            num+=1
            print(value['country'],value['name'])
        print("There are {} regions available".format(num))
        # be able to check the availablilty of regions

    def create(self):
        # post, need params and data
        append = "server/create"
        url = self.end_point + append
        data = {
            "DCID": self.DCID,
            "OSID": self.OSID,
            "SCRIPTID": self.SCRIPTID,
            "VPSPLANID": self.VPSPLANID,
            "DCID": "1",
        }
        params = {
            "api_key": self.api_key
        }
        r = requests.post(url=url, params=params,data=data)
        for key in r:
            self.SUBID.append(key)
        # create server

    def destroy(self,SUBID):
        #destroy all the server
        append = "server/destroy"
        url = self.end_point + append
        params = {
            "api_key": self.api_key
        }
        data = {
            "SUBID": SUBID
        }
        r = requests.post(url=url, params=params, data = data)

    def mthread(self, method, num):
        if (method == 1):
            # this is create method
            for i in range(0, num):
                t = threading.Thread(target=self.create)
                print("Creating proxy {0}".format(i))
                t.start()
            print(colored("Done",'green'))
            return

        if (method == 2):
            # this is destroy method
            self.check_ips()
            for SID in self.SUBID:
                t = threading.Thread(target=self.destroy, args=(SID,))
                t.start()
            print(colored("Destroy done", 'green'))
            return
        else:
            print("Sorry you enter the wrong method key")
            return

    def list(self):
        self.check_ips()
        y_proxy = 0
        n_proxy=0
        for proxy in self.ips:
            if(proxy=="0.0.0.0"):
                n_proxy=+1
                continue
            print(proxy)
            y_proxy+=1
        print("Total proxy: {0}  Not read proxy: {1}".format(colored(str(y_proxy), 'green'),colored(str(n_proxy), 'red')))

    def put_to_file(self):
        self.check_ips()
        if os.path.isfile("proxy.txt"):
            if os.stat("proxy").st_size != 0:
                os.remove("proxy.txt")
        with open("proxy.txt", "w+") as f:
            for ip in self.ips:
                f.write(ip+":3128:randall:proxy\n")
            print(colored("file created"),'green')


# be able to choose regions' availability
# more clean and convenient UI
# handle some error conditions

v = vultr()
method = 0
num = 0
user = ''
print("Welcome to Vultr".center(80, "="))
method=input(str("option:\nA: create B: destroy C: list\nD: region E: info F: put_ips_to_file\nG: exit\n").center(80, " "))

while( method != "G"):
    if(method == "B"):
        v.mthread(2, 2)
    elif(method == "A"):
        num = input("how many you want to create: ")
        v.mthread(1, int(num))
    elif(method== "C"):
        v.list()
    elif(method== "F"):
        v.put_to_file()
    elif(method== "D"):
        v.region_list()
    elif(method=="E"):
        v.info()
    else:
        print("Wrong input, try again")

    method=input(str("\noption:\nA: create B: destroy C: list\nD: region E: info F: put_ips_to_file\nG: exit\n").center(80, " "))
