import os
import sys
import tty
import termios
from colorama import Fore, Style
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from terminal_management.tman import clear
from input_management.validations import validate_ip, validate_port, getch


TARGET_IP = os.popen('hostname -I').read().split()[0]
TARGET_PORT = 0
PN_FLAG = False

def set_pn_flag():
    """
    Set the -Pn flag
    """
    global PN_FLAG
    PN_FLAG = not PN_FLAG

def set_target_ip():
    """
    Set the target IP address
    """
    global TARGET_IP
    print(f"{Fore.RED}Current target IP address: {TARGET_IP}{Style.RESET_ALL}")
    target = input("Enter the target IP address: ")
    if validate_ip(target):
        TARGET_IP = target
    else:
        print(f"{Fore.RED}Invalid IP address{Style.RESET_ALL}")


def set_port():
    """
    Set the port range for the scan
    """
    global TARGET_PORT
    print("Enter the port or port range (e.g. 1-1000): ")
    print("Type 0 to scan all ports")
    port_range = input(" > ")
    if validate_port(port_range):
        TARGET_PORT = port_range
    else:
        print(f"{Fore.RED}Invalid port or port range{Style.RESET_ALL}")

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
    if PN_FLAG:
        command += " -Pn"
    command += f" {TARGET_IP}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    if rc == 0:
        print(f"{Fore.GREEN}Scan completed successfully{Style.RESET_ALL}")
    elif rc == 1:
        print(f"{Fore.RED}Scan failed{Style.RESET_ALL}")
        print(process.stderr.read())
    input("Press Enter to continue...")

def Comprehensive_Scan():
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
    """
    if TARGET_PORT == 0:
        command = "nmap -p- -sV -sC -T4 --script=vuln --open --min-rate 100 -v"
    else:
        command = f"nmap -p {TARGET_PORT} -sV -sC -T4 --script=vuln --open --min-rate 100 -v"
    run_nmap(command)

def Fast_Comprehensive_Scan():
    """
    Fast Comprehensive Scan
    nmap -p- -sV --min-rate 1000 --open --max-retries 1 --host-timeout 15m -T4

    --min-rate 1000: Sends packets at a minimum rate of 1000 packets per second, speeding up the scan.
    --max-retries 1: Reduces the number of retries for each port.
    --host-timeout 15m: Limits the time spent scanning a single target to 15 minutes.
    """
    if TARGET_PORT == 0:
        command = "nmap -p- -sV --min-rate 1000 --open --max-retries 1 --host-timeout 15m -T4"
    else:
        command = f"nmap -p {TARGET_PORT} -sV --min-rate 1000 --open --max-retries 1 --host-timeout 15m -T4"
    run_nmap(command)

def stealthy_scan():
    """
    Stealthy Comprehensive Scan
    nmap -p- -sV -sS -T2 --script=vuln --open -v

    -sS: Conducts a SYN stealth scan, which is less likely to be logged.
    -T2: Uses a lower timing template to slow down the scan, making it less noticeable.
    """
    if TARGET_PORT == 0:
        command = "nmap -p- -sV -sS -T2 --script=vuln --open -v"
    else:
        command = f"nmap -p {TARGET_PORT} -sV -sS -T2 --script=vuln --open -v"
    run_nmap(command)

def fast_stealthy_scan():
    """
    Fast and Stealthy Comprehensive Scan
    nmap -p- -sV -sS --min-rate 500 --open --max-retries 1 --defeat-rst-ratelimit -T3

    --min-rate 500: Balances speed and stealth by sending packets at a moderate rate.
    --defeat-rst-ratelimit: Attempts to bypass restrictions that limit the number of reset packets.
    -T3: Balances speed and stealth more conservatively than -T4.
    """
    if TARGET_PORT == 0:
        command = "nmap -p- -sV -sS --min-rate 500 --open --max-retries 1 --defeat-rst-ratelimit -T3"
    else:
        command = f"nmap -p {TARGET_PORT} -sV -sS --min-rate 500 --open --max-retries 1 --defeat-rst-ratelimit -T3"
    run_nmap(command)


def interface():
    # Define color schemes
    command_color = Fore.BLUE + Style.BRIGHT
    variable_color = Fore.RED
    info_color = Fore.WHITE
    separator_color = Fore.WHITE + Style.DIM
    reset = Style.RESET_ALL

    # Construct options string with colored output
    options = [
        f"""
        {separator_color}--------------------------[ Configuration ]--------------------------{reset}
        {command_color}S{reset}: Set target IP                        {info_color}Target IP = {variable_color}{TARGET_IP}{reset}
        {command_color}P{reset}: Set target port (0 for all ports)    {info_color}Selected Ports = {variable_color}{'all ports' if TARGET_PORT == 0 else TARGET_PORT}{reset}
        {command_color}N{reset}: Set -Pn flag                         {info_color}-Pn = {variable_color}{'True' if PN_FLAG else 'False'}{reset}
        {separator_color}----------------------------------------------------------------------------{reset}
        {command_color}Q{reset}. Exit
        {command_color}1{reset}. Comprehensive Scan
        {command_color}2{reset}. Fast Comprehensive Scan
        {command_color}3{reset}. Stealthy Scan
        {command_color}4{reset}. Fast and Stealthy Scan
        {separator_color}----------------------------------------------------------------------------{reset}
        """
    ]

    print(options[0])
def nmap():
    while True:
        interface()
        print('> ', end='', flush=True)
        option = getch().upper()
        clear()
        if option == 'S':
            set_target_ip()
        elif option == 'P':
            set_port()
        elif option == 'N':
            set_pn_flag()
        elif option == 'Q':
            exit()
        elif option == '1':
            Comprehensive_Scan()
        elif option == '2':
            Fast_Comprehensive_Scan()
        elif option == '3':
            stealthy_scan()
        elif option == '4':
            fast_stealthy_scan()
        else:
            continue


def main():
    nmap()


if __name__ == "__main__":
    main()
