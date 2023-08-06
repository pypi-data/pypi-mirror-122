import socket
from IPy import IP 

def scan(target, portnum1, portnum2): # main function
	converted_ip = check_ip(target)
	print('\n' + '[Scanning ... ] ' + str(target))

	for port in range(portnum1, portnum2):
		scan_port(converted_ip, port)

def check_ip(ip):
	try:
		IP(ip)
		return(ip)
	except ValueError:
		return socket.gethostbyname(ip)

def get_banner(s):
	return s.recv(1024)

def scan_port(ipaddress, port):
	try:
		sock = socket.socket()
		sock.settimeout(0.2)
		sock.connect((ipaddress, port))
		try:
			banner = get_banner(sock)
			print(f'Open Port {port}: ' + str(banner.decode().strip('\n')))
		except:
			print(f'Open Port {str(port)}')
	except:
		pass