import pygame
from pygame.locals import *

class PlayerSprite:

    def __init__(self, source = "images/player/player.png"):
        self._image = pygame.image.load(source) # load the image
        self._position = self._xPos, self._yPos = 0, 0 # set the default starting position
        self._xRate = self._yRate = 1 # set the update rate of motion
        self._xStep = self._yStep = 1 # set the default direction of motion
        self._newRect = pygame.Rect(0,0,0,0) # create instance variables for where the block was, and where it is
        self._oldRect = pygame.Rect(0,0,0,0)

    # used to detect if this sprite has collided with another sprite
    def detectCollision(self, inputSprite):
        return self._newRect.colliderect(inputSprite._newRect)

