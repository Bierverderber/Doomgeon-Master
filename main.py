import pygame
import sys
import os

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
LetsGo = False
isMouseFocused = True


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():   # функция, отвечающая за главное меню
    fon = pygame.transform.scale(load_image('doomfon.jpg'), (width, height))
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
    fon = pygame.transform.scale(load_image('floor.jpg'), (width, height))
    screen.blit(fon, (0, 0))

    doomguy = DoomGuy()
    Cacodemon()
    Aim()

    left = right = up = down = False

    while True:
        screen.fill('black')
        screen.blit(fon, (0, 0))
        BossFight_sprites.draw(screen)
        Bullets_sprites.draw(screen)
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
        DoomGuy_sprite.update(left, right, up, down)
        Bullets_sprites.update()

        pygame.display.flip()
        clock.tick(fps)


class PlayButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(PlayButton_sprite, all_sprites)
        self.image = pygame.transform.scale(load_image('playbutton.png'), (130, 100))
        self.rect = self.image.get_rect()
        self.rect.x = width // 2 - self.image.get_width() // 2
        self.rect.y = 500

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

    def update(self, left, right, up, down):
        if left:
            self.rect.x -= 300 / fps
        if right:
            self.rect.x += 300 / fps
        if up:
            self.rect.y -= 300 / fps
        if down:
            self.rect.y += 300 / fps


class Cacodemon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(Cacodemon_sprite, BossFight_sprites, all_sprites)
        self.image = pygame.transform.scale(load_image('Cacodemon.png'), (300, 300))
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 350

    def update(self):
        pass


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
        self.start_x = start_pos_x
        self.start_y = start_pos_y
        self.end_x = end_pos[0]
        self.end_y = end_pos[1]
        self.hypotenuse = round((abs(self.start_x - self.end_x) ** 2 + abs(self.start_y - self.end_y) ** 2) ** 0.5)
        self.k = round(self.hypotenuse / (200 / fps))

    def update(self):
        if self.start_x < self.end_x:
            self.rect.x += (self.end_x - self.start_x) / self.k
        else:
            self.rect.x -= (self.start_x - self.end_x) / self.k
        if self.start_y < self.end_y:
            self.rect.y += (self.end_y - self.start_y) / self.k
        else:
            self.rect.y -= (self.start_x - self.end_y) / self.k
        if 0 > self.rect.x or self.rect.x > 1200 or 0 > self.rect.y or self.rect.y > 700:
            self.kill()










start_screen()
boss_fight()