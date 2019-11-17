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
    print(json.dumps(j, indent=4, sort_keys=True))

def engage_light():
    id_of_bulb = '0x00000000052bf666'

    # Either make sure you have no VPN turned on, or pass your current IP (in local network) to 'interface='
    bulbs = discover_bulbs()
    print(f'Found {len(bulbs)} bulbs.')

    needed = [x for x in bulbs if id_of_bulb == x['capabilities']['id']]

    if len(needed) == 0:
        print(f"Error: Bulb with id {id_of_bulb} not found.")
        return

    needed = needed[0]
    bulb = Bulb(needed['ip'], duration=1000)
    # bulb.set_hsv(0, 0, 0)
    bulb.turn_on(duration=1000)
    bulb.set_color_temp(6500)
    bulb.set_brightness(100)
    sleep(5)
    bulb.turn_off(duration=10000)

# engage_light()

slava_iphone_mac = 'b0-19-c6-d1-86-00'
vika_iphone_mac = '64-70-33-7b-92-a0'

# while True:

def get_ip(mac):
    regex = r"^\s*(\S+)\s*" + mac

    arp_a_output = subprocess.getoutput("arp -a")
    possible_ips = re.findall(regex, arp_a_output, re.MULTILINE)

    return possible_ips[0] if len(possible_ips) > 0 else None

print(get_ip(slava_iphone_mac))

slava_prev = False
vika_prev = False
while True:
    slava = get_ip(slava_iphone_mac)
    vika = get_ip(vika_iphone_mac)

    # Based on ping:
    # ping_slava = ping(slava)
    # ping_vika = ping(vika)

    ping_slava = slava is not None
    ping_vika = vika is not None

    print(slava, vika, ping_slava, ping_vika)

    if ((not slava_prev) and ping_slava) or \
        ((not vika_prev) and ping_vika):
        print('Engaging...')
        engage_light()

    slava_prev = ping_slava
    vika_prev = ping_vika
    sleep(1)