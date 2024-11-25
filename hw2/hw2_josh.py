import pymongo
from pymongo import MongoClient
import pdb
from tabulate import tabulate
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(
    f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASS')}@453cluster.zy6th.mongodb.net/?retryWrites=true&w=majority&appName=453cluster"
)
db = client.sample_airbnb
listings = db.listingsAndReviews

# Question 1
print("Question 1")
q1Query = {
    "$or": [
        {"amenities": {"$in": ["Garden"]}},
        {"amenities": {"$all": ["Fire extinguisher", "Smoke detector"]}},
    ]
}
q1 = listings.find(q1Query).sort("beds", pymongo.DESCENDING).limit(10)
q1Headers, q1Results = ["_id", "name", "property_type", "beds"], []
for result in q1:
    q1Results.append(
        [result["_id"], result["name"], result["property_type"], result["beds"]]
    )
print(tabulate(q1Results, headers=q1Headers), "\n")

# Question 2
print("Question 2")
q2 = listings.find().sort("price", pymongo.DESCENDING).limit(5)
q2Headers, q2Results = ["_id", "name", "price"], []
for result in q2:
    q2Results.append([result["_id"], result["name"], result["price"]])
print(tabulate(q2Results, headers=q2Headers), "\n")

# Question 3
print("Question 3")
q3Query = {
    "$match": {
        "$expr": {
            "$gt": [
                "$review_scores.review_scores_cleanliness",
                "$review_scores.review_scores_accuracy",
            ]
        }
    }
}
q3 = listings.aggregate(
    [
        q3Query,
        {"$sort": {"number_of_reviews": pymongo.ASCENDING}},
        {"$limit": 5},
    ]
)
q3Headers, q3Results = [
    "_id",
    "name",
    "number_of_reviews",
    "review_scores_cleanliness",
    "review_scores_accuracy",
], []
for result in q3:
    q3Results.append(
        [
            result["_id"],
            result["name"],
            result["number_of_reviews"],
            result["review_scores"]["review_scores_cleanliness"],
            result["review_scores"]["review_scores_accuracy"],
        ]
    )
print(tabulate(q3Results, headers=q3Headers), "\n")

# Question 4
print("Question 4")
q4Query = {
    "$match": {"$and": [{"address.country_code": "PT"}, {"bedrooms": {"$gte": 3}}]}
}
q4Sort = {
    "$sort": {
        "review_scores.review_scores_rating": pymongo.DESCENDING,
        "number_of_reviews": pymongo.DESCENDING,
    }
}
q4 = listings.aggregate([q4Query, q4Sort, {"$limit": 5}])
q4Headers, q4Results = [
    "_id",
    "name",
    "address.country",
    "review_scores_rating",
    "bedrooms",
    "number_of_reviews",
], []
for result in q4:
    q4Results.append(
        [
            result["_id"],
            result["name"],
            result["address"]["country"],
            result["review_scores"]["review_scores_rating"],
            result["bedrooms"],
            result["number_of_reviews"],
        ]
    )
print(tabulate(q4Results, headers=q4Headers), "\n")

# Question 5
print("Question 5")
q5Query = {
    "$match": {
        "$and": [
            {"number_of_reviews": {"$lt": 500}},
            {"review_scores.review_scores_communication": {"$gte": 9}},
        ]
    }
}
q5Sort = {
    "$sort": {
        "review_scores.review_score_checkin": pymongo.DESCENDING,
        "number_of_reviews": pymongo.DESCENDING,
    }
}
q5 = listings.aggregate([q5Query, q5Sort, {"$limit": 5}])
q5Headers, q5Results = [
    "_id",
    "name",
    "number_of_reviews",
    "reivew_scores_communication",
    "review_scores_checkin",
], []
for result in q5:
    q5Results.append(
        [
            result["_id"],
            result["name"],
            result["number_of_reviews"],
            result["review_scores"]["review_scores_communication"],
            result["review_scores"]["review_scores_checkin"],
        ]
    )
print(tabulate(q5Results, headers=q5Headers), "\n")

# Question 6
print("Question 6")
q6Query = {"$match": {"property_type": "House"}}
q6Group = {
    "$group": {
        "_id": {
            "host_id": "$host.host_id",
            "host_name": "$host.host_name"
        },
        "total_bedrooms": {
            "$sum": "$bedrooms",
        },
    }
}
q6Sort = {
    "$sort": {
        "total_bedrooms": pymongo.DESCENDING
    }
}
q6 = listings.aggregate([q6Query, q6Group, q6Sort, {"$limit": 5}])
q6Headers, q6Results = ["host_id", "host_name", "total_bedrooms"], []
for result in q6:
    q6Results.append([
        result["_id"]["host_id"],
        result["_id"]["host_name"],
        result["total_bedrooms"]
    ])
print(tabulate(q6Results, headers=q6Headers), "\n")