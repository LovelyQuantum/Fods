from flask import Blueprint, render_template

basic_bp = Blueprint('basic', __name__)

@basic_bp.route('/')
def index():
    return render_template('basic/index.html')
