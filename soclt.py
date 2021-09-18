from socket import *
import threading
import time
import sys
from queue import Queue
# from pynput import mouse, keyboard

SERVER_IP = '192.168.0.106'
PORT = 65432
back_log = 5
buffer_size = 1024
UID = 'client'
# the key for request data from server
RQST_KEY = '0x12'
STB = '0X10'
data_queue = Queue(maxsize=0)


# extract action from data got in queue
# then call appropriate mouse or keyboard function
def action(data):
    tag, a_info, status = data.split(':')
    # a_info: key.char
    if tag == 'kb':
        kb_action([a_info, status])
    # a_info: [x, y, button, status]
    if tag == 'mouse':
        mouse_action(a_info.append(status))

# perform mouse action
def mouse_action(action: list):
    print(action)

# perform keyboard action
def kb_action(action: list):
    print(action)

# run on another thread
# getting data from queue
# and perform action according to data
def worker(t_name):
    msg = data_queue.get()
    # print('thread {} working on {}'.format(t_name, msg))
    action(msg)

if __name__ == '__main__':
    t = threading.Thread(target=worker, args=('worker'))
    t.start()
    # listener for the message sent by the server
    with socket(AF_INET, SOCK_STREAM) as tcp_client:
        tcp_client.connect((SERVER_IP, PORT))

        while True:
            time.sleep(0.3)
            # cmd = input('>>>:').strip()
            # if not cmd: continue
            # if cmd == 'quit':
            #     break

            # request new data from server in a time interval
            tcp_client.sendall(bytes('{0}-{1}'.format(UID, RQST_KEY), 'utf-8'))

            data = tcp_client.recv(buffer_size).decode('utf-8')
            print('data sent by server is: ' + data)
            if data == STB:
                print('stanby...')
                continue
            else:
                print('putting data into queue.')
                data_queue.put(data)
