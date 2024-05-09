from enumeration.nmap import nmap
from terminal_management.tman import popen_command_new_terminal,clear_screen
def main():
    while True:
        ##clear_screen()
        options = [
           """
           Enumeration Options:
           1. Nmap
           2. Custom Nmap
           Bruteforce Options:
           3. Hydra
           """
        ]
        print(options[0])
        choice = input("Enter your choice: ")
        if choice == '1':
           nmap = popen_command_new_terminal('sudo python3 enumeration/custom_nmap.py')
        elif choice == '2':
           custom_nmap = popen_command_new_terminal('sudo python3 enumeration/custom_nmap.py')
        elif choice == '3':
              hydra = popen_command_new_terminal('hydra')










if __name__ == "__main__":
    main()