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

def pretty_print(j):
    log(json.dumps(j, indent=4, sort_keys=True))

def get_ip(mac):
    regex = r"^\s*(\S+)\s*" + mac

    arp_a_output = subprocess.getoutput("arp -a")
    possible_ips = re.findall(regex, arp_a_output, re.MULTILINE)

    return possible_ips[0] if len(possible_ips) > 0 else None

class Device:
    def __init__(self, name, mac):
        self.name = name
        self.mac = mac
        self.prev_available = True
        self.ip = 'init'

    def update_ip(self):
        self.ip = get_ip(self.mac)

    @property
    def available(self):
        # return ping(self.ip)
        return self.ip is not None

    def update(self):
        self.update_ip()

        if self.available != self.prev_available:
            self.prev_available = self.available

            if self.available:
                log(f'Detected {self.name} {self.ip}')
                return True

            else:
                log(f'Lost {self.name}')

        return False

class BulbContainer:
    def __init__(self, id):
        self.id = id
        self.bulb = None
        self.find_bulb()

    def find_bulb(self):
        log("Searching for the bulb...")

        # Either make sure you have no VPN turned on, or pass your current IP (in local network) to 'interface='
        bulbs = discover_bulbs(timeout=5)
        log(f'Found {len(bulbs)} bulbs.')

        needed = [x for x in bulbs if self.id == x['capabilities']['id']]

        if len(needed) == 0:
            log(f"Error: Bulb with id {self.id} not found.")
            return

        log("Found the bulb.")

        needed = needed[0]
        self.bulb = Bulb(needed['ip'], duration=1000)

    def blink(self, duration, retry=10):
        if not self.bulb:
            self.find_bulb()

        if not self.bulb:
            log('Blink error: The bulb is not available.')
        else:
            try:
                self.bulb.turn_on(duration=1000)
                self.bulb.set_color_temp(6500)
                self.bulb.set_brightness(100)
                sleep(duration)
                self.bulb.turn_off(duration=10000)

                return
            except Exception as ex:
                log(f"Blink error: {ex}")
                self.bulb = None

        if retry > 0:
            log(f'Retrying... ({retry} more time)')
            self.blink(duration, retry=retry-1)

devices = [
    Device('Slava', 'b0-19-c6-d1-86-00'),
    Device('Vika', '64-70-33-7b-92-a0')
]

bulb = BulbContainer('0x00000000052bf666')

log("Testing engagement...")
bulb.blink(1)
log("Testing finished.")

for d in devices:
    d.update()
    log(f'Device {d.name} available: {d.available}')

while True:
    for d in devices:
        if d.update():
            bulb.blink(3) # 3 minutes

    sleep(1)