from flask import Flask,render_template
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)



@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    #send(msg, broadcast = True)