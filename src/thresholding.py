import cv2
import numpy as np
import sys
import os.path
from matplotlib import pyplot as plt
from PIL import Image
import pytesseract

if len(sys.argv) != 4:
    print "%s input_dir output_dir text_dir" % (sys.argv[0])
    sys.exit()
else:
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    text_dir = sys.argv[3]

if not os.path.isdir(input_dir):
    print "No such directory '%s'" % input_dir
    sys.exit()

if not os.path.isdir(output_dir):
    print "No such directory '%s'" % output_dir
    sys.exit()

if not os.path.isdir(text_dir):
    print "No such directory '%s'" % text_dir
    sys.exit()

DEBUG = 1

for input_file_ in os.listdir(input_dir):

	# Load the image
	input_file = os.path.join(input_dir,input_file_)
	img_ = cv2.imread(input_file,0)
	print "Original image '%s'" % (input_file)
	# Add a border to the image for processing sake
	#img_ = cv2.copyMakeBorder(orig_img, 50, 50, 50, 50, cv2.BORDER_CONSTANT)
	
	img = cv2.resize(img_,(1000,1000), interpolation = cv2.INTER_CUBIC)
	# Calculate the width and height of the image
	img_y = len(img)
	img_x = len(img[0])
	
	if DEBUG:
	    print "Image is " + str(len(img)) + "x" + str(len(img[0]))
	
	#gray_img = cv2.cvtColor(img_,cv2.COLOR_BGR2GRAY)
	gray_img = img

	ret1,th1 = cv2.threshold(gray_img,180,255,cv2.THRESH_BINARY)
	
	th2 = cv2.adaptiveThreshold(gray_img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
	th3 = cv2.adaptiveThreshold(gray_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
	
#	titles = ['Original Image', 'Global Thresholding (v = 180)',
#	            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
#	images = [gray_img, th1, th2, th3]
#	for i in xrange(4):
#	    #cv2.imwrite(titles[i]+'.jpg',images[i])
#	    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
#	    plt.title(titles[i])
#	    plt.xticks([]),plt.yticks([])
#	plt.show()
	
	
	# Otsu's thresholding
	ret4,th4 = cv2.threshold(gray_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	# Otsu's thresholding after Gaussian filtering
	blur = cv2.GaussianBlur(gray_img,(5,5),0)

	th3 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
	blur1 = cv2.GaussianBlur(th3,(5,5),0)
	ret5,th5 = cv2.threshold(blur1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	#cv2.imwrite(output_file,th1)
	
	images = [gray_img, 0, th1,
	          gray_img, 0, th4,
	          blur, 0, th5]
	titles = ['Original Noisy Image','Histogram','Global Thresholding (v=180)',
	          'Original Noisy Image','Histogram',"Otsu's Thresholding",
	          'Gaussian filtered Image','Histogram',"Otsu's Thresholding"]
	for i in xrange(3):
	    plt.subplot(3,3,i*3+1),plt.imshow(images[i*3],'gray')
	    plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
	    plt.subplot(3,3,i*3+2),plt.hist(images[i*3].ravel(),256)
	    plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
	    plt.subplot(3,3,i*3+3),plt.imshow(images[i*3+2],'gray')
	    plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])
	plt.show()

	kernel = np.ones((5,5),np.uint8)
	blackhat = cv2.morphologyEx(th3, cv2.MORPH_BLACKHAT, kernel)
	ret,inverse_blackhat = cv2.threshold(blackhat,127,255,cv2.THRESH_BINARY_INV)

	tophat = cv2.morphologyEx(th3, cv2.MORPH_TOPHAT, kernel)
	ret,inverse_tophat = cv2.threshold(tophat,127,255,cv2.THRESH_BINARY_INV)

	output_file_ = ''.join(input_file_.split('.')[0]+'.jpg')
	output_file = os.path.join(output_dir,output_file_)
	cv2.imwrite(output_file,th5)
	
	input_text = pytesseract.image_to_string(Image.open(input_file))
	output_text = pytesseract.image_to_string(Image.open(output_file))
	input_textfile_ = ''.join(input_file_.split('.')[0]+'input.txt')
	input_textfile = os.path.join(text_dir,input_textfile_)
	output_textfile_ = ''.join(output_file_.split('.')[0]+'output.txt')
	output_textfile = os.path.join(text_dir,output_textfile_)
	file = open(input_textfile,'w')
	file.write(input_text)
	file.close()
	file = open(output_textfile,'w')
	file.write(output_text)
	file.close()

	# blur a bit to improve ocr accuracy
	#new_image = cv2.blur(new_image, (2, 2))
	#cv2.imwrite(output_file, new_image)
	#if DEBUG:
	#    cv2.imwrite('edges.png', edges)
	#    cv2.imwrite('processed.png', processed)
	#    cv2.imwrite('rejected.png', rejected)