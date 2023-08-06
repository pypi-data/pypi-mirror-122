# coding:utf-8
import socket
import os
import select
import termios
import threading
import tty
import atexit
import fcntl
import struct
import sys
import time
import termios
from pkt_common import get_payload2, gen_pkt2
import random

g_old_settings = None
g_is_exit = 0
g_tk = str(random.randrange(100000, 999999, 1))


def tty_to_raw():
    fd = sys.stdin.fileno()
    tty.setraw(fd)

def tty_setting_read():
    global g_old_settings
    fd = sys.stdin.fileno()
    g_old_settings = termios.tcgetattr(fd)


@atexit.register
def tty_restore():
    global g_old_settings
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSADRAIN, g_old_settings)


def read_local_and_send_to_remote(client):
    global g_is_exit
    try:
        fd = sys.stdin.fileno()
        while 1:
            # command = input()
            command = os.read(fd, 32)
            # for icmd in command:
            client.send(gen_pkt2(command, g_tk))

    except Exception as e:
        print('[-] Caught exception: ' + str(e))
        try:
            client.close()
        except:
            pass
        print('exit:read_local_and_send_to_remote-1')
        sys.exit(1)


def recv_remote_and_display_to_local(client):
    global g_is_exit
    while True:
        if g_is_exit:
            print('exit: recv_remote_and_display_to_local')
            sys.exit(0)
        try:
            reta = select.select([client.fileno()], [], [client.fileno()], 0.5)
            if reta[0]:
                output = os.read(client.fileno(), 8192)
                output = get_payload2(output, g_tk)
                if len(output)>0:
                    os.write(sys.stdout.fileno(), output)
                    sys.stdout.flush()
            elif reta[2]:
                print('exit: recv_remote_and_display_to_local-2')
                sys.exit(0)

        except Exception as e:
            print(e)
            print('exit: recv_remote_and_display_to_local-e')
            sys.exit(0)


def server_one(server_port=12345):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', server_port))
        sock.listen(100)
        print('[+] Listening:', server_port)
        client, addr = sock.accept()
    except Exception as e:
        print('[-] Listen/Bind/Accept failed: ' + str(e))
        sys.exit(1)
    print('[+] Got a connection!')
    tty_setting_read()
    tty_to_raw()

    # recv remote and display
    t = threading.Thread(target=recv_remote_and_display_to_local, args=(client,))
    t.start()
    # read input and send
    read_local_and_send_to_remote(client)


if __name__ == '__main__':
    server_port = 12345
    if len(sys.argv) > 1:
        server_port = int(sys.argv[1])
    server_one(server_port)
