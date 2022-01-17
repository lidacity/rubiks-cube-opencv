import base64
import cv2

def Header(FileName):
 """
 Write the <head> including css
 """
 if FileName is not None:
  SideMargin = 10
  SquareSize = 40
  Size = 3
  #
  with open(FileName, "a") as f:
   f.write("""\
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
 div.clear { clear: both; }
 div.clear_left { clear: left; }
 div.side { margin: %dpx; float: left; }
""" % SideMargin)
 
   for x in range(1, Size - 1):
    f.write(" div.col%d,\n" % x)
   f.write("""\
 div.col%d { float: left; }
 div.col%d { margin-left: %dpx; }
 div#upper, div#down { margin-left: %dpx; }
""" % ( Size - 1, Size, (Size - 1) * SquareSize, (Size * SquareSize) + (3 * SideMargin), ))
   f.write("""\
 span.half_square { width: %dpx; height: %dpx; white-space-collapsing: discard; display: inline-block; color: black; font-weight: bold; line-height: %dpx; text-align: center; }
 span.square { width: %dpx; height: %dpx; white-space-collapsing: discard; display: inline-block; color: black; font-weight: bold; line-height: %dpx; text-align: center; }
 div.square { width: %dpx; height: %dpx; color: black; font-weight: bold; line-height: %dpx; text-align: center; }
 div.square span { display: inline-block; vertical-align: middle; line-height: normal; }
 div#colormapping { float: left; }
 div#bottom { cursor: pointer; }
 div#bottom div.initial_rgb_values { display: none; }
</style>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<script>
$(document).ready(function()
{
 $("div#bottom").click(function(event)
 {
  if ($("div#bottom div.final_cube").is(":visible")) {
   $("div#bottom div.initial_rgb_values").show();
   $("div#bottom div.final_cube").hide();
  } else {
   $("div#bottom div.initial_rgb_values").hide();
   $("div#bottom div.final_cube").show();
  }
 })
});
</script>

<title>Rubiks Cube OpenCV Recognize</title>
</head>
<body>
<h1>Recognize</h1>
<h2>Sides</h2>
""" % ( int(SquareSize / 2), SquareSize, SquareSize, SquareSize, SquareSize, SquareSize, SquareSize, SquareSize, SquareSize, ))


def WriteSide(FileName, Face, Result, Source, Image):
 if FileName is not None:
  with open(FileName, "a") as f:
   f.write(f"<h3>Side {Face}</h3>\n")
   Res, JPG = cv2.imencode('.jpg', Source)
   UUE = base64.b64encode(JPG).decode('utf-8')
   #with open('temp/pic.jpg', 'wb') as f1:
   # f1.write(JPG1.tobytes())
   #print(UUE1)
   f.write("<table><tr><td>\n")
   f.write(f"<img alt='Source{Face}' src='data:image/jpg;base64,{UUE}' />\n")
   f.write("</td><td>&nbsp;&rarr;&nbsp;</td><td>\n")
   #
   Res, JPG = cv2.imencode('.jpg', Image)
   UUE = base64.b64encode(JPG).decode('utf-8')
   f.write(f"<img alt='Dest{Face}' src='data:image/jpg;base64,{UUE}' />\n")
   f.write("</td><td>&nbsp;&rarr;&nbsp;</td><td>\n")
   f.write("<pre>{")
   for i, (Key, Value) in enumerate(sorted(Result.items())):
    if i % 3 == 0:
     f.write(f"\n")
    f.write(f"\t{Key:2d}: '{Value}',")
   f.write("\n}</pre>\n")
   f.write("</td></tr></table>\n")
   f.write("<hr />\n")


def WriteResult(FileName, Get, Result):
 if FileName is not None:
  Name = {0: "ARRAY", 1: "STRING", 2: "JSON", 3: "DICT", }
  with open(FileName, "a") as f:
   f.write("<p>")
   f.write(f"<h2>Result: {Name[Get]}</h2>\n")
   f.write("<pre>\n")
   if Get == 0:
    f.write("[\n")
    for i, Value in enumerate(Result):
     if i % 9 == 0:
      f.write("\n\t")
     f.write(f"'{Value}', ")
    f.write("\n]\n")
   elif Get == 1:
    f.write(f"{Result}\n")
   elif Get == 2:
    f.write("{\n")
    for Key, Value in sorted(Result.items()):
     f.write(f"\t{Key}: {Value},\n")
    f.write("}\n")
   elif Get == 3:
    f.write("{\n")
    for Key, Value in sorted(Result.items()):
     f.write(f"\t{Key}: {Value},\n")
    f.write("}\n")
   f.write("</pre>\n</p>\n")


def Footer(FileName):
 if FileName is not None:
  with open(FileName, "a") as f:
   f.write("""\
</body>
</html>
""")
