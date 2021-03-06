#! /usr/bin/python2.7
import pygame
import communication
import ConfigParser

import subprocess

# taken from http://www.pygame.org/docs/ref/joystick.html

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

#keymap
accelerate_axis = 5
decelerate_axis = 2
steering_axis = 0
trimbutton = 7
trim = False
deadzone = 0.2

#handbrake pressed -> handbrake = True
handbrake = False
forward = 0.0
forward_old = 0.0
right = 0.0
right_old = 0.0
#joybutton = 14

communicator = None

def initNetwork():
    global communicator
    global sourceIP
    Users = ConfigParser.ConfigParser()
    Users.read('users.ini')
    options = Users.options('users')
#    print(options)
    dict1 = {}
    for option in options:
        username = option
#        print(username)
        try:
            dict1[option] = Users.get('users', option)
            password = dict1[username]
#            print(password)
#            print(dict1)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
            break
        except:
            print("exception on %s!" % option)
            dict1[option] = None
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
    port = int(dict1['port'])
    sourceport = int(dict1['sourceport'])    

    communicator = communication.Communication(username, password, ip, port, sourceport)
    communicator.auth()

# this funktion is used to convert the axes to steering information
def sendCommand(direction, percentage_float):
    global communicator
    if(communicator != None):
		percentage_int = int(percentage_float*100)
		communicator.movePercentage(direction,percentage_int)


# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputing the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def foo(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10
    
initNetwork()

pygame.init()

#Mjpeg-stream
child = subprocess.Popen("./Stream-Client.py")
 
# Set the width and height of the screen [width,height]
size = [200, 100]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("PiCarD-Remote-360")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
    
# Get ready to print
textPrint = TextPrint()

# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        #every button is handbrake
        if event.type == pygame.JOYBUTTONDOWN:
        	       # handbrake = joystick.get_button(joybutton)
        	
        	handbrake = True
        	trim = joystick.get_button(trimbutton)
        	#print("Handbrake pressed.")
        if event.type == pygame.JOYBUTTONUP:
        	
        	handbrake = False
        	#handbrake = joystick.get_button(joybutton)
        	#crappy code, but works
        	#forward_old = forward
        	forward = ((joystick.get_axis(accelerate_axis)+1) - (joystick.get_axis(decelerate_axis)+1))/2
            	#print("Handbrake released.")
            	trim = joystick.get_button(trimbutton)
        # my own events
        if event.type == pygame.JOYAXISMOTION:
        #alternative rechts/links = axis 3
        	if event.axis == steering_axis:
        		#right = joystick.get_axis(event.axis)
        		if abs(joystick.get_axis(event.axis)) > deadzone:
        			#right_old = right
        			right = joystick.get_axis(event.axis)
        		else:
        		    #right_old = right
        		    right = 0.0
        	if handbrake == True:
        		#forward_old = forward
        		forward = 0.0;

		else:
			if joystick.get_numaxes() >= accelerate_axis and joystick.get_numaxes() >= decelerate_axis:
				if event.axis == accelerate_axis or event.axis == decelerate_axis:
					#forward_old = forward
					forward = ((joystick.get_axis(accelerate_axis)+1) - (joystick.get_axis(decelerate_axis)+1))/2
					#print"forward value: {}".format(forward)
		    
 
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()
    
#    #exit on child exit
#    if child.poll() == True:
#        done = True
    
    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()
    # init joysticks:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
    
    #print own foo
    textPrint.foo(screen, "trim value: {}".format(trim) )
    textPrint.foo(screen, "handbrake value: {}".format(handbrake) )
    #textPrint.indent()
    textPrint.foo(screen, "forward value: {}".format(forward) )
    #textPrint.indent()
    textPrint.foo(screen, "right value: {}".format(right) )
    #textPrint.indent()
    
   #send messages
    if (abs(abs(forward) - abs(forward_old)) > 0.01):
       	forward_old = forward
       	if(forward >= 0.0):
		    sendCommand('forward',forward)
       	else:
		    sendCommand('backward', abs(forward))
    if (abs(abs(right) - abs(right_old)) > 0.01):
        right_old = right
        if(right >= 0.0):
		    sendCommand('right',right)
		    #print(right)
        else:
	    	sendCommand('left', abs(right))
	


    
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
#t._stop()
communicator.killTimer()

#try to kill child
try:
    child.kill()
except Exception, e:
    print("child is closed")
pygame.quit()

