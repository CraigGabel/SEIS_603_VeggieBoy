import pygame
from pygame.locals import *



class TextBox:

    def __init__(self, x = 0, y = 0):
        self._position = self._xPos, self._yPos = x, y # set the default starting position
        self._font = pygame.font.SysFont('Comic Sans MS', 30)
        self._text = ""
        self._textSurface = self._font.render(self._text, True, (200,200,200))
        self._newRect = pygame.Rect(0,0,0,0) # create instance variables for where the block was, and where it is
        self._oldRect = pygame.Rect(0,0,0,0)
