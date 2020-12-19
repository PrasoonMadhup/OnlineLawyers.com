import  pymongo
from flask import Flask, request, render_template, redirect, session
from flask_pymongo import PyMongo
from hashlib import sha256
from datetime import datetime
from congfig import config
from utils import get_random_string


app = Flask(_name_)
app.config["MONGO_URI"] = config["mongo_uri"]
mongo = PyMongo(app)
app.secret_key = b'j@ck@ss!!4sure!'

@app.route("/")
def show_mainpage():
    return render_template("frontend.html")

@app.route('/Signup1')
def show_LawyerSignup():
    if not 'userToken' in session:
        session['error'] = 'You must login to access this page.'
        return redirect('/Login1')

    # validate user login
    token_document = mongo.db.user_tokens.find_one({
        'sessionHash': session['userToken'],
    })

    if token_document is None:
        session.pop('userToken', None)
        session['error'] = 'You must login again to access this page.'
        return redirect('/Login1')


    return render_template('Lawyer.html')


@app.route('/Login1')
def lawyer_login():
    signupSuccess = ''
    if 'signupSuccess' in session:
        signupSuccess = session['signupSuccess']
        session.pop('signupSuccess', None)

    error = ''
    if 'error' in session:
        error = session['error']
        session.pop('error', None)
    return render_template('Login1.html', signupSuccess=signupSuccess, error=error)


@app.route('/check_login', methods=['POST'])
def check_login():
    try:
        name = request.form['name']
    except KeyError:
        name = ''
    try:
        Age = request.form['Age']
    except KeyError:
        Age = ''
    try:
        email = request.form['email']
    except KeyError:
        email = ''
    try:
        passoword = request.form['password']
    except KeyError:
        passoword = ''
    try:
        gender = request.form['gender']
    except KeyError:
        gender = ''
    try:
        Experience = request.form['Experience']
    except KeyError:
        Experience = ''
    try:
        Phone = request.form['Phone']
    except KeyError:
        Phone = ''
    try:
        Location = request.form['Location']
    except KeyError:
        Location = ''
    try:
         createdAt= request.form['datetime.utcnow()']
    except KeyError:
        createdAt = ''
    try:
        updatedAt = request.form['datetime.utcnow()']
    except KeyError:
        updatedAt = ''

    # check if email is blank
    if not len(email) > 0:
        session['error'] = 'Email is required'
        return redirect('/Login1')

    # check if password is blank
    if not len(passoword) > 0:
        session['error'] = 'Password is required'
        return redirect('/Login1')

    # find email in database
    user_document = mongo.db.users.find_one({ "email": email})
    if user_document is None:
        session['error'] = 'No account exists with this email address'
        return redirect('/Login1')

    # verify the password hash matches with original
    passoword_hash = sha256(passoword.encode('utf-8')).hexdigest()
    if user_document['password'] != passoword_hash:
        session['error'] = 'Password is wrong'
        return redirect('/Login1')

    # Generate token and save in session
    random_string = get_random_string()
    randomSessionHash = sha256(random_string.encode('utf-8')).hexdigest()
    token_object = mongo.db.user_tokens.insert_one({
        'userId': user_document['_id'],
        'sessionHash': randomSessionHash,
        'createdAT': datetime.utcnow(),
    })
    session['userToken'] = randomSessionHash

    return redirect('/')


@app.route('/Signup1')
def show_lawyerSignup():
    error = ''
    if 'error' in session:
        error = session['error']
        session.pop('error', None)
        result = mongo.db.users.insert_one({
            'name': request.form["name"],
            'Age': Age,
            'gender': gender,
            'Experience': Experience,
            'email': email,
            'Phone': Phone,
            'Location': Location,
            'password': password,
            'lastLoginDate': None,
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
        })
    return render_template('Login1.html', error=error)

@app.route('/handle_signup', methods=['POST'])
def handle_signup():
    try:
        email = request.form['email']
    except KeyError:
        email = ''
    try:
        passoword = request.form['password']
    except KeyError:
        passoword = ''

    # check if email is blank
    if not len(email) > 0:
        session['error'] = 'Email is required'
        return redirect('/signup')

    # check if email is invalid
    if not '@' in email or not '.' in email:
        session['error'] = 'Email is Invalid'
        return redirect('/signup')

    # check is passoword is blank
    if not len(passoword) > 0:
        session['error'] = 'Password is required'
        return redirect('/Signup1')

    # check if email already exists
    matching_user_count = mongo.db.users.count_documents({ "email": email})
    if matching_user_count > 0:
        session['error'] = 'Email already exists'
        return redirect('/Signup1')

    passoword = sha256(passoword.encode('utf-8')).hexdigest()

    # redirect to login page
    session['signupSuccess'] = 'Your user account is ready. You can login now'
    return redirect('/Login1')

@app.route('/logout')
def logout_user():
    session.pop('userToken', None)
    session['signupSuccess'] = 'You are now logged out.'
    return redirect('/Login1')

if _name_ == '_main_':
    app.run(debug=True)





@app.route('/Signup2')
def show_LawyerSignup():
    if not 'userToken' in session:
        session['error'] = 'You must login to access this page.'
        return redirect('/Login2')

    # validate user login
    token_document = mongo.db.user_tokens.find_one({
        'sessionHash': session['userToken'],
    })

    if token_document is None:
        session.pop('userToken', None)
        session['error'] = 'You must login again to access this page.'
        return redirect('/Login2')


    return render_template('Client.html')

@app.route('/Login2')
def lawyer_login():
    signupSuccess = ''
    if 'signupSuccess' in session:
        signupSuccess = session['signupSuccess']
        session.pop('signupSuccess', None)

    error = ''
    if 'error' in session:
        error = session['error']
        session.pop('error', None)
    return render_template('Login2.html', signupSuccess=signupSuccess, error=error)


@app.route('/check_login', methods=['POST'])
def check_login():
    try:
        name = request.form['name']
    except KeyError:
        name = ''
    try:
        Age = request.form['Age']
    except KeyError:
        Age = ''
    try:
        email = request.form['email']
    except KeyError:
        email = ''
    try:
        passoword = request.form['password']
    except KeyError:
        passoword = ''
    try:
        gender = request.form['gender']
    except KeyError:
        gender = ''
    try:
        District = request.form['District']
    except KeyError:
        District = ''
    try:
        Relief = request.form['Relief']
    except KeyError:
        Relief = ''
    try:
        Court = request.form['Court']
    except KeyError:
        Court = ''
    try:
         createdAt= request.form['datetime.utcnow()']
    except KeyError:
        createdAt = ''
    try:
        updatedAt = request.form['datetime.utcnow()']
    except KeyError:
        updatedAt = ''




 # check if password is blank
    if not len(passoword) > 0:
        session['error'] = 'Password is required'
        return redirect('/Login2')

    # find email in database
    user_document = mongo.db.users.find_one({ "email": email})
    if user_document is None:
        session['error'] = 'No account exists with this email address'
        return redirect('/Login2')

    # verify the password hash matches with original
    passoword_hash = sha256(passoword.encode('utf-8')).hexdigest()
    if user_document['password'] != passoword_hash:
        session['error'] = 'Password is wrong'
        return redirect('/Login2')

    # Generate token and save in session
    random_string = get_random_string()
    randomSessionHash = sha256(random_string.encode('utf-8')).hexdigest()
    token_object = mongo.db.user_tokens.insert_one({
        'userId': user_document['_id'],
        'sessionHash': randomSessionHash,
        'createdAT': datetime.utcnow(),
    })
    session['userToken'] = randomSessionHash

    return redirect('/')



@app.route('/Signup2')
def show_ClientSignup():
    error = ''
    if 'error' in session:
        error = session['error']
        session.pop('error', None)
        result = mongo.db.users.insert_one({
            'name': request.form["name"],
            'Age': Age,
            'gender': gender,
            'email': email,
            'Phone': Phone,
            'District': District,
            'State': State,
            'Relief': Relief
            'Court':Court
            'password': password,
            'lastLoginDate': None,
            'createdAt': datetime.utcnow(),
            'updatedAt': datetime.utcnow(),
        })
    return render_template('Login2.html', error=error)

@app.route('/handle_signup', methods=['POST'])
def handle_signup():
    try:
        email = request.form['email']
    except KeyError:
        email = ''
    try:
        passoword = request.form['password']
    except KeyError:
        passoword = ''

    # check if email is blank
    if not len(email) > 0:
        session['error'] = 'Email is required'
        return redirect('/Signup2')

    # check if email is invalid
    if not '@' in email or not '.' in email:
        session['error'] = 'Email is Invalid'
        return redirect('/Signup2')

    # check is passoword is blank
    if not len(passoword) > 0:
        session['error'] = 'Password is required'
        return redirect('/Signup2')

    # check if email already exists
    matching_user_count = mongo.db.users.count_documents({ "email": email})
    if matching_user_count > 0:
        session['error'] = 'Email already exists'
        return redirect('/Signup2')

    passoword = sha256(passoword.encode('utf-8')).hexdigest()

    # redirect to login page
    session['signupSuccess'] = 'Your user account is ready. You can login now'
    return redirect('/Login2')

@app.route('/logout')
def logout_user():
    session.pop('userToken', None)
    session['signupSuccess'] = 'You are now logged out.'
    return redirect('/Login2')

if _name_ == '_main_':
    app.run(debug=True)