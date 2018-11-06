import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('assets/player.png')
        self.rect = pygame.rect.Rect((320, 240), self.image.get_size())

    def update(self, tick):
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            self.rect.x -= 300 * tick
        if key[pygame.K_RIGHT]:
            self.rect.x += 300 * tick
        if key[pygame.K_UP]:
            self.rect.y -= 300 * tick
        if key[pygame.K_DOWN]:
            self.rect.y += 300 * tick


class Game(object):

    def __init__(self):
        super(Game, self).__init__()
        pygame.init()
        pygame.display.set_caption('PyGame Demo')
        self.screen = pygame.display.set_mode((640, 480))

    def main(self):
        clock = pygame.time.Clock()
        sprites = pygame.sprite.Group()
        self.player = Player(sprites)

        while True:
            # force 30fps
            # getting the current frame rate
            # and converting to seconds
            tick = clock.tick(30) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_ESCAPE):
                    return

            self.screen.fill((200, 200, 200))
            sprites.update(tick)
            sprites.draw(self.screen)
            pygame.display.flip()

    @classmethod
    def start(cls):
        game = cls()
        game.main()


if __name__ == '__main__':
    Game.start()
