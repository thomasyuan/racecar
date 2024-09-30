import threading

def get_serial():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('Serial'):
                    return line.split(':')[1].strip()
    except Exception as e:
        print(f"Error reading serial number: {e}")
        return "0000000000000000"

def start_daemon_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    return thread