import sqlite3

import pygame
import sys
from datetime import datetime
from Buttons import Button
from main import Game

# Инициализация pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 900, 600
MAX_FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

clock = pygame.time.Clock()

# Загрузка и установка курсора
cursor = pygame.image.load("assets/sto.png")
pygame.mouse.set_visible(False)  # Скрываем стандартный курсор


# Создаем главное меню(Основное окно)
def main_menu():
    # Создание кнопок
    start_button = Button(WIDTH / 2 - (252 / 2), 150, 252, 74, "Новая игра",
                          "image_button.jpg", "image_button_hover.jpg", 'song.mp3')
    info_button = Button(WIDTH / 2 - (252 / 2), 250, 252, 74, "Информация",
                         "image_button.jpg", "image_button_hover.jpg", 'song.mp3')
    rules_button = Button(WIDTH / 2 - (252 / 2), 350, 252, 74, "Правила",
                          "image_button.jpg", "image_button_hover.jpg", 'song.mp3')
    exit_button = Button(WIDTH / 2 - (252 / 2), 450, 252, 74, "Выйти", "image_button.jpg",
                         "image_button_hover.jpg", 'song.mp3')

    running = True
    while running:
        screen.fill((0, 0, 0))

        font = pygame.font.Font(None, 72)
        text_surface = font.render("Invader Are Out Of The Law", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH / 2, 100))
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == start_button:
                print("Кнопка 'Старт' была нажата!")
                fade()
                new_game()

            if event.type == pygame.USEREVENT and event.button == info_button:
                print("Кнопка 'Информация' была нажата!")
                fade()
                info_menu()

            if event.type == pygame.USEREVENT and event.button == rules_button:
                print("Кнопка 'Правила' была нажата!")
                fade()
                rules_menu()

            if event.type == pygame.USEREVENT and event.button == exit_button:
                pygame.quit()
                sys.exit()

            for btn in [start_button, info_button, exit_button, rules_button]:
                btn.handle_event(event)

        for btn in [start_button, info_button, exit_button, rules_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        # Отображение курсора в текущей позиции мыши
        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x - 2, y - 2))

        pygame.display.flip()


# Функция для вывода текста в окно
def text(text_main, size, color, pos):
    font = pygame.font.Font(None, size)
    x, y = pos
    for line in text_main.split('\n'):
        string_rendered = font.render(line, 1, color)
        intro_rect = string_rendered.get_rect()
        y += 10
        intro_rect.top = y
        intro_rect.x = 10
        y += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def new_name():
    pass


# Создание окна информации
def info_menu():
    pygame.display.set_caption("Information")
    back_button = Button(WIDTH / 2 - (252 / 2), 350, 252, 74, "Назад", "image_button.jpg",
                         "image_button_hover.jpg", 'song.mp3')

    running = True
    while running:
        screen.fill((0, 0, 0))

        text("История игры Invader Are Out Of The Law", 60, (255, 255, 255), (WIDTH / 2, 50))
        text(
            "В далеком космосе находилась мальнекая планета\n"
            "Жители, населявшие ее были счастливы до одного момента\n"
            "В их покой вторглись злые захватчики, которые несли уничтожение \n"
            "Пришельцы захотели захватить замок главного правителя\n"
            "Пожалуйста, помоги им уничтожить захватчиков\n",
            36, (255, 255, 255), (WIDTH / 2, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Возврат в меню
                if event.key == pygame.K_ESCAPE:
                    fade()
                    running = False

            if event.type == pygame.USEREVENT and event.button == back_button:
                fade()
                running = False

            for btn in [back_button]:
                btn.handle_event(event)

        for btn in [back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        # Отображение курсора в текущей позиции мыши
        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x - 2, y - 2))

        pygame.display.flip()


def new_game():
    pygame.display.set_caption("Game")
    # Создание кнопок
    back_welcome = Button(WIDTH / 2 - (252 / 2), 350, 252, 74, "Продолжить",
                          "image_button.jpg", "image_button_hover.jpg", 'song.mp3')

    running = True
    while running:
        screen.fill((0, 0, 0))

        text("Добро пожаловать в игру!", 72, (255, 255, 255), (WIDTH / 2, 100))

        # Проверки событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Возврат в меню
                if event.key == pygame.K_ESCAPE:
                    running = False

            # Возврат в меню
            if event.type == pygame.USEREVENT and event.button == back_welcome:
                print("Кнопка 'Добро пожаловать' была нажата!")
                game = Game((1200, 800), 60)
                steps = game.start()
                if steps is not None:
                    record_menu(steps)

            for btn in [back_welcome]:
                btn.handle_event(event)

        for btn in [back_welcome]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x - 2, y - 2))

        pygame.display.flip()


# Содание Правил
def rules_menu():
    pygame.display.set_caption("Rules")
    back_button = Button(WIDTH / 2 - (252 / 2), 450, 252, 74, "Назад", "image_button.jpg",
                         "image_button_hover.jpg", 'song.mp3')

    running = True
    while running:
        screen.fill((0, 0, 0))

        text("Правила игры:", 60, (255, 255, 255), (WIDTH / 2, 50))
        text(
            "Ваш игровой персонаж - это рыцарь\n"
            "Им помжно управлять при помощи стрелочек\n"
            "Рыцарь может передвигать коробку с оружием\n"
            "Также вы можете перезапустить уровень при помощи клавиши 'R' \n"
            "или вернуться в меню при помощи клавиши 'N'\n"
            "Ваша цель уничтожить всех пришельцевЮ, они умирают только \n"
            "когда вы придеватите их коробкой об кирпичную стену\n"
            "Важно это сделать за минимальное количество ходов\n"

            , 36, (255, 255, 255), (WIDTH / 2, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fade()
                    running = False

            if event.type == pygame.USEREVENT and event.button == back_button:
                fade()
                running = False

            for btn in [back_button]:
                btn.handle_event(event)

        for btn in [back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x - 2, y - 2))

        pygame.display.flip()


def record_menu(steps):
    connect = sqlite3.connect('assets/records.sqlite')
    font_data = pygame.font.Font(None, 36)
    font_intro = pygame.font.Font(None, 72)
    date = datetime.now().strftime("%D-%H:%M:%S")
    query_write = f"""INSERT INTO results(date,steps) VALUES("{date}",{steps})"""
    connect.cursor().execute(query_write)
    connect.commit()
    data = sorted(connect.cursor().execute("SELECT * FROM results").fetchall(), key=lambda x: x[1])[:10]

    def render(screen, font_data, font_intro, data, cell_width, cell_height, shift_x, shift_y):
        text_intro = font_intro.render('Результаты', 1, pygame.Color('white'))
        text_rect = text_intro.get_rect()
        text_rect.x, text_rect.y = WIDTH // 2 - 50, 25
        screen.blit(text_intro, text_rect)
        for i, row in enumerate(data):
            for j, cell in enumerate(row):
                cell_text = font_data.render(str(cell), 1, pygame.Color('red'))
                cell_rect = cell_text.get_rect()
                cell_rect.x = j * cell_width + 2 + shift_x
                cell_rect.y = i * cell_height + 2 + shift_y
                rect = pygame.Rect(j * cell_width + shift_x, i * cell_height + shift_y, cell_width, cell_height)
                pygame.draw.rect(screen, pygame.Color('white'), rect, width=2)
                screen.blit(cell_text, cell_rect)

    running = True
    while running:
        screen.fill(pygame.Color('black'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        render(screen, font_data, font_intro, data, 200, 50, WIDTH // 2 - 100, 100)
        pygame.display.flip()
        clock.tick(MAX_FPS)
    connect.close()


# затемнение
def fade():
    running = True
    fade_alpha = 0  # Уровень прозрачности для анимации

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Анимация затухания текущего экрана
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

        # Увеличение уровня прозрачности
        fade_alpha += 5
        if fade_alpha >= 105:
            fade_alpha = 255
            running = False

        pygame.display.flip()
        clock.tick(MAX_FPS)  # Ограничение FPS


if __name__ == "__main__":
    main_menu()
