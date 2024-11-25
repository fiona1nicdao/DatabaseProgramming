#NOTE: Remove tables in Atlas before running this script!

# screenshot needs to be from python - from terminal / command 
import pymongo
import datetime, pprint
from pymongo import MongoClient
from tabulate import tabulate

#Create connection (get connection string in Atlas) 
client = MongoClient(
    "mongodb+srv://lucuser:csclassluc@luccluster.k4by9.mongodb.net/?retryWrites=true&w=majority&appName=LUCcluster"
)

#Getting a database called test_database
db = client.sample_airbnb

#Getting a collection called posts
listings = db.listingsAndReviews

#query 1: 
q1Query = {"$or": [{"amenities":{"$all" : ["Garden"]}},
                   {"amenities":{"$all" : ["Fire extinguisher","Smoke detector"]}}]}
q1Project = {"_id":1, "name":1, "property_type":1, "beds":1}

q1 = listings.find(q1Query, q1Project).sort({"beds":-1}).limit(10)

q1Headers, q1Results = ["_id", "name","property_type", "beds"], []
for result in q1:
    q1Results.append(
        [result["_id"],result["name"],result["property_type"],result["beds"]]
    )
print("\n ## Query 1 ##")
print(tabulate(q1Results,headers=q1Headers),"\n")

#query 2: 
two = listings.find(
    {},
    {"_id":1, "name":1, "price":1}
).sort({"price":-1}).limit(5)
print("\n ## Query 2 ##")
for i in two :
    pprint.pprint(i)

#query 3: 
q3Query = {"$expr":{"$gt":["$review_scores.review_scores_cleanliness",
                     "$review_scores.review_scores_accuracy"]}}
q3Project = {"_id":1, "name":1, "number_of_reviews":1, 
     "review_scores.review_scores_cleanliness":1, 
     "review_scores.review_scores_accuracy":1}

q3 = listings.find(q3Query, q3Project).sort({"number_of_reviews":1}).limit(5)

q3Headers, q3Results = ["_id", "name","number_of_reviews", "review_scores_cleanliness","review_scores_accuracy"], []
for result in q3:
    q3Results.append(
        [result["_id"], result["name"],result["number_of_reviews"], result["review_scores"]["review_scores_cleanliness"],result["review_scores"]["review_scores_accuracy"]]
    )
print("\n ## Query 3 ##")
print(tabulate(q3Results,headers=q3Headers),"\n")


#query 4: 
four = listings.find(
    {"address.country":"Portugal","bedrooms": {"$gte":3}}, 
    {"_id":1, "name":1, "address.country":1, "review_scores.review_scores_rating":1, "bedrooms":1, "number_of_reviews":1 }
).sort({"review_scores.review_scores_rating":-1,"number_of_reviews":-1}).limit(5)
print("\n ## Query 4 ##")
for i in four:
    pprint.pprint(i)

#query 5: 
q5Query = {"$and" : [{"number_of_reviews": {"$lt": 500}}, {"review_scores.review_scores_communication":{"$gte":9}}]}
q5Project = {"_id":1, "name":1, "number_of_reviews":1, "review_scores.review_scores_communication":1, "review_scores.review_scores_checkin":1}
q5Sort = {"review_scores.review_scores_checkin":-1,"number_of_reviews":-1}
q5 = listings.find(q5Query, q5Project ).sort(q5Sort).limit(5)

q5Headers, q5Results = ["_id", "name", "number_of_reviews", "review_scores_communication", "review_scores_checkin"],[]
for result in q5:
    q5Results.append(
        [result["_id"], result["name"],result["number_of_reviews"], result["review_scores"]["review_scores_communication"], result["review_scores"]["review_scores_checkin"]]
    )
print("\n ## Query 5 ##")
print(tabulate(q5Results,headers=q5Headers),"\n")


# query 6:  
six = listings.aggregate([
    {"$match":{"property_type":"House"}},
    {"$group": {"_id":["$host.host_id","$host.host_name"],"total_bedrooms":{"$sum":"$bedrooms"}}},
    {"$sort":{"total_bedrooms":-1}},
    {"$limit": 7}
])
print("\n ## Query 6 ##")
for i in six:
    pprint.pprint(i)
