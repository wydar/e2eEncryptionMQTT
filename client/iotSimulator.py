from parser import parse_command
import security

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe

args = parse_command()

print('##############################')
print('--- IoT Device Simulator ----')
print('--- Input\t::\t' + str(args.input))
print('--- Output\t::\t' + str(args.output))
print('##############################')
print('\nTry -h --help for more information\n')

broker_auth = {'username': "try", 'password':"try"}

global pub_key


def on_connect(client, userdata, flags, rc):
    #client.subscribe('register')
    #client.subscribe('pub_k')
    print('antes de generar las claves')
    pub_key = security.get_pub_key()
    print('claves generadas\nantes de recibir clave publica del serivdor')
    print(pub_key)
    publish.single("pub_k", pub_key, hostname="broker.shiftr.io", auth=broker_auth)
    print('clave publica enviada al servidor\n esperando la clave del serivdor') 
    response_server_pub_key = subscribe.simple("pub_k_s", hostname="broker.shiftr.io", auth=broker_auth)
    print('clave publica del servidor recibida\ncreando clave compartida')
    security.set_derivated_key(response_server_pub_key.payload)
    print('handshake terminado')
    print('enviando mensaje de prueba encriptado: cuando el grajo vuela bajo hace un frio del carajo')
    #ct = security.Fernet_encrypt(b"cuando el grajo vuela bajo hace un frio del carajo")
    ct = security.AES_autenticated_encrypt(b"cuando el grajo vuela bajo hace un frio del carajo")
    publish.single("register", ct, hostname="broker.shiftr.io", auth=broker_auth)
    print('mensaje de prueba enviado')
    print(ct)
    print('descifrnado en local')
    #print(security.Fernet_decrypt(ct))
    print(security.AES_autenticated_decrypt(ct))



def on_message(client, userdata, msg):
    pass



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("try","try")

client.connect("broker.shiftr.io", 1883, 60)

client.loop_forever()


