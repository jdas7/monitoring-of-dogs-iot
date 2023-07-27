import pyrebase
from flask import Flask, request, render_template, redirect, session, jsonify
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

config = {
    'apiKey': "apiKey",
    'authDomain': "authDomain",
    'projectId': "projectId",
    'storageBucket': "storageBucket",
    'messagingSenderId': "messagingSenderId",
    'appId': "appId",
    'measurementId': "G-measurementId",
    'databaseURL': ''
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app.secret_key = 'secret'

# Ruta de la credencial JSON que descargaste al configurar Firebase
cred = credentials.Certificate("/code/src/api/cyberdog-cfc41-firebase-adminsdk-wvgs3-e763d8520a.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'databaseURL'
})


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


@app.route('/mq135', methods=['GET'])
def mq_135():
    ref = db.reference('cyberdog')
    data = ref.child('sensor_mq_135').get()
    return jsonify(data)


@app.route('/dht22', methods=['GET'])
def dht11():
    ref = db.reference('cyberdog')
    data = ref.child('sensor_dht22').get()
    return jsonify(data)


@app.route('/mpu6050', methods=['GET'])
def mpu6050():
    ref = db.reference('cyberdog')
    data = ref.child('sensor_mpu_6050').get()
    return jsonify(data)


@app.route('/xd58c', methods=['GET'])
def xd_58c():
    ref = db.reference('cyberdog')
    data = ref.child('sensor_xd_58c').get()
    return jsonify(data)


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5001')
