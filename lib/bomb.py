import pygame

YELLOW = (255,255,0)

class Bomb:
    def __init__(self, game, x, y, size):
        self.x = x
        self.y = y
        self.game = game
        self.size = size

    def draw(self):
        pygame.draw.rect(self.game.screen,
                        YELLOW,
                        pygame.Rect(self.x, self.y, self.size, self.size))
        self.y += 2

    def checkCollision(self, game):
        for rocket in game.rockets:
            if (rocket.x <= self.x + self.size and
                    rocket.x >= self.x and
                    rocket.y <= self.y + self.size and
                    rocket.y >= self.y):
                game.rockets.remove(rocket)
                game.bombs.remove(self)
                game.score += 25 * (6 - self.size)
