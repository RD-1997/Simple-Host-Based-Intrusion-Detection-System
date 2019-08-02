import socket
import sys
import struct

HOST = ''  # Symbolic name, meaning all available interfaces
PORT = 12345  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

def decrypt(data):
    shift = 3
    space = []

    ciphertext = data.split()
    sentence = []

    for word in ciphertext:
        cipher_ords = [ord(x) for x in word]
        plaintext_ords = [o - shift for o in cipher_ords]
        plaintext_chars = [chr(i) for i in plaintext_ords]
        plaintext = ''.join(plaintext_chars)
        sentence.append(plaintext)

    sentence = ' '.join(sentence)
    print('Decryption Successful\n')

    return sentence

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))

except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print('Socket bind complete')

# Start listening on socket
s.listen(10)
print('Socket now listening')

# now keep talking with the client
while 1:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    # print('Connected with ' + addr[0] + ':' + str(addr[1]))

    data = conn.recv(2048)
    newdata = data.decode('utf-8')
    # decrypted = decrypt(newdata)
    # print(decrypted)
    print(newdata)


s.close()
