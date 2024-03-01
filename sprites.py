import pygame
import os
import sys

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


def load_levels():
    levels = []
    for file in os.listdir('assets/level_maps'):
        with open(f'assets/level_maps/{file}') as file_in:
            level = [list(map(lambda x: x, line.rstrip('\n'))) for line in file_in.readlines()[:8]]
            levels.append(level)
    return levels


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
        self.cell_size = 100
        self.obj_id = obj_id
        self.direction = direction
        self.image = get_sprite(obj_id, direction)
        self.rect = self.image.get_rect()
        self.rect.x = x * self.cell_size
        self.rect.y = y * self.cell_size


class User(Sprite):

    def __init__(self, x, y):
        super().__init__('U', x, y, (1, 0), player_grp)

    def update(self, et, key):
        if key == pygame.K_RIGHT:
            self.direction = (1, 0)
            self.rect = self.rect.move(self.cell_size, 0)
            if pygame.sprite.spritecollideany(self, walls_grp):
                self.rect = self.rect.move(-self.cell_size, 0)
            if box := pygame.sprite.spritecollideany(self, box_grp):
                if not box.pushable(key):
                    self.rect = self.rect.move(-self.cell_size, 0)
        elif key == pygame.K_LEFT:
            self.direction = (-1, 0)
            self.rect = self.rect.move(-self.cell_size, 0)
            if pygame.sprite.spritecollideany(self, walls_grp):
                self.rect = self.rect.move(self.cell_size, 0)
            if box := pygame.sprite.spritecollideany(self, box_grp):
                if not box.pushable(key):
                    self.rect = self.rect.move(self.cell_size, 0)
        elif key == pygame.K_DOWN:
            self.rect = self.rect.move(0, self.cell_size)
            if pygame.sprite.spritecollideany(self, walls_grp):
                self.rect = self.rect.move(0, -self.cell_size)
            if box := pygame.sprite.spritecollideany(self, box_grp):
                if not box.pushable(key):
                    self.rect = self.rect.move(0, -self.cell_size)
        elif key == pygame.K_UP:
            self.rect = self.rect.move(0, -self.cell_size)
            if pygame.sprite.spritecollideany(self, walls_grp):
                self.rect = self.rect.move(0, self.cell_size)
            if box := pygame.sprite.spritecollideany(self, box_grp):
                if not box.pushable(key):
                    self.rect = self.rect.move(0, self.cell_size)
        elif key == pygame.K_r:
            self.remove(player_grp)
        if pygame.sprite.spritecollideany(self, enemy_grp):
            self.remove(player_grp)
        self.image = get_sprite(self.obj_id, self.direction, et)


class Permanent(Sprite):

    def __init__(self, x, y):
        super().__init__('P', x, y, (0, 0), enemy_grp)

    def update(self, et, step):
        self.image = get_sprite(self.obj_id, self.direction, et)
        if pygame.sprite.spritecollideany(self, walls_grp):
            self.remove(enemy_grp)

    def push(self, key):
        if key == pygame.K_RIGHT:
            self.rect = self.rect.move(self.cell_size, 0)
        elif key == pygame.K_LEFT:
            self.rect = self.rect.move(-self.cell_size, 0)
        elif key == pygame.K_DOWN:
            self.rect = self.rect.move(0, self.cell_size)
        elif key == pygame.K_UP:
            self.rect = self.rect.move(0, -self.cell_size)


class Vertical(Sprite):

    def __init__(self, x, y, direction=(0, 1)):
        super().__init__('V', x, y, direction, enemy_grp)

    def update(self, et, step):
        self.image = get_sprite(self.obj_id, self.direction, et)
        if step:
            if self.direction[1] == 1:
                self.rect = self.rect.move(0, self.cell_size)
                if pygame.sprite.spritecollideany(self, walls_grp) or pygame.sprite.spritecollideany(self, box_grp):
                    self.rect = self.rect.move(0, -2 * self.cell_size)
                    self.direction = (0, -1)
                    if pygame.sprite.spritecollideany(self, box_grp) or pygame.sprite.spritecollideany(self, walls_grp):
                        self.rect = self.rect.move(0, self.cell_size)
            elif self.direction[1] == -1:
                self.rect = self.rect.move(0, -self.cell_size)
                if pygame.sprite.spritecollideany(self, walls_grp) or pygame.sprite.spritecollideany(self, box_grp):
                    self.rect = self.rect.move(0, 2 * self.cell_size)
                    self.direction = (0, 1)
                    if pygame.sprite.spritecollideany(self, box_grp) or pygame.sprite.spritecollideany(self, walls_grp):
                        self.rect = self.rect.move(0, -self.cell_size)
        if pygame.sprite.spritecollideany(self, walls_grp):
            self.remove(enemy_grp)

    def push(self, key):
        if key == pygame.K_RIGHT:
            self.rect = self.rect.move(self.cell_size, 0)
        elif key == pygame.K_LEFT:
            self.rect = self.rect.move(-self.cell_size, 0)
        elif key == pygame.K_DOWN:
            self.rect = self.rect.move(0, self.cell_size)
        elif key == pygame.K_UP:
            self.rect = self.rect.move(0, -self.cell_size)


class Horizontal(Sprite):

    def __init__(self, x, y, direction=(1, 0)):
        super().__init__('H', x, y, direction, enemy_grp)

    def update(self, et, step):
        self.image = get_sprite(self.obj_id, self.direction, et)
        if step:
            if self.direction[0] == 1:
                self.rect = self.rect.move(self.cell_size, 0)
                if pygame.sprite.spritecollideany(self, walls_grp) or pygame.sprite.spritecollideany(self, box_grp):
                    self.rect = self.rect.move(-2 * self.cell_size, 0)
                    self.direction = (-1, 0)
                    if pygame.sprite.spritecollideany(self, box_grp) or pygame.sprite.spritecollideany(self, walls_grp):
                        self.rect = self.rect.move(self.cell_size, 0)
            elif self.direction[0] == -1:
                self.rect = self.rect.move(-self.cell_size, 0)
                if pygame.sprite.spritecollideany(self, walls_grp) or pygame.sprite.spritecollideany(self, box_grp):
                    self.rect = self.rect.move(2 * self.cell_size, 0)
                    self.direction = (1, 0)
                    if pygame.sprite.spritecollideany(self, box_grp) or pygame.sprite.spritecollideany(self, walls_grp):
                        self.rect = self.rect.move(-self.cell_size, 0)
        if pygame.sprite.spritecollideany(self, walls_grp):
            self.remove(enemy_grp)

    def push(self, key):
        if key == pygame.K_RIGHT:
            self.rect = self.rect.move(self.cell_size, 0)
        elif key == pygame.K_LEFT:
            self.rect = self.rect.move(-self.cell_size, 0)
        elif key == pygame.K_DOWN:
            self.rect = self.rect.move(0, self.cell_size)
        elif key == pygame.K_UP:
            self.rect = self.rect.move(0, -self.cell_size)


class Box(Sprite):

    def __init__(self, x, y):
        super().__init__('B', x, y, (0, 0), box_grp)

    def update(self):
        if enemy := pygame.sprite.spritecollideany(self, enemy_grp):
            enemy_grp.remove_internal(enemy)

    def pushable(self, key):
        box_grp_without_that_box = box_grp.copy()
        box_grp_without_that_box.remove_internal(self)
        moves = {pygame.K_RIGHT: [(self.cell_size, 0), (-self.cell_size, 0)],
                 pygame.K_LEFT: [(-self.cell_size, 0), (self.cell_size, 0)],
                 pygame.K_DOWN: [(0, self.cell_size), (0, -self.cell_size)],
                 pygame.K_UP: [(0, -self.cell_size), (0, self.cell_size)]}
        self.rect = self.rect.move(*moves[key][0])
        if pygame.sprite.spritecollideany(self, walls_grp):
            self.rect = self.rect.move(*moves[key][1])
            return False
        if enemy := pygame.sprite.spritecollideany(self, enemy_grp):
            enemy.push(key)
        if box := pygame.sprite.spritecollideany(self, box_grp_without_that_box):
            if not box.pushable(key):
                self.rect = self.rect.move(*moves[key][1])
                return False
        return True


class Wall(Sprite):

    def __init__(self, x, y):
        super().__init__('W', x, y, (0, 0), walls_grp)


def generate_level(level):
    enemy_grp.empty()
    player_grp.empty()
    box_grp.empty()
    walls_grp.empty()
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
