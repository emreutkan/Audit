from terminal_management.tman import popen_command_new_terminal

def nc():
    port = input("Enter the port number: ")
    if 1 <= int(port) <= 65535:
        popen_command_new_terminal(f'nc -lvnp {port}')
    else:
        print("Invalid port number")

if __name__ == '__main__':
    nc()