from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, URL


class CreatePostForm(FlaskForm):
    title = StringField(
        "Blog Post Title", validators=[DataRequired(), Length(max=250)]
    )
    subtitle = StringField("Subtitle", validators=[DataRequired(), Length(max=250)])
    img_url = StringField(
        "Blog Image URL", validators=[DataRequired(), URL(), Length(max=500)]
    )
    body = CKEditorField("Blog Content", validators=[DataRequired()])
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
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit")


class EmptyForm(FlaskForm):
    submit = SubmitField("Submit")
