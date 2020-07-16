import pygame
import random

pygame.init()
player_gif = pygame.image.load("player.gif")
alien_gif  = pygame.image.load("invader.gif")
ammo_gif   = pygame.image.load("ammo.gif")
ufo_gif    = pygame.image.load("ufo.gif")
end_screen = pygame.image.load("endscreen.gif")

def wait():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

class Game:

    def __init__(self, width, height):
        self.screen = None
        self.font = None
        self.clock = None
        self.aliens = []
        self.ufos = []
        self.rockets = []
        self.bombs = []
        self.lives = []
        self.lost = False
        self.width = width
        self.height = height
        self.wave = 1
        self.lives_count = 3
        self.score = 0
        self.max_ammo = 20

    def run(self):
        pygame.display.set_caption("Space Invaders")
        pygame.font.init()
        self.font = pygame.font.SysFont('courier', 18)

        self.screen = pygame.display.set_mode((self.width, self.height+100))
        self.clock = pygame.time.Clock()

        alien_speed = 0.04 + 0.01 * self.wave
        Generator(self, alien_speed)

        player = Player(self, self.width / 2, self.height - 20)
        l_x = 30
        l_y = 530
        for i in range(self.lives_count):
            self.lives.append(Life(self, l_x, l_y))
            l_x += 50

        scoreText = ScoreText(self, 10, 10)
        ammo = Ammo(self, 515, 525)
        #rocket = None

        done = False
        newwave = False
        top_enemy_y = 0
        waveText = WaveText(self, 500, 10)
        while not done:
            if self.lives_count == 0:
                done = True
                self.gameOver()
                break

            if len(self.aliens) == 0:
                self.score += 50
                self.rockets = []
                newwave = True

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                player.moveLeft()
            elif pressed[pygame.K_RIGHT]:
                player.moveRight()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.lost:
                    player.fire()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    done = True
                    self.gameOver()
                    break

            pygame.display.flip()
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))

            if newwave or top_enemy_y > 0.5 * self.height:
                self.score += 50 + 10 * self.wave
                alien_speed += 0.01
                self.wave += 1
                Generator(self, alien_speed)
                newwave = False

            top_enemy_y = self.height

            for alien in self.aliens:
                alien.draw()
                alien.checkCollision(self)
                if (alien.y > self.height - 24):
                    done = True
                    self.gameOver()
                    break
                elif (alien.y < top_enemy_y):
                    top_enemy_y = alien.y
                else:
                    alien.drop()

            for ufo in self.ufos:
                ufo.draw()
                ufo.checkCollision(self)
                ufo.drop()

            for rocket in self.rockets:
                rocket.draw()

            for bomb in self.bombs:
                bomb.draw()

            if not self.lost: 
                player.draw()
                player.checkCollision(self)
                scoreText.draw()
                waveText.draw()
                ammo.draw()
                for life in self.lives:
                    life.draw()

            # ground
            pygame.draw.line(self.screen, (128,128,0), (0,505), (600,505), 5)

        # End: while not done

    def gameOver(self):
        print("Game over!")
        self.lost = True
        self.screen.fill((0,0,0))
        self.screen.blit(end_screen, (0,0))
        textsurface = self.font.render("Final score: %s" % self.score, False, (255, 255, 255))
        self.screen.blit(textsurface, (210, 350))
        textsurface2 = self.font.render("Press enter...", False, (255, 255, 255))
        self.screen.blit(textsurface2, (225, 400))
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
        self.game.screen.blit(alien_gif, (self.x-12, self.y))
        self.y += self.speed

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

class Ufo:
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y
        self.speed = 1.9 + 0.1 * self.game.wave
        self.direction = -1
        self.size = 36

    def draw(self):
        self.game.screen.blit(ufo_gif, (self.x-18, self.y))
        self.x += self.direction * self.speed
        if self.x <= 20 or self.x >= self.game.width - 20:
            self.direction *= -1

    def drop(self):
        if random.random() < 0.01 + 0.002 * self.game.wave:
            self.game.bombs.append(Bomb(self.game, self.x, self.y, 5))

    def checkCollision(self, game):
        for rocket in game.rockets:
            if (rocket.x < self.x + 0.5*self.size and
                    rocket.x > self.x - 0.5*self.size and
                    rocket.y < self.y + 0.5*self.size and
                    rocket.y > self.y - 0.5*self.size):
                game.rockets.remove(rocket)
                game.ufos.remove(self)
                game.score += 100

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

class Life:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game

    def draw(self):
        self.game.screen.blit(player_gif, (self.x, self.y))

class Ammo:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game

    def draw(self):
        self.game.screen.blit(ammo_gif, (self.x, self.y))
        remaining_ammo = self.game.max_ammo - len(self.game.rockets)
        textsurface = self.game.font.render(str(remaining_ammo), False, (255, 255, 255))
        self.game.screen.blit(textsurface, (self.x + 35, self.y + 10))


class Generator:
    def __init__(self, game, speed):
        margin = 45
        height = 40
        width  = 50
        for x in range(margin, game.width - margin, width):
            for y in range(margin, int(game.height / 2) - margin, height):
                game.aliens.append(Alien(game, x, y, speed))
        game.ufos.append(Ufo(game, random.uniform(20,580), 28))

class Bomb:
    def __init__(self, game, x, y, size):
        self.x = x
        self.y = y
        self.game = game
        self.size = size

    def draw(self):
        pygame.draw.rect(self.game.screen,
                        (255, 255, 0),
                        pygame.Rect(self.x, self.y, self.size, self.size))
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
        if self.y <= 0:
            self.game.rockets.remove(self)

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
    game = Game(600, 500)
    game.run()
