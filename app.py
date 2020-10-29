from flask import Flask,render_template
app = Flask(__name__)

@app.route("/")
def show_mainpage():
    return render_template("frontend.html")



@app.route("/login1")
def show_lawyerlogin