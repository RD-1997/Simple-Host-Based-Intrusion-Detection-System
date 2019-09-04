import socket
import sys
import filemanager
import yaml

# imports config file for security measures
with open("config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

# symbolic name, meaning all available interfaces
HOST = cfg['socket']['host']
# port to communicate over
PORT = cfg['socket']['port']

# defining and creating socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

# bind socket to local host and port
try:
    s.bind((HOST, PORT))

except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print('Socket bind complete')

# start listening on socket up to 10 clients simultaneously
s.listen(cfg['socket']['maxcon'])
print('Socket now listening')

# keeps listening to the clients
while 1:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()

    # receives data up to these bytes. The max byte is set to 512 because it will only receive minimal data such as an md5 hash (which is 128bits)
    # and a filename which is also not much. a max byte of 512 is set because it could receive multiple inputs at once from several clients.
    data = conn.recv(cfg['socket']['maxbyte'])

    # decodes the data that is being send into UTF-8 format so it becomes usable
    receivedData = data.decode(cfg['socket']['decode'])

    # splits the data into two different variables
    scanner, filename, hash = receivedData.split(';')

    print('')
    print('Connected with ' + scanner + " from address: " + addr[0] + ':' + str(addr[1]))
    print('File received from scanner: ' + scanner)
    # sends the variables to validate the file
    filemanager.manageFiles(hash, filename, scanner)

s.close()
