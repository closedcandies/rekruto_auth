from flask import render_template_string, request, redirect, url_for, Flask
import random

app = Flask(__name__)

current_sid = 1234
LOGIN = 'rekruto'
PASSWORD = '12345'

login_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        .login-container {
            margin-top: 100px;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            display: inline-block;
        }
        input {
            margin: 10px 0;
            padding: 10px;
            width: 80%;
        }
        button {
            padding: 10px;
            background-color: #5cb85c;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #4cae4c;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>{{message}}</h2>
        <form action="/login" method="POST">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>"""

html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Случайный код</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f4f4f4;
            font-family: Arial, sans-serif;
        }
        .container {
            text-align: center;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        }
        h1 {
            font-size: 2.5rem;
            color: #333;
        }
        p {
            font-size: 1.5rem;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Ваш случайный код</h1>
        <p>{{ code }}</p>
    </div>
</body>
</html>
'''

@app.route('/')
def generate_code():
    global current_sid
    session_code = int(request.args.get('sid', 'no_sid'))
    if session_code != current_sid:
        return redirect(url_for('login'))
    else:
        current_sid = random.randint(1000, 9999)
        code = random.randint(1000, 9999)
        return render_template_string(html_template, code=code)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = 'Войдите'
    if request.method == 'POST':
        login = request.form['username']
        pswd = request.form['password']
        if login == LOGIN and pswd == PASSWORD:
            global current_sid
            return redirect(url_for('generate_code', sid=current_sid))
        else:
            message = 'Упс. Кажется, данные неверны. Попробуй еще раз'
    return render_template_string(login_template, message=message)


if __name__ == '__main__':
    app.run(debug=True)
