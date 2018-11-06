import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('assets/player.png')
        self.rect = pygame.rect.Rect((320, 240), self.image.get_size())

    def update(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            self.rect.x -= 10
        if key[pygame.K_RIGHT]:
            self.rect.x += 10
        if key[pygame.K_UP]:
            self.rect.y -= 10
        if key[pygame.K_DOWN]:
            self.rect.y += 10


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
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_ESCAPE):
                    return

            self.screen.fill((200, 200, 200))
            sprites.update()
            sprites.draw(self.screen)
            pygame.display.flip()

    @classmethod
    def start(cls):
        game = cls()
        game.main()


if __name__ == '__main__':
    Game.start()
