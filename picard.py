import socket
import json
import random
from Crypto.Random.random import getrandbits
import md5
import ConfigParser
try:
  from RPIO import PWM
  DEBUG = False
except ImportError:
  DEBUG = True

class Auth:
  def __init__(self):
    self.UDP_IP = '127.0.0.1'
    self.UDP_PORT = 5005
    self.sequence = 0
    self.sock = socket.socket(socket.AF_INET, # Internet
                       socket.SOCK_DGRAM) # UDP
    self.sock.bind(('', self.UDP_PORT))
    self.realm = 'picard@raspberrykai'
    self.Users = ConfigParser.ConfigParser()
    self.Users.read('users.ini')
    self.Settings = ConfigParser.ConfigParser()
    self.Settings.read('settings.ini')
    self.limits = dict(self.Settings.items('settings'))
    self.servoDirection = int(self.limits['straight'])
    self.nonces = {}
    self.sequences = {}
    if not DEBUG:
      self.servo = PWM.Servo(0,20000,int(self.limits['step']))

  def setServo(self, pin, value):
    if not DEBUG:
      self.servo.set_servo(pin, value)

  def moveInDirection(self,direction):
    if(direction == 'left'):
      if(self.servoDirection-int(self.limits['step']) > int(self.limits['maxleft'])):
        self.servoDirection -= int(self.limits['step'])
        print 'moving ' , direction, ' value: ', self.servoDirection
        self.setServo(25, self.servoDirection)
    elif(direction == 'right'):
      if(self.servoDirection+int(self.limits['step']) < int(self.limits['maxright'])):
        self.servoDirection += int(self.limits['step'])
        self.setServo(25, self.servoDirection)

  def moveInDicrection(self,direction,percentage):
    print 'moep'

  def lookup(self,username):
    if self.Users.has_option('users', username):
      return True
    else:
      return False

  def loop(self):
    while True:
      data, addr = self.sock.recvfrom(1024)
      print "received message:", data, addr
      try:
        decoded = json.loads(data)
        print 'DECODED:', decoded
        print decoded['sequence']
        if decoded['command'] == 'requestauth':
          if(self.lookup(decoded['username'])):
            self.nonces[decoded['username']] = str(getrandbits(128))
            self.sequences[decoded['username']] = random.randint(1,65536)
            print self.nonces[decoded['username']]
            print self.sequences[decoded['username']]
            message = '{"sequence":'+str(self.sequences[decoded['username']])+',"realm":"'+self.realm+'", "nonce":"'+self.nonces[decoded['username']]+'"}'
          else:
            message = '{"error":"username not found"}'
          self.sock.sendto(message, (addr[0], addr[1]))
        elif decoded['command'] == 'auth':
          print 'yay'
          m = md5.new()
          m.update(decoded['username']+':'+decoded['realm']+':'+self.Users.get('users', decoded['username']))
          ha1 = m.hexdigest()
          m.update('AUTH:'+str(decoded['sequence']))
          ha2 = m.hexdigest()
          m.update(ha1+':'+self.nonces[decoded['username']]+':'+ha2)
          response = m.hexdigest()

          if(response == decoded['response']):
            print 'authenticated'
            self.sequences[decoded['username']] = decoded['sequence']
            message = '{"info":"authenticated"}'
          else:
            message = '{"error":"unauthorized"}'
          self.sock.sendto(message, (addr[0], addr[1]))            
        else:
          print 'check hash'
          print self.realm
          if decoded['username'] in self.nonces:
            m = md5.new()
            m.update(decoded['username']+':'+self.realm+':'+self.Users.get('users', decoded['username']))
            ha1 = m.hexdigest()
            m.update('AUTH:'+str(decoded['sequence']))
            ha2 = m.hexdigest()
            m.update(ha1+':'+self.nonces[decoded['username']]+':'+ha2)
            if(decoded['hash'] == m.hexdigest()):
              print 'correct hash'
              print self.sequences[decoded['username']]
              if(self.sequences[decoded['username']] < decoded['sequence']):
                # execute command
                self.sequences[decoded['username']] = decoded['sequence']
                print 'received sequence > stored sequence'
                if decoded['command'].startswith('move'):
                  command = decoded['command'].replace('move','')
                  self.moveInDirection(command)

      except ValueError, e:
        print 'JSON decoding failed: '
        print e
      except KeyError, e:
        print 'Missing Key, check the client implementation: '
        print e

if __name__ == '__main__':
  auth = Auth()
  auth.loop()
