from gameloop import GameLoop


def main():
    game = GameLoop()
    game.set_up_game()
    game.play()

if __name__=="__main__":
    main()