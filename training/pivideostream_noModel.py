from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2
import numpy as np
import time
 
class PiVideoStream:
	def __init__(self, resolution=(320, 240), framerate=32):
		# initialize the camera and stream
		self.camera = PiCamera()
		self.camera.resolution = resolution
		self.camera.framerate = framerate
		self.rawCapture = PiRGBArray(self.camera, size=resolution)
		self.stream = self.camera.capture_continuous(self.rawCapture,
			format="bgr", use_video_port=True)
 
		# initialize the frame and the variable used to indicate
		# if the thread should be stopped
		self.frame = None
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		Thread(target=self.update, args=()).start()
		return self
 
	def update(self):
		# keep looping infinitely until the thread is stopped
		for f in self.stream:
			# grab the frame from the stream and clear the stream in
			# preparation for the next frame
				
			#self.frame = f.array
			self.frame = cv2.cvtColor(np.array(f.array), cv2.COLOR_BGR2GRAY)
			#cv2.imshow("see me!", self.frame)
			#img = cv2.imread(self.frame)
			#img = cv2.resize(img,(32,32))
			#img = np.reshape(img,[1,32,32,3])
			#classes = model.predict(img)
			#print classes
			self.rawCapture.truncate(0)
			# if the thread indicator variable is set, stop the thread
			# and resource camera resources
			if self.stopped:
				self.stream.close()
				self.rawCapture.close()
				self.camera.close()
				return

	def read(self):
		# return the frame most recently read
		return self.frame

	def write(self, frame, label):
		cv2.imwrite("images/{}/frame_{}.jpg".format(label,time.time()), frame)

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
