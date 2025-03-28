from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class ChatMessageForm(FlaskForm):
    """Form for sending a chat message."""
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Send')

class ChatTitleForm(FlaskForm):
    """Form for updating chat title."""
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Update')
