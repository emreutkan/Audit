from enumeration.nmap import getch
from terminal_management.tman import popen_command_new_terminal
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define color variables for better readability
HEADER_COLOR = Fore.MAGENTA
OPTION_COLOR = Fore.CYAN
ERROR_COLOR = Fore.RED

# Define the section lists

def main_menu():
    print(f"""{HEADER_COLOR}
    Main Menu
    {OPTION_COLOR}
    0. Exit
    1. Enumeration
    2. Listener
    3. Shells and Payloads
    {Style.RESET_ALL}""")

def enumeration_menu():
    print(f"""{HEADER_COLOR}
    Enumeration
    {OPTION_COLOR}
    0. Return to Main Menu
    1. Custom Nmap
    2. Nmap
    {Style.RESET_ALL}""")

def listener_menu():
    print(f"""{HEADER_COLOR}
    Listener
    {OPTION_COLOR}
    0. Return to Main Menu
    1. Spawn Python TCP Listener
    2. Spawn Netcat Listener
    {Style.RESET_ALL}""")

def shells_payloads_menu():
    print(f"""{HEADER_COLOR}
    Shells and Payloads
    {OPTION_COLOR}
    0. Return to Main Menu
    {Style.RESET_ALL}""")

# Navigation management function
def navigate_options(current_section):
    while True:
        current_section()
        print('> ', end='', flush=True)
        choice = getch().upper()

        if current_section == main_menu:
            if choice == '0':
                exit()
            elif choice == '1':
                return enumeration_menu
            elif choice == '2':
                return listener_menu
            elif choice == '3':
                return shells_payloads_menu
            else:
                print(f"{ERROR_COLOR}Invalid choice, please try again.")
        elif current_section == enumeration_menu:
            if choice == '0':
                return main_menu
            elif choice == '1':
                popen_command_new_terminal('sudo python3 enumeration/custom_nmap.py')
            elif choice == '2':
                popen_command_new_terminal('sudo python3 enumeration/nmap.py')
            else:
                print(f"{ERROR_COLOR}Invalid choice, please try again.")
        elif current_section == listener_menu:
            if choice == '0':
                return main_menu
            elif choice == '1':
                popen_command_new_terminal('sudo python3 listener/pythonListener.py')
            elif choice == '2':
                popen_command_new_terminal('sudo python3 listener/netcatListener.py')
            else:
                print(f"{ERROR_COLOR}Invalid choice, please try again.")
        elif current_section == shells_payloads_menu:
            if choice == '0':
                return main_menu
            else:
                print(f"{ERROR_COLOR}Invalid choice, please try again.")

# Main function
def main():
    current_section = main_menu
    while True:
        current_section = navigate_options(current_section)

if __name__ == "__main__":
    main()
