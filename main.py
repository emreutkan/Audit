from enumeration.nmap import nmap
from terminal_management.tman import popen_command_new_terminal

def main():
   while True:
       options = [
           """
           1. Nmap
           2. Custom Nmap
           """
       ]
       print(options[0])
       choice = input("Enter your choice: ")
       if choice == '1':
           nmap = popen_command_new_terminal('sudo python3 enumeration/custom_nmap.py')
       elif choice == '2':
           custom_nmap = popen_command_new_terminal('sudo python3 enumeration/custom_nmap.py')

       else:
           print("Invalid choice")

if __name__ == "__main__":
    main()