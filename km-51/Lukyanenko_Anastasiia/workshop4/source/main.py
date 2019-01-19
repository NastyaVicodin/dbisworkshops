from flask import Flask, render_template, request, make_response, session, redirect, url_for, flash
from wtf.form.forms import StudentPresent, Results

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        return render_template('mainPage.html')


presense_dictionary = [{
    "present_id": "1",
    "lesson_id": "1",
    "student_id": "km51",
    "date": "2019-01-10"
}]


@app.route('/presense', methods=["GET", "POST"])
def registration():
    form = StudentPresent()
    if request.method == "POST" and form.validate():
        d = {
            "present_id": request.form["present_id"],
            "lesson_id": request.form["lesson_id"],
            "student_id": request.form["student_id"],
            "date": request.form["date"],
        }
        presense_dictionary.append(d)
        return render_template('presense.html', form=form)
    else:
        return render_template('presense.html', form=form)


@app.route('/list', methods=["GET", "POST"])
def list():
    table = Results(presense_dictionary)
    table.border = True
    if request.method == "POST":
        return render_template('list.html', d=presense_dictionary, table=table)
    else:
        return render_template('list.html', d=presense_dictionary, table=table)


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True, port=8085)
