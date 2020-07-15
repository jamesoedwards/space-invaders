import pygame

class Game:
    screen = None
    aliens = []
    rockets = []
    lost = False

    def __init__(self, width, height):
        pygame.init()
        pygame.display.set_caption("Space Invaders")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        done = False
        alien_speed = 0.05

        hero = Hero(self, width / 2, height - 20)
        Generator(self, alien_speed)
        rocket = None

        wave_rate = 6000
        timer = 0
        dt = 0
        while not done:
            if len(self.aliens) == 0:
                self.displayText("VICTORY ACHIEVED")

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                hero.x -= 2 if hero.x > 20 else 0
            elif pressed[pygame.K_RIGHT]:
                hero.x += 2 if hero.x < width - 20 else 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.lost:
                    self.rockets.append(Rocket(self, hero.x+11, hero.y+3))

            pygame.display.flip()
            dt = self.clock.tick(60)
            self.screen.fill((0, 0, 0))
            timer += dt
            if timer % wave_rate == 0:
                alien_speed += 0.01
                Generator(self, alien_speed)

            for alien in self.aliens:
                alien.draw()
                alien.checkCollision(self)
                if (alien.y > height - 24):
                    self.lost = True
                    self.displayText("YOU DIED")

            for rocket in self.rockets:
                rocket.draw()

            if not self.lost: hero.draw()

    def displayText(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        textsurface = font.render(text, False, (44, 0, 62))
        self.screen.blit(textsurface, (110, 160))


class Alien:
    def __init__(self, game, x, y, speed):
        self.x = x
        self.game = game
        self.y = y
        self.speed = speed
        self.size = 24

    def draw(self):
        alien_gif = pygame.image.load("invader.gif")
        self.game.screen.blit(alien_gif, (self.x, self.y))
        self.y += self.speed

    def checkCollision(self, game):
        for rocket in game.rockets:
            if (rocket.x < self.x + 12 + 0.5*self.size and
                    rocket.x > self.x + 12 - 0.5*self.size and
                    rocket.y < self.y + 0.5*self.size and
                    rocket.y > self.y - 0.5*self.size):
                game.rockets.remove(rocket)
                game.aliens.remove(self)


class Hero:
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y

    def draw(self):
        hero_gif = pygame.image.load("player.gif")
        self.game.screen.blit(hero_gif, (self.x, self.y))


class Generator:
    def __init__(self, game, speed):
        margin = 30
        height = 40
        width  = 50
        for x in range(margin, game.width - margin, width):
            for y in range(margin, int(game.height / 2) - margin, height):
                game.aliens.append(Alien(game, x, y, speed))


class Rocket:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game

    def draw(self):
        pygame.draw.rect(self.game.screen,
                         (254, 52, 110),
                         pygame.Rect(self.x, self.y, 2, 4))
        self.y -= 2


if __name__ == '__main__':
    game = Game(600, 400)
