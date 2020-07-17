import pygame
from lib.rocket import Rocket

player_gif = pygame.image.load("images/player.gif")

class Player:
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y
        self.size = 24
        self.hit = False
        self.hit_iter = 0

    def draw(self):
        if not self.hit:
            self.game.screen.blit(player_gif, (self.x - 12, self.y))
        else:
            if self.hit_iter == 24:
                self.game.screen.blit(player_gif, (self.x - 12, self.y))
                self.hit_iter = 0
                self.hit = False
            elif self.hit_iter % 6 in [0,1,2]:
                self.game.screen.blit(player_gif, (self.x - 12, self.y))
                self.hit_iter += 1
            else:
                self.hit_iter += 1


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
                self.hit = True
