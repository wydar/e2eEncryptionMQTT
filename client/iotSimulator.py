from parser import parse_command
import security

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe

import json
from base64 import b64encode, b64decode
import uuid

args = parse_command()

print('##############################')
print('--- IoT Device Simulator ----')
print('--- Input\t::\t' + str(args.input))
print('--- Output\t::\t' + str(args.output))
print('##############################')
print('\nTry -h --help for more information\n')

broker_auth = {'username': "try", 'password':"try"}
id = str(uuid.uuid4())

global pub_key
encrypt_alg = 'AES-CCM'

def simulate_send_msg():
    #Simulamos el envio de un mensaje

    print('enviando mensaje de prueba encriptado: cuando el grajo vuela bajo hace un frio del carajo')

    if encrypt_alg == 'fernet':
        ct = security.Fernet_encrypt(b"cuando el grajo vuela bajo hace un frio del carajo")
        print('mensaje cifrado')
        print('preparando menjase para enviar...')
        msg = security.prepare_msg(ct = ct, encrypt_alg = encrypt_alg, nonce = None)
        print('mensaje preparado!!')
        print('enviando...')
        print(type(msg))
        publish.single("register", msg, hostname="broker.shiftr.io", auth=broker_auth)
        print('enviado!!!')
        print(security.Fernet_decrypt(ct))
    elif encrypt_alg == 'AES-CCM':
        st = "cuando el grajo vuela bajo hace un frio del carajo"
        ct, nonce = security.AES_autenticated_encrypt(st.encode())
        print('preparando menjase para enviar...')
        msg = security.prepare_msg(ct = ct, encrypt_alg = encrypt_alg, nonce = nonce)
        print('mensaje preparado!!')
        print('enviando...')
        publish.single("register", msg, hostname="broker.shiftr.io", auth=broker_auth, client_id=id)
        print('mensaje de prueba enviado')
        print(ct)
        print('descifrnado en local')
        print(security.AES_autenticated_decrypt(ct))
    else:
        print('pepe')
        p = b64encode('pepe'.encode('ascii'))
        print(p)
        print(b64decode(p).decode())
        print('fin')


def on_connect(client, userdata, flags, rc):
    print(client)
    print('antes de generar las claves')
    pub_key = security.get_pub_key()
    print('claves generadas')
    print('enviando clave publica al serivdor...')
    publish.single("pub_k", pub_key, hostname="broker.shiftr.io", auth=broker_auth, client_id=id)
    print('clave publica enviada al servidor')
    print('esperando la clave del serivdor...') 
    response_server_pub_key = subscribe.simple("pub_k_s", hostname="broker.shiftr.io", auth=broker_auth)
    print('clave publica del servidor recibida')
    print('creando clave compartida...')
    security.set_derivated_key(response_server_pub_key.payload)
    print('clave compartida creada!!')
    simulate_send_msg()




def on_message(client, userdata, msg):
    pass


client = mqtt.Client(client_id=id)
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("try","try")

client.connect("broker.shiftr.io", 1883, 60)

client.loop_forever()


