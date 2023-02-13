#!/bin/python3
from subprocess import run
from rich.prompt import Prompt, Confirm
from os import path
from os import mkdir
from os import chdir
from pathlib import Path

# if geteuid() != 0:
#     exit("You need to have root privileges to run this script.")

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
        #print(self.config)
        for i in range(len(self.config)):
            self.config[i] = self.config[i].strip()

    def Initiate(self):

        path = Prompt.ask("Where would you like to store your backup?", default="/mnt")
        exists = Confirm.ask("Would you like to initiate this backup repo?",default="y")
        if exists:
            run(["restic","init","--repo",path])
            print("Adding to the Backup.conf file")
            data = open("Backup.conf","a")
            data.write(path)
        else:
            print("Adding to the Backup.conf file")
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
    if Selector.upper() == "INITIATE":
        B.Initiate()
    elif Selector.upper() == "BACKUP":
        B.Backup()
    else:
        B.Restore()

if __name__ == "__main__":
    Does_conf_exist = path.isdir(CONFIG_FILE)
    #print(Does_conf_exist)
    if Does_conf_exist == False:
        mkdir(CONFIG_FILE)

    chdir(CONFIG_FILE)
    while True:
        try:
            main()
        except KeyboardInterrupt:
            exit("\nKeyboardInterrupt") 
    
