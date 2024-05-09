import os
import subprocess

terminals = ['x-terminal-emulator', 'gnome-terminal', 'konsole', 'xfce4-terminal']
terminal_pids = []
terminal_positions = [(0, 0), (0, 400), (0, 800), (800, 0), (800, 400),
                      (800, 800)]  # Define terminal window positions

def get_screen_resolution():
    try:
        output = subprocess.check_output("xdpyinfo | grep dimensions", shell=True, text=True)
        resolution = output.split()[1].split('x')
        return int(resolution[0]), int(resolution[1])
    except Exception as e:
        print(f"Error getting screen resolution: {e}")
        print("Using default resolution: 1920x1080")
        return 1920, 1080

def popen_command_new_terminal(command):
    screen_width, screen_height = get_screen_resolution()
    terminal_width = screen_width // 2
    terminal_height = screen_height // 3

    for terminal in terminals:
        if not terminal_positions:
            print("No more positions available for new terminals.")
            return

        position_index = len(terminal_pids) % len(terminal_positions)
        x, y = terminal_positions[position_index]

        if terminal == 'x-terminal-emulator':
            terminal_command = f"{terminal} -geometry {terminal_width}x{terminal_height}+{x}+{y} -e 'bash -c \"{command}; exec bash\"'"
        elif terminal == 'gnome-terminal':
            terminal_command = f"{terminal} --geometry=80x24+{x}+{y} -e '/bin/sh -c \"{command}; exec bash\"'"
        elif terminal == 'konsole':
            terminal_command = f"{terminal} -e /bin/sh -c '{command}; exec bash'"
        elif terminal == 'xfce4-terminal':
            terminal_command = f"{terminal} --geometry=80x24+{x}+{y} -e '/bin/sh -c \"{command}; exec bash\"'"
        else:
            continue

        try:
            print(f"Attempting to execute: {terminal_command}")
            process = subprocess.Popen(terminal_command, shell=True, preexec_fn=os.setsid)
            terminal_pids.append(process.pid)
            return process
        except Exception as e:
            print(f"Failed to start {terminal}: {e}. Trying the next terminal...\n")

    # Fallback if none of the terminals are available
    print("No suitable terminal found.")
    return None
