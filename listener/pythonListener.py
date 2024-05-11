import socket, sys, time

def listen(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(1)
    print("Listening on port " + str(port))
    conn, addr = s.accept()
    print('Connection received from ',addr)
    while True:
        ans = conn.recv(1024).decode()
        sys.stdout.write(ans)
        command = input()

        command += "\n"
        conn.send(command.encode())
        time.sleep(1)

        sys.stdout.write("\033[A" + ans.split("\n")[-1])


def start_tcp_listener(host=None, port=None):
    if not host or not port:
        host = input("Enter the host: ")
        port = int(input("Enter the port: "))
    # Create a socket object using TCP/IP protocol
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Prevent 'socket.error: [Errno 98] Address already in use' upon restart
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the address and port
    server_socket.bind((host, port))

    # Start listening for incoming connections
    server_socket.listen()

    print(f"Listening as {host}:{port} ...")

    # Accept a connection
    client_socket, client_address = server_socket.accept()
    print(f"{client_address[0]}:{client_address[1]} Connected!")

    try:
        # Keep the server running
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break

            client_socket.sendall(data)

    except KeyboardInterrupt:
        # Close the connection if Ctrl+C (interrupt) is received
        print("\nServer is shutting down.")
    finally:
        # Clean up the connection and close the server
        client_socket.close()
        server_socket.close()
        print("Server closed.")

if __name__ == '__main__':
    start_tcp_listener()