import socket

ip = "localhost"
port = 8888

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((ip, port))
while 1:
    data = connection.recv(8192)
    data = data.decode("utf-8")
    print(data)
    if len(data.split())<1:
        pass
    elif data.split()[0] == "CONNECT" or data.split()[0] == "YOUR":
        connection.sendall(input().encode())