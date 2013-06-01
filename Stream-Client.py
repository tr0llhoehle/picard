#!/usr/bin/env python
import httplib    #httplib modules for the HTTP interactions
from Tkinter import * #Tkinter modules for Windowing
from PIL import Image, ImageTk #Python Image Libraries, required for displaying jpegs
from time import sleep
import StringIO                 #For converting Stream from the server to IO for Image (PIL)
from StreamViewer import StreamViewer     

import ConfigParser     

def initNetwork():
#    global communicator
    global sourceIP
    Network = ConfigParser.ConfigParser()
    Network.read('network.ini')
    netOptions = Network.options('network')

    dict1 = {}
    for option in netOptions:
        try:
            dict1[option] = Network.get('network', option)

            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)

        except:
            print("exception on %s!" % option)
            dict1[option] = None

    ip = dict1['ip']
    sourceIP = ip
#    print(sourceIP)
    port = int(dict1['port'])
    sourceport = int(dict1['sourceport'])    


         
'''Gets the file from the specified
host, port and location/query'''
def get(host,port,query):
     h = httplib.HTTP(host, port)
     h.putrequest('GET', query)
     h.putheader('Host', host)
     h.putheader('User-agent', 'python-httplib')
     h.putheader('Content-type', 'image/jpeg')
     h.endheaders()
     
     (returncode, returnmsg, headers) = h.getreply()
     print "return code:",returncode
     print "return message:",returnmsg
     print "headers:",headers
     if returncode != 200:
         print returncode, returnmsg
         sys.exit()
     
     f = h.getfile()
     return f.read()

'''This is where we show the file on our StreamViewer'''
def streamfile(tbk, root):
     global sourceIP
     f = get(sourceIP,8080,'/?action=snapshot')
#     f = get('94.45.241.5',8080,'/?action=snapshot')
     img=Image.open(StringIO.StringIO(f)) #convert to jpeg object from the stream
     imagetk = ImageTk.PhotoImage(img) #Get a PhotoImage to pass to our Frame
     tbk.addImage(imagetk) #Image added
     root.update()

initNetwork()
root = Tk()
tbk = StreamViewer(root)
#As much space as we need, no more, no less
#we change the root geometry to the size of the streaming jpg #As much space as we need, no more, no less

root.geometry("%dx%d+0+0" % (640, 480))
root.resizable(False,False)
'''It's our overrated slideshow viewer .. hehe'''
while(1):
     streamfile(tbk,root)


