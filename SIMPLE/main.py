from meshtastic import serial_interface
import math
import os


interface = serial_interface.SerialInterface(dev='/dev/ttyUSB0')
while not interface.connected:
    pass
    
def onReceive(packet, interface):
    with open("messages.txt", "a") as a:
        a.write(f"{packet['text']}")

while shutdown == False:
    interface.addCallback(onReceive)
    task = input()
    #meshtastic word list
    meshtastic_wordlist = ["meshtastic", "mesh", "message", "messaging", "loRa", "LoRa", "radio", "walkie-talkie", "walkie talkie","emergency comms", "comms", "communication"]
    if any(words in task.lower for words in meshtastic_wordlist):
        app_exit = False
        while app_exit == False:
            message = input("You: ")
            if message.upper == "EXIT APP":
                app_exit = True
            else:
                interface.sendText(message, destinationId=portnums_pb2.PortNum.TEXT_MESSAGE_APP)
    file_wordlist = ["file", "files", "folder", "directory", "directories","folders"]
    elif any(words in task.lower for words in file_wordlist)