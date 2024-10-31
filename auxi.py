import pandas as pd
import os
import json
from datetime import datetime
from prettytable import PrettyTable

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

def detectChanges(devices, newDevices):
    add = []
    rm = []
    current = {tuple(device.items()) for device in devices}
    new = {tuple(device.items()) for device in newDevices}
    for device in new - current:
        add.append(dict(device))
    for device in current - new:
        rm.append(dict(device))
    return (len(add) != 0 or len(rm) != 0)

def addContent(data, newContent):
    currentChanges = "./currentChanges.json"

    curr = loadData(currentChanges)
    
    if data:
        changed = detectChanges(data[-1]["Devices"], newContent["Devices"])
        if (not changed):
            print("Nenhuma alteração ocorreu na rede")
            data[-1]["Date"] = newContent["Date"]
            return
        for new in newContent["Devices"]:
            exist = False
            for device in curr:
                if device["IP"] == new["IP"]:
                    device["Status"] = "Ativo"
                    exist = True
                else:
                    device["Status"] = "Inativo"
            if not exist:
                newContent["Status"] = "Ativo"
                curr.append(newContent)
        saveData(currentChanges, curr)
        data.append(newContent)
    else:
        for new in newContent["Devices"]:
            new["Status"] = "Ativo"
            curr.append(new)
        saveData(currentChanges, curr)
        data.append(newContent)    

def printLogTable(file):
    with open(file, "r") as f:
        log = json.load(f)

    table = PrettyTable()
    table.field_names = ["IP", "Mac Address", "Owner", "Tipo"]
    table.clear_rows()
    for device in log[-1]["Devices"]:
        table.add_row([device["IP"], device["Mac Address"], device["Owner"], device["Tipo"]])
    print(f"Log do Período: {log[-1]["Date"]}")
    print(table)

def printDevicesTable(file):
    with open(file, "r") as f:
        devices = json.load(f)

    table = PrettyTable()
    table.field_names = ["IP", "Mac Address", "Owner", "Tipo", "Status"]
    table.clear_rows()
    for device in devices:
        table.add_row([device["IP"], device["Mac Address"], device["Owner"], device["Tipo"], device["Status"]])
    print("Dispositivos conhecidos na rede: ")
    print(table)