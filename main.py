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
        menu = GameMenu(levels[0], screen)
        running = True
        while running:
            screen.fill(pygame.Color('black'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    pass
            menu.update(int(et))
            pygame.display.flip()
            et += self.clock.tick(self.fps) / 1000


class GameMenu:

    def __init__(self, level_state, screen):
        self.level_state = level_state
        self.screen = screen
        self.render()

    def render(self):
        self.screen.fill(pygame.Color('black'))
        sprites.generate_level(self.level_state)

    def update(self, et, key=None):
        sprites.enemy_grp.update(et)
        sprites.player_grp.update(et, key)
        sprites.player_grp.draw(self.screen)
        sprites.enemy_grp.draw(self.screen)
        sprites.box_grp.draw(self.screen)
        sprites.walls_grp.draw(self.screen)


if __name__ == '__main__':
    game = Game((1200, 800), 60)
    game.start()