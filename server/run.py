from app import app,socketio
from app import security
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

import json
from base64 import b64encode, b64decode


broker_auth = {'username': "try", 'password':"try"}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe('zzz')
    client.subscribe("register")
    client.subscribe('pub_k')
    security.gen_keys()
    print('claves generadas')
    


def on_message(client, userdata, msg):
    if msg.topic == 'pub_k':
        print('clave publica recibida del cliente')
        print('enviando clave publica al cliente...')
        #publish.single("pub_k_s", pub_key, hostname="broker.shiftr.io", auth=broker_auth)
        client.publish('pub_k_s',security.get_pub_key())
        print('clave publica enviada al cliente')
        print('creando clave compartida')
        security.set_derivated_key(msg.payload)
        print('Clave compartida creada')
    elif msg.topic == 'register':
        print('recibiendo mensaje de prueba cifrado')
        print(msg.payload.decode())
        print(type(msg.payload))
        print('descifrando mensaje...')
        c = client
        m = security.decrypt_msg(msg.payload)
        print(m)
        print('jejeje')
    else:
        m = 'hola caracola'
        socketio.emit('message',m)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("try","try")

client.connect("broker.shiftr.io", 1883, 60)


if __name__ == '__main__':
    client.loop_start()
    client.subscribe('zzz-adios')
    socketio.run(app,port=5000)


