from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models.user import User

class RegistrationForm(FlaskForm):
    """Form for user registration."""
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        """Check if username is already taken."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email is already registered."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered. Please use a different one.')

class LoginForm(FlaskForm):
    """Form for user login."""
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
