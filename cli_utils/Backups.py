#!/bin/python3
from subprocess import run
from rich.prompt import Prompt
from os import chdir
from os import geteuid
from pathlib import Path
import json 

if geteuid() != 0:
    exit("You need to have root privileges to run this script.")

CONFIG_FILE = Path.home() / ".config" 

class Back():
    def __init__(self):
        try:
            open("Backup.conf","x").close
            pass
        except:
            pass
        self.config= []
        path = open("Backup.conf","r")
        self.config = path.readlines()
        for i in range(len(self.config)):
            self.config[i] = self.config[i].strip()

    def Initiate(self):
        path = Prompt.ask("Where would you like to store your backup?", default="/mnt")
        run(["restic","init","--repo",path])
        data = open("Backup.conf","a")
        data.write(path)
        
    def Backup(self):
        where = Prompt.ask("Where is your backup?",choices=self.config, default=self.config[0])
        path = Prompt.ask("What would you like to backup?",default="/")
        run(["restic","--repo",where,"backup",path])
    
    def Restore(self):
        where = Prompt.ask("Where is your backup?",choices=self.config, default=self.config[0])
        target = Prompt.ask("Where would you like to restore your backup to?",default="/")
        version = Prompt.ask("Which backup would you like to restore?", default="latest")
        run(["restic","--repo",where,"restore",version,"--target",target])

def main():
    B = Back()
    Selector = Prompt.ask("What would you like to do?",choices=["Initiate","Backup","Restore"],default="Backup")
    if Selector == "Initiate":
        B.Initiate()
    elif Selector == "Backup":
        B.Backup()
    else:
        B.Restore()

if __name__ == "__main__":
    chdir(CONFIG_FILE)
    while True:
        try:
            main()
        except KeyboardInterrupt:
            exit("\nKeyboardInterrupt") 
    