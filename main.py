import pygame
import sprites
from tools import load_levels


class Game:

    def __init__(self, resolution, fps):
        self.resolution = resolution
        self.fps = fps
        self.clock = None

    def start(self):
        pygame.init()
        screen = pygame.display.set_mode(self.resolution)
        self.clock = pygame.time.Clock()
        et = 0
        key = None
        levels = load_levels()
        sprites.load_sprites()
        cur_lvl = 0
        menu = GameMenu(levels[cur_lvl], screen)
        running = True
        while running:
            screen.fill(pygame.Color('black'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    key = event.key
            menu.update(int(et), key=key)
            if not sprites.enemy_grp.sprites():
                cur_lvl += 1
                if cur_lvl > len(levels) + 1:
                    pygame.quit()
                menu.level_state = levels[cur_lvl]
                menu.render()
            if not sprites.player_grp.sprites():
                menu.level_state = levels[cur_lvl]
                menu.render()
            key = None
            pygame.display.flip()
            et += 3 * self.clock.tick(self.fps) / 1000


class GameMenu:

    def __init__(self, level_state, screen):
        self.level_state = level_state
        self.screen = screen
        self.render()

    def render(self):
        self.screen.fill(pygame.Color('black'))
        sprites.generate_level(self.level_state)

    def update(self, et, key=None):
        step = not (key is None)
        sprites.enemy_grp.update(et, step)
        sprites.player_grp.update(et, key)
        sprites.box_grp.update()
        sprites.player_grp.draw(self.screen)
        sprites.enemy_grp.draw(self.screen)
        sprites.box_grp.draw(self.screen)
        sprites.walls_grp.draw(self.screen)


if __name__ == '__main__':
    game = Game((1200, 800), 60)
    game.start()