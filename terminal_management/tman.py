import os
import subprocess
import shutil

terminals = ['x-terminal-emulator', 'gnome-terminal', 'konsole', 'xfce4-terminal']
terminal_pids = []
terminal_positions = [(0, 0), (0, 400), (0, 800), (800, 0), (800, 400), (800, 800)]


def get_screen_resolution():
    try:
        output = subprocess.check_output("xdpyinfo | grep dimensions", shell=True, text=True)
        resolution = output.split()[1].split('x')
        return int(resolution[0]), int(resolution[1])
    except Exception as e:
        print(f"Error getting screen resolution: {e}")
        return 1920, 1080  # Default resolution if detection fails


def popen_command_new_terminal(command):
    screen_width, screen_height = get_screen_resolution()
    terminal_width = screen_width // 2
    terminal_height = screen_height // 3

    for terminal in terminals:
        # Check if the terminal command is available on the system
        if shutil.which(terminal) is None:
            print(f"{terminal} is not installed. Trying the next terminal...")
            continue

        if not terminal_positions:
            print("No more positions available for new terminals.")
            continue

        position_index = len(terminal_pids) % len(terminal_positions)
        x, y = terminal_positions[position_index]

        terminal_command = f"{terminal} --geometry={terminal_width}x{terminal_height}+{x}+{y} -e 'bash -c \"{command}; exec bash\"'"

        try:
            print(f"Executing command: {terminal_command}")
            process = subprocess.Popen(terminal_command, shell=True, preexec_fn=os.setsid)
            terminal_pids.append(process.pid)
            return process
        except Exception as e:
            print(f"Failed to execute command in {terminal}: {e}")

    print("No suitable terminal emulator found. Please install one of the specified terminals.")
    return None

