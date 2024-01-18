import pygame
import os

SPRITES = dict()
all_sprites = pygame.sprite.Group()
walls_grp = pygame.sprite.Group()
enemy_grp = pygame.sprite.Group()
box_grp = pygame.sprite.Group()
player_grp = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('assets', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname).convert_alpha()
    return image


def load_sprites():
    global SPRITES
    sp_img = load_image('sprites.png')

    SPRITES['U'] = [sp_img.subsurface(0, 0, 16, 16), sp_img.subsurface(16, 0, 16, 16)]
    SPRITES['H'] = [sp_img.subsurface(0, 16, 16, 16), sp_img.subsurface(16, 16, 16, 16)]
    SPRITES['W'] = [sp_img.subsurface(32, 0, 16, 16)]
    SPRITES['B'] = [sp_img.subsurface(48, 0, 16, 16)]
    SPRITES['P'] = [sp_img.subsurface(32, 16, 16, 16), sp_img.subsurface(48, 16, 16, 16)]
    SPRITES['V'] = [sp_img.subsurface(0, 32, 16, 16), sp_img.subsurface(16, 32, 16, 16),
                    sp_img.subsurface(32, 32, 16, 16), sp_img.subsurface(48, 32, 16, 16)]


def get_sprite(obj_id, direction, animid=0, cell_size=100):
    sprite = SPRITES[obj_id]
    animid %= len(sprite)
    if obj_id in ['U', 'H']:
        sprite = sprite[animid]
        if direction[0] < 0:
            sprite = pygame.transform.flip(sprite, True, False)
    elif obj_id == 'V':
        _k = 2 if direction[1] < 0 else 0
        sprite = sprite[animid % 2 + _k]
    elif obj_id == 'P':
        sprite = sprite[animid]
    else:
        sprite = sprite[0]
    sprite = pygame.transform.scale(sprite, (cell_size, cell_size))
    return sprite


class Sprite(pygame.sprite.Sprite):

    def __init__(self, obj_id, x, y, direction, group):
        super().__init__(group)
        cell_size = 100
        self.obj_id = obj_id
        self.direction = direction
        self.image = get_sprite(obj_id, direction)
        self.rect = self.image.get_rect()
        self.rect.x = x * cell_size
        self.rect.y = y * cell_size


class User(Sprite):

    def __init__(self, x, y):
        super().__init__('U', x, y, (1, 0), player_grp)

    def update(self, et, key):
        # if key == pygame.K_RIGHT:
        #     self.direction = (1, 0)
        # elif key == pygame.K_LEFT:
        #     self.direction = (-1, 0)
        self.image = get_sprite(self.obj_id, self.direction, et)


class Permanent(Sprite):

    def __init__(self, x, y):
        super().__init__('P', x, y, (0, 0), enemy_grp)

    def update(self, et):
        self.image = get_sprite(self.obj_id, self.direction, et)


class Vertical(Sprite):

    def __init__(self, x, y, direction=(0, 1)):
        super().__init__('V', x, y, direction, enemy_grp)

    def update(self, et):
        self.image = get_sprite(self.obj_id, self.direction, et)


class Horizontal(Sprite):

    def __init__(self, x, y, direction=(1, 0)):
        super().__init__('H', x, y, direction, enemy_grp)

    def update(self, et):
        self.image = get_sprite(self.obj_id, self.direction, et)


class Box(Sprite):

    def __init__(self, x, y):
        super().__init__('B', x, y, (0, 0), box_grp)


class Wall(Sprite):

    def __init__(self, x, y):
        super().__init__('W', x, y, (0, 0), walls_grp)


def generate_level(level):
    player, x, y = None, None, None
    for y in range(8):
        for x in range(12):
            if level[y][x] == 'W':
                Wall(x, y)
            elif level[y][x] == 'P':
                Permanent(x, y)
            elif level[y][x] == 'U':
                User(x, y)
            elif level[y][x] == 'H':
                Horizontal(x, y)
            elif level[y][x] == 'V':
                Vertical(x, y)
            elif level[y][x] == 'B':
                Box(x, y)
