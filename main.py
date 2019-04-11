from game import Game

if __name__ == "__main__":
    demo = Game()
    demo.splash_screen()
    while demo.running:
        demo.new()
