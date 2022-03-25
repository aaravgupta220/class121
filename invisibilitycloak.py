import cv2
import time
import numpy as np

# To save the output in a file output.avi
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

#Starting the webcam
cap = cv2.VideoCapture(0)

#Allowing the webcam to start by making the code sleep for two seconds
time.sleep(2)
bg = 0 

#capturing bg for 60 frames
for i in range(60) :
  ret, bg = cap.read()

#Flipping the bg
bg = np.flip(bg, axis = 1)

#Reading the captured frame until the camera is open
while (cap.isOpened()):
  ret, img = cap.read()
  if not ret :
    break
  img = np.flip(img, axis = 1)

  # COnverting the color from BGR to HSV
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

  # Generating mass to detect red color these calues can also be changed as per the color
  lower_red1 = np.array([0, 120, 50])
  upper_red1 = np.array([10, 255, 255])
  mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

  lower_red2 = np.array([170, 120, 70])
  upper_red2 = np.array([180, 255, 255])
  mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

  mask1 = mask1 + mask2

  #Open and expand the image where there is mask1(color)
  mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint(8)))
  mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint(8)))

  #Selecting only the part that does not have mask 1 and saving in mask 2
  mask2 = cv2.bitwise_not(mask1)

  #Keeping only the part of the images without the red color 
  result1 = cv2.bitwise_and(img, img, mask = mask2)

  #Replacing only the part of the images with the red color with background
  result2 = cv2.bitwise_and(bg, bg, mask = mask1)

  #Generating the final ouput by merging result 1 and 2
  final_output = cv2.addWeighted(result1, 1, result2, 1, 0)
  output_file.write(final_output)

  #Displaying the output to the user
  cv2.imshow('Magic', final_output)
  cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()