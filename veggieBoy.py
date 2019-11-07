import pygame
from pygame.locals import *
import vegetableSprite
import playerSprite
import textBox
import random

class VeggieBoy:

    # constructor
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._screenSize = self._screenWidth, self._screenHeight = 600, 600


    # init program
    def on_init(self):
        pygame.init()
        logo = pygame.image.load("images/player/player.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Veggie-Boy          p = pause, r = restart, q = quit")
        self._clock = pygame.time.Clock()
        # self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_surf = pygame.display.set_mode(self._screenSize)
        self._display_surf.fill((0,0,0))
        pygame.display.flip() # paint the whole screen
        self.initSprites()
        self._scoreTextBox = textBox.TextBox(10, 10)
        self._tauntTextBox = textBox.TextBox(10, self._screenHeight - 50)
        self._tauntIndex = 0
        self._prevTimeTaunt = 0
        self._gameModeTextBox = textBox.TextBox(10, self._screenHeight - 50)
        self._livesTextBox = textBox.TextBox(self._screenWidth - 110, 10)
        self._livesRemaining = 5
        self._gameOverTextBox = textBox.TextBox()
        self._running = True
        self._updateIndex = 0
        self._deadRectangles = []
        self._prevTimeSpawnChange = 0
        self._spawnProbabilityChoice = 0
        self._NORMAL_MODE = 0
        self._SMILEYS_ONLY_MODE = 1
        self._REVERSE_KEYS_MODE = 2
        self._PLAYER_SUPER_SPEED_MODE = 3
        self._TRUMP_MODE = 4
        self._gameMode = self._NORMAL_MODE
        self._changeGameMode = 0
        self._prevTimeGameMode = 0
        self._pauseGame = False
        self._gameScore = 0
        self._gameStartStime = pygame.time.get_ticks()

    def initSprites(self):
        self._vegetableSprites = []
        self.initPlayerSprite()

    def initPlayerSprite(self):
        self._playerSprite = playerSprite.PlayerSprite()
        self._playerSprite._xPos = (self._screenWidth - pygame.Surface.get_width(self._playerSprite._image)) / 2
        self._playerSprite._yPos = (self._screenHeight - pygame.Surface.get_height(self._playerSprite._image)) / 2

    # events
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN:
            if self._pauseGame == True:
                self._pauseGame = False
            else:
                if event.key == pygame.K_p:
                    self._pauseGame = True

            if event.key == pygame.K_q:
                self._running = False

            if self._livesRemaining == 0:
                if event.key == pygame.K_r:
                    self.on_init()

    def game_over(self):
        self._gameOverTextBox._xPos = self._screenWidth // 2 - 150
        self._gameOverTextBox._yPos = self._screenHeight // 3 + 20
        self._gameOverTextBox._font = pygame.font.SysFont('Comic Sans MS', 60)
        self._gameOverTextBox._text = "game over"
        self._gameOverTextBox._textSurface = self._gameOverTextBox._font.render(self._gameOverTextBox._text, True, (200,0,0))
        self._gameOverTextBox._newRect = self._display_surf.blit(self._gameOverTextBox._textSurface, (self._gameOverTextBox._xPos, self._gameOverTextBox._yPos))
        pygame.display.update(self._gameOverTextBox._oldRect)
        pygame.display.update(self._gameOverTextBox._newRect)
        self._gameOverTextBox._oldRect = self._gameOverTextBox._newRect

    # delay for each loop cycle
    def game_rate(self):
        self._clock.tick(60)

    def manage_game_mode(self):
        if self._changeGameMode == 1:
            self._prevTimeGameMode = pygame.time.get_ticks()
            if self._gameMode == self._NORMAL_MODE:
                gameModeProbability = ([self._SMILEYS_ONLY_MODE] * 3 +
                                       [self._PLAYER_SUPER_SPEED_MODE] * 3 +
                                       [self._REVERSE_KEYS_MODE] * 3 +
                                       [self._TRUMP_MODE] * 1)
                self._gameMode = random.choice(gameModeProbability)
            self._changeGameMode = 0
        if self._gameMode != 0:
            gameModeDuration = 5000
            if self._gameMode == self._TRUMP_MODE:
                gameModeDuration *= 2
            if (pygame.time.get_ticks() - self._prevTimeGameMode) > gameModeDuration:
                self._gameMode = self._NORMAL_MODE

    # detect key presses specifically for moving the player, and set movement direction and step
    def check_movement_keys(self):
        if (self._gameMode == self._PLAYER_SUPER_SPEED_MODE):
            movementStep = 15
        else:
            movementStep = 5

        keys=pygame.key.get_pressed()
        if keys[K_w] or keys[K_UP]:
            self._playerSprite._yStep = -1 * movementStep
        if keys[K_a] or keys[K_LEFT]:
            self._playerSprite._xStep = -1 * movementStep
        if keys[K_s] or keys[K_DOWN]:
            self._playerSprite._yStep = movementStep
        if keys[K_d] or keys[K_RIGHT]:
            self._playerSprite._xStep = movementStep

        if (self._gameMode == self._REVERSE_KEYS_MODE):
            self._playerSprite._xStep *= -1
            self._playerSprite._yStep *= -1

    # all sprites move, this does the moving, elsewhere the movement direction and rate is calculated...here things are moved
    def update_sprite_positions(self):
        # for allowing things to update at different rates
        self._updateIndex += 1
        if self._updateIndex >= 65535:
            self._updateIndex = 0

        # update player location
        if (self._updateIndex % self._playerSprite._xRate) == 0:
            self._playerSprite._xPos += self._playerSprite._xStep
            self._playerSprite._xStep = 0
            # keep player in bounds
            if self._playerSprite._xPos > self._screenWidth - pygame.Surface.get_width(self._playerSprite._image):
                self._playerSprite._xPos = self._screenWidth - pygame.Surface.get_width(self._playerSprite._image)
            if self._playerSprite._xPos < 0:
                self._playerSprite._xPos = 0

        if (self._updateIndex % self._playerSprite._yRate) == 0:
            self._playerSprite._yPos += self._playerSprite._yStep
            # keep player in bounds
            if self._playerSprite._yPos > self._screenHeight - pygame.Surface.get_height(self._playerSprite._image):
                self._playerSprite._yPos = self._screenHeight - pygame.Surface.get_height(self._playerSprite._image)
            if self._playerSprite._yPos < 0:
                self._playerSprite._yPos = 0
            self._playerSprite._yStep = 0


        # update vegetable locations
        for i in range(0, len(self._vegetableSprites)):
            thisSprite = self._vegetableSprites[i]

            if (thisSprite._xRate != 0):
                if ((self._updateIndex % thisSprite._xRate) == 0):
                    thisSprite._xPos += thisSprite._xStep
                    # bounds for vegetable
                    if thisSprite._xPos > self._screenWidth + 1:
                        thisSprite._xPos = self._screenWidth + 1
                    if thisSprite._xPos < 0 - pygame.Surface.get_width(thisSprite._image) - 1:
                        thisSprite._xPos = 0 - pygame.Surface.get_width(thisSprite._image) - 1

            if (thisSprite._yRate != 0):
                if ((self._updateIndex % thisSprite._yRate) == 0):
                    thisSprite._yPos += thisSprite._yStep
                    # bounds for vegetable
                    if thisSprite._yPos > self._screenHeight + 1:
                        thisSprite._yPos = self._screenHeight + 1
                    if thisSprite._yPos < 0 - pygame.Surface.get_height(thisSprite._image) - 1:
                        thisSprite._yPos = 0 - pygame.Surface.get_height(thisSprite._image) - 1

    def detect_collisions(self):
        # must return after removing a sprite as the indicies are affected
        for i in range(0, len(self._vegetableSprites)):
            thisSprite = self._vegetableSprites[i]

            # vegetable/screen edge collision
            if thisSprite._xPos >= self._screenWidth + 1 or thisSprite._xPos <= 0 - pygame.Surface.get_width(thisSprite._image) - 1 or thisSprite._yPos >= self._screenHeight + 1 or thisSprite._yPos <= 0 - pygame.Surface.get_height(thisSprite._image) - 1:
                # self._deadRectangles.append(thisSprite._oldRect)
                self._vegetableSprites.remove(thisSprite)
                self._gameScore += 1
                return

            # vegetable/player collision
            if thisSprite.detectCollision(self._playerSprite):
                self._changeGameMode = 1
                if self._livesRemaining > 0:
                    self._livesRemaining -= 1
                self._vegetableSprites.remove(thisSprite)
                self._deadRectangles.append(thisSprite._oldRect)
                return

    def create_vegetables(self):
		# as time goes on, we want more veggies on screen
        minVegetableCount = 5 + ((pygame.time.get_ticks() - self._gameStartStime) // 5000)
        defaultStep = 5
        minSpeed = 1
        maxSpeed = 3
        while len(self._vegetableSprites) < minVegetableCount:
            if self._gameMode == self._SMILEYS_ONLY_MODE:
                tempSprite = vegetableSprite.VegetableSprite("images/player/player.png")
            elif self._gameMode == self._TRUMP_MODE:
                tempSprite = vegetableSprite.VegetableSprite("trumpTime")
            else:
                tempSprite = vegetableSprite.VegetableSprite()

			# each element of this list, is a list that represents a weighted choice for where
			# vegetable will spawn, and thus which direction they will move
			# each element (list) is a chosen pattern, for example, the first entry means:
			# there is equal chance that [0] and [1] are chosen, that means there is a 50/50 chance
			# the vegeteable spawns on the top or right side of the screen, and a 0% chance it will
			# spawn on the bottom or left side of the screen
			# the patterns were fun to make and the game seems more enjoyable with patterns instead of
			# complete randomness
            vegetableSpawnProbability = ([0] * 1 + [1] * 1 + [2] * 0 + [3] * 0,
										 [0] * 1 + [1] * 0 + [2] * 1 + [3] * 0,
                                         [0] * 1 + [1] * 0 + [2] * 0 + [3] * 1,
                                         [0] * 0 + [1] * 1 + [2] * 1 + [3] * 0,
                                         [0] * 0 + [1] * 1 + [2] * 0 + [3] * 1,
                                         [0] * 0 + [1] * 0 + [2] * 1 + [3] * 1,
                                         [0] * 5 + [1] * 5 + [2] * 5 + [3] * 85,
                                         [0] * 5 + [1] * 5 + [2] * 85 + [3] * 5,
                                         [0] * 5 + [1] * 85 + [2] * 5 + [3] * 5,
                                         [0] * 85 + [1] * 5 + [2] * 5 + [3] * 5)

			# as time progresses, we change which pattern in active
            if (pygame.time.get_ticks() - self._prevTimeSpawnChange) >= 10000:
                self._prevTimeSpawnChange = pygame.time.get_ticks()
                self._spawnProbabilityChoice = random.randint(0, len(vegetableSpawnProbability) - 1)

			# depending on where the vegetable spawns, we need to pick the correct movement direction and speed
            randomValue = random.choice(vegetableSpawnProbability[self._spawnProbabilityChoice])

            startingPosition = ((0 - pygame.Surface.get_width(tempSprite._image), random.randint(0, self._screenHeight - pygame.Surface.get_height(tempSprite._image))),
                                (self._screenWidth, random.randint(0, self._screenHeight - pygame.Surface.get_height(tempSprite._image))),
                                (random.randint(0, self._screenWidth - pygame.Surface.get_width(tempSprite._image)), 0 - pygame.Surface.get_height(tempSprite._image)),
                                (random.randint(0, self._screenWidth - pygame.Surface.get_width(tempSprite._image)), self._screenHeight))

            movementStep = ((defaultStep, 0),
                            (-1 * defaultStep, 0),
                            (0, defaultStep),
                            (0, -1 * defaultStep))

            movementRate = ((random.randint(minSpeed, maxSpeed), 0),
                            (random.randint(minSpeed, maxSpeed), 0),
                            (0, random.randint(minSpeed, maxSpeed)),
                            (0, random.randint(minSpeed, maxSpeed)))

			# all of these values (position and movement) are saved into the vegetable object
            (tempSprite._xPos, tempSprite._yPos) = startingPosition[randomValue]
            (tempSprite._xStep, tempSprite._yStep) = movementStep[randomValue]
            (tempSprite._xRate, tempSprite._yRate) = movementRate[randomValue]

            self._vegetableSprites.append(tempSprite)


    # paint/repaint things
    def on_render(self):
        # background fill for _oldRect locations and destroyed sprites
        self._display_surf.fill((0,0,0))

        # text stuff
        self._scoreTextBox._text = "score: %d" % self._gameScore
        self._scoreTextBox._textSurface = self._scoreTextBox._font.render(self._scoreTextBox._text, True, (200,200,200))
        self._scoreTextBox._newRect = self._display_surf.blit(self._scoreTextBox._textSurface, (self._scoreTextBox._xPos, self._scoreTextBox._yPos))
        # pygame.display.update(self._scoreTextBox._oldRect)
        # pygame.display.update(self._scoreTextBox._newRect)
        # self._scoreTextBox._oldRect = self._scoreTextBox._newRect

        taunts = ("let's go!!!",
                  "you need practice",
                  "aren't veggies good for you?",
                  "quick! look behind you!",
                  "try AVOIDING the veggies",
                  "don't you have chores?",
                  "whose cat is this?",
                  "can you shovel my driveway?",
                  "come on, get serious",
                  "don't you hate commercials?",
                  "do you know where Ljubljana is?",
                  "ya, tomato is a fruit, so what?")

        gameModes = ("normal",
                     "smileys only",
                     "reverse movement",
                     "player super speed",
                     "oh, dear god no!!!")

        if (pygame.time.get_ticks() - self._prevTimeTaunt) >= 5000:
            self._prevTimeTaunt = pygame.time.get_ticks()
            self._tauntIndex = random.randint(1, len(taunts) - 1)

        if self._gameMode == 0:
            self._tauntTextBox._text = taunts[self._tauntIndex]
            self._tauntTextBox._textSurface = self._tauntTextBox._font.render(self._tauntTextBox._text, True, (200,200,200))
            self._tauntTextBox._newRect = self._display_surf.blit(self._tauntTextBox._textSurface, (self._tauntTextBox._xPos, self._tauntTextBox._yPos))
            # pygame.display.update(self._tauntTextBox._oldRect)
            # pygame.display.update(self._gameModeTextBox._oldRect)
            # pygame.display.update(self._tauntTextBox._newRect)
            # self._tauntTextBox._oldRect = self._tauntTextBox._newRect
        else:
            self._gameModeTextBox._text = "game mode: " + gameModes[self._gameMode]
            self._gameModeTextBox._textSurface = self._gameModeTextBox._font.render(self._gameModeTextBox._text, True, (0,200,0))
            self._gameModeTextBox._newRect = self._display_surf.blit(self._gameModeTextBox._textSurface, (self._gameModeTextBox._xPos, self._gameModeTextBox._yPos))
            # pygame.display.update(self._gameModeTextBox._oldRect)
            # pygame.display.update(self._tauntTextBox._oldRect)
            # pygame.display.update(self._gameModeTextBox._newRect)
            # self._gameModeTextBox._oldRect = self._gameModeTextBox._newRect

        self._livesTextBox._text = "lives: %d" % self._livesRemaining
        self._livesTextBox._textSurface = self._livesTextBox._font.render(self._livesTextBox._text, True, (200,200,200))
        self._livesTextBox._newRect = self._display_surf.blit(self._livesTextBox._textSurface, (self._livesTextBox._xPos, self._livesTextBox._yPos))
        # pygame.display.update(self._livesTextBox._oldRect)
        # pygame.display.update(self._livesTextBox._newRect)
        # self._livesTextBox._oldRect = self._livesTextBox._newRect

        # player location
        # paint location for _newRect
        self._playerSprite._newRect = self._display_surf.blit(self._playerSprite._image, (self._playerSprite._xPos, self._playerSprite._yPos))

        # update locations on screen for _oldRect and _newRect
        # pygame.display.update(self._playerSprite._oldRect)
        # pygame.display.update(self._playerSprite._newRect)

        # save _newRect as _oldRect for next update
        # self._playerSprite._oldRect = self._playerSprite._newRect
        # end of player location

        # vegetable locations
        for i in range(0, len(self._vegetableSprites)):
            thisSprite = self._vegetableSprites[i]

            # paint location for _newRect
            thisSprite._newRect = self._display_surf.blit(thisSprite._image, (thisSprite._xPos, thisSprite._yPos))

            # update locations on screen for _oldRect and _newRect
            # pygame.display.update(thisSprite._oldRect)
            # pygame.display.update(thisSprite._newRect)

            # save _newRect as _oldRect for next update
            # thisSprite._oldRect = thisSprite._newRect
        # end of vegetable locations

        # clearing rectangles for destroyed sprites
        # for i in range(0, len(self._deadRectangles)):
        #     pygame.display.update(self._deadRectangles[i])

        # self._deadRectangles.clear()
        # end of destroyed rectangles

        pygame.display.flip()

    # ending the program
    def on_cleanup(self):
        pygame.quit()

    # main loop
    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            if self._livesRemaining > 0:
                if self._pauseGame == False:
                    self.manage_game_mode()
                    self.check_movement_keys()
                    self.update_sprite_positions()
                    self.detect_collisions()
                    self.create_vegetables()
                    self.on_render()
                    self.game_rate()
            else:
                self.game_over()
        self.on_cleanup()

def main():
    theApp = VeggieBoy()
    theApp.on_execute()

# calling "function" for main program
if __name__ == "__main__" :
    main()
