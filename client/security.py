import secrets
import base64
import random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.serialization import ParameterFormat
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.asymmetric.dh import DHParameterNumbers
from cryptography.hazmat.primitives.serialization import load_pem_parameters


def handShake():
    parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
    # Generate a private key for use in the exchange.
    server_private_key = parameters.generate_private_key()
    # In a real handshake the peer is a remote client. For this
    # example we'll generate another local private key though. Note that in
    # a DH handshake both peers must agree on a common set of parameters.
    peer_private_key = parameters.generate_private_key()
    shared_key = server_private_key.exchange(peer_private_key.public_key())
    # Perform key derivation.
    derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'handshake data', backend=default_backend()).derive(shared_key)
    # And now we can demonstrate that the handshake performed in the
    # opposite direction gives the same final value
    same_shared_key = peer_private_key.exchange(server_private_key.public_key())
    same_derived_key = HKDF( algorithm=hashes.SHA256(), length=32, salt=None, info=b'handshake data', backend=default_backend()).derive(same_shared_key)
    print(derived_key == same_derived_key)