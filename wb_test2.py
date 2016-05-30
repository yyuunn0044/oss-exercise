from flask import Flask
app = Flask(__name__)
import pymysql
import sys

##arcus##
from arcus import *
from arcus_mc_node import ArcusMCNodeAllocator
from arcus_mc_node import EflagFilter
import datetime, time, sys

client = Arcus(ArcusLocator(ArcusMCNodeAllocator(ArcusTranscoder())))


print('### connect to client')
client.connect("172.17.0.3:2181", "ruo91-cloud")


ret = client.set('test:string1', 'test...', 20)
print(ret.get_result())
assert ret.get_result() == True


##arcus##

db = pymysql.connect(user = 'root', passwd = 'password')
cursor = db.cursor()
cursor.execute("USE test")
cursor.execute("show tables")
char = ''
char_input = ''
word = ''
command = ''

cursor.execute("select * from jsp")

def db_write(name, pawd):
	command = "INSERT INTO jsp VALUES ('%s' , '%s')" % (name, pawd)
	cursor.execute(command)
	db.commit()
	command = ''

def db_read(name):
	command = "select id from jsp"
	cursor.execute(command)
	db.commit()
	command = ''

def arcus_set(name, value):
        client.set(name, value, 20)
        
def arcus_get(name):
        client.get(name)

def test_mysql(n):
        start_time = time.time()
        for i in range (10):
                db_write(str(i), 'garbage')
        for k in range (n):
                for i in range (10):
                        db_read(str(i))
        time_diff = time.time() - start_time
        print("execution time without arcus: %f" %(time_diff))
        return time_diff
                        
def test_arcus(n):
        start_time = time.time()
        for i in range (10):
                arcus_set(str(i), 'garbage')
        for k in range (n):
                for i in range (10):
                        arcus_get(str(i))
        time_diff = time.time() - start_time
        print("execution time with arcus: %f" %(time.time() - start_time))
        return time_diff



sum = 0
for i in range (5):
	sum += test_mysql(int(sys.argv[1]))
print("average execution time without arcus : %f" %(sum))
print("")
sum=0
for i in range (5):
	sum += test_arcus(int(sys.argv[1]))
print("average execution time with arcus %f" %(sum))
cursor.execute("select * from jsp")

for t in cursor:
	char += t[0] + '\n' + t[1] + '\n'

@app.route('/')
def hello_world():
	return char
if __name__ == '__main__':
        app.run("0.0.0.0", 8080)


#test_mysql()
#test_arcus()


