import threading
import socket



with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8',80))
        host=s.getsockname()[0]
port=9999#change port
nicknames=[]
clients=[]
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen(5)

def broadcast(msg):
    for client in clients:
        client.send(msg.encode('ascii'))


def handle(client):
    while True:
        try:
            msg=client.recv(1024).decode('ascii')
            broadcast(msg)
        except:
            index=clients.index(client)
            clients.remove(client)
            msg=f'{nicknames[index]} has left'
            nicknames.remove(nicknames[index])
            client.close()


def rec():
    while True:
        client,addres=server.accept()
        clients.append(client)
        client.send("NICK".encode('ascii'))
        nick=client.recv(102).decode('ascii')
        nicknames.append(nick)
        msg=f'{nick} has joined'
        print(msg)
        broadcast(msg)

        t=threading.Thread(target=handle,args=(client,))
        t.start()


print(f'server listeing on {host} :{port}')
rec()
