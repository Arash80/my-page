from flask_wtf import FlaskForm
from html import unescape
import re

from wtforms import HiddenField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, URL, ValidationError


def rich_text_required(_form, field):
    """Reject editor markup that contains no readable content."""
    text = unescape(re.sub(r"<[^>]*>", "", field.data or ""))
    if not text.replace("\xa0", " ").strip():
        raise ValidationError("This field is required.")


class CreatePostForm(FlaskForm):
    title = StringField(
        "Blog Post Title", validators=[DataRequired(), Length(max=250)]
    )
    subtitle = StringField("Subtitle", validators=[DataRequired(), Length(max=250)])
    img_url = StringField(
        "Blog Image URL", validators=[DataRequired(), URL(), Length(max=500)]
    )
    body = HiddenField("Blog Content", validators=[rich_text_required])
    submit = SubmitField("Save Post")


class RegisterForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(max=254)]
    )
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=128)]
    )
    submit = SubmitField("Sign Me Up!")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class CommentForm(FlaskForm):
    comment = HiddenField("Comment", validators=[rich_text_required])
    submit = SubmitField("Submit")


class EmptyForm(FlaskForm):
    submit = SubmitField("Submit")
