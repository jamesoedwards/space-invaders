import pygame, random
from lib.bomb import Bomb

alien_gif  = pygame.image.load("images/invader.gif")

class Alien:
    def __init__(self, game, x, y, speed):
        self.x = x
        self.game = game
        self.y = y
        self.speed = speed
        self.size = 24

    def draw(self):
        self.game.screen.blit(alien_gif, (self.x-12, self.y))
        self.x += self.speed * self.game.alien_direction

    def drop(self):
        if random.random() < 0.0001 * self.game.wave:
            self.game.bombs.append(Bomb(self.game, self.x, self.y, 3))

    def checkCollision(self, game):
        for rocket in game.rockets:
            if (rocket.x < self.x + 0.5*self.size and
                    rocket.x > self.x - 0.5*self.size and
                    rocket.y < self.y + 0.5*self.size and
                    rocket.y > self.y - 0.5*self.size):
                game.rockets.remove(rocket)
                game.aliens.remove(self)
                game.score += 10


