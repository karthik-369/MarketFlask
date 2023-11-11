
# from crypt import methods
from market import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from market.models import Item
from market.forms import RegisterForm, LoginForm
from market.models import User, Item
from market import db
from flask_login import login_user, logout_user, login_required
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/home')
def redirectHome():
    return render_template('home.html')

@app.route('/market')
@login_required
def toMarket():
    items = Item.query.all()
    return render_template('market.html',items=items) 


@app.route('/register', methods=['GET', 'POST'])
def registerPage():
    print("from  me")
    form = RegisterForm()
    print(f'Form submitted: {form.validate_on_submit()}')
    if form.validate_on_submit():
        print("successfull heheheheheh")
        existingUser = User.query.filter_by(userName=form.userName.data).first()
        existingEmail = User.query.filter_by(emailAddress=form.emailAddress.data).first()
        print(existingUser)
        if existingUser:
            flash(f'User Already Exists',category='danger')
        elif existingEmail:
            flash(f'Email Already in use', category='danger')
        else :
            user_to_create = User(userName=form.userName.data, emailAddress=form.emailAddress.data
                                , password=form.password1.data)
            db.session.add(user_to_create)
            db.session.commit()
            flash("Account created successfully", category="success")
            return redirect(url_for('login'))
        
        
    print(f'eroor: {form.errors}')
    print(form.errors)
    if form.errors :
        for err in form.errors.values():
            flash(f'Error:,{err}',category='danger')
    return render_template('regiForm.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("YES YSe")
        # flash('yes', category='danger')
        attempted_user = User.query.filter_by(userName=form.userName.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success, you are logged in as : {attempted_user.userName}', category='success')
            return redirect(url_for('toMarket'))
        else:
            flash('Username or Password is wrong, Please try again',category="danger")
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect(url_for("redirectHome"))