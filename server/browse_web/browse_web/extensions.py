from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from pymemcache.client.base import Client
from pymemcache import serde
from flask_dropzone import Dropzone

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
# csrf = CSRFProtect()
# ckeditor = CKEditor()
# moment = Moment()
# toolbar = DebugToolbarExtension()
dropzone = Dropzone()
mc = Client(
    ("yuhao_memcache", 12002),
    serializer=serde.python_memcache_serializer,
    deserializer=serde.python_memcache_deserializer,
)

@login_manager.user_loader
def load_user(user_id):
    from browse_web.models import Admin
    user = Admin.query.get(int(user_id))
    return user
