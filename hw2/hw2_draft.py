#NOTE: Remove tables in Atlas before running this script!

# screenshot needs to be from python - from terminal / command 
import pymongo
import datetime, pprint
from pymongo import MongoClient

#Create connection (get connection string in Atlas) 
# client = MongoClient("mongodb+srv://lucuser:csclassluc@luccluster.utk6w.mongodb.net/?retryWrites=true&w=majority&appName=LUCcluster")

# client = MongoClient("mongodb+srv://lucuser:csclassluc@luccluster.utk6w.mongodb.net/?retryWrites=true&w=majority&appName=LUCcluster")
client = MongoClient(
    "mongodb+srv://lucuser:csclassluc@luccluster.k4by9.mongodb.net/?retryWrites=true&w=majority&appName=LUCcluster"
)

#Getting a database called test_database
db = client.test_database

#Getting a collection called posts
posts = db.posts