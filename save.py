#!/usr/bin/env python
import sys
import cgi, cgitb
from PIL import Image

cgitb.enable()

form = cgi.FieldStorage()

bin1 = form["ref"]
fd = open("ref.png", 'wb')
fd.write(bin1.value)
fd.close()

bin2 = form["back"]
fd = open('back.jpg', 'wb')
fd.write(bin2.value)
fd.close()

imgb = Image.open("back.jpg")
imgr = Image.open("ref.png")
imgb.paste(imgr, (0,0), imgr)
imgb.save("./result.jpg")
print "Content-Type: text/plain"
print
print "Hello!"
