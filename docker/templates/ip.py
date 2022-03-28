# Get container ip
def get_ip():
    import socket
    return(socket.gethostbyname(socket.gethostname()))
