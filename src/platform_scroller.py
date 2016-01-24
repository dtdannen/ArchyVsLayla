"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

Main module for platform scroller example.

From:
http://programarcadegames.com/python_examples/sprite_sheets/

Explanation video: http://youtu.be/czBDKWJqOao

Part of a series:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/

Game art from Kenney.nl:
http://opengameart.org/content/platformer-art-deluxe

"""

import pygame
import xinput
import platform
from operator import attrgetter

import constants
import levels
from pygame.locals import *

from player import Player

import pytmx

def get_360_controller():
    '''
    Assume pygame.init() is called before this
    '''
    pygame.joystick.init()
    # Initialize a joystick object: grabs the first joystick
    PLATFORM = platform.uname()[0].upper()
    WINDOWS_PLATFORM = PLATFORM == 'WINDOWS'
    WINDOWS_XBOX_360 = False
    JOYSTICK_NAME = ''
    joysticks = xinput.XInputJoystick.enumerate_devices()
    device_numbers = list(map(attrgetter('device_number'), joysticks))
    joystick = None
    if device_numbers:
        joystick = pygame.joystick.Joystick(device_numbers[0])
        JOYSTICK_NAME = joystick.get_name().upper()
        print('Joystick: {} using "{}" device'.format(PLATFORM, JOYSTICK_NAME))
        if 'XBOX 360' in JOYSTICK_NAME and WINDOWS_PLATFORM:
            WINDOWS_XBOX_360 = True
            joystick = xinput.XInputJoystick(device_numbers[0])
            print('Using xinput.XInputJoystick')
            return joystick
        else:
            # put other logic here for handling platform + device type in the event loop
            print('Using pygame joystick')
            joystick.init()
            
    return False


def main():
    """ Main Program """
    pygame.init()
    pygame.joystick.init()
    joystick1 = get_360_controller()
    # Set the height and width of the screen
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Platformer with sprite sheets")

    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append(levels.Level_01(player))
    level_list.append(levels.Level_02(player))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    #Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

   

    # -------- Main Program Loop -----------
    while not done:
        
        # allow the joystick to start listening
        if joystick1:
            #print("joystick1 enabled")
            joystick1.dispatch_events()
        
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_DOWN:
                    player.go_down()
                if event.key == pygame.K_UP:
                    player.go_up()
                    

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
                if event.key == pygame.K_UP and player.change_y < 0:
                    player.stop()
                if event.key == pygame.K_DOWN and player.change_y > 0:
                    player.stop()

            # also check controller input
            if joystick1:
                if event.type == JOYAXISMOTION:
                    #print('JOYAXISMOTION: axis {}, value {}'.format(e.axis, e.value))
                    if event.axis == 2:
                        #left_trigger.value = event.value
                        print("1")
                        pass
                    elif event.axis == 5:
                        #right_trigger.value = event.value
                        print("2")
                        pass
                    elif event.axis == 1 or event.axis == 0:
                        # For smoother xbox 360 controls
                        left_right_on = False
                        up_down_on = False
                        if event.axis == 1: # right and left motion
                            if event.value > 0.2:
                                player.go_right(speed=event.value*5)
                            elif event.value < -0.2:    
                                player.go_left(speed=event.value*5)
                            else:
                                player.stop_left_right()
#                             if event.value > 0.3:
#                                 player.go_right()
#                                 left_right_on = True
#                             elif event.value < -0.3:
#                                 player.go_left()
#                                 left_right_on = True
                                
                        elif event.axis == 0: # up and down motion
                            if event.value > 0.2:
                                player.go_up(speed=-event.value*5)
                            elif event.value < -0.2:    
                                player.go_down(speed=-event.value*5)
                            else:
                                player.stop_up_down()
                            #print("event.value="+str(event.value*1))
#                             if event.value > 0.3:
#                                 player.go_up()
#                                 up_down_on = True
#                             elif event.value < -0.3:
#                                 player.go_down()
#                                 up_down_on = True
#                             
#                         if not (left_right_on or up_down_on):
#                                 player.stop()
#                                 
                    elif event.axis == 3:
                        #right_stick.y = stick_center_snap(event.value * -1)
                        pass
                    elif event.axis == 4:
                        #right_stick.x = stick_center_snap(event.value)
                        pass
                elif event.type == JOYBUTTONDOWN:
                    print("in JOYBUTTONDOWN")
                    #print('JOYBUTTONDOWN: button {}'.format(e.button))
                    #buttons[event.button].value = 1
                    if event.button == 0:
                        # jump
                        player.jump()
                    else:
                        print("event.button == "+str(event.button))
                elif event.type == JOYBUTTONUP:
                    #print('JOYBUTTONUP: button {}'.format(e.button))
                    #buttons[event.button].value = 0
                    pass
                elif event.type == JOYHATMOTION:
                    # pygame sends this; xinput sends a button instead--the handler converts the button to a hat event
                    #print('JOYHATMOTION: joy {} hat {} value {}'.format(e.joy, e.hat, e.value))
#                     if which_hat:
#                         hats[which_hat].value = 0
#                     if event.value != (0, 0):
#                         which_hat = event.value
#                         hats[which_hat].value = 1
                    pass
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit()
                

        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.x >= 500:
            diff = player.rect.x - 500
            player.rect.x = 500
            current_level.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.x <= 120:
            diff = 120 - player.rect.x
            player.rect.x = 120
            current_level.shift_world(diff)

        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

if __name__ == "__main__":
    main()
