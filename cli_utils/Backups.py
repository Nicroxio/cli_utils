#!/bin/python3
from subprocess import run
from rich.prompt import Prompt
from os import chdir
from os import geteuid
from pathlib import Path

if geteuid() != 0:
    exit("You need to have root privileges to run this script.")

CONFIG_FILE = Path.home() / ".config" 
class Back():
    def __init__(self):
        pass
    def Initiate(self):
        path = Prompt.ask("Where would you like to store your backup?", default="/mnt")
        run(["restic","init","--repo",path])
        conf = open("backup.conf","x")
        conf.write(path)
        conf.close()
    def Backup(self):
        conf = open("backup.conf","r")
        where = Prompt.ask("Where is your backup?",default=conf.read())
        path = Prompt.ask("What would you like to backup?",default="/")
        run(["restic","--repo",where,"backup",path])
        conf.close()
    def Restore(self):
        conf = open("backup.conf","r")
        target = Prompt.ask("Where would you like to restore your backup to?",default="/")
        version = Prompt.ask("Which backup would you like to restore?", default="latest")
        run(["restic","--repo",conf.read(),"restore",version,"--target",target])
        conf.close()



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
    pass

