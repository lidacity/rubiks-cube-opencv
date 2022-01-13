import numpy as np
import os
import cv2
import sys
import time


#def Merge(Dict1, Dict2):
#	return {**Dict1, **Dict2}
#	#return Dict1 | Dict2


def Extract(ImageName, Face):
	Bases = { "U": 1, "L": 10, "F": 19, "R": 28, "B": 37, "D": 46, }
	Colors = {
		"W": { "Lower": [70, 20, 130], "Upper": [180, 110, 255], },
		"Y": { "Lower": [15, 90, 130], "Upper": [60, 245, 245], },
		"B": { "Lower": [80, 180, 190], "Upper": [120, 255, 255], },
		"O": { "Lower": [5, 150, 150], "Upper": [15, 235, 250], },
		"G": { "Lower": [60, 110, 110], "Upper": [100, 220, 250], },
		"R": { "Lower": [120, 120, 140], "Upper": [180, 250, 200], },
	}
	#
	print(f"Face \"{Face}\" from {ImageName}")
	Image = cv2.imread(ImageName)
	Image = cv2.bilateralFilter(Image, 9, 75, 75)
	Image = cv2.fastNlMeansDenoisingColored(Image, None, 10, 10, 7, 24)
	Result = {}
	#
	Width, Height = Image.shape[:2]
	Rows = [0, Height // 3, 2 * Height // 3, Height]
	Cols = [0, Width // 3, 2 * Width // 3, Width]
	#
	HSV = cv2.cvtColor(Image, cv2.COLOR_BGR2HSV) # HSV image
	#
	Side = Bases[Face.upper()]
	for Color, Value in Colors.items():
		# HSV color code lower and upper bounds
		Lower = np.array(Value["Lower"], dtype=np.uint8)
		Upper = np.array(Value["Upper"], dtype=np.uint8)
		FrameThreshed = cv2.inRange(HSV, Lower, Upper)
		Gray = FrameThreshed
		#cv2.imshow(Color, FrameThreshed)
		Ret, Thresh = cv2.threshold(FrameThreshed, 127, 255, cv2.THRESH_BINARY)
		Contours, Hierarchy = cv2.findContours(Thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		Areas = [int(cv2.contourArea(c)) for c in Contours]
		MaxArea = max(Areas) if Areas else 0

		Get = []
		for i, a in enumerate(Areas):
			if a - MaxArea in range(-1000, 1000) and a >= 1500:
				x, y, w, h = cv2.boundingRect(Contours[i])
				Centroid_x, Centroid_y = int((x + x + w) / 2), int((y + y + h) / 2)
				cv2.rectangle(Image, (x, y), (x + w, y + h), (0, 255, 255), 2)
				cv2.circle(Image, (Centroid_x, Centroid_y), 4, (255, 255, 255), 2)
				cv2.circle(Image, (Centroid_x, Centroid_y), 2, (0, 0, 255), 2)
				for c in Contours[i]:
					if Cols[0] < Centroid_x < Cols[1]:
						if Rows[0] < Centroid_y < Rows[1]:
							Result[Side + 0] = Color
						elif Rows[1] < Centroid_y < Rows[2]:
							Result[Side + 3] = Color
						elif Rows[2] < Centroid_y < Rows[3]:
							Result[Side + 6] = Color
					if Cols[1] < Centroid_x < Cols[2]:
						if Rows[0] < Centroid_y < Rows[1]:
							Result[Side + 1] = Color
						elif Rows[1] < Centroid_y < Rows[2]:
							Result[Side + 4] = Color
						elif Rows[2] < Centroid_y < Rows[3]:
							Result[Side + 7] = Color
					if Cols[2] < Centroid_x < Cols[3]:
						if Rows[0] < Centroid_y < Rows[1]:
							Result[Side + 2] = Color
						elif Rows[1] < Centroid_y < Rows[2]:
							Result[Side + 5] = Color
						elif Rows[2] < Centroid_y < Rows[3]:
							Result[Side + 8] = Color

	cv2.line(Image, (Rows[0], Cols[1]), (Rows[3], Cols[1]), (255, 0, 0), 2)
	cv2.line(Image, (Rows[0], Cols[2]), (Rows[3], Cols[2]), (255, 0, 0), 2)
	cv2.line(Image, (Rows[1], Cols[0]), (Rows[1], Cols[3]), (255, 0, 0), 2)
	cv2.line(Image, (Rows[2], Cols[0]), (Rows[2], Cols[3]), (255, 0, 0), 2)
	#cv2.imshow(imageName, im)
	#cv2.waitKey()
	#cv2.destroyAllWindows()
	cv2.imwrite(os.path.splitext(ImageName)[0] + '_extracted.jpg', Image)
	print(f"{Face.upper()}: {Result}")
	return Result


def CaptureImage(ImageName):
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
#		cv2.imshow("Smile :D", Image)
#		cv2.imshow("cropped", Image)
#		if cv2.waitKey(33) == ord('a'):
#			print "pressed a"
#			cv2.imwrite("photo/captured.png", im)
#			Image = cv2.imread("photo/captured.jpg")
#			cv2.imshow("capture", Image)
		CropImage = Image[100:300, 100:300]
#		cv2.imshow("croppe", crop_imCropImage)
#		cv2.imwrite("photo/cropped.jpg", CropImage)
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
#		sys.exit(0)


def Solution(Position):
	Pos = ''
	for a in range(12):
		for i in range(2):
			Pos += Position[a * 2 + i]
		Pos += " "
	for a in range(8):
		for i in range(3):
			Pos += Position[24 + a * 3 + i]
		Pos += " "
	Pos = Pos.strip()
	with open('in.dat', 'w') as t:
		t.write(Pos)
	print(Pos)

	os.system("python2 solver.py < in.dat > result.txt")
	with open('result.txt', 'rb') as t:
		p = t.read().decode('utf-8')
	p = p.replace('\n', '')
	print(p)
	

def GetCube(Cube):
	Result = []
	for Key, Color in sorted(Cube.items()):
		Result.append(Color)
	return Result


def main():
	F = Extract('photo/F.bmp', 'f')
	R = Extract('photo/R.bmp', 'r')
	B = Extract('photo/B.bmp', 'b')
	L = Extract('photo/L.bmp', 'l')
	U = Extract('photo/U.bmp', 'u')
	D = Extract('photo/D.bmp', 'd')
#	print(GetCube({**F, **R, **B, **L, **U, **D}))
#	print("".join(GetCube({**F, **R, **B, **L, **U, **D})))

	Edges = [
		[ F[20], U[8], ],
		[ R[29], U[6], ],
		[ B[38], U[2], ],
		[ L[11], U[4], ],
		[ F[26], D[47], ],
		[ R[35], D[51], ],
		[ B[44], D[53], ],
		[ L[17], D[49], ],
		[ F[24], R[31], ],
		[ R[33], B[40], ],
		[ B[42], L[13], ],
		[ L[15], F[22], ],
	]

	TempEdges = [
		['F', 'U'],
		['R', 'U'],
		['B', 'U'],
		['L', 'U'],
		['F', 'D'],
		['R', 'D'],
		['B', 'D'],
		['L', 'D'],
		['F', 'R'],
		['R', 'B'],
		['B', 'L'],
		['L', 'F'],
	]

	Position = {}

	FinalEdges = [
		['O', 'B'],
		['Y', 'O'], # ?['O', 'Y'],
		['O', 'G'],
		['O', 'W'],
		['R', 'B'],
		['R', 'Y'],
		['R', 'G'],
		['R', 'W'],
		['B', 'Y'],
		['B', 'W'],
		['G', 'Y'],
		['G', 'W'],
	]

	for Pos, Color in enumerate(Edges):
		for i, c in enumerate(Color):
			P = None
			for j, f in enumerate(FinalEdges):
				if set(Color) == set(f):
					P = j * 2 + f.index(c)
					break
			Position[P] = TempEdges[Pos][i]

	print(f"Edges: {Edges}")
	print(f"TempEdges: {TempEdges}")


	Corners = [
		[ F[19], U[7], L[12], ],
		[ F[21], U[9], R[28], ],
		[ R[30], U[3], B[37], ],
		[ B[39], U[1], L[10], ],
		[ F[25], D[46], L[18], ],
		[ F[27], D[48], R[34], ],
		[ R[36], D[54], B[43], ],
		[ B[45], D[52], L[16], ],
	]

	TempCorners = [
		['F', 'U', 'L'], 
		['F', 'U', 'R'],
		['R', 'U', 'B'],
		['B', 'U', 'L'],
		['F', 'D', 'L'],
		['F', 'D', 'R'],
		['R', 'D', 'B'],
		['B', 'D', 'L'],
	]

	FinalCorners = [
		['O', 'B', 'Y'],
		['O', 'Y', 'G'],
		['O', 'G', 'W'],
		['O', 'W', 'B'],
		['R', 'Y', 'B'],
		['R', 'B', 'W'],
		['R', 'W', 'G'],
		['R', 'G', 'Y'],
	]

	for Pos, Color in enumerate(Corners):
		for i, c in enumerate(Color):
			P = None
			for j, f in enumerate(FinalCorners):
				if set(Color) == set(f):
					P = 24 + j * 3 + f.index(c)
					break
			Position[P] = TempCorners[Pos][i] 

	print(f"Corners: {Corners}")
	print(f"TempCorners: {TempCorners}")

	print(f"Position: {Position}")
	Solution(Position)
	
								
main()
