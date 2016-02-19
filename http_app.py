"""Sending HTTP requests to a web server and display the response.

Things are done with the help of socket module.

Hint: 
Some sites are NOT friendly to robots so please add "User-Agent: Mozilla" to
enchance your chance of getting response from the server.

ch3cooh @ 2016
"""
import socket

def clean_host(host):
    """Remove leading http:// and trailing /path_to_somewhere in host name"""
    host = host.strip()
    prefixes = ['http://']
    for prefix in prefixes:
        if host.lower().startswith(prefix):
            host = host[len(prefix):]
    slash = host.find('/')
    if slash>0:
        host = host[:slash]
    return host

def get_ipv4_list(host, port=80):
    """Return the list of ips corresponding to given host and port number"""
    info = socket.getaddrinfo(host, port)
    return [item[4][0] for item in info]

def send_request(ip, data, remote_port=80,bufsize=1024):
    """Send data to give ip and receive response from the server"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, remote_port))
    sock.send(data)
    recv_data = []
    while True:
        buf = sock.recv(bufsize)
        if not buf:
            break
        recv_data += [buf]
    sock.close()
    return ''.join(recv_data)

def read_text(promp='> ', promp2='~ '):
    """Read in text from stdin terminted by EOF"""
    text = []
    try:
        while True:
            if not text:
                text = [raw_input(promp)+'\n']
            else:
                text += [raw_input(promp2)+'\n']
    except EOFError:
        return ''.join(text)
    return ''

def http_app():
    remote_host = raw_input('Input remote host name (for example www.baidu.com): ')
    remote_port = 80
    buf = raw_input('Input remote port number (default 80): ')
    if buf.isdigit() and 0<=int(buf)<=65535:
        remote_port = int(buf)
    print remote_host, 'at port', remote_port
    
    print 'Resolving host...'
    ip_list = get_ipv4_list(clean_host(remote_host), port=remote_port)
    ip = ip_list[0]
    print 'Using ip address', ip
    while True:
        data = read_text()
        if not data:
            break
        print '[REQUEST]'
        print data
        response = send_request(ip, data, remote_port=remote_port)
        print '[REPONSE]'
        print response

if __name__ == '__main__':
    print 'Running http_app. Press Ctrl+C to quit'
    while True:
        try:
            http_app()
        except KeyboardInterrupt:
            if raw_input('Quit? (y/n)').lower() == 'y':
                break
