import sys
import docker
import os
import time
import subprocess

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def taskchecker():
    VOLUMENAME='datastore'
    client = docker.from_env()
    volume = client.volumes.list(filters={'name': VOLUMENAME})
    volume = str(volume)


    if VOLUMENAME in volume:
        print(bcolors.OKGREEN + "%s volume is created" % VOLUMENAME + bcolors.ENDC)
        time.sleep(0.5)
    else:
        print(bcolors.FAIL + "%s volume is not  created" % VOLUMENAME  + bcolors.ENDC)
        sys.exit(1)
        time.sleep(0.5)        

    CONTAINERNAME='webapp'
    client = docker.from_env()
    container = client.containers.list(filters={'name': CONTAINERNAME})
    container = str(container)
    if "Container" in container:
        print(bcolors.OKGREEN + "%s container is created" % CONTAINERNAME + bcolors.ENDC)
        time.sleep(0.5)
    else:
        print(bcolors.FAIL + "%s container is not  created" % CONTAINERNAME  + bcolors.ENDC)
        sys.exit(1)
        time.sleep(0.5)  

    CONTAINERNAME='webapp'
    client = docker.from_env()
    container = client.containers.list(filters={'name': CONTAINERNAME}) 
    
    VOLUMENAME="datastore"
    VOLUMESTATE=''
    for i in container:
        DATA = i.attrs
        VOLUMESTATE = DATA["Mounts"][0]["Name"]
 
    if VOLUMENAME in VOLUMESTATE:
        print(bcolors.OKGREEN + "%s volume is attached" % VOLUMENAME + bcolors.ENDC)
        time.sleep(0.5)
    else:
        print(bcolors.FAIL + "%s volume is not  attached" % VOLUMENAME  + bcolors.ENDC)
        sys.exit(1)
        time.sleep(0.5)       
