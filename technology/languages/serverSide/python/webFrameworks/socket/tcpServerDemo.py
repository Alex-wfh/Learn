import socket
import datetime

HOST = '0.0.0.0'
PORT = 9527

# AF_INET: IPv4, SOCK_STREAM: TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

while True:
    conn, addr = s.accept()
    print(f'Client {addr} connected')
    dt = datetime.datetime.now()
    msg = f'Current time is {dt}'
    conn.send(msg.encode('utf8'))
    print(f'send {msg}')
    conn.close()
    break

s.close()