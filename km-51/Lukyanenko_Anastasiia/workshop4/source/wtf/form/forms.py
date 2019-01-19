from flask_wtf import Form
from wtforms import StringField, validators, SubmitField
from wtforms.fields.html5 import DateField
from flask_table import Table, Col

class StudentPresent(Form):
    present_id = StringField("Present_id:", [validators.DataRequired("Required")])
    lesson_id = StringField("Lesson_id:", [validators.DataRequired("Required")])
    student_id = StringField("Student_id:", [validators.DataRequired("Required")])
    date = DateField("Date:", [validators.DataRequired("Required")])
    submit = SubmitField("Add")

class Results(Table):
    present_id = Col('present_id')
    lesson_id = Col('lesson_id')
    student_id = Col('student_id')
    date = Col('date')
