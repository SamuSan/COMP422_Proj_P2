import PIL, os, glob, fnmatch, numpy
from numpy import *
from PIL import Image

baseDir = "images/"
data = []

data_str = ""
att_str = []
left_eye = (5,5)
right_eye = (14,5)
sub ="" 
cur_file = ""
eye_template = {}


def extract_local_regions(Image):
	global att_str
	left =0
	upper =0
	right =0
	lower =0
	right = (Image.size[0] /2) 
	lower = (Image.size[1]/2)
	

	boxes = []
	boxes.append(cut_box(left, upper, right, lower,Image))#left quad
	boxes.append(cut_box(right + 1, upper, Image.size[0], lower,Image)) #righr qaud
	boxes.append(cut_box(left, lower + 1, right,Image.size[1],Image))#low left quad
	boxes.append(cut_box(right +1, lower +1, Image.size[0], Image.size[1],Image ))#low right quad	
	boxes.append(cut_box(9,0,10,Image.size[1], Image))#center strip
	boxes.append(cut_box(0,9,Image.size[0],10, Image))#
	boxes.append(cut_box(4,4,13,13,Image))
	add_val_strings(boxes)
	get_mean_dif(boxes)

def cut_box(lft,up,rght,lwr, Image):
	Image.load()
	box = (lft, up, rght ,lwr)
	i = Image.crop(box)
	return i

def add_val_strings(boxes):
	global data_str
	for x in boxes:
		data_str = data_str + str(std(x.getdata()) )+ ","
		data_str = data_str + str(mean(x.getdata()) )+ ","



def get_mean_dif(boxes):
	global data_str
	global att_str
	maxMean = max(mean(boxes[0].getdata()),mean(boxes[1].getdata()))
	minMean = min(mean(boxes[0].getdata()),mean(boxes[1].getdata()))
	data_str = data_str + str(maxMean - minMean)+ ","

def is_face():
	return not sub.__contains__("non-face")

def add_class(directory):
	global data_str
	if directory.__contains__("non-face"):
		data_str = data_str + ",0"

	else:
		data_str = data_str + ",1"


def eye_regions(image):
	print "Eye regions in " + sub + " image : " + str(cur_file)
	matrix = create_matrix(image)
	get_eye(matrix, left_eye, image)
	get_eye(matrix, right_eye, image)

def get_eye(matrix,center, image):
	global eye_template
	eye_vals = {}
	radius = 5		
	for i in range(19):
		for j in range(19):
			a = i - center[0]
			b = j - center[1]
			if a*a + b*b <= radius:
				eye_vals[(i,j)] = matrix[i][j]
	avge = mean(eye_vals.values())
	for x in eye_vals.keys():
		eye_template[x] = eye_vals[x]



def create_matrix(image):
	pixData = image.getdata()
	matrix = [[0 for x in xrange(19)] for x in xrange(19)]
	idx =0;
	for i in range(19):
		for j in range(19):
			matrix[i][j] = pixData[idx]
			idx+=1
	return matrix



def getTemplate():
	print "Doing template"
	fp = open("images" +'/train/face/'+'face02428.pgm', "r")
	img = Image.open(fp)
	eye_regions(img)	

def assess_template(image):
	global data_str
	global att_str
	dif=0.0
	num =0.0
	for x in list(eye_template.keys()):
		# print "Image value : " + str(image.getpixel(x)) + " Matrix value : " + str(eye_template[x])
		dif += abs(eye_template[x] - image.getpixel(x)  )
		num +=1
		# print x
	data_str = data_str + str(dif / num)





def process_images(imageDir):
	global data_str
	for subdir, dirs, files in os.walk(imageDir):
	    for file in files:
	    	# if fnmatch.fnmatch(file,'face02428TESTIMAGE.pgm'):
	    		
	    	if fnmatch.fnmatch(file,'*.pgm'):
	    		fp = open(subdir +'/'+file, "r")
	    		# print subdir
	    		sub = subdir
	    		cur_file = file
	    		img = Image.open(fp)
	    		pixVals = list(img.getdata())
	    		ex = img.getextrema()
	    		regions = extract_local_regions(img)
	    		data_str = data_str + str(ex[0] )+ ","

	    		data_str = data_str + str(ex[1] )+ ","

	    		data_str = data_str + str(std(img.getdata()) )+ ","

	    		data_str = data_str + str(mean(img.getdata()) )+ ","

	    		assess_template(img)
	    		add_class(subdir)
	    		data.append(data_str)
	    		data_str = ""
	    		fp.close()

def write_out(imageDir):
	fname = "imageRecogFeatures" + str(imageDir)
	outfile = open(fname, "w")
	outfile.write("@RELATION images\n\n")

	outfile.write("""@ATTRIBUTE left_quad_std NUMERIC
@ATTRIBUTE left_quad_mean NUMERIC
@ATTRIBUTE right_quad_std NUMERIC
@ATTRIBUTE right_quad_mean NUMERIC
@ATTRIBUTE low_left_quad_std NUMERIC
@ATTRIBUTE low_left_quad_mean NUMERIC
@ATTRIBUTE low_right_quad_std NUMERIC
@ATTRIBUTE low_right_quad_mean NUMERIC
@ATTRIBUTE cent_vert_strip_std NUMERIC
@ATTRIBUTE cent_vert_strip_mean NUMERIC
@ATTRIBUTE cent_hor_strip_std NUMERIC
@ATTRIBUTE cent_hor_strip_mean NUMERIC
@ATTRIBUTE cent_box_std NUMERIC
@ATTRIBUTE cent_box_mean NUMERIC
@ATTRIBUTE left_right_top_mean_dif NUMERIC
@ATTRIBUTE global_min NUMERIC
@ATTRIBUTE global_max NUMERIC
@ATTRIBUTE global_std NUMERIC
@ATTRIBUTE global_mean NUMERIC
@ATTRIBUTE eye_dif_val NUMERIC
@ATTRIBUTE class {0,1}\n""")

	outfile.write("\n@DATA\n")
	for x in data:
		s = str(x) + str("\n")
		outfile.write(s)
	outfile.close()


getTemplate()
process_images(baseDir + "train")
write_out("train")
data =[];
process_images(baseDir + "test")
write_out("test")








