from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class SignupForm(FlaskForm):
    """User Signup Form."""
    name = StringField('Name',
                       validators=[DataRequired()])
    email = StringField('Email',
                        validators=[Length(min=6),
                                    Email(message='Enter a valid email.'),
                                    DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password',
                            validators=[DataRequired(),
                                        EqualTo('password', message='Passwords must match.')])
    website = StringField('Website',
                          validators=[Optional()])
    submit = SubmitField('Submit')


class SigninForm(FlaskForm):
    """User Signin Form."""
    email = StringField('Email', validators=[DataRequired(),
                                             Email(message='Enter a valid email.')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ResetPasswordRequestForm(FlaskForm):
    """Reset Password Request Form."""
    email = StringField('Email adress', validators=[DataRequired(),
                                                    Email(message='Enter a valid email.')])
    submit = SubmitField('Send email link')


class ResetPasswordForm(FlaskForm):
    """Reset Password Form."""
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password',
                            validators=[DataRequired(),
                                        EqualTo('password', message='Passwords must match.')])

    submit = SubmitField('Reset password')


class NoteForm(FlaskForm):
    """Note Form"""
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[
                            Optional()])
    tags = StringField('Tags', validators=[Optional()])
    submit = SubmitField('Submit')
