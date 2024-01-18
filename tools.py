import os


def load_levels():
    levels = []
    for file in os.listdir('assets/level_maps'):
        with open(f'assets/level_maps/{file}') as file_in:
            level = [list(map(lambda x: x, line.rstrip('\n'))) for line in file_in.readlines()[:8]]
            levels.append(level)
    return levels
