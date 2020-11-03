from flask import Flask,render_template,redirect
from flask_pymongo import PyMongo
from congfig import config

app = Flask(__name__)
app.config["MONGO_URI"] = config["mongo_uri"]
mongo = PyMongo(app)
app.secret_key = b'j@ck@ss!!4sure!'



@app.route("/")
def show_mainpage():
    return render_template("frontend.html")



@app.route("/Login1")
def show_lawyerlogin():
    return render_template("Login1.html")

@app.route("/Signup1", methods=["POST"])
def show_lawyerSignup():
    result = mongo.db.users.insert_one({
        'name':name,
        'Age':Age,
        'gender':gender,
        'Experience': Experience,
        'email': email,
        'Phone':Phone,
        'Location':Location,
        'password': password,
        'lastLoginDate': None,
        'createdAt': datetime.utcnow(),
        'updatedAt': datetime.utcnow(),
    })

    return redirect("Login1.html")
if __name__ == '__main__':
    app.run(debug=True)



