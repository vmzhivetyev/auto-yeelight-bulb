import colorsys
import os
import sys
from time import sleep
import json
from yeelight import discover_bulbs, Bulb
import subprocess
import re
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from datetime import datetime


def log(msg):
    print(datetime.now(), '>', msg)

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    if not host:
        return False

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', '-w', '200', host]

    return subprocess.call(command, stdout=open(os.devnull, 'wb')) == 0

def ping_nmap(ip, port):
    output = subprocess.getoutput(f"nmap -p {port} {ip} -Pn")
    return "Host is up." in output

def pretty_print(j):
    log(json.dumps(j, indent=4, sort_keys=True))

class Device:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip

        self.prev_available = True
        self.available = True
        self.triggered = False

        self.failCounter = 0

    def update(self):
        if ping_nmap(self.ip, 443):
            self.failCounter = 0
            self.available = True
            log(f'{self.name} pinged!')
        else:
            self.failCounter += 1
            log(f'{self.name} not pinged x{self.failCounter}')
            if self.failCounter >= 10:
                self.available = False

        if self.available != self.prev_available:
            self.prev_available = self.available

            if self.available:
                log(f'Detected {self.name} {self.ip}')
                self.triggered = True

            else:
                log(f'Lost {self.name}')

class BulbContainer:
    def __init__(self, ip):
        self.bulb = Bulb(ip, duration=1000)

    def blink(self, duration, retry=10):
        try:
            self.bulb.turn_on(duration=1000)
            self.bulb.set_color_temp(6500)
            self.bulb.set_brightness(100)
            sleep(duration)
            self.bulb.turn_off(duration=10000)

        except Exception as ex:
            log(f"Blink error: {ex}")
            self.bulb = None

            if retry > 0:
                log(f'Retrying... ({retry} more time)')
                self.blink(duration, retry=retry-1)

bulb = BulbContainer('192.168.1.70')
devices = [
    Device('Slava', '192.168.1.69'), # 'b0-19-c6-d1-86-00'
    Device('Vika', '192.168.1.65') # '64-70-33-7b-92-a0'
]

log("Testing bulb...")
bulb.blink(1)
log("Testing finished.")

for d in devices:
    d.update()
    log(f'Device {d.name} available: {d.available}')

while True:
    for d in devices:
        d.update()
        if d.triggered:
            d.triggered = False
            bulb.blink(3)

    sleep(1)