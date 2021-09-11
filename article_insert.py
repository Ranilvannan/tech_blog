import os
import json
from datetime import datetime


class ArticleInsert:

    def __init__(self, article, category, sub_category, tag, gallery, path, file_suffix):
        self.article = article
        self.category = category
        self.sub_category = sub_category
        self.tag = tag
        self.gallery = gallery
        self.path = path
        self.file_suffix = file_suffix

    def trigger_import(self):
        files = self.get_json_files()

        for file in files:
            self.get_json_data(file)
            # if os.path.exists(file):
            #     os.remove(file)

    def update_article(self, rec):
        table = self.article
        data_dict = {"article_id": rec["article_id"]}
        data = {
            "article_id": rec["article_id"],
            "date": datetime.strptime(rec["date"], "%Y-%m-%d"),
            "published_on": datetime.strptime(rec["published_on"], "%Y-%m-%d %H:%M:%S"),
            "blog_type": rec["blog_type"],
            "name": rec["name"],
            "url": rec["url"],
            "title": rec["title"],
            "preview": rec["preview"],
            "content": rec["content"],
            "category_url": rec["category_url"],
            "sub_category_url": rec["sub_category_url"],
            "previous": rec["previous"],
            "next": rec["next"],
            "related_ids": rec["related_ids"],
        }
        row = table.find(data_dict).count()

        if row:
            table.find_one_and_replace(data_dict, data)
        else:
            table.insert_one(data)

        return True

    def update_category(self, rec):
        table = self.category
        data_dict = {"category_id": rec["category_id"]}
        data = {
            "category_id": rec["category_id"],
            "name": rec["category_name"],
            "url": rec["category_url"],
            "code": rec["category_code"],
            "description": rec["category_description"]
        }
        row = table.find(data_dict).count()

        if row:
            table.find_one_and_replace(data_dict, data)
        else:
            table.insert_one(data)

        return True

    def update_sub_category(self, rec):
        table = self.sub_category
        data_dict = {"sub_category_id": rec["sub_category_id"]}
        data = {
            "sub_category_id": rec["sub_category_id"],
            "name": rec["sub_category_name"],
            "url": rec["sub_category_url"],
            "code": rec["sub_category_code"],
            "description": rec["sub_category_description"]
        }
        row = table.find(data_dict).count()

        if row:
            table.find_one_and_replace(data_dict, data)
        else:
            table.insert_one(data)

        return True

    def update_tag(self, rec):
        table = self.tag
        data_dict = {"tag_id": rec["tag_id"]}
        data = {
            "tag_id": rec["tag_id"],
            "tag_name": rec["tag_name"],
            "tag_url": rec["tag_url"],
            "tag_code": rec["tag_code"],
            "tag_description": rec["tag_description"]
        }
        row = table.find(data_dict).count()

        if row:
            table.find_one_and_replace(data_dict, data)
        else:
            table.insert_one(data)

        return True

    def update_gallery(self, rec):
        table = self.gallery
        data_dict = {"gallery_id": rec["gallery_id"]}
        data = {
            "gallery_id": rec["gallery_id"],
            "gallery_name": rec["gallery_name"],
            "gallery_path": rec["gallery_path"],
            "gallery_description": rec["gallery_description"]
        }
        row = table.find(data_dict).count()

        if row:
            table.find_one_and_replace(data_dict, data)
        else:
            table.insert_one(data)

        return True

    def get_json_data(self, file):
        with open(file) as json_file:
            recs = json.load(json_file)

            if isinstance(recs, list):
                for rec in recs:
                    if "article_id" in rec:
                        self.update_article(rec)

                    if "category_id" in rec:
                        self.update_category(rec)

                    if "sub_category_id" in rec:
                        self.update_sub_category(rec)

                    if "gallery_id" in rec:
                        self.update_gallery(rec)

                    if "galleries" in rec:
                        for gallery in rec["galleries"]:
                            self.update_gallery(gallery)

                    if "tags" in rec:
                        for tag in rec["tags"]:
                            self.update_tag(tag)

        return True

    def get_json_files(self):
        list_files = os.listdir(self.path)
        json_list = []

        for item in list_files:
            if item.endswith(self.file_suffix):
                file_path = os.path.join(self.path, item)
                json_list.append(file_path)

        return json_list
