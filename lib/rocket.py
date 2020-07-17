import pygame

RED = (255,50,100)

class Rocket:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game

    def draw(self):
        pygame.draw.rect(self.game.screen,
                         RED,
                         pygame.Rect(self.x, self.y, 2, 4))
        self.y -= 3
        if self.y <= 0:
            self.game.rockets.remove(self)
