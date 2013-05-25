import socket
import curses
import time
import signal
import sys

class Communication:
	def __init__(self):
		self.UDP_IP = "127.0.0.1"
		self.UDP_PORT = 5005
		self.sequence = 0
		self.sock = socket.socket(socket.AF_INET, # Internet
	                     socket.SOCK_DGRAM) # UDP

	def sendmessage(self, command):
		message = '{"sequence":'+str(self.sequence)+',"command":"'+command+'"}'
		self.sequence += 1
		self.sock.sendto(message, (self.UDP_IP, self.UDP_PORT))

def main(screen):
	comm = Communication()
	screen.nodelay(1)
	while True:
	    char = screen.getch()
	    if char == 113: break  # q
	    elif char == curses.KEY_RIGHT: comm.sendmessage('moveright')
	    elif char == curses.KEY_LEFT: comm.sendmessage('moveleft')
	    elif char == curses.KEY_UP: comm.sendmessage('moveforward')
	    elif char == curses.KEY_DOWN: comm.sendmessage('movebackward')
	    time.sleep(0.1)

if __name__ == '__main__':
    curses.wrapper(main)