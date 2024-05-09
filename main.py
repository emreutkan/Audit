from enumeration.nmap import nmap
from terminal_management.tman import popen_command_new_terminal,clear_screen,test
import keyboard
from pynput.keyboard import Key, Controller
def main():
    while True:
        clear_screen()
        options = [
           """
           1. Nmap
           2. Custom Nmap
           3.
           """
        ]
        print(options[0])
        choice = input("Enter your choice: ")
        if choice == '1':
           nmap = popen_command_new_terminal('sudo python3 enumeration/custom_nmap.py')
        elif choice == '2':
           custom_nmap = popen_command_new_terminal('sudo python3 enumeration/custom_nmap.py')
        elif choice == '3':
            test = popen_command_new_terminal('sudo python3 enumeration/custom_nmap.py')

        keyboard.press(Key.enter)
        keyboard.release(Key.enter)



if __name__ == "__main__":
    main()