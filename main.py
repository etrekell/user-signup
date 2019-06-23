from flask import Flask, request, redirect, render_template
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def display_user_form():
    template = template = jinja_env.get_template('user_signup.html')
    return template.render(username="", username_error="",
                            password="",password_error="",
                            verify_password="", verify_password_error="",
                            email="", email_error="")

@app.route('/', methods=['POST'])
def validate_user():
    username = request.form["username"]
    password = request.form["password"]
    verify_password = request.form["verify_password"]
    email = request.form["email"]

    username_error = ""
    password_error = ""
    verify_password_error = ""
    email_error = ""

    username_space = False
    password_space = False
    email_space = False
    email_at = False
    email_dot =False

    for char in username:
        if char == " ":
            username_space = True

    for char in password:
        if char == " ":
            password_space = True

    for char in email:
        if char == " ":
            email_space = True

    for char in email:
        if char == "@":
            email_at = True

    for char in email:
        if char == ".":
            email_dot = True

    if username == "":
        username_error = "You must enter a username."
    elif len(username) < 3 or len(username) > 20 or username_space:
        username_error = "Username must be between 3 and 20 characters, and not contain any spaces."

    if password == "":
        password_error = "You must enter a password."
    elif len(password) < 3 or len(password) > 20 or password_space:
        password_error = "Password must be between 3 and 20 characters, and not contain any spaces."

    if verify_password == "":
        verify_password_error = "You must verify your password."

    if password != verify_password:
        verify_password_error = "Your password doesn't match."

    if email != "":
        if len(email) < 3 or len(email) > 20 or email_space or (not email_at) or (not email_dot):
            email_error = "Invalid email."

    if not username_error and not password_error and not verify_password_error and not email_error:
        display_name = username
        return redirect("/welcome?display_name={0}".format(display_name))
    else:
        template = template = jinja_env.get_template('user_signup.html')
        return template.render(title="User Signup",username_error=username_error,
                         password_error=password_error,
                         verify_password_error=verify_password_error,
                         email_error=email_error,
                         username=username, password="", 
                         verify_password="", email=email)

@app.route("/welcome")
def welcome():
    template = template = jinja_env.get_template('welcome.html')
    display_name = request.args.get("display_name")
    return template.render(title="Welcome", display_name=display_name)

app.run()