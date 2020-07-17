from lib.alien import Alien

class Generator:
    def __init__(self, game, speed):
        x_margin = 25
        y_margin = 45
        height = 40
        width  = 50
        for x in range(x_margin, game.width - x_margin, width):
            if game.alien_direction == -1:
                x += 50
            for y in range(y_margin, int(game.height / 2) - y_margin, height):
                game.aliens.append(Alien(game, x, y, speed))
