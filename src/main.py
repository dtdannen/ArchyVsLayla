'''
Created on Jan 23, 2016

@author: Dustin
'''

import pygame
import xinput
import platform
from operator import attrgetter

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
    pygame.init()
    # first get the controller
    joystick = get_360_controller()
    
    pass

if __name__ == '__main__':
    print("Successfully imported pygame!")