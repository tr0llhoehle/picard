#!/usr/bin/python2.7
import socket
import curses
import time
import signal
import sys
import md5
import json
import argparse

username = ''
password = ''
ip = '127.0.0.1'
port = 5005
sourceport = 6666

class Communication:
	def __init__(self, screen, username, password, ip, port, sourceport):
		self.screen = screen
		self.UDP_IP =  ip
		self.UDP_PORT = port
		self.sequence = 0
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(('', sourceport))
		self.realm = ''
		self.nonce = ''
		self.username = username
		self.password = password

	def sendmessage(self, command):
		self.sequence += 1
		hash = self.gethash()
		message = '{"sequence":'+str(self.sequence)+',"command":"'+command+'", "username":"'+self.username+'", "hash":"'+hash+'"}'
		self.sock.sendto(message, (self.UDP_IP, self.UDP_PORT))

	def auth(self):
		message = '{"sequence":0, "command":"requestauth", "username":"'+self.username+'"}'
		self.sock.sendto(message, (self.UDP_IP, self.UDP_PORT))
		data, addr = self.sock.recvfrom(1024)
		decoded = json.loads(data)

		self.screen.clear()
		self.screen.refresh()
		self.screen.addstr(0,0,decoded.get('error', 'success'))
		if(decoded.get('error', 'success') == 'success'):
			self.realm = decoded['realm']
			self.nonce = decoded['nonce']
			self.sequence = decoded['sequence']+1
			response = self.gethash()
			message = '{"sequence":'+str(self.sequence)+', "command":"auth", "username":"'+self.username+'", "nonce":"'+decoded['nonce']+'", "response":"'+response+'", "realm":"'+decoded['realm']+'"}'
			self.sock.sendto(message, (self.UDP_IP, self.UDP_PORT))
			self.sequence = decoded['sequence']+1
			data, addr = self.sock.recvfrom(1024)
			decoded = json.loads(data)
			if(decoded.get('error', 'success') == 'success'):
				self.screen.clear()
				self.screen.refresh()
				self.screen.addstr(0,0,'authenticated')
			else:
				self.screen.clear()
				self.screen.refresh()
				self.screen.addstr(0,0,'error authenticating')

	def gethash(self):
		m = md5.new()
  		m.update(self.username+':'+self.realm+':'+self.password)
		ha1 = m.hexdigest()
		m.update('AUTH:'+str(self.sequence))
		ha2 = m.hexdigest()
		m.update(ha1+':'+self.nonce+':'+ha2)
		return m.hexdigest()

def main(screen):

	comm = Communication(screen, username, password, ip, port, sourceport)
	screen.nodelay(1)
	while True:
	    char = screen.getch()
	    if char == 113: break  # q
	    elif char == 97: comm.auth() # a = authentication
	    elif char == curses.KEY_RIGHT: comm.sendmessage('moveright')
	    elif char == curses.KEY_LEFT: comm.sendmessage('moveleft')
	    elif char == curses.KEY_UP: comm.sendmessage('moveforward')
	    elif char == curses.KEY_DOWN: comm.sendmessage('movebackward')
	    time.sleep(0.1)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='An application that sends control messages to picard')

	parser.add_argument('-u', '--username', nargs=1, dest='username', default='', required=True, help='the username')
	parser.add_argument('-p', '--password', nargs=1, dest='password', default='', required=True, help='the password')
	parser.add_argument('--ip', nargs=1, dest='ip', default='127.0.0.1', help='the ip')
	parser.add_argument('--port', nargs=1, dest='port', default=[5005], help='the port')
	parser.add_argument('--sourceport', nargs=1, dest='sourceport', default=[6666], help='the sourceport')
	parser.add_argument('--version', action='version', dest='version', version='%(prog)s 0.1')

	results = parser.parse_args()

	username = results.username[0]
	password = results.password[0]
	ip = results.ip[0]
	port = int(results.port[0])
	sourceport = int(results.sourceport[0])	
	curses.wrapper(main)