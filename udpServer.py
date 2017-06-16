import random
from socket import *
import time

ipVersion = 'ipv4'

# which ip version to use
if ipVersion == 'ipv4':
    recieve_host = '800.0.0.1'
    remote_host = '100.0.0.1'
    # ipv4 socket
    serverSocket = socket(AF_INET, SOCK_DGRAM)
elif ipv4Version is 'ipv6':
    recieve_host = '80::1'
    remote_host = '90::1'
    # ipv6 socket
    serverSocket = socket(AF_INET6, SOCK_DGRAM)

recieve_port = 1024
remote_port = 12000
serverSocket.settimeout(1.0)
serverSocket.bind((recieve_host, recieve_port))


def send_message(message, wait=False):
    serverSocket.sendto(message, (remote_host, remote_port))
    return wait_for_response()

print 'now listening..'

start_time = time.time()
# wait for a ping and respond with one back
while True:
    # message received
    message, address = serverSocket.recvfrom(remote_port)
    end_time = time.time()
    print 'got message at ' + str(end_time)
    print 'Recieved: ' + message + '\n'
    print '+-+-+-+-+-+-+-+-+-+-+-+-+-+-+'
    serverSocket.sendto(message, address)
