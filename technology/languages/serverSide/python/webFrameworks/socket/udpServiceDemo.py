import socket

HOST = '0.0.0.0'
PORT = 9527

# SOCK_DGRAM: udp
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

while True:
    data, addr = s.recvfrom(1024)
    print(f'Received {data} from {addr}')
    break

s.close()