import os

import pytest
from werkzeug.security import generate_password_hash

os.environ.setdefault("SECRET_KEY", "module-import-test-secret")

from main import BlogPost, Comment, User, create_app, db


@pytest.fixture()
def app(tmp_path):
    database_path = (tmp_path / "test.db").as_posix()
    app = create_app(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,
            "SECRET_KEY": "test-secret",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}",
            "ADMIN_USER_ID": 1,
        }
    )
    with app.app_context():
        db.drop_all()
        db.create_all()
        admin = User(
            email="admin@example.com",
            name="Admin",
            password=generate_password_hash("admin-pass-123", method="scrypt"),
        )
        member = User(
            email="member@example.com",
            name="Member",
            password=generate_password_hash("member-pass-123", method="scrypt"),
        )
        db.session.add_all([admin, member])
        db.session.commit()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def login(client, email, password):
    return client.post(
        "/login", data={"email": email, "password": password}, follow_redirects=True
    )


def create_post(app):
    with app.app_context():
        post = BlogPost(
            title="Existing post",
            subtitle="A subtitle",
            body="<p>Safe body</p>",
            img_url="https://example.com/image.jpg",
            date="July 15, 2026",
            author=db.session.get(User, 1),
        )
        db.session.add(post)
        db.session.commit()
        return post.id


def test_public_pages_and_missing_post(client):
    for path in ("/", "/about", "/contact", "/login", "/register"):
        assert client.get(path).status_code == 200
    assert client.get("/post/9999").status_code == 404


def test_admin_crud_uses_post_for_changes(app, client):
    login(client, "admin@example.com", "admin-pass-123")

    response = client.post(
        "/new-post",
        data={
            "title": "New post",
            "subtitle": "New subtitle",
            "img_url": "https://example.com/new.jpg",
            "body": "<p>Hello</p><script>alert(1)</script>",
        },
    )
    assert response.status_code == 302

    with app.app_context():
        post = db.session.scalar(db.select(BlogPost).filter_by(title="New post"))
        assert post is not None
        assert "<script" not in post.body
        post_id = post.id

    response = client.post(
        f"/edit-post/{post_id}",
        data={
            "title": "Updated post",
            "subtitle": "Updated subtitle",
            "img_url": "https://example.com/updated.jpg",
            "body": "<p>Updated</p>",
        },
    )
    assert response.status_code == 302
    assert client.get(f"/delete/{post_id}").status_code == 405
    assert client.post(f"/delete/{post_id}").status_code == 302

    with app.app_context():
        assert db.session.get(BlogPost, post_id) is None


def test_non_admin_cannot_manage_posts(app, client):
    post_id = create_post(app)
    login(client, "member@example.com", "member-pass-123")
    assert client.get("/new-post").status_code == 403
    assert client.get(f"/edit-post/{post_id}").status_code == 403
    assert client.post(f"/delete/{post_id}").status_code == 403


def test_comment_html_is_sanitized(app, client):
    post_id = create_post(app)
    login(client, "member@example.com", "member-pass-123")
    payload = '<p>Hello</p><script>alert("xss")</script>'
    response = client.post(
        f"/post/{post_id}", data={"comment": payload}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b'<script>alert("xss")</script>' not in response.data

    with app.app_context():
        comment = db.session.scalar(db.select(Comment))
        assert comment is not None
        assert "<script" not in comment.text


def test_seed_content_is_useful_and_idempotent(app):
    runner = app.test_cli_runner()
    assert runner.invoke(args=["seed-content"]).exit_code == 0
    assert runner.invoke(args=["seed-content"]).exit_code == 0

    with app.app_context():
        posts = db.session.scalars(db.select(BlogPost)).all()
        assert len(posts) == 3
        assert db.session.get(User, 1).name == "Arash"
        assert all(len(post.body) > 400 for post in posts)
        assert all("<script" not in post.body for post in posts)
