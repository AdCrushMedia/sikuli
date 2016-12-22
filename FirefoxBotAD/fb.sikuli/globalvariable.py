from sikuli import *
load("lib\\mysql\\mysql-connector-java-5.1.39-bin.jar") 
from com.ziclix.python.sql import zxJDBC

import random

import json
from pprint import pprint

import os
script_dir = os.path.dirname(__file__)

with open(script_dir + '\\settings.json') as data_file:    
    setting = json.load(data_file)


#load("lib\\mysql\\mysql-connector-java-5.1.39-bin.jar") # see comment



DBHOST = "jdbc:mysql://138.68.7.25/sikuli_db" #138.68.7.25
DBUSERNAME = "root"
DBPASSWORD = "3e66f8cc193a18b9" #3e66f8cc193a18b9

db = False

try:

	db = zxJDBC.connect(DBHOST, DBUSERNAME, DBPASSWORD, "com.mysql.jdbc.Driver", CHARSET='utf-8')

except Exception, e:

	print "Failed to connect to the database. Please check your internet connection"


fbUrl = "http://facebook.com"

broserLocation = setting['chrome'] #path for google chrome


defaultEmail = setting['fb']['email'] #setting['fb']['email'] #facebook email
defaultPassword = setting['fb']['password'] #setting['fb']['password'] #facebook password

#CSV LOCATIONS
#fanpageCsvPath = 'C:\\Users\\Jason Javier\\Desktop\\fb.sikuli\\csv\\fanpage.csv'  #fanpage csv location
#commentCsvPath = 'C:\\Users\\Jason Javier\\Desktop\\fb.sikuli\\csv\\comments.csv' #comment csv location
#postCsvPath = 'C:\\Users\\Jason Javier\\Desktop\\fb.sikuli\\csv\\post.csv' #post csv location


actionPattern1 = ["likes",   "like_fan_page",  "buzzfeed", 'trending', "page_feed", "post_status", "logout"]  #"likes", "view_friends",  "like_fan_page",  "buzzfeed", "page_feed", "post_status"
actionPattern2 = ["likes", "post_status",  "view_friends",  'trending', "buzzfeed",  "logout"] 
actionPattern3 = ["likes", "like_fan_page", "page_feed", "post_status", "buzzfeed", "view_friends", 'trending', "logout"] 
actionPattern4 = ["likes", "post_status", "buzzfeed" ,  'trending',  "logout"] 
testPattern = ["page_feed"]

#like_fan_page, page_feed, post_status

actionPattern = [actionPattern1, actionPattern2, actionPattern3, actionPattern4] #[actionPattern1, actionPattern2, actionPattern3] #, actionPattern2, actionPattern3

#searchBar = Pattern("1465713188410.png").targetOffset(-63,0) #Pattern("images/searchBar.png").similar(0.80).targetOffset(121,0) #Pattern("images/searchBar.png").similar(0.80).targetOffset(53,0)
loginLogo = "images/loginLogo.png"
checkNotifCount = 0
