import socket
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
  data, addr = sock.recvfrom(1024)
  print "received message:", data

  try:
    decoded = json.loads(data)
    print 'DECODED:', decoded
    print decoded['sequence']
  except ValueError, e:
    print 'JSON decoding failed: '
    print e
