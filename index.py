from flask import Flask, request, render_template, redirect, url_for
from db import *
from verify import sendEmail
import string
import random

app = Flask(__name__, template_folder="html")


def randomHash():
    return ''.join(random.choices(string.digits, k=4))


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email, password = request.form["email"], request.form["password"]
        if emailExist(email):
            account_password  = getPassword(email)

            if account_password == password:
                return redirect(url_for("success"))
            
            elif account_password != password:
                return render_template("login.html", error="Password not correct!")

        elif not emailExist(email):
            return render_template("login.html", error="Email does not exist")

    return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email, password = request.form['email'], request.form['password']

        if len(email) > 5 and len(password) > 5:
            if not emailExist(email):
                createAccount(email, password)
                return redirect(url_for("login"))
            
            elif emailExist(email):
                return render_template("register.html", error="Email already exists")

        else:
            return render_template("register.html", error="Please input an email and password bigger than 5 characters")


    return render_template("register.html")


@app.route("/forgot-password", methods=['GET', 'POST'])
def forgot_password():
    if request.method == "POST":
        email = request.form['email']

        if emailExist(email):
            forgot_hash = randomHash()
            addEmailHash(email, forgot_hash)

            hash_link = "http://127.0.0.1:5000/reset-password?pin=" + forgot_hash

            sendEmail(email, hash_link)

            return render_template("forgot-password.html", msg="password reset link has been sent")

        elif not emailExist(email):
            return render_template("forgot-password.html", error="Email does not exist")

    return render_template("forgot-password.html")


@app.route("/reset-password", methods=['GET', 'POST'])
def resetPassword():
    hash = request.args['pin']
    if request.method == "GET":
        if getEmailFromHash(hash):
            return render_template("resetpassword.html")

        elif not getEmailFromHash(hash):
            return "<code>hash is not valid</code>"

    elif request.method == "POST":
        new_password, new_password2 = request.form['new_password'], request.form['new_password2']

        if new_password != new_password2:
            return render_template("resetpassword.html", error="Passwords do not match!")

        elif new_password == new_password2:
            account_email = getEmailFromHash(hash)
            changePassword(account_email, new_password)
            removeHashEntry(hash)

            return redirect(url_for("login"))


@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == '__main__':
    app.run()