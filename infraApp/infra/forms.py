from flask.ext.wtf import Form
from wtforms import StringField, DateField, TextField, FloatField, SubmitField, SelectField
from wtforms.validators import Required, Length, Optional
from flask.ext.pagedown.fields import PageDownField

class AddProjectForm(Form):

    prjID = StringField('Project ID', validators=[Required(), Length(1,64)])
    title = StringField('Title of Project', validators=[Required(), Length(1,128)])
    cost = 	FloatField('Cost', validators=[Required()])
    contractor = StringField('Contractor', validators=[Required(), Length(1,64)])
    address = TextField('Address of Project', validators=[Required()])
    status = FloatField('% Completed', validators=[Required()])
    dateStart = DateField('Date Start i.e.(YYYY-MM-DD)', validators=[Required()])
    dateEnd = DateField('Date End i.e.(YYYY-MM-DD)', validators=[Required()])
    agency = StringField('Implementing Agency', validators=[Required(), Length(1,64)])
    funding = StringField('Source of Funds', validators=[Required(), Length(1,64)])
    lat = FloatField('Latitude', validators=[Required()],id='latitude')
    lon = FloatField('Longitude', validators=[Required()],id='longitude')
    region = SelectField(u'Region',
            coerce=int,
            choices=[
                (1, '01'),(2, '02'),(3, '03'),(4, '04A'),(5, '04B'),(6, '05'),(7, '06'),
                (8, '07'),(9, '08'),(10, '09'),(11, '10'),(12, '11'),(13, '12'),(13, '12'),
                (14, '13'),(15, 'CAR'),(16, 'NCR')
            ])
    submitData = SubmitField('Submit Project')

class CommentForm(Form):
    name = StringField('Name', validators=[Required(), Length(1,64)])
    email = StringField('Email', validators=[Required(), Length(1,64)])
    body = PageDownField('Comment', validators=[Required()])
    submit = SubmitField('Submit')

class SearchForm(Form):
    title = StringField('', validators=[Required()])
    submit = SubmitField('Go')

class ProjectEditorForm(Form):
    actComp = StringField('Actual Completion', validators=[Required(), Length(1,64)])
    status = FloatField('% Completed')
    lat = FloatField('Latitude:', validators=[Required(), Length(1,64)],id='latitude')
    lng = FloatField('Longitude:', validators=[Required(), Length(1,64)],id='longitude')
    submit = SubmitField('Update')
