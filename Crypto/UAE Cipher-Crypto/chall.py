import os
from base64 import b64encode
flag="DEVSTORM{!4e4bD@AmVtTCUVM}".encode()
flag = b64encode(flag)
enc = b""
for i in range(len(flag)):
	enc += bytes([flag[i] ^ flag[(i+1) %len(flag)]])
enc = b64encode(enc)
print(enc)
