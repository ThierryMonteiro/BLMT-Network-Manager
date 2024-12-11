import threading
import time
from socket import socket, socketpair

import detectHosts
import OwnInformation
import auxi
import asyncio

def ensure(cond: bool, message: str):
    if not cond:
        print(message)
        exit(1)

def fail(message: str):
    print(message)
    exit(1)

class LexemeExchanger:
    def __init__(self, s: socket):
        self.s = s
        self.remainder = [b'']

    # Não é possível que na história do Python eu seja o primeiro
    # pessoa a ter que codar isso...
    def nextLexeme(self) -> str:
        assert len(self.remainder) >= 1

        while 1 == len(self.remainder):
            data = self.s.recv(4096)
            if not data:
                print("I'm in love with the beat")
                exit(1)
            indivs = data.split(b'\0')
            self.remainder[0] += indivs.pop(0)
            self.remainder.extend(indivs)

        return self.remainder.pop(0).decode("utf-8");

def __someTable(le: LexemeExchanger, n_column: int) -> [(str,)]:
    n_row = int(le.nextLexeme())
    ensure(n_row >= 0, "Give me a reason for your love")
    print(n_row)

    return [tuple(le.nextLexeme() for _ in range(n_column)) for _ in range(n_row)]

def getInterfaces(le: LexemeExchanger) -> [(str, str, str, str)]:
    le.s.send(b"1.3.6.2.1\0ifTable\0R\0")
    return __someTable(le, 4)

def getDevices(le: LexemeExchanger, interface: str) -> [(str, str, str, str, str)]:
    assert '\0' not in interface
    print("hey")
    le.s.send(b"1.3.6.3.2163275\0discoverDevices\0W\0" + interface.encode("utf-8") + b'\0')
    print("ho")
    le.s.send(b"1.3.6.3.2163275\0discoveredDeviceTable\0R\0")
    print("hooooo")
    return __someTable(le, 5)

# OwnInformation pega as informações de rede do prórpio host

async def main():

    ownInformation = OwnInformation.managerDevice()
    ownInformation.print_table()
    IPs = ownInformation.ips
    masks = ownInformation.getNetworkRange()

    informations_list = []

    for i in range(len(IPs)):
        if i == 0:
            detectedHosts = detectHosts.detectHosts(IPs[i], masks[i])
            detectedHosts.printTable()
            informations_list.append(await detectedHosts.getInformations())

    print("Informações dos hosts detectados:")

    jsonFile = "./output.json"
    data = auxi.loadData(jsonFile)
    for info in informations_list:
        auxi.addContent(data, info)
    auxi.saveData(jsonFile, data)

    auxi.printLogTable("./output.json")
    auxi.printDevicesTable("./currentChanges.json")

um = None
outro = None

def gerenciando() -> None:
    le = LexemeExchanger(um)
    withIp = next(i for i in getInterfaces(le) if len(i[1]) > 1)
    print(withIp[0])
    devices = getDevices(le, withIp[0])
    for dev in devices:
        print(dev[0], dev[1], dev[2], dev[3], dev[4])
    time.sleep(2)
    print("after two seconds")
    devices = getDevices(le, withIp[0])
    for dev in devices:
        print(dev[0], dev[1], dev[2], dev[3], dev[4])
    le.s.close()

def agenciando() -> None:
    le = LexemeExchanger(outro)
    while True:
        match le.nextLexeme():
            case "1.3.6.3.2163275": # A nossa MIB
                match le.nextLexeme():
                    case "discoverDevices":
                        ensure("W" == le.nextLexeme(), "what for")
                        le.nextLexeme()
                    case "discoveredDeviceTable":
                        ensure("R" == le.nextLexeme(), "love is like a fantasy for you and me")
                        le.s.send(b'1\00010.1.1.7\0003a:8a:10:89:91:12\0UNDEFINED\0Not Router\000Inativo\0')
                    case _:
                        fail("c'mon raise your hands up")
            case "1.3.6.2.1": # MIB-II
                match le.nextLexeme():
                    case "ifTable":
                        ensure("R" == le.nextLexeme(), "I want you and you want me")
                        le.s.send(b'1\0{D64760D3-955B-4B84-A7BB-E7A5EE73C5A0}\000192.168.56.1\000255.255.255.0\000192.168.56.255\0')
                    case _:
                        fail("let the music take you to the highest high")
                pass
            case _:
                fail("you can the sky")

if __name__ == "__main__":
    #asyncio.run(main())

    (um, outro) = socketpair()

    threading.Thread(target=agenciando).start()
    lala = threading.Thread(target=gerenciando)
    lala.start()
    lala.join()
