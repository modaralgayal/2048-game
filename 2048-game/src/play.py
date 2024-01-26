""" 
The app is run from here
"""
from gameloop import GameLoop


def main():
    """ Main function """
    game = GameLoop()
    game.set_up_game()
    game.play()


if __name__ == "__main__":
    main()
