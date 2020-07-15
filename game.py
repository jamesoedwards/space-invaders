import pygame
import random

def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                return

class Game:
    screen = None
    aliens = []
    rockets = []
    bombs = []
    lost = False

    def __init__(self, width, height):
        pygame.init()
        pygame.display.set_caption("Space Invaders")
        pygame.font.init()
        self.font = pygame.font.SysFont('courier', 18)

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        done = False
        alien_speed = 0.05

        hero = Hero(self, width / 2, height - 20)
        Generator(self, alien_speed)
        self.score = 0
        scoreText = ScoreText(self, 10, 10)
        rocket = None

        self.wave = 1
        waveText = WaveText(self, 500, 10)
        wave_rate = 10000
        newwave = False
        timer = 0
        dt = 0
        while not done:
            if len(self.aliens) == 0:
                newwave = True

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                hero.x -= 2 if hero.x > 20 else 0
            elif pressed[pygame.K_RIGHT]:
                hero.x += 2 if hero.x < width - 20 else 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.lost:
                    self.rockets.append(Rocket(self, hero.x, hero.y+3))

            pygame.display.flip()
            dt = self.clock.tick(60)
            self.screen.fill((0, 0, 0))
            timer += dt
            if timer >= wave_rate * self.wave:
                newwave = True

            if newwave and top_enemy_y > 0.5 * height:
                alien_speed += 0.01
                self.wave += 1
                Generator(self, alien_speed)
                newwave = False

            top_enemy_y = height

            for alien in self.aliens:
                alien.draw()
                alien.checkCollision(self)
                if (alien.y > height - 24):
                    done = True
                    self.gameOver()
                    break
                elif (alien.y < top_enemy_y):
                    top_enemy_y = alien.y
                else:
                    alien.drop()

            for rocket in self.rockets:
                rocket.draw()

            for bomb in self.bombs:
                bomb.draw()

            if not self.lost: 
                hero.draw()
                scoreText.draw()
                waveText.draw()

    def gameOver(self):
        print("Game over!")
        self.lost = True
        end_screen = pygame.image.load("endscreen.gif")
        self.screen.fill((0,0,0))
        self.screen.blit(end_screen, (0,0))
        pygame.display.flip()
        wait()



class Alien:
    def __init__(self, game, x, y, speed):
        self.x = x
        self.game = game
        self.y = y
        self.speed = speed
        self.size = 24

    def draw(self):
        alien_gif = pygame.image.load("invader.gif")
        self.game.screen.blit(alien_gif, (self.x-12, self.y))
        self.y += self.speed

    def drop(self):
        if random.random() < 0.001:
            self.game.bombs.append(Bomb(self.game, self.x, self.y))

    def checkCollision(self, game):
        for rocket in game.rockets:
            if (rocket.x < self.x + 0.5*self.size and
                    rocket.x > self.x - 0.5*self.size and
                    rocket.y < self.y + 0.5*self.size and
                    rocket.y > self.y - 0.5*self.size):
                game.rockets.remove(rocket)
                game.aliens.remove(self)
                game.score += 10


class Hero:
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y

    def draw(self):
        hero_gif = pygame.image.load("player.gif")
        self.game.screen.blit(hero_gif, (self.x-12, self.y))

    def checkCollision(self, game):
        for bomb in game.bombs:
            if (bomb.x < self.x + 0.5*self.size and
                    bomb.x > self.x - 0.5*self.size and
                    bomb.y < self.y + 0.5*self.size and
                    bomb.y > self.y - 0.5*self.size):
                game.bombs.remove(bomb)
                # lose a life


class Generator:
    def __init__(self, game, speed):
        margin = 30
        height = 40
        width  = 50
        for x in range(margin, game.width - margin, width):
            for y in range(margin, int(game.height / 2) - margin, height):
                game.aliens.append(Alien(game, x, y, speed))

class Bomb:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game

    def draw(self):
        pygame.draw.rect(self.game.screen,
                        (255, 255, 0),
                        pygame.Rect(self.x, self.y, 3, 3))
        self.y += 2


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

class ScoreText:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y

    def draw(self):
        textsurface = self.game.font.render("Score: %s" % self.game.score, False, (255, 255, 255))
        self.game.screen.blit(textsurface, (self.x, self.y))

class WaveText:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y

    def draw(self):
        textsurface = self.game.font.render("Wave: %s" % self.game.wave, False, (255, 255, 255))
        self.game.screen.blit(textsurface, (self.x, self.y))

if __name__ == '__main__':
    game = Game(600, 400)
