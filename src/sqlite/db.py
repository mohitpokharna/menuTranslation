import sqlite3
import codecs
import os

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


def create_table(conn,create_table_sql):
	"""create a table from the create_table_sql statement
	:param conn: Connnection object returned by create_connection
	:param create_table_sql: a CREATE TABLE statement
	:return:
	"""

	try:
		c=conn.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)


def insert_dishdb(conn,dish):
	"""create a new row into projectdb table
	:param conn:
	:param dish
	:return: rowid
	"""
	sql='''INSERT INTO menudb(dish_name,hindi_name,image)
			VALUES(?,?,?)'''
	cur=conn.cursor()
	cur.execute(sql,dish)
	return cur.lastrowid	

def main():
	
	database=	"projectdb.sqlite"

	sql_create_table_menudb="""CREATE TABLE IF NOT EXISTS menudb(
								id integer PRIMARY KEY,
								dish_name text NOT NULL,
								hindi_name text NOT NULL,
								image blob NOT NULL);"""


	#create a db connection
	conn=create_connection(database)
	print("checkpost1\n")

	if conn is not None:
		#create table
		create_table(conn,sql_create_table_menudb)

	else:
		print("Error ! cannot create database connection")


	with open('dish_name.txt') as f:
		fcount_dish=sum(1 for _ in f)
    #"""fcount_dish stores number of dish in text files"""

	#print("checkpost2\n")
	#f=open('dish_name.txt')
	#s=f.read()
	#s=str.split(s,'\n') #s contains list of dish names now


	#reading file in unicode ncoding
	f=codecs.open('dish_name.txt',encoding='utf-8')
	s=f.read()
	s=unicode.split(s,'\n')#s contains one more entry due to eof. S is now a list of dishname and their hindi encodings

	s=s[0:fcount_dish] #ignoring eof

	#reading image names
	imagelist=os.listdir("dish_images")
	#http://www.numericalexpert.com/blog/sqlite_blob_time/                                  link for reading images from sqlite
	i=1
	for name in s:
		imagefile=open("dish_images/"+str(i)+".jpeg",'rb')
		i=i+1
		ablob=imagefile.read()
		print("checkpost3\n")
		name=unicode.split(name,'\t')#name now is a list of two dishname in englsih and unicode of hindi translation.
		dish=(name[0],name[1],sqlite3.Binary(ablob))
   		row_id=insert_dishdb(conn,dish)

   	conn.commit()	

if __name__=='__main__':
	main()