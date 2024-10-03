import threading
import socket
import netifaces

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

def get_ip_addresses():
    """Get all IP addresses of the current machine."""
    ip_addresses = []
    for interface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            for addr_info in addresses[netifaces.AF_INET]:
                
                ip_address = addr_info.get('addr')
                if ip_address and ip_address != '127.0.0.1':
                    ip_addresses.append(ip_address)
    return ip_addresses