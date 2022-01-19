import os
import sys
import time

import numpy as np
import cv2

import rubiks_cube_opencv.report

#Cube:

#           01 02 03
#           04 05 06
#           07 08 09
#
# 10 11 12  19 20 21  28 29 30  37 38 39
# 13 14 15  22 23 24  31 32 33  40 41 42
# 16 17 18  25 26 27  34 35 36  43 44 45
#
#           46 47 48
#           49 50 51
#           52 53 54

#   U
# L F R B
#   D


Faces = { "U": 1, "L": 10, "F": 19, "R": 28, "B": 37, "D": 46, }

#Sides = [ "F", "R", "B", "L", "U", "D", ]
Sides = list(Faces.keys())

Colors = {
 "W": { "Lower": [70, 20, 130], "Upper": [180, 110, 255], }, #white
 "Y": { "Lower": [15, 90, 130], "Upper": [60, 245, 245], }, #yellow
 "B": { "Lower": [80, 180, 190], "Upper": [120, 255, 255], }, #blue
 "O": { "Lower": [5, 150, 150], "Upper": [15, 235, 250], }, #orange
 "G": { "Lower": [60, 110, 110], "Upper": [100, 220, 250], }, #green
 "R": { "Lower": [120, 120, 140], "Upper": [180, 250, 200], }, #red
}

ARRAY, STRING, JSON, DICT = range(4)


def Extract(SourceImage, Face, IsJson=False, Debug=None, Show=False):
 Result = {}
 #
 Image = cv2.bilateralFilter(SourceImage, 9, 75, 75)
 Image = cv2.fastNlMeansDenoisingColored(Image, None, 10, 10, 7, 24)
 Width, Height = Image.shape[:2]
 HSV = cv2.cvtColor(Image, cv2.COLOR_BGR2HSV) # HSV image
 #
 Side = Faces[Face.upper()]
 for Color, Value in Colors.items():
  # HSV color code lower and upper bounds
  Lower, Upper = np.array(Value["Lower"], dtype=np.uint8), np.array(Value["Upper"], dtype=np.uint8)
  FrameThreshed = cv2.inRange(HSV, Lower, Upper)
  Gray = FrameThreshed
  if Show:
   cv2.imshow(Color, FrameThreshed)
   cv2.waitKey()
   cv2.destroyAllWindows()
  Ret, Thresh = cv2.threshold(FrameThreshed, 127, 255, cv2.THRESH_BINARY)
  Contours, Hierarchy = cv2.findContours(Thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  Areas = [int(cv2.contourArea(c)) for c in Contours]
  MaxArea = max(Areas) if Areas else 0
  #
  for i, a in enumerate(Areas):
   if a - MaxArea in range(-1000, 1000) and a >= 1500:
    x, y, w, h = cv2.boundingRect(Contours[i])
    Centroid_x, Centroid_y = int((x + x + w) / 2), int((y + y + h) / 2)
    Z = None
    for c in Contours[i]:
     Z = 3 * Centroid_y // Height * 3 + 3 * Centroid_x // Width # Achtung! That's right
     if IsJson:
      Result[Side + Z] = tuple(np.array(cv2.mean(Image[y:y+h, x:x+w])).astype(np.uint8))[2::-1] #Average color (BGR->RGB)
      #Result[Side + Z] = [int(i) for i in list(np.array(cv2.mean(Image[y:y+h, x:x+w])))[2::-1]] #Average color (BGR->RGB)
     else:
      Result[Side + Z] = Color
    if Debug is not None:
     cv2.rectangle(Image, (x, y), (x + w, y + h), (0, 255, 255), 2)
     cv2.circle(Image, (Centroid_x, Centroid_y), 4, (255, 255, 255), 2)
     cv2.circle(Image, (Centroid_x, Centroid_y), 2, (0, 0, 255), 2)
     cv2.putText(Image, Color, (Centroid_x, Centroid_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (64, 64, 64), 2)
 #
 if Debug is not None:
  Rows = [0, Height // 3, 2 * Height // 3, Height]
  Cols = [0, Width // 3, 2 * Width // 3, Width]
  cv2.line(Image, (Rows[0], Cols[1]), (Rows[3], Cols[1]), (255, 0, 0), 2)
  cv2.line(Image, (Rows[0], Cols[2]), (Rows[3], Cols[2]), (255, 0, 0), 2)
  cv2.line(Image, (Rows[1], Cols[0]), (Rows[1], Cols[3]), (255, 0, 0), 2)
  cv2.line(Image, (Rows[2], Cols[0]), (Rows[2], Cols[3]), (255, 0, 0), 2)
  ImageName = os.path.splitext(os.path.join("temp", f"{Face}.jpg"))[0] + '_extracted.jpg'
  if Show:
   cv2.imshow(ImageName, Image)
   cv2.waitKey()
   cv2.destroyAllWindows()
  cv2.imwrite(ImageName, Image)
 report.WriteSide(Debug, Face, Result, SourceImage, Image)
 return Result


def CaptureImage(ImageName, Debug=False, Show=False):
 TimeOut = 15
 FirstTime = time.time()
 LastTime = FirstTime
 Cam = cv2.VideoCapture(0)
 cv2.namedWindow("cropped", cv2.CV_WINDOW_AUTOSIZE)
 cv2.namedWindow("Smile :D", cv2.CV_WINDOW_AUTOSIZE)
 print('Ready')
 s = True
 while s:
  s, Image = Cam.read()
  cv2.rectangle(Image, (300, 300), (100, 100), (0, 255, 0), 3)
#  cv2.imshow("Smile :D", Image)
#  cv2.imshow("cropped", Image)
#  if cv2.waitKey(33) == ord('a'):
#   print "pressed a"
#   cv2.imwrite("photo/captured.png", im)
#   Image = cv2.imread("photo/captured.jpg")
#   cv2.imshow("capture", Image)
  CropImage = Image[100:300, 100:300]
#  cv2.imshow("croppe", crop_imCropImage)
#  cv2.imwrite("photo/cropped.jpg", CropImage)
  NewTime = time.time()
  if NewTime - LastTime > TimeOut:
   LastTime = NewTime
   print(f"Its been {NewTime - FirstTime} seconds")
   cv2.imwrite(ImageName, CropImage)
   break
  Key = cv2.waitKey(10)
  if Key == 27:
   print('done')
   cv2.destroyWindow("Smile :D")
   break
#  sys.exit(0)


def GetRecognize(List=None, Get=DICT, Show=False, Debug=None):
 report.Header(Debug)
 Cube = {}
 for Side in Sides:
  if List is None:
   Image = cv2.imread(os.path.join("images", f"{Side}.bmp"))
  elif isinstance(List[Side], str):
   Image = cv2.imread(List[Side])
  else:
   Image = List[Side]
  Cube[Side] = Extract(Image, Side, IsJson=Get==JSON, Show=Show, Debug=Debug)
 #
 Result = None
 if Get == DICT:
  Result = Cube
 else:
  Json = {}
  for _, Color in Cube.items():
   Json.update(Color)
  if Get == JSON:
   Result = Json
  #
  Array = [Color for _, Color in sorted(Json.items())]
  if Get == ARRAY:
   Result = Array
  elif Get == STRING:
   Result = "".join(Array)
 report.WriteResult(Debug, Get, Result)
 #
 report.Footer(Debug)
 return Result

