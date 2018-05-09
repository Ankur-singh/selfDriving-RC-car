from __future__ import print_function
import pygame
import time
import numpy as np
from control import *
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-r', '--recordMode', required=False, help='record mode on/off', default='off')
ap.add_argument('-s', '--streamMode', required=False, help='stream mode on/off', default='off')
args = vars(ap.parse_args())

pygame.init()
gameDisplay = pygame.display.set_mode((300,300))
pygame.display.set_caption('blank')
pygame.display.update()

if(args['recordMode'] == 'off'):
	take = 0
else:
	from pivideostream_noModel import PiVideoStream
	take = 1
	print ('[INFO] Initializing record mode...')
	vs = PiVideoStream().start()
	time.sleep(2.0)
	
	
if(args['streamMode'] == 'off'):
	stream = 0
else:
	if(take == 0):
		from pivideostream_noModel import PiVideoStream
		print ('[INFO] Initializing Stream mode...')
		vs = PiVideoStream().start()
		time.sleep(2.0)
	
	stream = 1
	fps = 30
	clock = pygame.time.Clock()

controls = {'forward':forward, 'left':left, 'right':right, 'reverse':reverse}
gameExit = False
x = ""
start = time.time()
img = None
while not gameExit:
	#print('Dist: '+str(distance()))
	if x != "":
		controls[x](0.1)
		if(take == 1):
			img = vs.read()
			vs.write(img, x)
		if(stream == 1):
			if img is None:
				img = vs.read()
			img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
			img = np.rot90(img)
			surf = pygame.surfarray.make_surface(img)
			gameDisplay.blit(surf,(0,0))
			pygame.display.flip();
			clock.tick(fps)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				x = "left"
			elif event.key == pygame.K_RIGHT:
				x = "right"
			elif event.key == pygame.K_UP:
				x = "forward"
			elif event.key == pygame.K_DOWN:
				x = "reverse"
			elif event.key == pygame.K_q:
				gameExit = True
			print(x)
				
		elif event.type == pygame.KEYUP:
			print("Keyup")
			x = ""


pygame.quit()
print(str(time.time()-start))
if(take == 1 or stream == 1):
	vs.stop()
quit()
