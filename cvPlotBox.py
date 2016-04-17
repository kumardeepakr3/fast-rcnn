import cv2
import numpy as np
from collections import defaultdict
from os.path import isfile


fileName = "/home/deepak/INRIA/data/comp4-3935_det_test_person.txt"
imagePath = "/home/deepak/INRIA/data/Images/"
outPath = "/home/deepak/INRIA/data/Output/"
font = cv2.FONT_HERSHEY_SIMPLEX



def getBoxes(fileName):
	image_box_dict = defaultdict(list)
	with open(fileName) as f:
		lines = [x.strip() for x in f.readlines()]
	listOfBoxes = [x.split(' ') for x in lines]
	for i, roi in enumerate(listOfBoxes):
		image_box_dict[roi[0]].append(roi)
	return image_box_dict


def plotBoxes(image_box_dict):
	dictKeys = image_box_dict.keys()
	for imgName in dictKeys:
		if isfile(imagePath+imgName+".png"):
			imgExtPath = imagePath+imgName+".png"
		elif isfile(imagePath+imgName+".jpg"):
			imgExtPath = imagePath+imgName+".jpg"
		else:
			print "ERROR IMG DOES NOT EXIST"
		img = cv2.imread(imgExtPath)
		box_for_img = image_box_dict[imgName]
		for box in box_for_img:
			prob = str(box[1])
			xmin = int(float(box[2]))
			ymin = int(float(box[3]))
			xmax = int(float(box[4]))
			ymax = int(float(box[5]))
			if float(prob) > 0.1:
				cv2.rectangle(img, (xmin,ymin), (xmax, ymax), (0,0,255), 3)
				cv2.putText(img, prob, (xmin, ymin-4), font, 0.5, (255,255,255), 1)
		cv2.imwrite(outPath+imgName+".jpg", img)
		# break


plotBoxes(getBoxes(fileName))
# img = cv2.imread('/home/deepak/INRIA/data/Images/person_and_bike_190.png')

# font = cv2.FONT_HERSHEY_SIMPLEX
# cv2.putText(img,'Hello World!',(224,152-4), font, 0.5 ,(255, 255,0),1)
# cv2.rectangle(img, (224,152), (300, 360), (0,0,255), 2)

# cv2.imshow('pic', img)
# cv2.waitKey(0)
# #224.3 152.8 300.7 360.0
# # 290.6 121.1 380.4 374.0