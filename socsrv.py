import queue
import socketserver
import socket
from queue import Queue

HOST_NAME = socket.gethostname()
HOST = socket.gethostbyname(HOST_NAME)
PORT = 65432
buffer_size = 1024
client_list = []
# default client ip
c_ip = '192.168.0.103'
c_addr = ()
c_ready = False

# storage for data received from host
host_msg_list = []
host_msg_queue = Queue(maxsize=0)
# data not avaliable
STB = '0X10'
RQST_KEY = '0x12'

print('server ip is : ' + HOST)

class TCPsvr(socketserver.BaseRequestHandler):

    def handle(self):
        global c_ip, c_addr, c_ready

        client_list.append(self)
        print('{} clients connected.'.format(len(client_list)))

        # identify who is connecting
        if (self.client_address[0] == HOST):
            print('host connected.')
        else:
            if self.client_address[0] != c_ip:
                c_ip = self.client_address[0]
            c_addr = self.client_address
            c_ready = True
            print('addr is {}'.format(c_addr))
            print('client connected.')
        

        # print('conn is: %s, addr is : %s' % (conn, addr))

        while True:
            try:
                # get message from host or clients
                data = self.request.recv(buffer_size).decode('utf-8').split('-')
                if not data: break
                print('received data: %s' % data)

                # separating sender id and message
                try:
                    _uid = data[0]
                    print('uid is : ' + _uid)
                    _msg_body = data[1]
                    print('msg body is : ' + _msg_body)

                    # when client is connected then save data sent from host
                    if c_ready:
                        # print('client is ready')
                        # saving data sent from host
                        if _uid == 'host':
                            try:
                                # host_msg_list.append(_msg_body)
                                host_msg_queue.put(_msg_body)
                            except queue.Full as e:
                                print('err: ' + e)
                        if _uid == 'client':
                            # this client ask for data
                            # response when data queue has data
                            if _msg_body == RQST_KEY and host_msg_queue.qsize() > 0:
                                # sent data to client when client ask for
                                print('sending data to client.' + str(c_addr))
                                self.request.sendall(bytes(host_msg_queue.get(), 'utf-8'))
                            else:
                                print('no data avaliable.')
                                self.request.sendall(bytes(STB, 'utf-8'))
                except IndexError as e:
                    print(e)
                    break
                # only send data to client
                # if c_addr:
                    # print('sending data to client.' + str(c_addr))
                    # self.request.sendto(bytes(data, 'utf-8'), c_addr)
            except Exception as e:
                print(e)
                break

if __name__ == '__main__':
    with socketserver.ThreadingTCPServer((HOST, PORT), TCPsvr) as s:
        s.serve_forever(poll_interval=0.5)