import pygame

_TSIZE = 16
_SWIDTH = 640
_SHEIGHT = 480


class Player(pygame.sprite.Sprite):

    def __init__(self, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('assets/player.png')
        self.rect = pygame.rect.Rect((320, 240), self.image.get_size())
        self.resting = False
        self.dy = 0

    def update(self, tick, game):
        last = self.rect.copy()
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            self.rect.x -= 300 * tick
        if key[pygame.K_RIGHT]:
            self.rect.x += 300 * tick

        if self.resting and key[pygame.K_SPACE]:
            self.dy = -500
        self.dy = min(400, self.dy + 40)
        self.rect.y += self.dy * tick

        new = self.rect
        self.resting = False
        for cell in pygame.sprite.spritecollide(self, game.walls, False):
            cell = cell.rect
            if last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
            if last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
            if last.bottom <= cell.top and new.bottom > cell.top:
                self.resting = True
                new.bottom = cell.top
                self.dy = 0
            if last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom
                self.dy = 0


class Game(object):

    def __init__(self):
        super(Game, self).__init__()
        pygame.init()
        pygame.display.set_caption('PyGame Demo')
        self.screen = pygame.display.set_mode((_SWIDTH, _SHEIGHT))

    def main(self):
        clock = pygame.time.Clock()
        sprites = pygame.sprite.Group()
        self.player = Player(sprites)

        # create walls
        self.walls = pygame.sprite.Group()
        block = pygame.image.load('assets/block.png')
        for x in range(0, _SWIDTH, _TSIZE):
            for y in range(0, _SHEIGHT, _TSIZE):
                if x in (0, _SWIDTH-_TSIZE) or y in (0, _SHEIGHT-_TSIZE):
                    wall = pygame.sprite.Sprite(self.walls)
                    wall.image = block
                    wall.rect = pygame.rect.Rect((x, y), block.get_size())
        sprites.add(self.walls)

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

            self.screen.fill((55, 155, 55))
            sprites.update(tick, self)
            sprites.draw(self.screen)
            pygame.display.flip()

    @classmethod
    def start(cls):
        game = cls()
        game.main()


if __name__ == '__main__':
    Game.start()
