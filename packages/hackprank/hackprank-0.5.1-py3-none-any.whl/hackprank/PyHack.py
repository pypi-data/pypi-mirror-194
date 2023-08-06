import pyfiglet
from rich.console import Group
from rich.panel import Panel
from rich.console import Console
from rich.prompt import IntPrompt, Prompt
from rich.progress import Progress, track
from time import sleep
from os import *
from colorama import *
import random
import sys 

def nukeShutDown():
    for x in track(range(25),"Initializing..."):
        sleep(0.1)
    country = Prompt.ask("Which Country's Nukes Do You Want To Shutdown")
    for x in track(range(100), "Bypassing Government Mainframe"):
        sleep(0.1)
    for x in track(range(100), f"Gathering Information About {country}"):
        sleep(0.1)
    with Progress(transient=True) as prog:
        locate = prog.add_task("Locating Nuke Control Systems", total=300)
        hacking = prog.add_task("Hacking Government Systems", total=500)
        nHacking = prog.add_task("Hacking Nuclear Controls", total=900)
        while not prog.finished:
            prog.update(hacking,advance=0.4)
            prog.update(locate,advance=0.7)
            prog.update(nHacking,advance=0.5)
            sleep(0.1)
    con.print("Hacked Nuclear Contorols", style="bold green")
    for x in track(range(100), "Preparing Nuclear Systems Shutdown"):
        sleep(0.1)
    with Progress(transient=True) as prog:
        exploite = prog.add_task("Exploting Nuclear System", total=300)
        selfDestruct = prog.add_task("Self Destructing", total=900)
        while not prog.finished:
            prog.advance(exploite, 0.5)
            prog.advance(selfDestruct, 0.7)
            sleep(0.1)
    con.print(f"{country.title()} Nuclear Systems Destoyed")

def web_hacking():
    for x in track(range(25),"Initializing..."):
        sleep(0.1)
    url = Prompt.ask("Enter The Website's Url")
    for i in track(range(100), f"Bypassing Mainframe"):
        sleep(0.1)
    for i in track(range(100),f"Gathering Information On {url}"):
        sleep(0.1)
    with Progress(transient=True) as prog :
        exploiting = prog.add_task("Exploiting The Website",total=500)
        decoding = prog.add_task("Cracking The Passwords Hashes",total=300)
        dumping = prog.add_task("Dumping Plain Text Passwords",total=900)
        while not prog.finished:
            prog.update(exploiting,advance=0.9)
            prog.update(decoding,advance=0.3)
            prog.update(dumping,advance=0.5)
            sleep(0.1)
    con.print("Password: Password", style="bold green")
    with Progress(transient=True) as prog:
        code = prog.add_task("Entering Malicious Code To Website", total=300)
        capture = prog.add_task("Getting User Passwords", total = 500)
        change = prog.add_task("Changing All Passwords And Username To One Master Key", total=900)
        while not prog.finished:
            prog.update(capture,advance=0.9)
            prog.update(change,advance=0.3)
            prog.update(code,advance=0.5)
            sleep(0.1)
    con.print("Master Key: 0x1a23x", style="bold green")
    return

def Phishing_hack():
    for x in track(range(25),"Initializing..."):
        sleep(0.1)
    target = Prompt.ask("Enter The Target's Email Or Press [1] To Make A Phishing Site")  
    for i in track(range(100),f"Making Hook Script And Fake Logins"):
        sleep(0.1)
    with Progress(transient=True) as prog:
        exploiting = prog.add_task("Deploying Website",total=900)
        decoding = prog.add_task("Entering Malicious Scripts",total=500)
        while not prog.finished:
            prog.update(exploiting,advance=0.3)
            prog.update(decoding,advance=0.9)
            sleep(0.1)
    if target != "1":
        with Progress(transient=True) as prog:
            fake_account = prog.add_task("Making Fake Account As Google Security", total=500)
            encrypt = prog.add_task("Encrypting Email And Attaching Malicious Code", total=300)
            send_email = prog.add_task("Sending Email", total=900)
            while not prog.finished:
                prog.update(fake_account,advance=0.9)
                prog.update(send_email,advance=0.3)
                prog.update(encrypt,advance=0.5)
                sleep(0.1)
        con.print(f"Phishing Email Sent To {target}", style="bold green")
        return
    elif target == "1":
        con.print("Phising Site Domain: www.googlo.com", style="bold green")
        return

def WIFI_hack():
    for x in track(range(25),"Initializing..."):
        sleep(0.1)
    wifi = Prompt.ask("Enter The Wifi Name")
    for i in track(range(100), f"Bypassing Mainframe"):
        sleep(0.1)
    for i in track(range(100),f"Gathering Information On {wifi}"):
        sleep(0.1)
    with Progress(transient=True) as prog:
        exploiting = prog.add_task(f"Exploting {wifi}",total=500)
        script = prog.add_task("Entering Maliciouus Scripts",total=300)
        back_door = prog.add_task(f"Back Dooring {wifi}",total=900)
        while not prog.finished:
            prog.update(exploiting,advance=0.9)
            prog.update(back_door,advance=0.3)
            prog.update(script,advance=0.5)
            sleep(0.1)
    con.print(f"Wifi Password: password\nUsername{wifi}\nWifi Provider:Rogers Inc.", style="bold green")
    return

def find():
    for x in track(range(25),"Initializing..."):
        sleep(0.1)
    name = Prompt.ask("Enter The Target's Name")
    for i in track(range(100), f"Bypassing Mainframe"):
        sleep(0.1)
    for i in track(range(100),f"Gathering Information On {name}"):
        sleep(0.1)
    with Progress(transient=True) as prog:
        locate = prog.add_task(f"Locating {name}", total=300)
        exploiting = prog.add_task(f"Exploiting {name}", total=500)
        info = prog.add_task(f"Finding Info About {name}", total=900)
        while not prog.finished:
            prog.update(exploiting, advance=0.6)
            prog.update(info, advance=0.3)
            prog.update(locate, advance=0.5)
            sleep(0.1)
    with Progress(transient=True) as prog:
        master = prog.add_task("Gathering All Info Into One Master Key", total=500)
        while not prog.finished:
            prog.update(master, advance=0.5)
            sleep(0.1)
    con.print(f"Master Key: 0x1bx1a6x20 \nIP: {f'{random.randrange(125, 225)}.{random.randrange(1, 225)}.{random.randrange(1, 225)}.{random.randrange(1, 225)}'}", style="bold green")
    return
    

def remote():
    for x in track(range(25),"Initializing..."):
        sleep(0.1)
    ip = Prompt.ask("Enter The IP Of Target") 
    for i in track(range(100), f"Bypassing Mainframe"):
        sleep(0.1)
    for i in track(range(100),f"Gathering Information On {ip}"):
        sleep(0.1)
    with Progress(transient=True) as prog:
        info = prog.add_task("Getting Login Info", total=500)
        shutdown = prog.add_task(f"Shutting Down {ip}", total=900)
        while not prog.finished:
            prog.update(shutdown, advance=0.3)
            prog.update(info, advance=0.9)
            sleep(0.1)
    con.print(f"{ip} Successfully Shutdown", style="bold green")
    con.print(f"Username: professional\nPassword: password", style="bold green")
    return

def nuke():
    explode = """
                          ____/ (  (    )   )  \___
                       ((     (   )(    )  )   (   )  )
                     ((/  ( _(   )   (   _) ) (  () )  )
                    ( (  ( (_)   ((    (   )  .((_ ) .  )_
                   ( (  )    (      (  )    )   ) . ) (   )
                  (  (   (  (   ) (  _  ( _) ).  ) . ) ) ( )
                  ( (  (   ) (  )   (  ))     ) _)(   )  )  )
                 ( (  ( \ ) (    (_  ( ) ( )  )   ) )  )) ( )
                  (  (   (  (   (_ ( ) ( _    )  ) (  )  )   )
                 ( (  ( (  (  )     (_  )  ) )  _)   ) _( ( )
                  ((  (   )(    (     _    )   _) _(_ (  (_ )
                   (_((__(_(__(( ( ( |  ) ) ) )_))__))_)___)
                   ((__)        \\||lll|l||///          \_))
                            (   /(/ (  )  ) )\   )
                          (    ( ( ( | | ) ) )\   )
                           (   /(| / ( )) ) ) )) )
                         (     ( ((((_(|)_)))))     )
                          (      ||\(|(|)|/||     )
                        (        |(||(||)||||        )
                          (     //|/l|||)|\\ \     )
                        (/ / //  /|//||||\\  \ \  \ _)"""

    for x in track(range(25),"Initializing..."):
        sleep(0.1)      
    name = Prompt.ask("Enter The Target City's Longitude And Latitude")
    nuke = Prompt.ask("Which Nuke Would You Like To Use")

    for x in track(range(100), "Bypassing Government Mainframe"):
        sleep(0.1)
    for x in track(range(100), f"Gathering Information About {nuke}"):
        sleep(0.1)
    with Progress(transient=True) as prog:
        locate = prog.add_task(f"Locating {nuke}", total=300)
        gHack = prog.add_task("Hacking Government Systems", total=500)
        nHack = prog.add_task("Hacking Into Nuclear Controls", total=900)
        while not prog.finished:
            prog.advance(locate, 0.9)
            prog.advance(gHack, 0.5)
            prog.advance(nHack, 0.3)
            sleep(0.1)
    con.print("Government Systems Have Been Hacked And You Now Have Access To Nuke Controls", style="bold green")
    with Progress(transient=True) as prog:
        verify = prog.add_task("Verifying Target Location", total=300)
        pLaunch = prog.add_task("Preparing For Launch", total=600)
        while not prog.finished:
            prog.advance(verify, 0.9)
            prog.advance(pLaunch, 0.5)
            sleep(0.1)
    con.print(f"{nuke.title()} Launched To {name}", style="bold green")

    con.print(explode, style="red")
    sleep(2)
    con.print("Target Location Successfully Eliminated")
    return


    



def hack():
    global con
    con = Console()

    banner = pyfiglet.figlet_format("Cypher",font="banner3-D")
    con.print(banner,"modern hacking framework to hack any possible device in the whole entire world",style="bold green")

    options = Group(
        Panel("1. Web App Hacking"),
        Panel("2. Phishing Attack"),
        Panel("3. WIFI Hacking"),
        Panel("4. Find User IP"),
        Panel("5. Remote Shutdown/Login"),
        Panel("6. Deploy Nukes"),
        Panel("7. Shutdown Nukes")
    )
    con.print(Panel(options),style="bold green")


    answer = IntPrompt.ask("Which one do you pick? ",choices=['1','2','3','4','5','6'])

    if answer == 1:
        web_hacking()
    elif answer == 2:
        Phishing_hack()
    elif answer == 3:
        WIFI_hack()
    elif answer == 5:
        remote()
    elif answer == 4:
        find()          
    elif answer == 6:
        nuke()    
    elif answer == 7:
        nukeShutDown()                 


