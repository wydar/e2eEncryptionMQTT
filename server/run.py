from app import app,socketio
from app import security
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("register")
    client.subscribe('pub_k')
    security.gen_keys()
    print('claves generadas')


def on_message(client, userdata, msg):
    if msg.topic == 'pub_k':
        print('clave publica recibida del servidor\nenviando clave publica al cliente')
        client.publish('pub_k_s',security.get_pub_key())
        print('clave publica enviada al cliente\ncreando clave compartida')
        security.set_derivated_key(msg.payload)
        print('Clave compartida creada')
    elif msg.topic == 'register':
        print('recibiendo mensaje de prueba cifrado')
        print(msg.payload)
        print('mensaje descifrado')
        #print(security.Fernet_decrypt(msg.payload))
        print(security.AES_autenticated_decrypt(msg.payload))
        print('jeje')
    #print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("try","try")

client.connect("broker.shiftr.io", 1883, 60)


if __name__ == '__main__':
    client.loop_start()
    client.subscribe('zzz-adios')
    socketio.run(app,port=5000)


