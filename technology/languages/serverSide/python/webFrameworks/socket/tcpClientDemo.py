import socket

HOST = '127.0.0.1'
PORT = 9527

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))
print(f'Connect {HOST}:{PORT} OK')
data = s.recv(1024)
print(f'Received: {data}')
s.close()