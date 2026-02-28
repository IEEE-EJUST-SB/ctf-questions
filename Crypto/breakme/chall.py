from Crypto.Util.number import *
from Crypto.PublicKey import RSA

# Read flag from file
with open("flag.txt", "rb") as f:
    FLAG = f.read()

# Generate prime
p_factor = getPrime(2048)

# Construct p and q
p = p_factor * p_factor          # p_factor^2
q = pow(p_factor, 6)             # p_factor^6

# RSA parameters
e = 0x10001
N = p * q                        # p_factor^8

# Compute phi(N) for p^8 (since N = p_factor^8)
phi = pow(p_factor, 8) - pow(p_factor, 7)

# Encrypt
m = bytes_to_long(FLAG)
ciphertext = pow(m, e, N)

# Export public key
exported = RSA.construct((N, e)).publickey().exportKey()

with open("key.pem", 'wb') as f:
    f.write(exported)

with open('ciphertext.txt', 'w') as f:
    f.write(hex(ciphertext)[2:])

