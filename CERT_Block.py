import urllib.request
import urllib
import os
from sys import platform
import PySimpleGUI as gui

# Global Def:
CERT_Alarm = '195.187.6.33'
CERT_Url = 'https://hole.cert.pl/domains/domains.txt'
Color1 = "#0B132B"
Color2 = "#FCFCFC"
Color3 = "#FF495C"
Color4 = "#39A2AE"

# Executes changes
def save():
    with open(HostsPath, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if not line.__contains__(CERT_Alarm):
                file.write(line)
        file.truncate()
    with open(HostsPath, 'a') as file:
        for domain in BlockList:
            file.write('\n' + CERT_Alarm + '\t' + str(domain) + '\t#Domain blocked by CERT_Block')

# Add user specified url
def manualAdd():
    addUrl = gui.popup_get_text("Enter URL to add", keep_on_top=True)
    BlockList.append(addUrl)

# OS safety check
if platform == "win32":
    HostsPath = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
else:
    exit('OS error')
if not os.path.isfile(HostsPath):
        exit("File error")

# Load website list to CertList
CertList = []
for line in urllib.request.urlopen(CERT_Url):
    CertList.append(line.decode('utf-8').rstrip())

# Read blocked websites from hosts to BlockList
BlockList = []
with open(HostsPath, 'r') as file:
    for line in file:
        if(line.__contains__(CERT_Alarm)):
            lineSplit = line.split()
            if len(lineSplit) >= 1:
                BlockList.append(lineSplit[1])     

# Creating list of unblocked dangerous websites
UnblockList = list(set(CertList) - set(BlockList))

# Creating GUI in 3 columns
dangerousList = [
    [
        gui.Text("Dangerous domains", font=(30), background_color=Color1, text_color=Color2),
    ],
    [
        gui.Listbox(values=UnblockList, enable_events=True, size=(40, 30), key="-DANGEROUS LIST", select_mode=gui.LISTBOX_SELECT_MODE_MULTIPLE, background_color=Color2)
    ]]

buttonCol = [
    [
        gui.Button("Block", key="-BLOCK", size=(10,1), button_color=(Color1, Color4))
    ],
    [
        gui.Button("Unblock", key="-UNBLOCK", size=(10,1), button_color=(Color1, Color4))
    ],
    [
        gui.Button("Block All", key="-BLOCKALL", size=(10,1), button_color=(Color1, Color4))
    ],
    [
        gui.Button("Unblock All", key="-UNBLOCKALL", size=(10,1), button_color=(Color1, Color4))
    ],
    [
        gui.Button("Manual Add", key="-MANUAL", size=(10,1), button_color=(Color1, Color4))
    ],
    [
        gui.Button("Save & Exit", key="-SAVE", size=(10,1), button_color=(Color1, Color3))
    ]]

blockedList = [
    [
        gui.Text("Blocked domains", font=(30), background_color=Color1, text_color=Color2),
    ],
    [
        gui.Listbox(values=BlockList, enable_events=True, size=(40, 30), key="-BLOCKED LIST", select_mode=gui.LISTBOX_SELECT_MODE_MULTIPLE, background_color=Color2)
    ]
    ]

# GUI layout
layout = [
    [
        gui.Column(dangerousList, background_color=Color1),
        gui.Column(buttonCol, background_color=Color1),
        gui.Column(blockedList, background_color=Color1)
    ]
]
window = gui.Window("CERT Block", layout, background_color=Color1)

# App does not execute changes until save is clicked for performance, handling arrays turned out to be way quicker than handling hosts file
while True:
    event, values = window.read()
    if event == gui.WIN_CLOSED:
        break
    elif event == "-BLOCK":
        for domain in values["-DANGEROUS LIST"]:
            BlockList.append(domain)
            UnblockList.remove(domain)
        window['-DANGEROUS LIST'].update(UnblockList)
        window['-BLOCKED LIST'].update(BlockList)
    elif event == "-UNBLOCK":
        for domain in values["-BLOCKED LIST"]:
                UnblockList.append(domain)
                BlockList.remove(domain)
        window['-DANGEROUS LIST'].update(UnblockList)
        window['-BLOCKED LIST'].update(BlockList)
    elif event == "-UNBLOCKALL":
        UnblockList.extend(BlockList)
        BlockList.clear()
        window['-DANGEROUS LIST'].update(UnblockList)
        window['-BLOCKED LIST'].update(BlockList)
    elif event == "-BLOCKALL":
        BlockList.extend(UnblockList)
        UnblockList.clear()
        window['-DANGEROUS LIST'].update(UnblockList)
        window['-BLOCKED LIST'].update(BlockList)
    elif event == "-SAVE":
        save()
        exit()
    elif event == "-MANUAL":
        manualAdd()
        window['-DANGEROUS LIST'].update(UnblockList)
        window['-BLOCKED LIST'].update(BlockList)
