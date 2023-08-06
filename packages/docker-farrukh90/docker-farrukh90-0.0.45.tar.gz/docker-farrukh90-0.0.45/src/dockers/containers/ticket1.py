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
    client = docker.from_env()
    container = client.containers.list(all=True, filters={'name':'jenkins'})

    CONTAINERSTATE=""
    PORT=""
    IMAGE=""

    for i in container:
        DATA = i.attrs
        IMAGE = str(i.image)
        CONTAINERSTATE= DATA["State"]["Status"]
        NETWORKDATA = DATA["NetworkSettings"]["Ports"]
        PORT = NETWORKDATA["8080/tcp"][0]["HostPort"]



    if CONTAINERSTATE == "running":
        print(bcolors.OKGREEN + "Jenkins container is running"+ bcolors.ENDC)
        time.sleep(0.5)
    else:
        print(bcolors.FAIL + "Container might be named improperly or not running. Please rename it as jenkins"+ bcolors.ENDC)
        sys.exit(1)
        time.sleep(0.5)

    if PORT == "8080":
        print(bcolors.OKGREEN + "Jenkins container is running on the correct port"+ bcolors.ENDC)
        time.sleep(0.5)
    else:
        print(bcolors.FAIL + "Jenkins container is not running on the correct port"+ bcolors.ENDC)
        sys.exit(1)
        time.sleep(0.5)

    if "jenkins" in IMAGE:
        print(bcolors.OKGREEN + "Jenkins container is running with right image"+ bcolors.ENDC)
        time.sleep(0.5)
    else:
        print(bcolors.FAIL + "Jenkins container is not running with right image"+ bcolors.ENDC)
        sys.exit(1)
        time.sleep(0.5)        
