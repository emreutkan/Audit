from terminal_management.tman import popen_command_new_terminal

def nc():
    from main import local_port
    print(f"")
    print(f"Listening on port {local_port} ...")
    popen_command_new_terminal(f'nc -lvnp {local_port}')