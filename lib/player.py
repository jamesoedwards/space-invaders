import pygame
from lib.rocket import Rocket

player_gif = pygame.image.load("images/player.gif")

class Player:
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y
        self.size = 24

    def draw(self):
        self.game.screen.blit(player_gif, (self.x - 12, self.y))

    def fire(self):
        if len(self.game.rockets) < self.game.max_ammo:
            self.game.rockets.append(Rocket(self.game, self.x, self.y + 3))

    def moveLeft(self):
        self.x -= 2 if self.x > 20 else 0

    def moveRight(self):
        self.x += 2 if self.x < self.game.width -  20 else 0

    def checkCollision(self, game):
        for bomb in game.bombs:
            if (bomb.x < self.x + 0.55*self.size and
                    bomb.x > self.x - 0.55*self.size and
                    bomb.y < self.y + 18 + 0.35*self.size and
                    bomb.y > self.y + 18 - 0.25*self.size):
                game.bombs.remove(bomb)
                # lose a life
                game.lives_count -= 1
                game.lives.pop()
