class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    MONGO_URI = "mongodb://localhost:27017/tech_blog"
    MONGO_DATABASE = "tech_blog"

    IMPORT_PATH = "/var/tech_blog"
    CUSTOM_IMAGES_PATH = "/var/tech_blog/images"

    MONGO_BLOG_TABLE = "blog"
    MONGO_GALLERY_TABLE = "gallery"
    TEMPLATE_FOLDER_PATH = "template"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
