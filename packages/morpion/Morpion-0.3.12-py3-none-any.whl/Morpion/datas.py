from termcolor import colored
from art import *
import os
import time
import json
import platform
import requests
import urllib3
import getpass
import pkg_resources
def internet_on() ->bool:
    url = "http://www.google.com"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False

def isfirst(pathToSave)->bool:
    try:
        with open(pathToSave+"/save.json", "r"):
            pass
    except FileNotFoundError:
        print('Initializing filesystem')
        print(pathToSave)
        a = input('...')
        os.system(f'mkdir {pathToSave}')
        os.system(f'/Users/{getpass.getuser()}/PetchouApps/save.json')
        with open(f"/Users/{getpass.getuser()}/PetchouApps/save.json", "w") as troubleshot:
            dict_init = {"#509 troubleshooting": "debug"}
            json.dump(dict_init, troubleshot)
            a = input()
        


commands = {"Windows": ["cls", "exit", "pip install --upgrade Morpion ", "python -m Morpion"], "Linux":["clear", """
        osascript -e 'tell application "Terminal" to close first window' && exit
        """, "pip3 install --upgrade Morpion", "python3 -m Morpion"], "Darwin": ["clear", """
        osascript -e 'tell application "Terminal" to close first window' && exit
        """, "pip3 install --upgrade Morpion ", "python3 -m Morpion"] }
sys = platform.system()
class variables():
    def __init__(self):
        self.colors = ['blue', 'green', 'red', 'yellow','cyan', 'grey']
        self.title = ["Morpion", ""]
        self.scheme = ["debug", colored("1", 'green'), colored("2", 'green'), colored("3", 'green'), colored("4", 'green'), colored("5", 'green'), colored("6", 'green'), colored("7", 'green'), colored("8", 'green'), colored("9", 'green')]
        self.cases = self.scheme


def loadFormat(x, base=2) -> int:
    return base * round(x/base)

def loading(currentVersion, path, SavePath):
    
    if isfirst(SavePath):
        print('Bienvenue, ceci est votre première session, voulez-vous créer une icon de bureau ? En cas de refus, cette action sera toujours disponible dans les paramètres de fin de partie.')
        print('non -> tapez n')
        print("oui -> tapez n'importe quelle touche")
        a = input('')
        if a != 'n':
            setIcon(platform.system(), path)

    os.system(commands[sys][0])
    tprint("morpion")
    fill = colored('■', "blue")
    percent = 0
     
     

    for progress in range(0, 1020):
        progress = progress/10
        percent = progress
        bar = f"Loading  [---------------------------------------------------] {percent} %" #11
        progress = loadFormat(progress)
        if progress!= 0:
                
                
            progress = int(progress/2)
            bar = bar.replace('-', fill, progress)
            print(f"{bar}", end="\r")
        else:
            print(f"{bar}", end='\r')
        time.sleep(0.001)
    percent = 100
    bar = f"Loading  |{fill*50}| 100 %        "

    print(bar)
    print('Checking for updates...')
    if internet_on():
        os.system(commands[sys][2])
        v = pkg_resources.get_distribution("Morpion").version
        if v != currentVersion:
            os.system(f"{commands[sys][3]} ")

    time.sleep(1)
    os.system(commands[sys][0])

global cases
cases = []

def setGrid(turn, case, value) ->list:
    global cases
    vars = variables()
    if turn == 1:
        cases = vars.cases
    else:
        cases[case] = value
    global grid1
    global grid2
    global grid3
    global grid4
    global grid5
    grid1 = f"           {cases[1]} | {cases[2]} | {cases[3]}"
    grid2 = "           --+---+--"
    grid3 = f"           {cases[4]} | {cases[5]} | {cases[6]}       tour {turn}"        
    grid4 = "           --+---+--"
    grid5 = f"           {cases[7]} | {cases[8]} | {cases[9]}"
    return [grid1, grid2, grid3, grid4, grid5]


def getPlayers(path) -> dict:
    with open(f'{path}/save.json', 'r') as save:
        players = {}
        #récupérer les données des joueurs précédents
        players = json.load(save)
        #j1
        p1 = input('Joueur 1, qui êtes vous ?\n')
        if players.get(p1):
            print(f'Content de de te revoir {p1} ')
        else:
            players[p1] = [0, 0, 0]
            print(f'Bienvenue {p1}')
        #j2
        #os.system('clear')
        def P2(p1) -> str:
            p2 = input('Joueur 2, qui êtes vous ?\n')
            if p2 == p1:
                print('Joueur déja dans la partie, entrez un autre nom.')
                return P2(p1)
            else:
                return p2

        p2 = P2(p1)
        if players.get(p2):
            print(f'Content de de te revoir {p2} ')
        else:
            players[p2] = [0, 0, 0]
            print(f'Bienvenue {p2}')
    players['currentPlayers'] = [p1, p2]
    #print(players)
    time.sleep(1.0)
    return players
        
def notDone(turn) -> bool:
    
    global cases
    if cases[1] == cases[2] == cases[3] == cases[4] == cases[5] == cases[6] == cases[7] == cases[8] == cases[9]:
        return True
    elif turn == 10:
        return False
    elif cases[1] == cases[2] == cases[3]:
        return False
    elif cases[4] == cases[5] == cases[6]:
        return False
    elif cases[7] == cases[8] == cases[9]:
        return False
    elif cases[1] == cases[4] == cases[7]:
        return False
    elif cases[2] == cases[5] == cases[8]:
        return False
    elif cases[3] == cases[6] == cases[9]:
        return False
    elif cases[1] == cases[5] == cases[9]:
        return False
    elif cases[3] == cases[5] == cases[7]:
        return False
    else:
        return True

def isWinner() -> bool:
    if cases[1] == cases[2] == cases[3]:
        return False
    elif cases[4] == cases[5] == cases[6]:
        return False
    elif cases[7] == cases[8] == cases[9]:
        return False
    elif cases[1] == cases[4] == cases[7]:
        return False
    elif cases[2] == cases[5] == cases[8]:
        return False
    elif cases[3] == cases[6] == cases[9]:
        return False
    elif cases[1] == cases[5] == cases[9]:
        return False
    elif cases[3] == cases[5] == cases[7]:
        return False
    else:
        return True


def setIcon(FM, path):
    if FM == 'Windows':
        try:
            os.system('pip install winshell')
            os.system('pip install pywin32')
            os.system('pip install pypiwin32')
            import winshell
            desktop = winshell.desktop()
            with winshell.shortcut(os.path.join(desktop, "Morpion.lnk")) as shortcut:
                shortcut.path = f"{path}\morpion.bat"
                shortcut.icon = f"{path}\morpionIcon.png"
                shortcut.description = "PetchouApps' Morpion/TicTacToe game"
        except os.error:
            pass
    else:
        os.system(f'cp {path}/morpionUnix.sh /Users/{getpass.getuser()}/Desktop/Morpion.sh')
        os.system('chmod 755 /Users/{getpass.getuser()}/Desktop/Morpion.sh')