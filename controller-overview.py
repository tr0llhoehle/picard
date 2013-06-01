#! /usr/bin/python2.7
import pygame

# taken from http://www.pygame.org/docs/ref/joystick.html

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)


#handbrake pressed -> handbrake = True
handbrake = False
forward = 0.0
right = 0.0
#joybutton = 14
accelerate_axis = 5
decelerate_axis = 2
steering_axis = 0
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
    

pygame.init()

 
# Set the width and height of the screen [width,height]
size = [300, 1700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("PiCarD-Remote")

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
        
#        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
#        #every button is handbrake
#        if event.type == pygame.JOYBUTTONDOWN:
#        	       # handbrake = joystick.get_button(joybutton)
#        	handbrake = True
#        	#print("Handbrake pressed.")
#        if event.type == pygame.JOYBUTTONUP:
#        	handbrake = False
#        	#handbrake = joystick.get_button(joybutton)
#        	#crappy code, but works
#        	forward = ((joystick.get_axis(accelerate_axis)+1) - (joystick.get_axis(decelerate_axis)+1))/2
#            	#print("Handbrake released.")
#        # my own events
#        if event.type == pygame.JOYAXISMOTION:
#        #alternative rechts/links = axis 3
#        	if event.axis == steering_axis:
#        		right = joystick.get_axis(event.axis)
#        		if abs(right) < 0.2:
#        			right = 0.0
#        	if handbrake == True:
#        		forward = 0.0;

#		else:
#			if joystick.get_numaxes() >= accelerate_axis and joystick.get_numaxes() >= decelerate_axis:
#				if event.axis == accelerate_axis or event.axis == decelerate_axis:
#					forward = ((joystick.get_axis(accelerate_axis)+1) - (joystick.get_axis(decelerate_axis)+1))/2
#					#print"forward value: {}".format(forward)
		    
 
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()
    
    
    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()
    # init joysticks:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
    
#    #print own foo
#    textPrint.foo(screen, "handbrake value: {}".format(handbrake) )
#    #textPrint.indent()
#    textPrint.foo(screen, "forward value: {}".format(forward) )
#    #textPrint.indent()
#    textPrint.foo(screen, "right value: {}".format(right) )
#    #textPrint.indent()
    


    textPrint.foo(screen, "Number of joysticks: {}".format(joystick_count) )
    textPrint.indent()
    
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
    
        textPrint.foo(screen, "Joystick {}".format(i) )
        textPrint.indent()
    
        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.foo(screen, "Joystick name: {}".format(name) )
        
        
        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.foo(screen, "Number of axes: {}".format(axes) )
        textPrint.indent()
        
        for i in range( axes ):
            axis = joystick.get_axis( i )
            textPrint.foo(screen, "Axis {} value: {:>6.3f}".format(i, axis) )
        textPrint.unindent()
            
        buttons = joystick.get_numbuttons()
        textPrint.foo(screen, "Number of buttons: {}".format(buttons) )
        textPrint.indent()

        for i in range( buttons ):
            button = joystick.get_button( i )
            textPrint.foo(screen, "Button {:>2} value: {}".format(i,button) )
        textPrint.unindent()
            
        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        textPrint.foo(screen, "Number of hats: {}".format(hats) )
        textPrint.indent()

        for i in range( hats ):
            hat = joystick.get_hat( i )
            textPrint.foo(screen, "Hat {} value: {}".format(i, str(hat)) )
        textPrint.unindent()
        
        textPrint.unindent()

    
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit ()
