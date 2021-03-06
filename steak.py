# -*- coding: utf-8 -*-
"""steak.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UwJQLOxjkDPqhNQCjLj2q6aB5OFORAmf

Notes:
*   Change **url** variable to test a different image.
Future:
*   Adjust for camera focal length -- stitch images?
"""

# import packages
import cv2 #opencv library
from matplotlib import pyplot as plt
import numpy as np
import requests
import imutils
import cv2
import itertools
from google.colab.patches import cv2_imshow #fixes colab bug
#NOTE: works best with a black background

#Get and prep image
#white image
#url = "https://media.istockphoto.com/photos/ribeye-beef-steak-isolated-on-white-picture-id155380939?b=1&k=20&m=155380939&s=170667a&w=0&h=dg_vMJhrNUR345ngE8RgBzixhctYA15BZWpRlsdPzhc="
#other test images:
#https://thumbs.dreamstime.com/b/raw-chicken-meat-isolated-black-background-clipping-path-175187093.jpg

#black image
url = "https://s3.envato.com/files/267533387/28743%201.jpg"

r = requests.get(url)
with open('food.jpg', 'wb') as f: #open as write binary - img file
    f.write(r.content) 

#load image 
#convert to grayscale, apply Gaussian blur
image = cv2.imread("food.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

#remove noise
thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=2)

#find largest contour
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	    cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = max(cnts, key=cv2.contourArea)

#determine max points
extLeft = tuple(c[c[:, :, 0].argmin()][0])
extRight = tuple(c[c[:, :, 0].argmax()][0])
extTop = tuple(c[c[:, :, 1].argmin()][0])
extBot = tuple(c[c[:, :, 1].argmax()][0])
print("Leftmost point:", extLeft)
print("Rightmost point:", extRight)
print("Top point:", extTop)
print("Bottom point:", extBot)
#draw outlines and points
cv2.drawContours(image, [c], -1, (0, 255, 255), 2)
cv2.circle(image, extLeft, 8, (0, 0, 255), -1)
cv2.circle(image, extRight, 8, (0, 255, 0), -1)
cv2.circle(image, extTop, 8, (255, 0, 0), -1)
cv2.circle(image, extBot, 8, (255, 255, 0), -1)
# show image
cv2_imshow(image) #fixes error message
cv2.waitKey(0)

#generate rectangle
#top left, bottom right
#(left, top), (right, bottom)
#GCODE FILE
#G01 X64 Y100
#G01 X64 Y246
cv2.rectangle(image,(extLeft[0],extTop[1]),(extRight[0], extBot[1]),(0, 255, 0),1)
cv2_imshow(image)

"""GRID_SIZE controls the spacing between points

*   Increase for fewer coordinates
*   Decrease for more coordinates
"""

coordX = [ ]
coordY = [ ]

GRID_SIZE = 10 #adjustable
for x in range(extLeft[0], extRight[0], GRID_SIZE):
     cv2.line(image, (x, extBot[1]), (x, extTop[1]), (0, 255, 0), 1, 1)
     #print("x coordinate is: ", x)
     coordX.append(x)
     #print("coordx: ", coordX[0])
#start, end
'''
print("image right:", image.shape[0])
print("steak right:", extRight[0], extTop[0])
'''

for y in range(extTop[1], extBot[1], GRID_SIZE):
     cv2.line(image, (extLeft[0],y), (extRight[0],y), (0, 255, 0), 1, 1)
     #print("y coordinate is: ", y)
     coordY.append(y)

#coord_pairs = []
'''
coord_pairs = zip(coordX, coordY)
pairs_list = list(coord_pairs)
print(list(pairs_list))
'''

pairs = list(map(list, zip(coordX, coordY)))
#print("Coordinate pairs: ", pairs)

'''
for n in range(extBot[1], extTop[1], GRID_SIZE):
     cv2.line(image, (250,n), (250, n), (0, 0, 255), 1, 1)
'''
#vertical completed
'''
y = 100
cv2.line(image, (extBot[0], y), (extTop[1], y), color=(0,0,255), thickness=4)
'''
cv2_imshow(image)
key = cv2.waitKey(0)

"""*   Click Files on left tab to view coordinates.txt, where the outputted coordinates are stored.
  *   Can change which file you want to output the results to by changing the "coordinates.txt" argument in f = open("coordinates.txt", "w").
*   Change base_url variable if IP address, etc. changes.
*   Change speed variable to change the "FXXX" parameter.



"""

f = open("coordinates.txt", "w")
combined = []

#format: http://192.168.0.182/rr_gcode?gcode=G01 X250 Y250 F1000
for r in itertools.product(coordX, coordY): 
  #print("X" + str(r[0]) + "\t" + "Y" + str(r[1],), file = f)

  #NOTE: want to print the URL version? Comment out the above line and uncomment (delete the #) for the 2 lines below
  #print(base_url + "X" + str(r[0]) + "\t" + "Y" + str(r[1],), file = f)
  #base_url = "http://192.168.0.182/rr_gcode?gcode=G01 "
  
  speed = "F1000"
  print("G01" + " " + "X" + str(r[0]) + " " + "Y" + str(r[1],) + " " + speed, file = f)
  #f.write(str(r[0]) + "\t" + str(r[1]))

f.close()
#around ~1520 combos should output
print("Coordinate pairs: ", combined)

#EXTRA TESTING...
width = extRight[0] - extLeft[0]
height = extBot[1] - extTop[1]
print("height:", height, "width:", width)

cameraX = width / GRID_SIZE
cameraY = height / GRID_SIZE

print("camera at X:", cameraX, "\ncamera at Y:", cameraY)