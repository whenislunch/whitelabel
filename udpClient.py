import time
from socket import *

ipVersion = 'ipv4'

# which ip version to use
if ipVersion == 'ipv4':
    recieve_host = '100.0.0.1'
    remote_host = '80.0.0.1'
    # ipv4 socket
    serverSocket = socket(AF_INET, SOCK_DGRAM)
elif ipv4Version is 'ipv6':
    recieve_host = '10::1'
    remote_host = '80::1'
    # ipv6 socket
    serverSocket = socket(AF_INET6, SOCK_DGRAM)

recieve_port = 1024
remote_port = 12000
serverSocket.settimeout(1.0)
serverSocket.bind((recieve_host, recieve_port))


def send_message(message, wait=False):
    """
    Message to send when pinging
    """
    serverSocket.sendto(message, (remote_host, remote_port))
    if wait is False:
        return
    else:
        try:
            message, address = serverSocket.recvfrom(remote_port)
            return message
        except Exception:
            return


def run(routes, ipVersion):
    """
    Keep sending pings until one comes back and write the result to a file
    """
    start_time = time.time()
    received = False
    while received is False:
        # Create message with current sequence_number and time
        message = 'PING ' + str(time.time())
        # Recieve ping
        recieved = send_message(message, True)
        recieved_array = recieved.split(' ')
        recieved_type = recieved_array[0].upper()

        if recieved_type == 'PING':
            # time it took to get ping back
            time_taken = time.time() - start_time

            received = True
            print 'TOOK :', time_taken
            with open("/result/" + 'routes', "a") as log:
                # append taken time to file
                print 'TOOK :', time_taken
                log.write(str(time_taken) + '\n')
            serverSocket.close()
            return time_taken
