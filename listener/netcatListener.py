
import sys
import os
import subprocess
def nc():
    # list all network interface IPs
    command = 'ip -4 a | grep inet'
    subprocess.run(command, shell=True, text=True)

    ipaddress = input("\nIP address: ")
    port = input("Port: ")
    if 1 <= int(port) <= 65535:
        command = f'sudo nc -lnv {ipaddress} {port}'
        subprocess.run(command, shell=True, text=True)
    else:
        print("Invalid port number")

if __name__ == '__main__':
    nc()