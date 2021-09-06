class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    MONGO_URI = "mongodb://localhost:27017/tech_blog"
    MONGO_DATABASE = "tech_blog"
    BLOG_CODE = "TECH"

    # IMPORT_PATH = "/var/tech_blog"
    IMPORT_PATH = "/home/ramesh/Desktop"
    CUSTOM_IMAGES_PATH = "/var/tech_blog/images"

    MONGO_BLOG_TABLE = "blog"
    TEMPLATE_FOLDER_PATH = "template"

    MONGO_ARTICLE_TABLE = "article"
    MONGO_CATEGORY_TABLE = "category"
    MONGO_SUB_CATEGORY_TABLE = "sub_category"
    MONGO_TAG_TABLE = "tag"
    MONGO_GALLERY_TABLE = "gallery"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
