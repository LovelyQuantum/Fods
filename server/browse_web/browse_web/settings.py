import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

SQLALCHEMY_DATABASE_URI = 'postgresql://quantum:429526000@postgres/mydb'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'secret string'

MAX_CONTENT_LENGTH = 30 * 1024 * 1024
DROPZONE_ALLOWED_FILE_CUSTOM = True
DROPZONE_ALLOWED_FILE_TYPE = 'image/*'
DROPZONE_MAX_FILE_SIZE = 3 * 1024
DROPZONE_MAX_FILES = 30
DROPZONE_ENABLE_CSRF = False
DROPZONE_DEFAULT_MESSAGE = "点击或者将图片、视频拖拽到此区域以上传"

TEMP_PATH = basedir + '/browse_web/static/img/dataset/temp/'
STORAGE_PATH = basedir + '/browse_web/static/img/dataset/storage/'
SHOW_PATH = basedir + '/browse_web/static/img/dataset/show/'
SCREEN_SHOT_PATH = basedir + '/browse_web/static/img/screen_shot/'
SCREEN_RECORD_PATH = basedir + '/browse_web/static/img/records/'

INFO_PER_PAGE = 10
HISTORY_INFOS_PER_PAGE = 15
TEMP_IMAGES_PER_PAGE = 6
DATASET_IMAGES_PER_PAGE = 9
TARGET_CLASSES = ['石头', '木块']
