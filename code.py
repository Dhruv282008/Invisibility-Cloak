import cv2
import time
import numpy as np

#To save the output in a file output.avi
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

#Starting the Webcam
cap = cv2.VideoCapture(0)

#Allowing the webcam to start by making the code sleep for 2 seconds
time.sleep(2)
bg = 0
 
#Capturing background for 60 frames
for i in range(60):
  ret, bg = cap.read()

#Flipping the background because the camera captures the image inverted
bg = np.flip(bg, axis = 1)

#Reading the captured frame until the camera is open
while (cap.isOpened()):
  ret, img = cap.read()
  if not ret:
    break
  #Flipping the image for consistency
  img = np.flip(img, axis = 1)

  #Converting the color from BGR(Blue Green Red) to HSV(Hue Saturation Value), so that we can detect red color more efficiently. 
  #HSV :    1. Hue: This channel encodes color information. Hue can be thought of as an angle where 0 degree corresponds to the red color, 120 degrees corresponds to the green color, and 240 degrees corresponds to the blue color
  #         2. Saturation: This channel encodes the intensity/purity of color. For example, pink is less saturated than red.
  #         3. Value: This channel encodes the brightness of color. Shading and gloss components of an image appear in this channel reading the videocapture video.
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

  #Generating mask to detect color, these values can also be changed as per the color.
  lower_red = np.array([0, 120, 50])
  upper_red = np.array([10, 255, 255])
  mask_1 = cv2.inRange(hsv, lower_red, upper_red)

  lower_red = np.array([170, 120, 70])
  upper_red = np.array([180, 255, 255])
  mask_2 = cv2.inRange(hsv, lower_red, upper_red)

  mask_1 = mask_1 + mask_2

  #Open and expand the image where there is mask 1 (color)
  mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

  mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

  #Selecting only the part that does not have mask_1 and saving in mask_2
  mask_2 = cv2.bitwise_not(mask_1)

  #morphologyEx(src, dst, op, kernel) This method accepts the following parameters: ● src − An object representing the source (input) image. ● dst − object representing the destination (output) image.
  #● op − An integer representing the type of the Morphological operation. ● kernel − A kernel matrix.
  #morphologyEx() is the method of the class Img Processing which is used to perform operations on a given image

  #Keeping only the part of the images without the red color 
    #(or any other color you may choose)
  res_1 = cv2.bitwise_and(img, img, mask=mask_2)

    #Keeping only the part of the images with the red color
    #(or any other color you may choose)
  res_2 = cv2.bitwise_and(bg, bg, mask=mask_1)

    #Generating the final output by merging res_1 and res_2
  final_output = cv2.addWeighted(res_1, 1, res_2, 1, 0)
  output_file.write(final_output)
    #Displaying the output to the user
  cv2.imshow("magic", final_output)
  cv2.waitKey(1)


cap.release()
out.release()
cv2.destroyAllWindows()