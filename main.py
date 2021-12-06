from Crypto.PublicKey import ECC
import random
import hashlib

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

key = ECC.generate(curve='P-256')

message_hash = hashlib.sha256('Hello'.encode()).hexdigest()
q = int(key._curve.order)
G = key.pointQ
d = int(key.d)
B = d * G

def sign():
    k = random.randint(0, q)
    R = G * k
    r = int(R.x)
    s = ((int(message_hash, 16) + d * r) * modinv(k, q))
    return r, s

def verify():
    w = modinv(s, q)
    u1 = w * int(message_hash, 16) % q
    u2 = w * r % q
    P = u1 * G + u2 * B
    return P.x == r % q

r, s = sign()

print('r: {}'.format(r))
print('s: {}'.format(s))

print(verify())
