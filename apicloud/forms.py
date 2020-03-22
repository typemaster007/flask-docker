from flask_wtf import FlaskForm
from wtforms import Form, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class SearchNoteForm(FlaskForm):
    
    search = StringField('')

    submit1 = SubmitField('Submitform')

    submit2 = SubmitField('Submit Note')

    cancel = SubmitField('Back to Search Page')




class AddNote(FlaskForm):

    addnote = StringField('Add Note')

    retnote = StringField('Retrieve Note')

    ret = SubmitField('Retrieve Note')

    submit2 = SubmitField('Submit Note')

    cancel = SubmitField('Back to Search Page')

    cancel2 = SubmitField('Back to Results Page')


