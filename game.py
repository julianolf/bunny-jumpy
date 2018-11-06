import pygame


class Game(object):

    def __init__(self):
        super(Game, self).__init__()
        pygame.init()
        pygame.display.set_caption('PyGame Demo')
        self.screen = pygame.display.set_mode((640, 480))

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_ESCAPE):
                    return

    @classmethod
    def start(cls):
        game = cls()
        game.main()


if __name__ == '__main__':
    Game.start()
