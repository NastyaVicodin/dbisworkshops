from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello from Flask<h1>'


work_dictionary = {
    "name": "Software engineer",
    "salary": "1000"
}

person_dictionary = {
    "name": "Anastasia Lukianenko",
    "skill": "C"
}

available_dictionary = dict.fromkeys(['work', 'person'], "dict_name")


@app.route('/api/<action>', methods=['GET'])
def apiGet(action):
    if action == "work":
        return render_template("work.html", work=work_dictionary)
    elif action == "person":
        return render_template("person.html", person=person_dictionary)
    elif action == "all":
        return render_template("all.html", person=person_dictionary, work=work_dictionary)
    else:
        return render_template("404.html", action_value=action, available=available_dictionary)


@app.route('/api', methods=['POST'])
def apiPost():
    if request.form["action"] == "work_update":
        work_dictionary["name"] = request.form["name"]
        work_dictionary["salary"] = request.form["salary"]
        return redirect(url_for('apiGet', action="all"))

    elif request.form["action"] == "person_update":
        person_dictionary["name"] = request.form["name"]
        person_dictionary["skill"] = request.form["skill"]
        return redirect(url_for('apiGet', action="all"))


if __name__ == '__main__':
    app.run(debug=True, port=8085)