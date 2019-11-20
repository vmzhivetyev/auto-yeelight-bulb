# What is it

This script toggles on a yeelight lamp for a certain amount of time (3 min.) 
when your iPhone (or other Wi-Fi enabled device) becomes reachable on the local network.
 
# How it works

## Attempts

### arp -a

The first tested solution was to dynamically discover bulb's and iPhone's ip addresses 
by their MAC addresses using the `arp -a` command. 

This method was tested: Continuous calls of `arp -a` were somehow killing network and causing all devices 
on the network to lose connection to the internet after some time (about 5 minutes). 

### ping

iPhone seems to not answer simple ping packets when it's screen locked.

### nmap (port 443 used for push notifications delivery)

```nmap -p 443 192.168.1.69 -Pn``` scans for services on port **443**.
 `-Pn` assumes that host is live, host discovery using ping is skipped.

## Final implementation

I decided to create **Static DHCP** table for the bulb and the iPhone (Set static IPs for them). 
Those IPs are hardcoded.

`nmap` is used to test 
if port **443** [(it's used for push notifications)](https://support.apple.com/en-us/HT203609) is available on the specific IP.

# Installation

1) Clone this repo

2) Install requirements

    `pip3 install -r requirements.txt`
    
3) Install nmap 

    `sudo apt-get install nmap`
    
4) Setup autorun for the script (for raspberry pi).

    > TODO

# Notes

## nmap
**nmap** will scan local network for devices to update **arp** cache.

```nmap -sP 192.168.1.*``` will scan the entire .1 to .254 range of IPs.
