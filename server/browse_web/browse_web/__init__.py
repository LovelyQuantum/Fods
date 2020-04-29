from flask import Flask
from browse_web.extensions import login_manager, bootstrap, db, dropzone
from browse_web.models import Admin


app = Flask('browse_web')
app.config.from_pyfile('settings.py')

db.init_app(app)
login_manager.init_app(app)
bootstrap.init_app(app)
dropzone.init_app(app)
# csrf.init_app(app)


from browse_web import views, commands, errors
