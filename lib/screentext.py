WHITE  = (255,255,255)

class ScoreText:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y

    def draw(self):
        textsurface = self.game.font.render("Score: %s" % self.game.score, False, WHITE)
        self.game.screen.blit(textsurface, (self.x, self.y))


class WaveText:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y

    def draw(self):
        textsurface = self.game.font.render("Wave: %s" % self.game.wave, False, WHITE)
        self.game.screen.blit(textsurface, (self.x, self.y))
