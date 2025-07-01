from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect    
    )          
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/mini_blog_efi"

db = SQLAlchemy(app)
migrate = Migrate(app,db)

from models import User, Post, Comment

@app.route("/")
def index():
    return render_template(
        "index.html"
    )

app.route("/new_user")
def new_user():
    return render_template(
        "new_user.html"
    )
    