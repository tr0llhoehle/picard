#!/usr/bin/python2.7
import socket
import time
import sys
import md5
import json
import threading

class Communication:
	def __init__(self, username, password, ip, port, sourceport):
		self.UDP_IP =  ip
		self.UDP_PORT = port
		self.sequence = 0
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(('', sourceport))
		self.realm = ''
		self.nonce = ''
		self.username = username
		self.password = password
		self.timer_enabled = True

	def auth(self):
		message = '{"sequence":0, "command":"requestauth", "username":"'+self.username+'"}'
		self.sock.sendto(message, (self.UDP_IP, self.UDP_PORT))
		data, addr = self.sock.recvfrom(1024)
		decoded = json.loads(data)
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
				print 'authenticated'
				self.keepalive()
			else:
				print 'error authenticating'

	def gethash(self):
		m = md5.new()
  		m.update(self.username+':'+self.realm+':'+self.password)
		ha1 = m.hexdigest()
		m = md5.new()
		m.update('AUTH:'+str(self.sequence))
		ha2 = m.hexdigest()
		m = md5.new()
		m.update(ha1+':'+self.nonce+':'+ha2)
		return m.hexdigest()

	def keepalive(self):
		self.sequence += 1
		hash = self.gethash()
		command = 'keepalive'
		message = '{"sequence":'+str(self.sequence)+',"command":"'+command+'", "username":"'+self.username+'", "hash":"'+hash+'"}'
		self.sock.sendto(message, (self.UDP_IP, self.UDP_PORT))
		self.setupTimer()
    	
	def killTimer(self):
	    self.timer_enabled = False
	
	def setupTimer(self):
	    if self.timer_enabled == True:
	        t = threading.Timer(0.2,self.keepalive)
	        t.start()

	def movePercentage(self,direction,percentage):
		self.sequence += 1
		hash = self.gethash()
		command = 'move' + direction
		message = '{"sequence":'+str(self.sequence)+',"command":"'+command+'", "percentage":'+str(percentage)+', "username":"'+self.username+'", "hash":"'+hash+'"}'
		self.sock.sendto(message, (self.UDP_IP, self.UDP_PORT))
