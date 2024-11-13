#NOTE: Remove tables in Atlas before running this script!

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

#Create a document called post
post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        # "date": datetime.datetime.now(datetime.UTC)
         "date": datetime.datetime.now()
        }

#Insert the post document into the database
post_id = posts.insert_one(post).inserted_id

#Verify that the post document was created successfully
collection_name = db.list_collection_names()
print("### Verify Collection Creation ###")
print(collection_name)

#Print the ID of the first post entry to verify its creation
print("\n### Retrieve Mike's Post ID ###")
print("Post ID:",post_id) 

#Display the Mike's first blog post
print("\n### Retrieve Mike's First Blog Post ###")
pprint.pprint(posts.find_one())

#Display the first document where Mike is the author
print("\n### Retrieve first document where author='Mike' ###")
pprint.pprint(posts.find_one({"author": "Mike"}))

#Create two more documents
new_posts = [{"author": "Mike",
              "text": "Another post!",
              "tags": ["bulk", "insert"],
              "date": datetime.datetime(2024, 4, 3, 11, 14)}, 
              #datetime.datetime(year, month, day, hour, minute)

             {"author": "Eliot",
              "title": "MongoDB is fun",
              "text": "and pretty easy too!",
              "date": datetime.datetime(2024, 4, 3, 10, 45)}]

#Insert new_posts into the posts collection
result = posts.insert_many(new_posts)

#Display the new_posts IDs to verify their creation
print("\n### Retrieve New Post IDs ###")
print(result.inserted_ids)

#Query multiple documents & display them
print("\n### Show Posts By Any User ###")
for post in posts.find():
	pprint.pprint(post)

#Display the documents that have Mike listed as the author
print("\n### Show Only Mike's Blog Posts ###")
for post in posts.find({"author": "Mike"}):
  pprint.pprint(post)