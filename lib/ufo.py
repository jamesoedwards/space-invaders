import pygame, random
from lib.bomb import Bomb

ufo_gif    = pygame.image.load("images/ufo.gif")

class Ufo:
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y
        self.speed = 1.9 + 0.1 * self.game.wave
        self.direction = -1
        self.size = 36

    def draw(self):
        self.game.screen.blit(ufo_gif, (self.x-18, self.y-8))
        self.x += self.direction * self.speed
        if self.x < -self.game.width or self.x > 2 * self.game.width:
            self.direction *= -1

    def drop(self):
        if self.x < self.game.width and self.x > 0:
            if random.random() < 0.009 + 0.001 * self.game.wave:
                self.game.bombs.append(Bomb(self.game, self.x-2, self.y+2, 5))

    def checkCollision(self, game):
        for rocket in game.rockets:
            if (rocket.x < self.x + 0.5*self.size and
                    rocket.x >= self.x - 0.5*self.size and
                    rocket.y < self.y + 0.25*self.size and
                    rocket.y > self.y - 0.25*self.size):
                game.rockets.remove(rocket)
                game.ufos.remove(self)
                game.score += 250
