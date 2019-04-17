from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class NewPostForm(FlaskForm):
    title = TextField('Title', validators=[DataRequired()])
    content = TextAreaField('Content')
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Submit')
