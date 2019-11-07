To run the code:
    1) open project in pycharm, or create a new project
    2) Run the "veggieBoy.py" file (it contains the main() method)
    3) Game controls:
        - arrow keys or WASD for movement
        - p, q, r - pause, quit, restart
    4) Enjoy!


Files:
    - veggieBoy.py
        - main() method
        - all game logic
        - screen painting
    - vegetableSprite.py
        - a class used to create vegetable sprites (objects)
    - playerSprite.py
        - a class used to create the player sprite (object)
    - textBox.py
        - a class used to create textboxes (objects) to print on screen
        - in writing this README, I realize that I forgot to discuss the file in my video.  It is a simple class that allows me to build textboxes to paint on screen.  It has attributes such as: the pygame "surface" that represents the textbox, the position to paint the textbox, and the pygame.rectangle that describes where the textbox is and how big it is
    - images (folder)
        - source (unprocessed) vegetable images
        - processed vegetable and player images (.png) for use in game
    - updates and future improvements.txt
        - if anyone in the future wants to make improvements or additions to the game, this file gives some ideas
    - README.txt
        - this file
