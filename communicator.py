#!/usr/bin/python2.7
import socket
import curses
import time
import signal
import sys
import md5
import json
import argparse
import communication

username = ''
password = ''
ip = '127.0.0.1'
port = 5005
sourceport = 6666

def main(screen):
	comm = communication.Communication(username, password, ip, port, sourceport)
	screen.nodelay(1)
	percentagedir = 100
	percentage = 80
	while True:
		char = screen.getch()
		if char == 113: break  # q
		elif char == 65: comm.auth() # A = authentication
		elif char == 119: comm.movePercentage('forward',percentage) # w
		elif char == 87: comm.movePercentage('left', 0) # W
		elif char == 97: comm.movePercentage('left',percentagedir) # a
		elif char == 115: comm.movePercentage('backward',percentage) # s
		elif char == 100: comm.movePercentage('right',percentagedir) #d
		elif char == 32: comm.movePercentage('forward',0) # space
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