import pandas as pd
import os
import json
from datetime import datetime

def ouiExtractor(macAdress):
    csvFile = "./oui.csv"
    data = pd.read_csv(csvFile)
    prefixoMac = macAdress.replace(":", "")[:6].upper()
    resultado = data[data["Assignment"].str.contains(prefixoMac, na=False)]
    if resultado.empty:
        return "UNDEFINED"
    name = resultado['Organization Name'].values[0]
    return name

def cidr(IP, mask):
    pieces = mask.split(".")
    bitCount = 0
    for piece in pieces:
        num = int(piece)
        bitCount += bin(num).count("1")
    return f"{IP}/{bitCount}"

def loadData(file):
    if  os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return []

def saveData(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def detectChanges(devices, newDevices, date):
    add = []
    rm = []
    current = {tuple(device.items()) for device in devices}
    new = {tuple(device.items()) for device in newDevices}
    for device in new - current:
        add.append(dict(device))
    for device in current - new:
        rm.append(dict(device))
    return add, rm

def addContent(data, newContent):
    if data:
        add, rm = detectChanges(data[-1]["Devices"], newContent["Devices"], newContent["Date"])
        if add or rm:
            saveData("./currentChanges.json", {"Added Devices": add, "Removed Devices": rm})
            data.append(newContent)
            print("Arquivos adicionados ou removidos. Arquivo de log currentDevices criado.")
        else:
            print("Nenhuma alteração ocorreu na rede")
            saveData("./currentChanges.json", {"Added Devices": [], "Removed Devices": []})
            data[-1]["Date"] = newContent["Date"]
    else:
        data.append(newContent)
