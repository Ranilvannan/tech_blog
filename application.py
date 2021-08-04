from flask import Flask, request, render_template, abort, send_from_directory, make_response
from blog_insert import BlogInsert
from flask_paginate import Pagination
import pymongo
import os
from datetime import datetime
from urllib.parse import urlparse
from category_data import category_data

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
app.template_folder = app.config.get("TEMPLATE_FOLDER_PATH")
PER_PAGE = 10
START_DATE = "2021-01-01"


def data_collect(table):
    uri = app.config.get("MONGO_URI")
    database = app.config.get("MONGO_DATABASE")
    client = pymongo.MongoClient(uri)
    db = client[database]
    return db[table]


@app.route('/images/<path:filename>')
def custom_images(filename):
    path = app.config['CUSTOM_IMAGES_PATH']
    gallery = app.config.get("MONGO_GALLERY_TABLE")
    gallery_col = data_collect(gallery)
    gallery = gallery_col.find_one({"filename": filename})

    if not gallery:
        abort(404)

    image_path = os.path.join(path, gallery["filepath"])
    return send_from_directory(image_path, filename)


@app.route('/')
def home_page():
    return render_template('home_page.html')


@app.route('/category/<category_url>/')
@app.route('/category/<category_url>')
def category_page(category_url):
    if category_url not in category_data.keys():
        return abort(404)

    category = category_data[category_url]
    blog = app.config.get("MONGO_BLOG_TABLE")
    blog_col = data_collect(blog)
    page = request.args.get("page", type=int, default=1)

    data_dict = {"blog_code": app.config['BLOG_CODE'],
                 "category_url": category_url,
                 "date": {
                     "$gte": START_DATE,
                     "$lt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                 }}
    total_story = blog_col.find(data_dict).count(True)
    pagination = Pagination(page=page, total=total_story, search=False, record_name='users', css_framework='bootstrap4')

    # No Blog found
    if not (1 <= page <= pagination.total_pages):
        return render_template('no_result.html')

    articles = blog_col.find(data_dict)\
        .sort("blog_id", -1)\
        .skip(PER_PAGE*(page-1))\
        .limit(PER_PAGE)

    return render_template('category_page.html',
                           articles=articles,
                           category=category,
                           pagination=pagination)


@app.route('/category/<category_url>/<blog_url>/')
@app.route('/category/<category_url>/<blog_url>')
def blog_page(category_url, blog_url):
    blog = app.config.get("MONGO_BLOG_TABLE")
    blog_col = data_collect(blog)
    article = blog_col.find_one({"url": blog_url})

    if not article:
        abort(404)

    return render_template('blog_page.html', article=article)


@app.route("/sitemap.xml")
def sitemap_page():
    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc
    dynamic_urls = list()

    dynamic_urls.append({"loc": host_base,
                         "lastmod": datetime.now().strftime("%Y-%m-%d")})

    # Dynamic routes - Blog
    blog = app.config.get("MONGO_BLOG_TABLE")
    blog_col = data_collect(blog)
    data_dict = {"blog_code": app.config['BLOG_CODE'],
                 "date": {
                     "$gte": START_DATE,
                     "$lt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                 }}
    articles = blog_col.find(data_dict)

    for article in articles:
        url = {
            "loc": f"{host_base}/category/{article['category_url']}/{article['url']}",
            "lastmod": article['date']
        }
        dynamic_urls.append(url)

    # Dynamic routes - Category
    for rec in category_data:
        url = {
            "loc": f"{host_base}/category/{rec}",
            "lastmod": datetime.now().strftime("%Y-%m-%d")
        }
        dynamic_urls.append(url)

    xml_sitemap = render_template("sitemap.xml", dynamic_urls=dynamic_urls, host_base=host_base)
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response


@app.route('/robots.txt')
def robot_file():
    return send_from_directory(app.static_folder, request.path[1:])


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404


@app.cli.command('blog_update')
def blog_update():
    path = app.config.get("IMPORT_PATH")
    blog_code = app.config.get("BLOG_CODE")
    blog = app.config.get("MONGO_BLOG_TABLE")
    col = data_collect(blog)
    params = "blog_id"
    file_suffix = "_{0}_blog.json".format(blog_code)

    bi = BlogInsert(path, col, params, file_suffix)
    bi.trigger_import()


@app.cli.command('gallery_update')
def gallery_update():
    path = app.config.get("IMPORT_PATH")
    gallery = app.config.get("MONGO_GALLERY_TABLE")
    col = data_collect(gallery)
    params = "gallery_id"
    file_suffix = "_gallery.json"

    bi = BlogInsert(path, col, params, file_suffix)
    bi.trigger_import()
