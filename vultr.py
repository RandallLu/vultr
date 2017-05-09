import json
import requests
import time
from pprint import pprint
import threading
from termcolor import colored
import os

api_key = "DGQEZJP6ININKTW5QOCGXRULMVFDQCIEXDYA"

#script_id = "53890"
script_id="58551"
end_point = "https://api.vultr.com/v1/"
OSID="160"
DCID="3"
VPSPLANID='201'

class vultr:

    def __init__(self):
        self.api_key = api_key # put your api key in here
        self.end_point = end_point # endpoint, usually "https://api.vultr.com/v1/"
        self.SUBID = []  # need it when destroying servers
        self.ips = [] # to store all the ip address of your server
        self.proxy_list = [] # store the proxy list
        self.OSID = OSID #Ubuntu 14.04 X64 your operation system id
        ###self.location = location # your server location
        self.DCID = DCID # your location Id
        self.VPSPLANID=VPSPLANID # your sever plan id
        self.SCRIPTID = script_id # your start script id if you have one


    def info(self):
        # get
        # params more get method while data used in post method
        append = "account/info"
        url = self.end_point + append
        params = {"api_key": self.api_key}
        r = requests.get(url=url,params=params)
        re = r.text
        print(r)

    def check_ips(self):
        # get, api
        append = "server/list"
        url = self.end_point + append
        params = {
            "api_key": self.api_key,
        }
        r = requests.get(url=url, params=params)
        r_json = r.json()
        # now we retrive all the ips
        self.ips = []
        self.SUBID = []
        for key in r_json:
            self.ips.append(r_json[key]['main_ip'])
            self.SUBID.append(r_json[key]['SUBID'])

    def region(self):
        # get, no auth
        append = "regions/list"
        url = end_point + append
        r = requests.get(url=url)
        r_json = r.json()
        num = 0
        for key in r_json:
            num+=1
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
        for key in r.json():
            self.SUBID.append(key)
        # create server

    def destroy(self,SUBID):
        #destroy all the server
        append = "server/destroy"
        url = end_point + append
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
                print("======creating proxy {0}".format(i))
                t.start()
            print(colored("======Done======",'green'))
            return

        if (method == 2):
            # this is destroy method
            self.check_ips()
            for SID in self.SUBID:
                t = threading.Thread(target=self.destroy, args=(SID,))
                t.start()
            print(colored("======destroy done======", 'green'))
            return
        else:
            print("======sorry you enter the wrong method key======")
            return

    def list(self):
        self.check_ips()
        y_proxy = 0
        n_proxy=0
        for proxy in self.ips:
            if(proxy=="0.0.0.0"):
                n_proxy=+1
                continue
            proxy = proxy + ":3128:randall:proxy"
            print(proxy)
            y_proxy+=1
        print("Total proxy: {0}  Not read proxy: {1}".format(colored(str(y_proxy), 'green'),colored(str(n_proxy), 'red')))

    def file(self):
        self.check_ips()
        if os.path.isfile("proxy.txt"):
            if os.stat("proxy").st_size != 0:
                os.remove("proxy.txt")
        with open("proxy.txt", "w+") as f:
            for ip in self.ips:
                f.write(ip+":3128:randall:proxy\n")
            print(colored("======file created======"))


# be able to choose regions' availability
# more clean and convenient UI
# handle some error conditions

v = vultr()
method = 0
num = 0
user = ''
print("Welcome to Vultr proxy")
method=input("======What do you want to do ?======\ncreate destroy list file region info exit\nLet's go: ")
while( method != "exit"):
    if(method == "destroy"):
        v.mthread(2, 2)
    elif(method == "create"):
        num = input("how many you want to create: ")
        v.mthread(1, int(num))
    elif(method== "list"):
        v.list()
    elif(method== "file"):
        v.file()
    elif(method== "region"):
        v.region()
    elif(method=="info"):
        v.info()
    else:
        print("Wrong input, try again")

    method=input("What do you want to do ?\ncreate destroy exit list: ")
