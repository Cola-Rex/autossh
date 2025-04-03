import subprocess
import sys
import time
import threading
import socket
import signal
import os
import select

ssh_process = None
should_exit = False
ssh_lock = threading.Lock()  # Add thread lock

ssh_path = "/usr/bin/ssh"  # Use absolute path to ensure it works after packaging

def check_local_port(port):
    """
    # This function is no longer used to determine whether the tunnel is disconnected,
    # to avoid misjudging that the tunnel is broken when no client connects yet.
    """
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=2):
            return True
    except:
        return False

def start_ssh(cmd_args):
    global ssh_process
    print("[ausossh] Starting SSH tunnel...")
    cmd_args = [
        "-v",  # Enable verbose logging
        "-o", "ServerAliveInterval=5",
        "-o", "ServerAliveCountMax=3"
    ] + cmd_args
    with ssh_lock:
        ssh_process = subprocess.Popen(
            [ssh_path] + cmd_args,
            stderr=subprocess.PIPE  # Keep only stderr to avoid interfering with ProxyJump's stdin/stdout
        )
    return ssh_process

def monitor_tunnel(local_port, cmd_args):
    """
    Only determine whether the tunnel is alive based on ssh_process.poll().
    If the process exits, restart it.
    No longer use local port checks to avoid false positives.
    """
    global ssh_process, should_exit

    while not should_exit:
        with ssh_lock:
            # If ssh_process has exited, restart it
            if ssh_process is None or ssh_process.poll() is not None:
                print("[ausossh] SSH process terminated, restarting...")
                ssh_process.wait()  # Wait for process to fully terminate
                ssh_process = start_ssh(cmd_args)

        try:
            # Check every second
            select.select([], [], [], 1)
        except select.error:
            continue

def extract_local_port(args):
    for i, arg in enumerate(args):
        if arg == "-L" and i + 1 < len(args):
            port_part = args[i + 1]
            local_port = port_part.split(":")[0]
            if local_port.isdigit():
                return local_port
    return None

def signal_handler(sig, frame):
    global should_exit
    print("\n[ausossh] Caught interrupt. Exiting.")
    should_exit = True
    with ssh_lock:
        if ssh_process:
            ssh_process.terminate()
    sys.exit(0)

def main():
    global ssh_process
    args = sys.argv[1:]

    if not args:
        subprocess.run([ssh_path])  # Show ssh help info
        return

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    local_port = extract_local_port(args)
    if not local_port:
        print("[ausossh] Warning: No -L port detected. No port monitoring will happen.")
        # If no port forwarding is set, just run ssh directly
        ssh_process = start_ssh(args)
        ssh_process.wait()
    else:
        # First start the SSH process
        ssh_process = start_ssh(args)
        # Then start the monitoring thread
        threading.Thread(target=monitor_tunnel, args=(local_port, args), daemon=True).start()
        # Wait for the main process to prevent exit
        ssh_process.wait()

if __name__ == "__main__":
    main()
