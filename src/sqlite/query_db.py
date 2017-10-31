import sqlite3
from difflib import SequenceMatcher

from PIL import Image, ImageFont, ImageDraw, ImageEnhance

def create_connection(db_file):
	"""create a database connection to the sqlite database specifed by the db_file
	:param db_file:database file
	:return:  	Connection object or none
	"""
	try:
		conn=sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
	return None

def similar(a, b):
	"""returns similarity score of two strings a and b
	:param a:string
	:param b:string
	:return: score"""
	return SequenceMatcher(None, a, b).ratio()


def generate_output(textfile,database,translatedImage,hindiTextImage):
	f = open(textfile,'r')
	dish_all = f.read()
	#dish = dish_all.split('\n')[0]
	dish=dish_all.split('\n')
	print dish
	dish=dish[0]
	#print database
	print "-------------------------------------------------------------------------"
	print "\t\t\tDATABASE LOOKUP"
	print "-------------------------------------------------------------------------"
	conn=create_connection(database)
	cur=conn.cursor()
	
	cur.execute("SELECT dish_name from menudb")
	dish_namelist=cur.fetchall()#this is a lsit of all dishnames in the database
	ratio_list=[similar((dish).upper(),(x[0].encode("ascii")).upper()) for x in dish_namelist]
	print "ratiolist" ,ratio_list
	#fidning index of maximum element in ratio list
	max_index=0
	max_score=ratio_list[0]
	for i in range(len(ratio_list)):
		if(max_score<ratio_list[i]):
			max_score=ratio_list[i]
			max_index=i
	cur.execute("SELECT * from menudb WHERE dish_name=?",(dish_namelist[max_index][0].encode("ascii"),))
	all_cols=cur.fetchall()
	#print all_cols
	ablob= all_cols[0][3]

	#return all_cols[0][2] # this returns hindi translation of it in unicode
	dish_image = translatedImage
	with open(dish_image,'wb') as output_file:
		output_file.write(ablob)
	
	text = all_cols[0][2]
	tcolor = (255,255,255,1)
	text_pos = (10,40)
	font5 = ImageFont.truetype('src/sqlite/arialuni.ttf', 24)
	print "-------------------------------------------------------------------------"
	print "\t\t\t",all_cols[0][1],"\t",text
	print "-------------------------------------------------------------------------"
	img = Image.new('RGB',(800,800),(0,0,0,0))
	draw = ImageDraw.Draw(img)
	draw.text(text_pos, text, font=font5, fill=tcolor)
	del draw
	
	img.save(hindiTextImage)	