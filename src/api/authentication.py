import pyrebase

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

email = 'test@gmail.com'
password = '123456'

user = auth.create_user_with_email_and_password(email, password)
print(user)
