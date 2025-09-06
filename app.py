from datetime import datetime

from flask import (
    Flask,
    flash,
    render_template,
    request,
    redirect,
    url_for, 
    )        
#importacion para generar las migraciones de la db
from flask_migrate import Migrate
#importacion para la db
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import desc

#importacion para login
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
    )

import os

#importacion para hashear la contraseña
from werkzeug.security import(
    check_password_hash,
    generate_password_hash
    )


app = Flask(__name__)

#Secret key para sesiones seguras
app.secret_key = "cualquiercosa"


# Configuración para Clever Cloud
#app.config["SQLALCHEMY_DATABASE_URI"] = (
#    f"mysql+pymysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}@"
#    f"{os.environ['MYSQL_HOST']}:{os.environ['MYSQL_PORT']}/{os.environ['MYSQL_DB']}"
#)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://umxnwsbwkclpvycq:YjEX2rsYKFK3kMQQjM3g@"
    "b8q5w1qdvo7omjytxant-mysql.services.clever-cloud.com:3306/"
    "b8q5w1qdvo7omjytxant"
)

db = SQLAlchemy(app)
migrate = Migrate(app,db)


login_manager= LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
#importacion de los models para poder hacer los migrates
from models import User, Post, Comment, Category


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    

@app.route("/")
def index():
    return render_template(
        "index.html",
        fecha = datetime.today()
    )
    
#metodo para el login
@app.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("mi_muro"))
    
    if request.method == "POST":

        name = request.form["username"]
        password = request.form["password"]
    
        user = User.query.filter_by(name=name).first()
        if user and check_password_hash(pwhash=user.password_hash, password=password):
            login_user(user)
            return redirect(url_for("mi_muro"))
        
        elif user is None:
            flash("Usuario no encontrado", "danger")
            return redirect(url_for('login'))

        
    return render_template(
        "auth/login.html"
    )
      
#metodo para el register
@app.route("/register", methods=["GET","POST"])
def register():
    #si el usuario esta autenticado redirecciona al perfil
    if current_user.is_authenticated:
        return redirect(url_for("mi_muro"))
    
    #recibe la info del form
    if request.method == "POST":
        name = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        
        #verificacion que no exista el nombre de usuario
        user = User.query.filter_by(name=name).first()
        if user:
            flash("El nombre de usuario no esta disponible", "error")
            return redirect(url_for("register"))
        
        #Hasheo de contraseña
        password_hash = generate_password_hash(
            password=password,
            method = "pbkdf2"
        )
        #creacion del nuevo usuario
        new_user = User(
            name = name,
            email = email,
            password_hash = password_hash
        )
        #agregando nuevo usuario a la db
        db.session.add(new_user)
        db.session.commit()
        flash("Usuario creado correctamente", "success")
        return redirect(url_for("login"))
    
    return render_template(
        "auth/register.html"
    )

#metodo para cerrar sesion
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

#metodo para el template de mi muro
@app.route("/mi_muro")
@login_required
def mi_muro():
    posts = Post.query.filter_by(user_id=current_user.id).order_by(desc(Post.date_time)).all()
    return render_template(
        "mi_muro.html", posts = posts
    )
    
#Eliminar un post cambiandole el valor de is_active
@app.route("/post/delete/<int:post_id>", methods= ["POST"])
def delete_post(post_id):
    post_delate =  Post.query.get_or_404(post_id)
    post_delate.is_active = 0
    db.session.commit()
    return redirect(url_for('mi_muro'))

    
@app.route("/inicio", methods=["GET","POST"])
@login_required
def inicio():
    if request.method == "POST":
        form_type = request.form.get("form_type")
        if form_type == "post":
            title = request.form["title"]
            content = request.form["content"]
            category_id = request.form["category"]
            
            date_time = datetime.now()
            user_id = current_user.id
            new_post =  Post(
            title = title,
            content = content,
            date_time = date_time,
            user_id = user_id,
            category_id = category_id
            )
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for("inicio"))
        elif form_type == "comment":
            text_comment = request.form["comment"]
            post_id = request.form.get("post_id")
            new_comment = Comment(
            text_comment = text_comment,
            date_time = datetime.now(),
            user_id = current_user.id,
            post_id = int(post_id)
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for("inicio"))
    categorias = Category.query.all()
    posts = Post.query.filter_by(is_active=1).order_by(desc(Post.date_time)).all()    
    return render_template("inicio.html", posts=posts, categorias=categorias)
        
        
    
    
    
