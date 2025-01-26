# Імпорт необхідних бібліотек для роботи програми
import pygame
import json
from start import play  # Імпорт функції play з файлу start.py
from game_over import gameover_screen  # Імпорт функції gameover_screen з файлу game_over.py
from main_game_gameover import main_gameover  # Імпорт функції main_gameover з файлу main_game_gameover.py
from win_menu import win_screen  # Імпорт функції win_screen з файлу win_menu.py
from main_game import gameplay  # Імпорт функції gameplay з файлу main_game.py
import os

# Ініціалізація Pygame
pygame.init()
pygame.display.set_caption("50 seconds")

# Завантаження фонової музики
bg_music = pygame.mixer.Sound("sounds\\main_menu.mp3")

# Шлях до файлу збереження
path = "saving_file.json"

# Функція для відображення налашувань
def options():
    # Створення вікна для налашувань
    screen = pygame.display.set_mode((1600, 900))
    surface = pygame.Surface((1600, 900), pygame.SRCALPHA)
    running = True
    bg = pygame.image.load("images\\main_menu_bg.jpg").convert()
    font = pygame.font.Font(None, 100)
    # Кнопки налаштувань
    buttons = {"back_button": [font.render("НАЗАД", False, "white"), pygame.Rect(100, 70, 260, 120), 120]}

    while running:
        mouse_pos = pygame.mouse.get_pos()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False 
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in buttons.values():
                    if button[1].collidepoint(mouse_pos):
                        running = False
            # Зміна кольору кнопки при наведенні
            for button in buttons.values():
                if button[1].collidepoint(mouse_pos):
                    button[2] = 255
                else:
                    button[2] = 120

            screen.blit(bg, (0,0))
            screen.blit(surface, (0,0))

            pygame.draw.rect(surface, (105,105,105, buttons["back_button"][2]), buttons["back_button"][1])
            screen.blit(buttons["back_button"][0], (100,100))

        pygame.display.update()
    main_menu()

# Головне меню гри
def main_menu():
    bg_music.stop()
    bg_music.play(-1)
    screen = pygame.display.set_mode((1600, 900))
    surface = pygame.Surface((1600, 900), pygame.SRCALPHA)
    running = True
    bg = pygame.image.load("images\\main_menu_bg.jpg").convert()
    font = pygame.font.Font(None, 100)
    # Кнопки головного меню
    buttons = {"play_button": [font.render("НОВА ГРА", False, "white"), pygame.Rect(400, 220, 390, 120), 120, "play"],
               "options_button": [font.render("НАЛАШТУВАННЯ", False, "white"), pygame.Rect(530, 370, 650, 120), 120, "options"],
               "exit_button": [font.render("ВИХІД", False, "white"), pygame.Rect(700, 520, 260, 120), 120, "exit"],
               "continue_button": [font.render("ПРОДОВЖИТИ", False, "white"), pygame.Rect(800, 220, 570, 120), 120, "continue"]}
    
    window = None
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        events = pygame.event.get()
        screen.blit(bg, (0, 0))
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in buttons.values():
                    if button[1].collidepoint(mouse_pos):
                        window = button[3]
                        running = False

        for button in buttons.values():
            if button[1].collidepoint(mouse_pos):
                button[2] = 255
            else:
                button[2] = 120

        screen.blit(surface, (0, 0))
        
        # Відображення кнопок головного меню
        pygame.draw.rect(surface, (105,105,105, buttons["play_button"][2]), buttons["play_button"][1])
        screen.blit(buttons["play_button"][0], (420,250))

        if os.path.isfile(path):
            pygame.draw.rect(surface, (105,105,105, buttons["continue_button"][2]), buttons["continue_button"][1])
            screen.blit(buttons["continue_button"][0], (820,250))

        pygame.draw.rect(surface, (105,105,105, buttons["options_button"][2]), buttons["options_button"][1])
        screen.blit(buttons["options_button"][0], (550,400))

        pygame.draw.rect(surface, (105,105,105, buttons["exit_button"][2]), buttons["exit_button"][1])
        screen.blit(buttons["exit_button"][0], (720,550))
        
        pygame.display.update()

    # Виклик функцій в залежності від вибору користувача
    if window == "play":
        bg_music.stop()
        play()
        # Отримання результату гри
        file = open("win_lose.txt", "r")
        line = file.readline()
        file.close()
        if line == "lose":
            gameover_screen()
            file = open("game_over_choice.txt", "r")
            line = file.read()
            file.close()
            if line == "menu":
                main_menu()
        if line == "win":
            win_screen()
            file = open("win_menu_choice.txt", "r")
            line = file.read()
            file.close()
            
            if line == "play":
                gameplay()
                file = open("main_game_final.json", "r")
                data = json.load(file)
                file.close()
                if data["callback"] == "end":
                    main_gameover()
                    os.remove("saving_file.json")
                    file = open("main_gameover_choice.txt", "r")
                    line = file.read()
                    file.close()
                    if line != "quit":
                        main_menu()
    
    elif window == "continue":
        bg_music.stop()
        gameplay()
        file = open("main_game_final.json", "r")
        data = json.load(file)
        file.close()
        if data["callback"] == "end":
            main_gameover()
            os.remove("saving_file.json")
            file = open("main_gameover_choice.txt", "r")
            line = file.read()
            file.close()
            if line != "quit":
                main_menu()
    elif window == "options":
        options()
    
    else:
        pygame.quit()
        exit()
        
# Виклик головного меню гри
main_menu()
