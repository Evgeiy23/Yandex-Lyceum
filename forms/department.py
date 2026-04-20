from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email


class DepartmentForm(FlaskForm):
    title = StringField('Название департамента', validators=[DataRequired()])
    chief = IntegerField('ID руководителя', validators=[DataRequired()])
    members = StringField('Участники (ID через запятую)',
                          validators=[DataRequired()])
    email = StringField('Почта департамента',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Принять')