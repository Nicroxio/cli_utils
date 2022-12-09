#!/bin/python3
import subprocess
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.console import Console
from os import chdir
from os import geteuid
from pathlib import Path

sudo = True
if geteuid() != 0:
    continue_anyway = Confirm.ask("You need to have root privileges to run this script.\nDo you want to continue anyway?",default="y")
    if continue_anyway==False:
        exit()
    else:
        sudo = False

class service_create():
    def __init__(self):
        pass
    def Unit(self):
        Description = Prompt.ask("[red]What is the Description of the service? [/red]",default="Na")
        Description = f"Description={Description}"
        After = Prompt.ask("What do you want this to run after?", default="network.Target")
        After = f"After={After}"
        return Description, After
    def Service(self):
        Type = Prompt.ask("[red]What Type of service?[/red]",choices=["simple","forking","oneshot","notify","dbus","idle"],default="simple")
        Type = f"Type={Type}"
        ExecStart = Prompt.ask("[blue]What would you like to run?[/blue]",default="/bin/bash")
        ExecStart = f"ExecStart={ExecStart}"
        return Type, ExecStart
    def Install(self):
        WantedBy=Prompt.ask("Wanted by?", default="multi-user.target")
        WantedBy=f"WantedBy={WantedBy}"
        return WantedBy


def main():
    Name = Prompt.ask("What is your service called?",default="Nothing")
    Create_service = service_create()
    Description, After = Create_service.Unit() 
    Type, ExecStart = Create_service.Service()
    WantedBy = Create_service.Install()

    Formatting = f"""
    [Unit]
    {Description}
    {After}
    [Service]
    {Type}
    {ExecStart}
    [Install]
    {WantedBy}
    """

    table = Table(title="Final Result")

    table.add_row(Formatting)
    console = Console()
    console.print(table)
    return Name, Formatting

if __name__ == "__main__":

    Name, Formatting = main()
    if Confirm.ask("Would You like to continue?", default="y"):
        if sudo == True:
            chdir("/etc/systemd/system")
            service = open(f"{Name}.service","w")
            service.write(Formatting)
            service.close()
        else:
            chdir(Path.home())
            service = open(f"{Name}.service","w")
            service.write(Formatting)
            service.close()
    else:
        exit()
    if sudo:
        if Confirm.ask("Would you like to start and enable?",default="n"):
            subprocess.run(["systemctl","enable",f"{Name}"])
            subprocess.run(["systemctl", "start", f"{Name}"])
