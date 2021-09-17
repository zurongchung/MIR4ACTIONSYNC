
from socket import *
from pynput import mouse, keyboard

HOST = '192.168.0.106'
PORT = 65432
back_log = 5
buffer_size = 1024
UID = 'host'

tcp_client = socket(AF_INET, SOCK_STREAM)
tcp_client.connect((HOST, PORT))

def on_click(x, y, button, pressed):
    status = 'pressed' if pressed else 'released'
    tcp_client.sendall(bytes('{0}-{1}:{2}:{3}'.format(UID, 'mouse', [x, y, str(button)], status), 'utf-8'))

# helper function
#NOTE: can not use numpad
def send_kb_event(tag, key, status):
    try:
        tcp_client.sendall(bytes('{0}-{1}:{2}:{3}'.format(UID, tag, str(key.char), status), 'utf-8'))
    except AttributeError:
        tcp_client.sendall(bytes('{0}-{1}:{2}:{3}'.format(UID, tag, str(key), status), 'utf-8'))

def on_press(key):
    send_kb_event('kb', key, 'pressed')

def on_release(key):
    send_kb_event('kb', key, 'released')

# register mouse listener
listener = mouse.Listener(on_click=on_click)
listener.start()

# register keyboard listener
kbListener = keyboard.Listener(on_press=on_press, on_release=on_release)
kbListener.start()

while True:
    cmd = input('>>>:').strip()
    if cmd == '': continue
    if cmd == 'quit':
        listener.stop()
        kbListener.stop()
        break