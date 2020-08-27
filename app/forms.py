"""Creates a form to use on a testing page that will create a json and
pass it to the api
"""

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, \
    SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class TestForm(FlaskForm):
    """Gets needed values for a campaign to send to api
    """
    name = StringField('Name of Campaign', validators=[DataRequired()])
    desc = TextAreaField('Description of Campaign', )
    goal = FloatField('Amount', )
    keywords = StringField('Descriptive Keywords', )
    disable_com = SelectField('Are Communications Enabled?',
                              choices=[('False', 'Yes'), ('True', 'No')],)
    country = StringField('Country of Campaign', )
    currency = StringField('Type of Currency?', )
    length = IntegerField('Durration of Campaign (In Days)', )
    submit = SubmitField('Submit')
