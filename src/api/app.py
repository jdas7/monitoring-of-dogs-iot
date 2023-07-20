import pyrebase
from flask import Flask, request, render_template, redirect, session

app = Flask(__name__)

config = {
    'apiKey': "apiKey",
    'authDomain': "authDomain",
    'projectId': "projectId",
    'storageBucket': "storageBucket",
    'messagingSenderId': "messagingSenderId",
    'appId': "appId",
    'measurementId': "measurementId",
    'databaseURL': ''
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app.secret_key = 'secret'


@app.route('/', methods=['POST', 'GET'])
def index():
    if 'user' in session:
        return render_template('menu.html')  # Redirigir a la página del menú

    error_message = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            return render_template('menu.html')  # Redirigir a la página del menú
        except:
            error_message = 'Failed to login'

    return render_template('home.html', error_message=error_message)


@app.route('/monitoreo')
def monitoring():
    return render_template('monitoring.html')


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5001')
