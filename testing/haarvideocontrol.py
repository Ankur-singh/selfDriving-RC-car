from __future__ import print_function
import pygame
import time
from videocontrolbase import PiVideoStream
import cv2
import numpy as np
from control import *
import picamera
import imutils
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import argparse

def maxIndex(tup):
	tup = tuple(tup)
	max_ = max(tup)
	if max_ > 0.40:
		return tup.index(max(tup))
	else:
		return -1

def findContours(frame):
	frame = cv2.GaussianBlur(frame,(3,3),0)
	frame = cv2.Canny(frame, 30,150)
	(cnts,_) = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	return cnts

def drawContours(frame):
	global stop_cascade
        frame = cv2.flip(frame,0)
	cascade_obj = stop_cascade.detectMultiScale(frame,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))
        #cnts = findContours(frame)
        #frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        #cv2.drawContours(frame, cnts, -1, (0,255,0), 2)
        return frame, cascade_obj

def process(image):
        #image = frame[0:160,0:320]
        image = imutils.resize(image, width=320)
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to gray scale
        #cv2.imshow('gray', image)
        image = np.stack((image,)*3,-1)
        image = cv2.GaussianBlur(image, (3,3),0) # blurs the image
        #cv2.imshow('processed', image)

        image = cv2.resize(image,(32,32))
        #print image.shape
        image = image.astype('float')/255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        return image


vs = PiVideoStream().start()
time.sleep(2.0)

ap = argparse.ArgumentParser()
#ap.add_argument('-i','--image', required=False, help='path to image', default='./data/right')
ap.add_argument('-m','--model', required=False, help='path to image', default='./model.h5')
args =vars(ap.parse_args())

stop_cascade = cv2.CascadeClassifier('stop_sign.xml')

model_path = args['model']
print('[INFO] loading model...')
model = load_model(model_path)
count_a, count_b, count_c = 0,0,0
controls = {'forward':forward, 'left':left, 'right':right, 'reverse':reverse}
y = 'forward'

while True:
	#controls[x](0.1)
	frame = vs.read()
	frame_gray = frame
	cascade_obj = stop_cascade.detectMultiScale(frame_gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))
	#frame = imutils.resize(frame, width=640)
	image = frame[0:160,0:320]
	image = imutils.resize(image, width=320)
	#image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to gray scale
	#cv2.imshow('gray', image)
	image = np.stack((image,)*3,-1)
	image = cv2.GaussianBlur(image, (3,3),0) # blurs the image
	#cv2.imshow('processed', image)
	image = cv2.resize(image, (32,32))
	image = image.astype('float')/255.0
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)
	prob = model.predict(image)[0]
	'''
	frame = imutils.resize(frame, width=640)
	#frame = cv2.imread(args['image'])
                
	image = process(frame[0:160,0:320]) 
	prob = model.predict(image)[0]
	frame, cascade_obj = drawContours(frame)
	'''
	print(prob)
	i = maxIndex(prob)
	if(i == 0):
		print('forward')
		x = 'forward'
		count_a += 1
	elif(i == 1):
		controls['forward'](0.1)
		print('left')
		x = 'left'
		count_b += 1
	elif(i == 2):
		controls['forward'](0.1)
		print('right')
		#print(prob[2])
		x = 'right'
		if(prob[2] == 1):
			#print(prob[2])
			controls['right'](0.1)
		if((x == y) and (prob[2] - prob[0] <= 0.2)):
			x = 'forward'
		else:
			x = 'right'
		count_c += 1

	if(i != -1):
		if((x == 'right') and (prob[2] != 1)):
			controls[x](0.05)
		else:
			controls[x](0.1)

		y = x

	for (x_pos, y_pos, width, height) in cascade_obj:
		cv2.rectangle(frame, (x_pos+5, y_pos+5), (x_pos+width-5, y_pos+height-5), (255, 255, 255), 2)
		#v = y_pos + height - 5
		if width/height == 1:
			cv2.putText(frame, 'STOP', (x_pos, y_pos-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

	cv2.imshow('frame', frame)
	key = cv2.waitKey(1) &0xFF
	if key == ord('q'):
		break

vs.stop()
quit()
