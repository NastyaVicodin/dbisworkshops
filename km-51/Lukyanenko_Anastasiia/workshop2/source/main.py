from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello from Flask<h1>'


vacancy_dictionary = {
    "vacancy_name": "Software engineer",
    "salary": "1000",
    "sphere": "IT",
    "location": "Ukraine",
    "company": "Global Logic"
}

user_request_dictionary = {
    "user_name": "Anastasia Lukianenko",
    "salary": "1000",
    "sphere": "IT",
    "specialization": "C developer",
    "location": "Ukraine"
}

available_dictionary = dict.fromkeys(['vacancy', 'user_request'], "dict_name")


@app.route('/api/<action>', methods=['GET'])
def apiGet(action):
    if action == "vacancy":
        return render_template("vacancy.html", vacancy=vacancy_dictionary)
    elif action == "user_request":
        return render_template("user_request.html", user_request=user_request_dictionary)
    elif action == "all":
        return render_template("all.html", user_request=user_request_dictionary, vacancy=vacancy_dictionary)
    else:
        return render_template("404.html", action_value=action, available=available_dictionary)


@app.route('/api', methods=['POST'])
def apiPost():
    if request.form["action"] == "vacancy_update":
        vacancy_dictionary["vacancy_name"] = request.form["vacancy_name"]
        vacancy_dictionary["salary"] = request.form["salary"]
        vacancy_dictionary["sphere"] = request.form["sphere"]
        vacancy_dictionary["location"] = request.form["location"]
        vacancy_dictionary["company"] = request.form["company"]
        return redirect(url_for('apiGet', action="all"))

    elif request.form["action"] == "user_request_update":
        user_request_dictionary["user_name"] = request.form["user_name"]
        user_request_dictionary["salary"] = request.form["salary"]
        user_request_dictionary["sphere"] = request.form["sphere"]
        user_request_dictionary["specialization"] = request.form["specialization"]
        user_request_dictionary["location"] = request.form["location"]
        return redirect(url_for('apiGet', action="all"))


if __name__ == '__main__':
    app.run(debug=True, port=8085)