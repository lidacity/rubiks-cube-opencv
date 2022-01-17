#!.env/bin/python

from rubiks_cube_opencv import GetRecognize
from rubiks_cube_opencv import ARRAY, STRING, JSON, DICT

import os
import sys


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
 #
 os.system("python2 solver.py < in.dat > result.txt")
 with open('result.txt', 'rb') as t:
  p = t.read().decode('utf-8')
 p = p.replace('\n', '')
 return p
 


def main():
 #print(GetRecognize(Debug="report.html", Get=JSON))
 #sys.exit(0)
 #
 Cube = GetRecognize(Debug="report.html")
 F, R, B, L, U, D = Cube["F"], Cube["R"], Cube["B"], Cube["L"], Cube["U"], Cube["D"]


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
 print(Solution(Position))



if __name__ == "__main__":
 main()
