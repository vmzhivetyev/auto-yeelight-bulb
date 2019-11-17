import pyautogui
import numpy as np
from PIL import Image
import colorsys

# import matplotlib.pyplot as plt
# from PIL import Image
# pic = Image.open("kek.jpg")

def mymean(pic):
	di = {}
	pixels = np.array(pic)
	for x in pixels:
		for y in x:
			yy = tuple(y)
			if not yy in di:
				di[yy] = 0
			di[yy] = di[yy] + 1

	di = sorted(di.items(), key=lambda kv: kv[1])
	di = di[-50:]
	di = [(x[0]) for x in di]
	print(di)

	dimean = np.mean(di, axis=(0))

	print('dimean = ',dimean)

	return dimean

def fullmean(pic):
	pixels = np.array(pic)
	fullmean = (np.mean(pixels, axis=(0, 1)))
	print('fullmean = ',fullmean)
	return fullmean


import socket
myip = socket.gethostbyname(socket.getfqdn())
print(myip)
# exit(0)


from time import sleep
from yeelight import discover_bulbs, Bulb
bulbs = discover_bulbs() # Either make sure you have no VPN turned on, or pass your current IP (in local network) to 'interface='

import json
bulbs_json = json.dumps(bulbs, indent=4, sort_keys=True)
print(bulbs_json)
exit(0)

if len(bulbs) > 0:
	bulbip = bulbs[0]['ip']

bulbs = [Bulb(x['ip'], duration=1000) for x in bulbs]
for b in bulbs:
	# b.start_music()
	print('initialized bulb ', b)


# bulb = Bulb(bulbip, duration=1000)
# bulb.start_music()

def lerp(a,b,t):
	return a + t*(b-a)

dt = 0.1

ch,cs,cv = 0,0,0
while True:
	# print('sleep done')
	pic = pyautogui.screenshot()
	size = 1, 1
	pic.thumbnail(size, Image.ANTIALIAS)
	# print('screenshot taken')
	r,g,b = pic.getpixel((0,0))

	h,s,v = colorsys.rgb_to_hsv(r, g, b)
	h *= 360
	s *= 200
	# v /= 255
	# v = s/2

	lmult = 5
	ch = lerp(ch, h, dt * lmult)
	cs = lerp(cs, s, dt * lmult)
	cv = lerp(cv, v, dt * lmult)

	if s < 70:
		s = 80
	for b in bulbs:
		pass
		# b.set_hsv(h,s)
	# bulb.set_hsv(ch,cs)

	#bulb.set_brightness(v)
	# bulb.set_brightness(sum([r,g,b]) / 255*3 * 4)
	
	# print(ch,cs,cv)

	sleep(dt)