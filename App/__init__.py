from flask import Flask
from App.core.views import core


app =  Flask(__name__)

app.register_blueprint(core)

app.config['SECRET_KEY'] = 'mysecret'