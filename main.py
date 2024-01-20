import pygame
import sys
import os
import random

pygame.init()
width, height = 1200, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Doomgeon Master')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


fps = 60
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
Logo_sprite = pygame.sprite.Group()
PlayButton_sprite = pygame.sprite.Group()
BossFight_sprites = pygame.sprite.Group()
DoomGuy_sprite = pygame.sprite.Group()
Cacodemon_sprite = pygame.sprite.Group()
Bullets_sprites = pygame.sprite.Group()
Aim_sprite = pygame.sprite.Group()
EnemyBullets_sprites = pygame.sprite.Group()
LetsGo = False
Lose = False
Win = False
isMouseFocused = True


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():   # функция, отвечающая за главное меню
    fon = pygame.transform.scale(load_image('hellfon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    PlayButton()
    Logo()

    PlayButton_sprite.draw(screen)
    Logo_sprite.draw(screen)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            PlayButton_sprite.update(event)
        if LetsGo:
            return


def boss_fight():   # Функция, отвечающая за битву с боссом
    global isMouseFocused
    fon = pygame.transform.scale(load_image('hellfloor.png'), (width, height))
    screen.blit(fon, (0, 0))

    doomguy = DoomGuy()
    cacodemon = Cacodemon()
    Aim()
    health_bar = HealthBar(250, 650, 700, 20, 250)
    doomguyhb = HealthBar(50, 50, 200, 20, 5)

    left = right = up = down = False

    while not (Lose or Win):
        if str(EnemyBullets_sprites)[7] == '0':
            cacodemon.attack(EnemyBullet)
        screen.fill('black')
        screen.blit(fon, (0, 0))
        BossFight_sprites.draw(screen)
        Bullets_sprites.draw(screen)
        EnemyBullets_sprites.draw(screen)
        health_bar.draw(screen)
        doomguyhb.draw(screen)
        if isMouseFocused:
            Aim_sprite.update(pygame.mouse.get_pos())
            Aim_sprite.draw(screen)
            pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if not pygame.mouse.get_focused():
                isMouseFocused = False
            else:
                isMouseFocused = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                Bullet(doomguy.rect.x + doomguy.image.get_width() // 2,
                       doomguy.rect.y + doomguy.image.get_height() // 2,
                       event.pos)
            if event.type == pygame.KEYDOWN:    # Передвижение Думгая
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    left = True
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    right = True
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    up = True
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    down = True
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    left = False
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    right = False
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    up = False
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    down = False
        DoomGuy_sprite.update(left, right, up, down, doomguyhb, cacodemon)
        Bullets_sprites.update(cacodemon, health_bar)
        EnemyBullets_sprites.update(doomguy, doomguyhb)
        Cacodemon_sprite.update(health_bar)

        pygame.display.flip()
        clock.tick(fps)
    return


class PlayButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(PlayButton_sprite, all_sprites)
        self.image = pygame.transform.scale(load_image('playbutton.png'), (300, 125))
        self.rect = self.image.get_rect()
        self.rect.x = width // 2 - self.image.get_width() // 2
        self.rect.y = 550

    def update(self, *args):
        global LetsGo
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            LetsGo = True


class Logo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, Logo_sprite)
        self.image = pygame.transform.scale(load_image('doomgeonmasterlogo.png'), (763, 67))
        self.rect = self.image.get_rect()
        self.rect.x = width // 2 - self.image.get_width() // 2
        self.rect.y = 100


class DoomGuy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(DoomGuy_sprite, BossFight_sprites, all_sprites)
        self.image = pygame.transform.scale(load_image('DoomGuy.png'), (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100

    def update(self, left, right, up, down, doomguyhb, cacodemon):
        global Lose
        if left:
            self.rect.x -= 300 / fps
        if right:
            self.rect.x += 300 / fps
        if up:
            self.rect.y -= 300 / fps
        if down:
            self.rect.y += 300 / fps
        if doomguyhb.hp <= 0:
            self.kill()
            Lose = True
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > width - self.image.get_width():
            self.rect.x = width - self.image.get_width()
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > height - self.image.get_height():
            self.rect.y = height - self.image.get_height()
        if pygame.sprite.spritecollideany(self, Cacodemon_sprite):
            doomguyhb.hp -= 1


class Cacodemon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(Cacodemon_sprite, BossFight_sprites, all_sprites)
        self.image = pygame.transform.scale(load_image('Cacodemon.png'), (300, 300))
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 350
        self.positions = (random.randint(1, width - self.image.get_width()),
                          random.randint(1, height - self.image.get_height()))
        self.v = 150

        self.hp = 20

    def update(self, health_bar):
        if self.positions[0] > self.rect.x:   # демон бегит
            x_move = 1
        else:
            x_move = -1
        if self.positions[1] > self.rect.y:
            y_move = 1
        else:
            y_move = -1
        if self.rect.x != self.positions[0] or self.rect.y != self.positions[1]:
            if (x_move == 1 and self.rect.x + (self.v / fps) * x_move >= self.positions[0]) \
                    or (x_move == -1 and self.rect.x + (self.v / fps) * x_move <= self.positions[0]):
                self.rect.x = self.positions[0]
            else:
                self.rect.x = self.rect.x + (self.v / fps) * x_move
            if (y_move == 1 and self.rect.y + (self.v / fps) * y_move >= self.positions[1]) \
                    or (y_move == -1 and self.rect.y + (self.v / fps) * y_move <= self.positions[1]):
                self.rect.y = self.positions[1]
            else:
                self.rect.y = self.rect.y + (self.v / fps) * y_move
        else:
            self.positions = (random.randint(1, width - self.image.get_width()),
                              random.randint(1, height - self.image.get_height()))
        if health_bar.hp <= 0:
            self.kill()

    def attack(self, EnemyBullet):
        num_attack = random.randint(1, 3)
        if num_attack == 1:
            self.attack1(EnemyBullet)
        elif num_attack == 2:
            self.attack2(EnemyBullet)
        elif num_attack == 3:
            self.attack3(EnemyBullet)

    def attack1(self, EnemyBullet):
        for j in range(5):
            for i in range(6):
                EnemyBullet(i * (width // 6) + 30, -70 * j, 2)

    def attack2(self, EnemyBullet):
        for j in range(5):
            for i in range(3):
                EnemyBullet(- 70 * j, i * (height // 4) + 40, 1)

    def attack3(self, EnemyBullet):
        EnemyBullet1 = EnemyBullet(0, 0, -2)
        EnemyBullet1.image = pygame.transform.scale(load_image('EnemyBullet.png'), (300, 300))
        EnemyBullet1.rect = EnemyBullet1.image.get_rect()
        EnemyBullet1.rect.x = 100
        EnemyBullet1.rect.y = 800

        EnemyBullet2 = EnemyBullet(0, 0, -2)
        EnemyBullet2.image = pygame.transform.scale(load_image('EnemyBullet.png'), (300, 300))
        EnemyBullet2.rect = EnemyBullet2.image.get_rect()
        EnemyBullet2.rect.x = 700
        EnemyBullet2.rect.y = 800


class Aim(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, Aim_sprite)
        self.image = pygame.transform.scale(load_image('etg_aim.png'), (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100

    def update(self, pos):
        self.rect.x = pos[0] - (self.image.get_width() // 2)
        self.rect.y = pos[1] - (self.image.get_height() // 2)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos_x, start_pos_y, end_pos):
        super().__init__(all_sprites, Bullets_sprites)
        self.image = pygame.transform.scale(load_image('bullet.png'), (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = start_pos_x
        self.rect.y = start_pos_y
        self.need_pos = (end_pos[0] - self.image.get_width() // 2, end_pos[1] - self.image.get_height() // 2)
        self.v = 400
        self.flag = True
        if abs(self.need_pos[0] - self.rect.x) > abs(self.need_pos[1] - self.rect.y):
            self.kostil = 0
        else:
            self.kostil = 1
        if self.need_pos[0] > self.rect.x:
            self.x_move = 1
        else:
            self.x_move = -1
        if self.need_pos[1] > self.rect.y:
            self.y_move = 1
        else:
            self.y_move = -1

    def update(self, cacodemon, health_bar):
        if (self.rect.x != self.need_pos[0] or self.rect.y != self.need_pos[1]) and self.flag:  # пули летают
            if (self.x_move == 1 and self.rect.x + (self.v / fps) * self.x_move >= self.need_pos[0]) \
                    or (self.x_move == -1 and self.rect.x + (self.v / fps) * self.x_move <= self.need_pos[0]):
                self.rect.x = self.need_pos[0]
            else:
                self.rect.x = self.rect.x + (self.v / fps) * self.x_move
            if (self.y_move == 1 and self.rect.y + (self.v / fps) * self.y_move >= self.need_pos[1]) \
                    or (self.y_move == -1 and self.rect.y + (self.v / fps) * self.y_move <= self.need_pos[1]):
                self.rect.y = self.need_pos[1]
            else:
                self.rect.y = self.rect.y + (self.v / fps) * self.y_move
        else:
            self.flag = False
            if self.kostil == 0:
                self.rect.x = self.rect.x + (self.v / fps) * self.x_move
            else:
                self.rect.y = self.rect.y + (self.v / fps) * self.y_move
        if pygame.sprite.spritecollideany(self, Cacodemon_sprite):
            if (cacodemon.rect.x + 70 < self.rect.x < cacodemon.rect.x + 210 and
                    cacodemon.rect.y + 85 < self.rect.y < cacodemon.rect.y + 220):
                self.kill()
                health_bar.hp -= 1
        if self.rect.x < -10 or self.rect.x > width + 10 or self.rect.y < -10 or self.rect.y > height + 10:
            self.kill()


class HealthBar():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        if self.hp > 0:
            ratio = self.hp / self.max_hp
            pygame.draw.rect(surface, (180, 0, 0), (self.x, self.y, self.w, self.h))
            pygame.draw.rect(surface, (0, 180, 0), (self.x, self.y, self.w * ratio, self.h))


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, start_pos_x, start_pos_y, need_move):
        super().__init__(all_sprites, EnemyBullets_sprites)
        self.image = pygame.transform.scale(load_image('EnemyBullet.png'), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = start_pos_x
        self.rect.y = start_pos_y
        self.v = 180
        self.need_move = need_move

    def update(self, doomguy, doomguyhb):
        if pygame.sprite.spritecollideany(self, DoomGuy_sprite):
            self.kill()
            doomguyhb.hp -= 1
        if self.need_move in (-1, 1):
            self.rect.x += (self.v // fps) * self.need_move
        elif self.need_move in (-2, 2):
            self.rect.y += (self.v // fps) * (self.need_move // 2)
        if self.rect.x < -300 or self.rect.x > width + 300 or self.rect.y < -300 or self.rect.y > height + 300:
            self.kill()








start_screen()
boss_fight()