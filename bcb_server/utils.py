import socket


def validate_port(port) -> int:
    if not (type(port) == int):
        raise
    elif port <= 1024 or port >= 65000:
        raise
    return port


def get_ip(remote_addr="127.0.0.1"):

    if remote_addr != "127.0.0.1":
        return remote_addr

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP
