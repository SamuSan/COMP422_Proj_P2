import PIL, os, glob, fnmatch, numpy
from numpy import *
from PIL import Image
print "Doing a python"

print os.getcwd()

imageDir = "images/"
images = {"":Image}


def extract_local_regions(Image):
	left =0
	upper =0
	right =0
	lower =0
	right = (Image.size[0] /2)
	lower = (Image.size[1]/2)
	
	boxes = []
	boxes.append(cutBox(left, upper, right, lower,Image))
	boxes.append(cutBox(right + 1, upper, Image.size[0], lower,Image))
	boxes.append(cutBox(left, lower + 1, right,Image.size[1],Image))
	boxes.append(cutBox(right +1, lower +1, Image.size[0], Image.size[1],Image ))	
	add_val_strings(boxes)

def cutBox(lft,up,rght,lwr, Image):
	box = (lft, up, rght ,lwr)
	i = Image.crop(box)
	return i

def add_val_strings(boxes):
	global data_str
	for x in boxes:
		data_str = data_str + str(std(x.getdata()) )+ ", "
		data_str = data_str + str(mean(x.getdata()) )+ ", "
		print x	
		print std(x.getdata())
		print mean(x.getdata())




data_str = "";

for subdir, dirs, files in os.walk(imageDir):
    for file in files:
    	if fnmatch.fnmatch(file,'GULF_64.pgm'):
    		fp = open(subdir +'/'+file, "r")
    		img = Image.open(fp)
    		pixVals = list(img.getdata())
    		print img.size
    		pix = (0,0)
    		print mean(img.getdata())
    		print std(img.getdata())
    		print img.getpixel(pix)
    		# print img.histogram()
    		print ptp(img.getdata())
    		print img.getextrema()
    		regions = extract_local_regions(img)
    		# print pixVals
    		fp.close()
    		print file

print data_str








