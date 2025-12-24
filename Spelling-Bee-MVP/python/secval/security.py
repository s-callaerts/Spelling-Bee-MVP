import os
import hashlib
import hmac

algorithm = 'sha256'
iterations = 260000
klen = 32

def hash_password(password):
    bit_password = password.encode('utf-8')
    salt = os.urandom(16)

    stored_password = hashlib.pbkdf2_hmac(algorithm, bit_password, salt, iterations, klen).hex()
    stored_salt = salt.hex()

    return f'{stored_password}${stored_salt}${algorithm}${iterations}${klen}'

def validate_login_password(input_password, stored_password):
    #stored_password will have to be retrieved from db

    test_password, stored_salt, stored_algorithm, stored_iterations, stored_klen = stored_password.split('$')
    bit_salt = bytes.fromhex(stored_salt)
    login_password = hashlib.pbkdf2_hmac(stored_algorithm, input_password.encode('utf-8'), bit_salt, int(stored_iterations), int(stored_klen))

    return print(hmac.compare_digest(bytes.fromhex(test_password), login_password))