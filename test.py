import pymongo
from datetime import datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["tech_blog"]
mycol = mydb["blog"]

article = {
    "category_url": "blog",
    "category_name": "Blog",
    "url": "test_url",
    "title": "Transfer files using python",
    "preview": "India has been a federal republic since 1950, governed in a democratic parliamentary system. It is a pluralistic, multilingual and multi-ethnic society.",
    "published_on": "2021-07-05",
    "blog_code": "tech_blog",
    "date": "2021-07-05"

}


x = mycol.insert_one(article)


# data_dict = {"blog_code": "tech_blog",
#              "category_url": "blog",
#              "date": {
#                  "$gte": "2021-01-01",
#                  "$lt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                  }}
# total_story = mycol.find(data_dict).count(True)
#
# print(total_story)
