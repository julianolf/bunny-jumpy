import pygame


class Game(object):
    def main(self, screen):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_ESCAPE):
                    return


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('PyGame Demo')
    screen = pygame.display.set_mode((640, 480))
    game = Game()
    game.main(screen)
