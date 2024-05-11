import os
import sys
import tty
import termios


def getch():
    """Gets a single character from standard input, does not echo to the screen."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def validate_ip(target):
    """
    Check if the target IP address is valid

    :param target: target IP address
    """
    parts = target.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not 0 <= int(part) <= 255:
            return False
    return True

def validate_port(port):
    """
    Check if the port or port range is valid
    """
    try:
        if 1 <= int(port) <= 65535:
            return True
    except ValueError:
        if (0 <= int(port.split("-")[0]) <= 65535
                and 0 <= int(port.split("-")[1]) <= 65535
                and int(port.split("-")[0]) < int(port.split("-")[1])):
            return True
    return False


def validate_singe_port():
    # Check if the port is valid (not a range)
    while True:
        port = input("Enter the listener port: ")
        if validate_port(port):
            return port
        else:
            print("Invalid port number")


def validate_path():
    while True:
        path = input("Path: ")
        if path == "":
            path = os.getcwd()
            return path
        normalized_path = os.path.normpath(path)
        if os.path.exists(normalized_path):
            return normalized_path
        else:
            # check for wsl (Windows path interpretation on Linux) e.g., C:\Users\s\Documents\IntroToReact to /mnt/c/Users/s/Documents/IntroToReact
            if os.path.exists('/mnt/c'):
                wsl_path = '/mnt/c/' + normalized_path.replace('\\', '/').replace('C:', '').replace('D:', '').replace('E:', '').replace('F:', '').replace('G:', '').replace('H:', '').replace('I:', '').replace('J:', '').replace('K:', '').replace('L:', '').replace('M:', '').replace('N:', '').replace('O:', '').replace('P:', '').replace('Q:', '').replace('R:', '').replace('S:', '').replace('T:', '').replace('U:', '').replace('V:', '').replace('W:', '').replace('X:', '').replace('Y:', '').replace('Z:', '')
                if os.path.exists(wsl_path):
                    return wsl_path
                else:
                    print(f"Path provided: {path}")
                    print(f"Exists: {os.path.exists(normalized_path)}")
                    print(f"Normalized path: {normalized_path}")
                    print("Invalid path")
                    return False

def validate_file(file_path):
    while True:
        normalized_path = os.path.normpath(file_path)
        if os.path.exists(file_path):
            return file_path
        else:
            # check for wsl (Windows path interpretation on Linux) e.g., C:\Users\s\Documents\IntroToReact to /mnt/c/Users/s/Documents/IntroToReact
            # if windows
            if os.path.exists('/mnt/c'):
                wsl_path = '/mnt/c/' + normalized_path.replace('\\', '/').replace('C:', '')
                if os.path.exists(wsl_path):
                    return wsl_path
                else:
                    print(f"Path provided: {file_path}")
                    print(f"Exists: {os.path.exists(normalized_path)}")
                    print(f"Normalized path: {normalized_path}")
                    print(f'wsl path: {wsl_path}')
                    print("Invalid path")
                    return False
