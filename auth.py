from flask import (
    Blueprint, render_template, redirect, url_for, request, flash
)
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .modelsdb import User
from . import db
from Constants.FlashMessagesModule import *

auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    loginError = False
    flashMessage = ""

    if email.replace(" ", "") ==  "" or password.replace(" ", "") == "":
        loginError = True
        flashMessage = FIELD_IS_EMPTY
        #flash(flashMessage)
        #return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()

    if user is None and loginError is False:
        loginError = True
        flashMessage = USERNAME_DOES_NOT_EXIST

    if user is not None and loginError is False:
        if not check_password_hash(user.password, password): #if user is None or (not user and check_password_hash(user.password, password))
            loginError = True
            flashMessage = PASSWORD_INCORRECT

    if loginError is True:
        flash(flashMessage)
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('main.purchase_order_index'))

@auth.route("/signup")
def signup():
    return render_template("SignUp.html")

@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    key = request.form.get("key")

    user = User.query.filter_by(email=email).first()

    if user:
        flash("Email address already exists")
        return redirect(url_for('auth.signup'))

    if not user and key == "arb0l":
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), title="Administrator")
        db.session.add(new_user)
        db.session.commit()
        print("Administrator user just signed up ")
        return redirect(url_for('auth.login'))

    if not user and not key:
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), title="Guest")
        db.session.add(new_user)
        db.session.commit()
        print("Guest user just signed up ")

    return redirect(url_for('auth.login'))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.addPurchaseOrder"))