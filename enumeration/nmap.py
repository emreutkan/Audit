import os
import sys
import tty
import termios
from colorama import Fore, Style
import subprocess

from terminal_management.tman import popen_command_new_terminal

TARGET_IP = os.popen('hostname -I').read().split()[0]

def validate_ip(target):
    """
    Check if the target IP address is valid

    :param target: target IP address
    """
    parts = target.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not 0 <= int(part) <= 255:
            return False
    return True
def select_target():
    """
    Prompt the user to select a target to scan

    :return: the target IP address
    """
    global TARGET_IP
    target = input("Enter the target IP address: ")
    if validate_ip(target):
        TARGET_IP = target
        return TARGET_IP
    else:
        print("Invalid IP address")
        select_target()

def getch():
    """Gets a single character from standard input, does not echo to the screen."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def run_nmap(command):
    command += f" {TARGET_IP}"
    print(f"Running command: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc

def nmap():
    """
    Comprehensive Scan for All Vulnerabilities on All Ports
    nmap -p- -sV -sC -T4 --script=vuln --open --min-rate 100 -v <target>

    -p-: Scans all 65535 ports.
    -sV: Enables version detection.
    -sC: Executes default scripts.
    -T4: Sets the timing template to "aggressive" (faster execution).
    --script=vuln: Uses scripts categorized as vulnerability checks.
    --open: Shows only open ports.
    --min-rate 100: Sends packets at a minimum rate of 100 packets per second.
    -v: Increases verbosity.

     2. Fast Comprehensive Scan
     nmap -p- -sV --min-rate 1000 --open --max-retries 1 --host-timeout 15m -T4

    --min-rate 1000: Sends packets at a minimum rate of 1000 packets per second, speeding up the scan.
    --max-retries 1: Reduces the number of retries for each port.
    --host-timeout 15m: Limits the time spent scanning a single target to 15 minutes.

    3. Stealthy Comprehensive Scan
    nmap -p- -sV -sS -T2 --script=vuln --open -v

    -sS: Conducts a SYN stealth scan, which is less likely to be logged.
    -T2: Uses a lower timing template to slow down the scan, making it less noticeable.

    4. Fast and Stealthy Comprehensive Scan
    nmap -p- -sV -sS --min-rate 500 --open --max-retries 1 --defeat-rst-ratelimit -T3

    --min-rate 500: Balances speed and stealth by sending packets at a moderate rate.
    --defeat-rst-ratelimit: Attempts to bypass restrictions that limit the number of reset packets.
    -T3: Balances speed and stealth more conservatively than -T4.
    :return:
    """
    while True:
        options = [
            """
            1. Comprehensive Scan for All Vulnerabilities on All Ports
            
                 nmap -p- -sV -sC -T4 --script=vuln --open --min-rate 100 -v
                
            2. Fast Comprehensive Scan
                                
                nmap -p- -sV --min-rate 1000 --open --max-retries 1 --host-timeout 15m -T4
                
            3. Stealthy Comprehensive Scan

                nmap -p- -sV -sS -T2 --script=vuln --open -v
                
            4. Fast and Stealthy Comprehensive Scan
                
                nmap -p- -sV -sS --min-rate 500 --open --max-retries 1 --defeat-rst-ratelimit -T3 

            """
        ]
        print(options[0])
        print("\n> ")
        option = getch().upper()
        if option == '1':
            popen_command_new_terminal("nmap -p- -sV -sC -T4 --script=vuln --open --min-rate 100 -v " + TARGET_IP)
        elif option == '2':
            popen_command_new_terminal("nmap -p- -sV --min-rate 1000 --open --max-retries 1 --host-timeout 15m -T4 " + TARGET_IP)
        elif option == '3':
            popen_command_new_terminal("nmap -p- -sV -sS -T2 --script=vuln --open -v " + TARGET_IP)
        elif option == '4':
            popen_command_new_terminal("nmap -p- -sV -sS --min-rate 500 --open --max-retries 1 --defeat-rst-ratelimit -T3 " + TARGET_IP)
        else:
            continue

def main():
    nmap()

if __name__ == "__main__":
    main()
