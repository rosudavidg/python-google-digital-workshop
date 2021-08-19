from exceptions import ServerException
from get_docker_secret import get_docker_secret
import jwt
import hashlib
import binascii
import os
import secrets

ACTIVATION_TOKEN_LENGTH = 64


def extract_fields(request, *fields):
    body = request.get_json()

    if body is None:
        raise ServerException(f'Body is missing', 400)

    data = []

    for field in fields:
        if field not in body:
            raise ServerException(f'Field \'{field}\' is missing', 400)

        data.append(body[field])

    return data


def hash_password(password):
    '''
    Hash a password for storing
    '''

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)

    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    '''
    Verify a stored password against one provided by user
    '''

    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')

    return pwdhash == stored_password


def jwt_encode(data):
    '''
    Encode data into jwt
    '''

    return jwt.encode(data, get_docker_secret(os.environ['AUTH_JWT_KEY']), algorithm='HS256')


def jwt_decode(token):
    '''
    Decode data from jwt
    '''

    return jwt.decode(token, get_docker_secret(os.environ['AUTH_JWT_KEY']), algorithms=['HS256'])


def generate_activation_token():
    return secrets.token_urlsafe(ACTIVATION_TOKEN_LENGTH)[:ACTIVATION_TOKEN_LENGTH]
