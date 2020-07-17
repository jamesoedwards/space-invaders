import pygame
import random

from lib.ammo import Ammo
from lib.generator import Generator
from lib.life import Life
from lib.player import Player
from lib.screentext import ScoreText, WaveText
from lib.ufo import Ufo
from lib.functions import pause, wait

BLACK  = (0,0,0)
WHITE  = (255,255,255)
GREEN  = (128,128,0)

pygame.init()
end_screen = pygame.image.load("images/endscreen.gif")

class Game:

    def __init__(self, width, height):
        self.width  = width
        self.height = height

        self.player = None
        self.screen = None
        self.font   = None
        self.clock  = None

        self.aliens  = []
        self.ufos    = []
        self.rockets = []
        self.bombs   = []
        self.lives   = []

        self.scoreText = ScoreText(self, 10, 10)
        self.waveText  = WaveText(self, 500, 10)
        self.ammo      = Ammo(self, 515, 525)

        self.lost            = False
        self.newwave         = False
        self.wave            = 1
        self.alien_direction = random.choice([-1,1])
        self.lives_count     = 3
        self.score           = 0
        self.max_ammo        = 6
        self.top_enemy_y     = 0

    def run(self):
        pygame.display.set_caption("Space Invaders")
        pygame.font.init()
        self.font = pygame.font.SysFont('courier', 18)

        self.screen = pygame.display.set_mode((self.width, self.height+100))
        self.clock = pygame.time.Clock()

        self.alien_speed = 0.09 + 0.01 * self.wave
        Generator(self, self.alien_speed)

        self.player = Player(self, self.width / 2, self.height - 20)
        l_x = 30
        l_y = 530
        for i in range(self.lives_count):
            self.lives.append(Life(self, l_x, l_y))
            l_x += 50

        done = False
        while not done:
            if self.lives_count == 0:
                done = True
                self.gameOver()
                break

            if len(self.aliens) == 0:
                self.score += 50
                self.newwave = True

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                self.player.moveLeft()
            elif pressed[pygame.K_RIGHT]:
                self.player.moveRight()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.lost:
                    self.player.fire()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    textsurface = self.font.render("PAUSED", False, WHITE)
                    self.screen.blit(textsurface, (270, 300))
                    pygame.display.flip()
                    pause()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    done = True
                    self.gameOver()
                    break

            pygame.display.flip()
            self.clock.tick(60)
            self.screen.fill(BLACK)
            self.newWave()
            self.redraw()
        # End: while not done

    def newWave(self):
        if self.newwave or self.top_enemy_y > 0.5 * self.height:
            self.score += 100 * self.wave
            self.alien_speed += 0.01
            self.wave += 1
            Generator(self, self.alien_speed)
            self.newwave = False
        self.top_enemy_y = self.height

    def redraw(self):
        for alien in self.aliens:
            alien.draw()
            alien.checkCollision(self)
            if (alien.y > self.height - 24):
                done = True
                self.gameOver()
                break
            elif (alien.y < self.top_enemy_y):
                self.top_enemy_y = alien.y
            alien.drop()
            if (alien.x > self.width - 25 or alien.x < 25):
                self.shiftAliens()

        for ufo in self.ufos:
            ufo.draw()
            ufo.checkCollision(self)
            ufo.drop()
        if len(self.ufos) == 0:
            game.ufos.append(Ufo(game, random.choice([-self.width, 2*self.width]), 28))

        for rocket in self.rockets:
            rocket.draw()

        for bomb in self.bombs:
            if bomb.y > self.height:
                self.score += 1
                self.bombs.remove(bomb)
            else:
                bomb.draw()

        if not self.lost: 
            self.player.draw()
            self.player.checkCollision(self)
            self.scoreText.draw()
            self.waveText.draw()
            self.ammo.draw()
            for life in self.lives:
                life.draw()

        # ground
        pygame.draw.line(self.screen, GREEN, (0,505), (600,505), 5)


    def shiftAliens(self):
        self.alien_direction *= -1
        for alien in self.aliens:
            alien.y += 24

    def gameOver(self):
        print("Game over!")
        self.lost = True
        self.screen.fill(BLACK)
        self.screen.blit(end_screen, (0,0))
        textsurface = self.font.render("Final score: %s" % self.score, False, WHITE)
        self.screen.blit(textsurface, (210, 350))
        textsurface2 = self.font.render("Press enter...", False, WHITE)
        self.screen.blit(textsurface2, (225, 400))
        pygame.display.flip()
        wait()


if __name__ == '__main__':
    game = Game(600, 500)
    game.run()

