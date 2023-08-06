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


client = docker.from_env()
container = client.containers.list(all=True, filters={'name':'jenkins'})

for i in container:
    DATA = i.attrs
    IMAGE = str(i.image)
    CONTAINERSTATE= DATA["State"]["Status"]
    NETWORKDATA = DATA["NetworkSettings"]["Ports"]
    PORT = NETWORKDATA["8080/tcp"][0]["HostPort"]



if CONTAINERSTATE == "running":
    print("Jenkins container is running")
else:
    print("Container might be named improperly or not running. Please rename it as jenkins")


if PORT == "8080":
    print("Jenkins container is running on the correct port")
else:
    print("Jenkins container is not running on the correct port")


if "jenkins" in IMAGE:
    print("Jenkins container is running with right image")
else:
    print("Jenkins container is not running with right image")