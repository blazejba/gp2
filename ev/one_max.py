#!/usr/bin/env python3
from time import sleep
import sys
import subprocess

def main():
    child = subprocess.Popen(["python","test1.py"],stdout=subprocess.PIPE)
    while(1):
        print("a")
        if(child.poll()):
            print(child.returncode)
            break
        sleep(1)

main()
