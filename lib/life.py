import pygame

player_gif = pygame.image.load("images/player.gif")

class Life:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game

    def draw(self):
        self.game.screen.blit(player_gif, (self.x, self.y))
