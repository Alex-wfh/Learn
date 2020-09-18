import socket

HOST = '127.0.0.1'
PORT = 9527

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = 'Hello UDP!'
s.sendto(data.encode('utf8'), (HOST, PORT))
print(f'Send: {data} to {HOST}:{PORT}')
s.close()