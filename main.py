from flask import Flask, request, redirect, render_template
import cgi
import os

app = Flask(__name__)
app.config['DEBUG'] = True


form = """
<!doctype html>
<html>
    <body>
        <form action="/hello" method="post">
            <label for="first-name">First Name:</label>
            <input id="first-name" type="text" name="first_name" />
            <input type="submit" />
        </form>
    </body>
</html>
"""


@app.route("/")
def index():
    return form


@app.route("/hello", methods=['POST'])
def hello():
    first_name = request.form['first_name']
    return '<h1>Hello, ' + first_name + '</h1>'


time_form = """
    <style>
        .error {{ color: red; }}
    </style>
    <h1>Validate Time</h1>
    <form method='POST'>
        <label>Hours (24-hour format)
            <input name="hours" type="text" value='{hours}' />
        </label>
        <p class="error">{hours_error}</p>
        <label>Minutes
            <input name="minutes" type="text" value='{minutes}' />
        </label>
        <p class="error">{minutes_error}</p>
        <input type="submit" value="Validate" />
    </form>
    """
#################################################
@app.route('/validate-time')
def display_time_form():
    return time_form.format(hours='', hours_error='',
                            minutes='', minutes_error='')

user_form = """
    <style>
        .error {{ color: red; }}
    </style>
    <h1>User Signup</h1>

    <form method='POST'>

    <div>
        <label>Username:
            <input name="username" type="text" value='{username}' />
        </label>
        <span class="error">{username_error}</span>
    </div>

    <div>
        <label>Password:
            <input name="password" type="password" value='{password}' />
        </label>
        <span class="error">{password_error}</span>
    </div>

    <div>
        <label>Verify Password:
            <input name="verify_password" type="password" value='{verify_password}' />
        </label>
        <span class="error">{verify_password_error}</span>
    </div>

    <div>
        <label>Email (optional):
            <input name="email" type="text" value='{email}' />
        </label>
        <span class="error">{email_error}</span>
    </div>

    <div>
        <input type="submit" value="Sign Up" />
    </div>
</form>
    """

@app.route('/validate-user')
def display_user_form():
    return user_form.format(username="", username_error="",
                            password="",password_error="",
                            verify_password="", verify_password_error="",
                            email="", email_error="")

@app.route('/validate-user', methods=['POST'])
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
        return user_form.format(username_error=username_error,
                         password_error=password_error,
                         verify_password_error=verify_password_error,
                         email_error=email_error,
                         username=username, password="", 
                         verify_password="", email=email)

@app.route("/welcome")
def welcome():
    display_name = request.args.get("display_name")
    return "<h1>Welcome, {0}!</h1>".format(display_name)




    





########################################################
def is_integer(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


@app.route('/validate-time', methods=['POST'])
def validate_time():

    hours = request.form['hours']
    minutes = request.form['minutes']

    hours_error = ''
    minutes_error = ''

    if not is_integer(hours):
        hours_error = 'Not a valid integer'
        hours = ''
    else:
        hours = int(hours)
        if hours > 23 or hours < 0:
            hours_error = 'Hour value out of range (0-23)'
            hours = ''

    if not is_integer(minutes):
        minutes_error = 'Not a valid integer'
        minutes = ''
    else:
        minutes = int(minutes)
        if minutes > 59 or minutes < 0:
            minutes_error = 'Minutes value out of range (0-59)'
            minutes = ''

    if not minutes_error and not hours_error:
        return "Success!"
    else:
        return time_form.format(hours_error=hours_error,
                                minutes_error=minutes_error,
                                hours=hours,
                                minutes=minutes)


app.run()
