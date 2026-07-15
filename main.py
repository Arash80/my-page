import hashlib
import os
import warnings
from datetime import date
from functools import wraps

import nh3
from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    url_for,
)

# Flask-CKEditor warns when its optional Bleach helper is unavailable. This app
# deliberately uses the maintained nh3 sanitizer instead.
warnings.filterwarnings(
    "ignore",
    message='The "bleach" library is not installed.*',
    category=UserWarning,
    module="flask_ckeditor.utils",
)

from flask_ckeditor import CKEditor  # noqa: E402
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from markupsafe import Markup
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from forms import CommentForm, CreatePostForm, EmptyForm, LoginForm, RegisterForm


load_dotenv()

db = SQLAlchemy()
ckeditor = CKEditor()
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message_category = "info"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship(
        "Comment", back_populates="comment_author", cascade="all, delete-orphan"
    )


class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"), nullable=False)
    comment_author = relationship("User", back_populates="comments")
    comment_post = relationship("BlogPost", back_populates="comments")


class BlogPost(db.Model):
    __tablename__ = "blog_posts"

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    author = relationship("User", back_populates="posts")
    comments = relationship(
        "Comment", back_populates="comment_post", cascade="all, delete-orphan"
    )


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def is_admin_user():
    return (
        current_user.is_authenticated
        and current_user.id == current_app.config["ADMIN_USER_ID"]
    )


def admin_only(view):
    @wraps(view)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return login_manager.unauthorized()
        if not is_admin_user():
            abort(403)
        return view(*args, **kwargs)

    return decorated_function


def sanitize_html(value):
    """Sanitize rich text before storage and whenever legacy content is rendered."""
    return nh3.clean(value or "")


def create_app(test_config=None):
    app = Flask(__name__)
    database_url = os.getenv("DATABASE_URL", "sqlite:///blog.db")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY") or os.getenv("secure_key"),
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        ADMIN_USER_ID=int(os.getenv("ADMIN_USER_ID", "1")),
        CONTACT_EMAIL=os.getenv("CONTACT_EMAIL", ""),
    )
    if test_config:
        app.config.update(test_config)
    if not app.config["SECRET_KEY"]:
        raise RuntimeError("SECRET_KEY is required. Copy .env.example to .env and set it.")

    db.init_app(app)
    ckeditor.init_app(app)
    login_manager.init_app(app)

    @app.template_filter("safe_html")
    def safe_html(value):
        return Markup(sanitize_html(value))

    @app.context_processor
    def template_defaults():
        return {
            "is_admin": is_admin_user(),
            "logout_form": EmptyForm(),
            "current_year": date.today().year,
        }

    @app.template_global()
    def gravatar_url(email, size=100):
        digest = hashlib.md5(email.strip().lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?s={size}&d=retro&r=g"

    @app.get("/")
    def get_all_posts():
        posts = db.session.scalars(
            db.select(BlogPost).order_by(BlogPost.id.desc())
        ).all()
        return render_template("index.html", all_posts=posts)

    @app.route("/register", methods=["GET", "POST"])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            email = form.email.data.strip().lower()
            existing_user = db.session.scalar(db.select(User).filter_by(email=email))
            if existing_user:
                flash("That email is already registered. Please log in.", "info")
                return redirect(url_for("login"))

            new_user = User(
                email=email,
                name=form.name.data.strip(),
                password=generate_password_hash(form.password.data, method="scrypt"),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("get_all_posts"))
        return render_template("register.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data.strip().lower()
            user = db.session.scalar(db.select(User).filter_by(email=email))
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("get_all_posts"))
            flash("Invalid email or password.", "danger")
        return render_template("login.html", form=form)

    @app.post("/logout")
    def logout():
        form = EmptyForm()
        if form.validate_on_submit():
            logout_user()
        return redirect(url_for("get_all_posts"))

    @app.route("/post/<int:post_id>", methods=["GET", "POST"])
    def show_post(post_id):
        post = db.get_or_404(BlogPost, post_id)
        form = CommentForm()
        if form.validate_on_submit():
            if not current_user.is_authenticated:
                flash("Please log in or register to comment.", "info")
                return redirect(url_for("login"))
            db.session.add(
                Comment(
                    text=sanitize_html(form.comment.data),
                    comment_author=current_user,
                    comment_post=post,
                )
            )
            db.session.commit()
            return redirect(url_for("show_post", post_id=post.id))
        return render_template("post.html", post=post, form=form)

    @app.get("/about")
    def about():
        return render_template("about.html")

    @app.get("/contact")
    def contact():
        return render_template("contact.html", contact_email=app.config["CONTACT_EMAIL"])

    @app.route("/new-post", methods=["GET", "POST"])
    @admin_only
    def add_new_post():
        form = CreatePostForm()
        if form.validate_on_submit():
            post = BlogPost(
                title=form.title.data.strip(),
                subtitle=form.subtitle.data.strip(),
                body=sanitize_html(form.body.data),
                img_url=form.img_url.data.strip(),
                author=current_user,
                date=date.today().strftime("%B %d, %Y"),
            )
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("get_all_posts"))
        return render_template("make-post.html", form=form, is_edit=False)

    @app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
    @admin_only
    def edit_post(post_id):
        post = db.get_or_404(BlogPost, post_id)
        form = CreatePostForm(obj=post)
        if form.validate_on_submit():
            post.title = form.title.data.strip()
            post.subtitle = form.subtitle.data.strip()
            post.img_url = form.img_url.data.strip()
            post.body = sanitize_html(form.body.data)
            db.session.commit()
            return redirect(url_for("show_post", post_id=post.id))
        return render_template("make-post.html", form=form, is_edit=True)

    @app.post("/delete/<int:post_id>")
    @admin_only
    def delete_post(post_id):
        form = EmptyForm()
        if not form.validate_on_submit():
            abort(400)
        post = db.get_or_404(BlogPost, post_id)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
