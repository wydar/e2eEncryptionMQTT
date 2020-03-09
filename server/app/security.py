import base64
import random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
import os
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import load_pem_parameters
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESCCM
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


pub_key = '' 
priv_key = ''
derivated_key = ''
nonce = os.urandom(13)
aad = b"authenticated but unencrypted data"

def gen_keys():
    parameters = dh.generate_parameters(generator=2, key_size=512, backend=default_backend())

    p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
    g = 2

    params_numbers = dh.DHParameterNumbers(p,g)
    parameters = params_numbers.parameters(default_backend())

    # Generate a private key for use in the exchange.
    global priv_key
    priv_key = parameters.generate_private_key()
    global pub_key
    pub_key = priv_key.public_key()

def get_pub_key():
    return pub_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)


def set_derivated_key(response):
    client_pub_key = serialization.load_pem_public_key(data=response, backend = default_backend())
    print('---clave publica del cliente cargada')
    print(client_pub_key)
    shared_key = priv_key.exchange(client_pub_key)
    print('---clave compartida creada')
    print(shared_key)
    global derivated_key
    print('---creando clave derivada...')
    #derivated_key = HKDF(algorithm=hashes.SHA256(), length=32, salt='E2Eencrpytion', info=b'handshake data', backend=default_backend()).derive(shared_key)
    derivated_key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b'jeje', iterations=100000, backend=default_backend()).derive(shared_key)
    print('---clave derivada creada')
    print(derivated_key)
    

def AES_autenticated_encrypt(data):
    print('--creo el objeto AES')
    aesccm = AESCCM(derivated_key)
    print('--cifrando..')
    return aesccm.encrypt(nonce, data, aad)

def AES_autenticated_decrypt(ct):
    print('--creo el objeto AES')
    aesccm = AESCCM(derivated_key)
    print('--descifrando..')
    return aesccm.decrypt(nonce, ct, aad)
    
def Fernet_encrypt(data):
    print(data)
    print('--creando el objeto fernet')
    fernet = Fernet(base64.urlsafe_b64encode(derivated_key))
    print('--cifrando..')
    return fernet.encrypt(data)

def Fernet_decrypt(ct):
    print('--creando el objeto fernet')
    fernet = Fernet(base64.urlsafe_b64encode(derivated_key))
    print('--descifrando..')
    print(ct)
    return fernet.decrypt(ct)
