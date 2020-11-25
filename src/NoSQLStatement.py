import hashlib
import datetime as dt
import pymongo
import urllib

client = pymongo.MongoClient("mongodb+srv://admin:IBXxRxezhvT9f4D3@cluster0.vkqbl.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client["ICT2103_Project"]


# Topic: Percentage of people with different tier privileges.(PIE CHART)(HM)
# def TierAnalysis(db):
#     selectedTable = db["Users"]
#     # query = [{"$group":{_id:"$TierID",count:{$sum:1}}}]
#     # fields = {"_id": 1}
#     # result = selectedTable.aggregate(query, fields)
#     # result = selectedTable.aggregate([{$group:{_id:"$TierID",count:{$sum:1}}}])
#     result = selectedTable.aggregate([{'$group':{'_id':'$TierID','count':{'$sum':1}}},{'$sort':{'count':-1}}])
#     for x in result:
#         print(x)
#     return result


# Topic: SENTIMENT VALUE WITH CATEGORY NAME---(BAR CHART)(HM)
# def SentimentValueCategory(db):
#     selectedTable = db["Articles"]
#     # result = selectedTable.aggregate([{'$group':{'_id':'$CategoryName','sentiment':{'$sum':'$SentimentRating'}}}])
#     result = selectedTable.aggregate([{'$group': {'_id': '$CategoryName', 'sentiment': {'$sum': '$SentimentRating'}}}])
#     for x in result:
#         print(x)
#     return result


# Topic:Most popular Agency(for article likes)--(bar chart)(HM)(FIXED)
# def MostArticleLikedAgency(db):
#     selectedTable = db["Articles"]
#     # result = selectedTable.aggregate([{'$project':{'AgencyName':1,'total likes':{'$cond':{'if':{'$isArray':'$likeList'},'then':{'$size':'$likeList'},'else':0}}}}])
#     result = selectedTable.aggregate([{'$group':{'_id':'$AgencyName','total':{'$sum':{'$cond':{'if':{'$isArray':'$likeList'},'then':{'$size':'$likeList'},'else':0}}}}}])
#     for x in result:
#         print(x)
#     return result


# Topic: Percentage of Articles written by different Agencies(PIE CHART)(HM)
# def NumOfArticlesByAgencyWithName(db):
#     selectedTable = db["Articles"]
#     result = selectedTable.aggregate([{'$group':{'_id':'$AgencyName','count':{'$sum':1}}}])
#     for x in result:
#         print(x)
#     return result


# Topic:TOP 10 MOST LIKES for article(FOR SUGGESTION PAGE INSTEAD)(hm)(fixed)(WORKING)
# def TopTenMostLikesArticleWithArticleTitle(db):
#     selectedTable = db["Articles"]
#     result = selectedTable.aggregate([{'$project':{'ArticleTitle':1,'total likes':{'$cond':{'if':{'$isArray':'$likeList'},'then':{'$size':'$likeList'},'else':0}}}},{'$sort':{'total likes':-1}},{'$limit':10}])
#     # result = selectedTable.aggregate([{'$group': {'_id': '$ArticleTitle','total':{'$cond':{'if':{'$isArray':'$likeList'},'then':{'$size':'$likeList'},'else':0}}}},{'$sort':{'total likes':-1}},{'$limit':10}])
#
#     for x in result:
#         print(x)
#     return result


# Topic:Avg sentiment value for each agency(bar chart)
# def AllAvgSentimentRating(db):
#    selectedTable = db["Articles"]
#    result = selectedTable.aggregate([{'$group': {'_id': '$AgencyName','sentiment':{'$avg':'$SentimentRating'}}},{'$sort':{'sentiment':-1}}])
#    for x in result:
#        print(x)
#    return result


# Topic:TOP 10 sentiment value for article(list/bar graph)
def TopTenSentimentForAllCategory(db):
    selectedTable = db["Articles"]
    result = selectedTable.find({},{'ArticleTitle':1,'SentimentRating':1,'_id':0}).sort({"SentimentRating":-1}).limit(10)

    # result = selectedTable.find({"AgencyName":"Today"}).sort({"SentimentRating":-1}).limit(10)

    for x in result:
        print(x)
    return result


# TierAnalysis(db)
# SentimentValueCategory(db)
# MostArticleLikedAgency(db)
# NumOfArticlesByAgencyWithName(db)
# TopTenMostLikesArticleWithArticleTitle(db)
# AllAvgSentimentRating(db)
TopTenSentimentForAllCategory(db)