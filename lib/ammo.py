import pygame

WHITE  = (255,255,255)
ammo_gif   = pygame.image.load("images/ammo.gif")

class Ammo:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game

    def draw(self):
        self.game.screen.blit(ammo_gif, (self.x, self.y))
        remaining_ammo = self.game.max_ammo - len(self.game.rockets)
        textsurface = self.game.font.render(str(remaining_ammo), False, WHITE)
        self.game.screen.blit(textsurface, (self.x + 35, self.y + 10))
