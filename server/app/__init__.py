from flask import Flask,render_template
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("hola")


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("try","try")

client.connect("broker.shiftr.io", 1883, 60)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    #send(msg, broadcast = True)