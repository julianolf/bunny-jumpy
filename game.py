import pygame


class Game(object):

    def __init__(self):
        super(Game, self).__init__()
        pygame.init()
        pygame.display.set_caption('PyGame Demo')
        self.screen = pygame.display.set_mode((640, 480))

    def main(self):
        clock = pygame.time.Clock()
        image = pygame.image.load('assets/player.png')
        position = [320, 240]

        while True:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_ESCAPE):
                    return

            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                position[0] -= 10
            if key[pygame.K_RIGHT]:
                position[0] += 10
            if key[pygame.K_UP]:
                position[1] -= 10
            if key[pygame.K_DOWN]:
                position[1] += 10

            self.screen.fill((200, 200, 200))
            self.screen.blit(image, tuple(position))
            pygame.display.flip()

    @classmethod
    def start(cls):
        game = cls()
        game.main()


if __name__ == '__main__':
    Game.start()
