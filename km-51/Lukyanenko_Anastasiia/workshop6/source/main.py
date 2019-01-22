import datetime
from functools import wraps

from flask import Flask, render_template, request, make_response, session, redirect, url_for, flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

from dao.userhelper import *
from dao.vacancy_helper import *
from wtf.form.forms import LoginForm, RegistrationForm, ProfileForm, PasswordForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://system:100498@127.0.0.1:1521'
admin = Admin(app)
db = SQLAlchemy(app)


class UserAdmin(db.Model):
    __tablename__ = 'check_in_user'
    last_name = db.Column('last_name', db.VARCHAR(30))
    first_name = db.Column('first_name', db.VARCHAR(30))
    login = db.Column('login', db.VARCHAR(30), primary_key=True)
    password = db.Column('password', db.VARCHAR(30))
    email = db.Column('email', db.VARCHAR(30))
    salary = db.Column('salary', db.VARCHAR(30))
    specialization = db.Column('specialization', db.VARCHAR(30))
    location = db.Column('location', db.VARCHAR(30))
    sphere = db.Column('sphere', db.VARCHAR(30))


class VacancyAdmin(db.Model):
    __tablename__ = 'vacancy'
    vacancy_name = db.Column('vacancy_name', db.VARCHAR(30))
    company = db.Column('company', db.VARCHAR(30))
    email = db.Column('email', db.VARCHAR(30), primary_key=True)
    salary = db.Column('salary', db.VARCHAR(30))
    location = db.Column('location', db.VARCHAR(30))
    sphere = db.Column('sphere', db.VARCHAR(30))


admin.add_view(ModelView(UserAdmin, db.session))
admin.add_view(ModelView(VacancyAdmin, db.session))


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'login' in session:
            return f(*args, **kwargs)
        elif request.cookies.get("cookiename") is not None:
            session['login'] = request.cookies.get("cookiename")
            return f(*args, **kwargs)
        else:
            flash('Please log in', 'danger')
            return redirect(url_for('login'))

    return wrap


@app.route('/', methods=["GET"])
@is_logged_in
def index():
    if request.method == "GET":
        return render_template('mainPage.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if not form.validate():
            return render_template('login.html', form=form)
        elif User().authorization(p_login=request.form["login"], p_password=request.form["password"]) == 'OK':
            expire_date = datetime.datetime.now()
            expire_date = expire_date + datetime.timedelta(days=1)
            response = make_response(redirect(url_for('index')))
            response.set_cookie("cookiename", request.form["login"], expires=expire_date)
            session['login'] = request.form['login']
            return response
        else:
            return render_template('login.html', form=form, error='Invalid login or password')
    else:
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('login', None)
    response = make_response(redirect(url_for('login')))
    response.set_cookie("cookiename", '', expires=0)
    return response


@app.route('/register', methods=["GET", "POST"])
def registration():
    form = RegistrationForm()
    if request.method == "POST" and form.validate():
        status = User().register(p_last_name=request.form["last_name"],
                                 p_first_name=request.form["first_name"],
                                 p_email=request.form["email"], p_login=request.form["login"],
                                 p_salary=request.form["salary"], p_specialization=request.form["specialization"],
                                 p_location=request.form["location"], p_sphere=request.form["sphere"],
                                 p_password=request.form["password"])

        if status == 'OK':
            flash("You are registered", 'success')
            response = make_response(redirect(url_for('index')))
            return response
        else:
            flash(status, 'danger')
            return render_template('registration.html', form=form)
    else:
        return render_template('registration.html', form=form)


@app.route('/profile', methods=["GET", "POST"])
@is_logged_in
def profile():
    form = ProfileForm()
    user = User().get_user(p_login=session['login'])
    if request.method == "GET":
        if user is not None:
            form.last_name.data = user[0]
            form.first_name.data = user[1]
            form.login.data = user[2]
            form.email.data = user[4]
            form.salary.data = user[5]
            form.specialization.data = user[6]
            form.location.data = user[7]
            form.sphere.data = user[8]

            return render_template('profile.html', form=form)
        else:
            return render_template('profile.html', form=form)
    elif request.method == "POST" and form.validate():
        status = User().update(p_last_name=request.form["last_name"],
                               p_first_name=request.form["first_name"],
                               p_email=request.form["email"], p_login=request.form["login"],
                               p_salary=request.form["salary"], p_specialization=request.form["specialization"],
                               p_location=request.form["location"], p_sphere=request.form["sphere"])
        if status == 'OK':
            flash("Update", 'success')
            session['login'] = request.form["login"]
            return render_template('profile.html', form=form)
        else:
            flash('Invalid info', 'danger')
            return render_template('profile.html', form=form)
    else:
        flash('Invalid info', 'danger')
        return render_template('profile.html', form=form)


@app.route('/password', methods=["GET", "POST"])
def password():
    form = PasswordForm()
    user = User().get_user(p_login=session['login'])
    if request.method == "GET":
        return render_template('password.html', form=form)
    elif request.method == "POST" and form.validate():
        status = User().update_password(p_login=user[2], p_old_password=request.form["old_password"],
                                        p_new_password=request.form["new_password"],
                                        )
        if status == 'OK':
            flash("Update", 'success')
            return render_template('password.html', form=form)
        else:
            flash('Invalid password', 'danger')
            return render_template('password.html', form=form)


@app.route('/search', methods=["GET", "POST"])
@is_logged_in
def search():
    vacancies_result_data = []
    user = User().get_user(p_login=session['login'])
    vacancies = Vacancy().get_all_vacancies()
    for vacancy in vacancies:
        if (vacancy[5] == user[8] or vacancy[0] == user[6]) and vacancy[4] == user[7]\
                 and int(vacancy[3]) >= int(user[5]):
            vacancies_result_data.append(vacancy)
    return render_template('search.html', data=vacancies_result_data)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True, port=8085)
