import pygame
from pygame.locals import *
import random

class VegetableSprite:

    # old list
    # vegetables = ("artichoke", "beet", "broccoli", "cabbage", "carrot", "corn", "eggplant", "garlic", "leek", "mushroom", "onion", "potato", "pumpkin", "rutabaga", "tomato", "zucchini")

    # new list
    vegetables = ("broccoli",
                  "broccoli3",
                  "carrot",
                  "carrot2",
                  "carrot3",
                  "cauliflour",
                  "cucumber",
                  "eggplant",
                  "eggplant2",
                  "eggplant3",
                  "greenOnion",
                  "greenOnion3",
                  "greenPepper",
                  "greenPepper2",
                  "iceburgLettuce",
                  "onion",
                  "onion2",
                  "peapod",
                  "peapod3",
                  "pumpkin",
                  "purple1",
                  "purple2",
                  "radish",
                  "radish3",
                  "redPepper",
                  "tomato",
                  "tomato3",
                  "yellowSquash")

    trumps = ("trump0", "trump1", "trump2", "trump3", "trump4")

    # index = 0

    def __init__(self, source = None):
        # if the vegetable type isnt given, we pick a random one
        if source == None:
            source = "images/vegetables/" + VegetableSprite.vegetables[random.randint(0, len(VegetableSprite.vegetables) - 1)] +".png"
            # source = "images/vegetables/" + VegetableSprite.vegetables[VegetableSprite.index] +".png"
            # VegetableSprite.index += 1
            # if (VegetableSprite.index >= len(VegetableSprite.vegetables)):
            #     VegetableSprite.index = 0
        elif source == "trumpTime":
            source = "images/trump/" + VegetableSprite.trumps[random.randint(0, len(VegetableSprite.trumps) - 1)] +".png"
        self._image = pygame.image.load(source) # load the image
        self._position = self._xPos, self._yPos = 0, 0 # set the default starting position
        self._xRate = self._yRate = 10 # set the update rate of motion
        self._xStep = self._yStep = 1 # set the default direction of motion
        self._newRect = pygame.Rect(0,0,0,0) # create instance variables for where the block was, and where it is
        self._oldRect = pygame.Rect(0,0,0,0)

    # used to detect if this sprite has collided with another sprite
    def detectCollision(self, inputSprite):
        return self._newRect.colliderect(inputSprite._newRect)
