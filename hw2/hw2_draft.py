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
db = client.sample_airbnb

#Getting a collection called posts
airbnbs = db.listingsAndReviews

# collection_name = db.list_collection_names()
# print("### Verify Collection Creation ###")
# print(collection_name)

#query 1: List properties that include a garden amenity or have both a fire extinguisher and a smoke detector. Sort by the number of beds in descending order. Return the first 10 records.	
#(Fields): _id, name, property_type, beds
one = db.listingsAndReviews.find(
    {'$or': [{'amenities':{'$all' : ["Garden"]}},
             {'amenities':{'$all' : ["Fire extinguisher","Smoke detector"]}}
             ]},
    {'_id':1, 'name':1, 'property_type':1, 'beds':1}
).sort({'beds':-1}).limit(10)

# for i in one :
#     pprint.pprint(i)

#query 2:  List the 5 most expensive properties based on listing price.
# (Fields): _id, name, price
two = db.listingsAndReviews.find(
    {},
    {'_id':1, 'name':1, 'price':1}
).sort({'price':-1}).limit(5)

# for i in two :
#     pprint.pprint(i)

#query 3: List properties where the cleanliness rating is higher than the accuracy rating. Sort by the number of reviews in ascending order. Return the first 5 records.
# (Fields): _id, name, number_of_reviews, review_scores_cleanliness, review_scores_accuracy
three = db.listingsAndReviews.aggregate([
    {'$match': {'$expr':{'$gt':['$review_scores.review_scores_cleanliness','$review_scores.review_scores_accuracy']}}},
    {'$project': {'_id':1, 'name':1, 'number_of_reviews':1, 'review_scores.review_scores_cleanliness':1, 'review_scores.review_scores_accuracy':1}},
    {'$sort' : {'number_of_reviews':1}},
    {'$limit':5}
])

# for i in three:
#     pprint.pprint(i)

#query 4: List properties located in Portugal with 3 or more bedrooms. Sort by review score rating in descending order and, if ratings are the same, sort by the number of reviews in descending order. List the first 5 records.
# (Fields): _id, name, address.country, review_scores_rating, bedrooms, number_of_reviews
four = db.listingsAndReviews.find(
    {'address.country':"Portugal",'bedrooms': {'$gte':3}}, 
    {'_id':1, 'name':1, 'address.country':1, 'review_scores.review_scores_rating':1, 'bedrooms':1, 'number_of_reviews':1 }
).sort({'review_scores.review_scores_rating':-1,'number_of_reviews':-1}).limit(5)
# print()
# for i in four:
#     pprint.pprint(i)
# print()

#query 5: List properties with fewer than 500 reviews that have a review score of 9 or above for communication. Sort by review score for checkin in descending order, and if scores are the same, sort by the number of reviews in descending order. Display the first 5 records.	
#(Fields): _id, name, number_of_reviews, review_scores_communication, review_scores_checkin
five = db.listingsAndReviews.find(
    {'number_of_reviews': {'$lt': 500}, 'review_scores.review_scores_communication':{'$gte':9}},
    {'_id':1, 'name':1, 'number_of_reviews':1, 'review_scores.review_scores_communication':1, 'review_scores.review_scores_checkin':1}
).sort({'review_scores.review_scores_checkin':-1,'number_of_reviews':-1}).limit(5)

# print()
# for i in five:
#     pprint.pprint(i)
# print()

# query 6:  List the 5 hosts with the most bedrooms across all of their property listings as type ‘House’. Group by host to calculate the total number of bedrooms for each host. Sort the results by the total number of bedrooms in descending order and display each host’s ID, name, and total bedrooms.
# (Fields): host_id, host_name, total_bedrooms
six = db.listingsAndReviews.aggregate([
    {'$match':{'property_type':'House'}},
    {'$group': {'_id':['$host.host_id','$host.host_name'],'total_bedrooms':{'$sum':'$bedrooms'}}},
    {'$sort':{'total_bedrooms':-1}},
    {'$limit': 5}
])

print()
for i in six:
    pprint.pprint(i)
print()