from flask import Flask, render_template, request, make_response, session, redirect, url_for, flash


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("cookie_1.html")

@app.route('/delete')
def delete():
    return render_template("cookie_2.html")

@app.route('/api', methods=['POST'])
def apiPost():
    if request.form["action"] == "sum":
        a = request.form["A"]
        b = request.form["B"]
        sum_ = str(int(a) + int(b))
        response = make_response(redirect(url_for('index')))
        response.set_cookie("result", sum_)
        login_cook = request.cookies.get("login")
        if login_cook:
            response = make_response(redirect(url_for('delete')))
            response.set_cookie("result", sum_)
            return response
        response.set_cookie("login", "random")
        return response
    elif request.form["action"] == "delete":
        response = make_response(redirect(url_for('index')))
        response.set_cookie("login", "", expires=0)
        return response
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=8085)