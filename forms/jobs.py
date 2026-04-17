from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    team_leader = IntegerField('ID руководителя', validators=[DataRequired()])
    work_size = IntegerField('Продолжительность (в часах)',
                             validators=[DataRequired()])
    collaborators = StringField('Список участников (ID)',
                                validators=[DataRequired()])
    is_finished = BooleanField('Работа завершена?')
    submit = SubmitField('Добавить')