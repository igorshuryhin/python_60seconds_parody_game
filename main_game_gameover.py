import pygame
import json

# Ініціалізація Pygame
pygame.init()
pygame.display.set_caption('50 seconds')

# Завантаження шрифту для використання
font = pygame.font.Font("days_font.otf", 50)

def main_gameover():
    running = True
    screen = pygame.display.set_mode((1600,900))
    surface = pygame.Surface((1600,900), pygame.SRCALPHA)
    
    # Завантаження даних з файлу JSON
    file = open("main_game_final.json", "r")
    data = json.load(file)
    file.close()

    # Створення кнопок
    buttons = {"menu_button": [font.render("ДО ГОЛОВНОГО МЕНЮ", False, "white"), pygame.Rect(480, 750, 760, 120), 120],
               "exit_button": [font.render("ВИХІД", False, "white"), pygame.Rect(20, 750, 260, 120), 120]}
    

    while running:
        mouse_pos = pygame.mouse.get_pos()
        events = pygame.event.get()
        screen.fill((0,0,0))  # Заливка екрану чорним кольором
        screen.blit(surface,(0,0))  # Відображення поверхні

        for event in events:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in buttons.values():
                    if button[1].collidepoint(mouse_pos):
                        # Запис в файл вибору користувача
                        file = open("main_gameover_choice.txt", "w")
                        file.write("menu")
                        file.close()
                        running = False
        # Відображення тексту на екрані
        screen.blit(font.render("ВИ ПРОГРАЛИ!", False, "white"), (580, 50))
        screen.blit(font.render("ДНІВ ПРОЖИТО: "+str(data["days"]), False, "white"), (540, 300))
            
        pygame.draw.rect(surface, (220,220,220, buttons["menu_button"][2]), buttons["menu_button"][1])
        screen.blit(buttons["menu_button"][0], (540,790))

        pygame.draw.rect(surface, (220,220,220, buttons["exit_button"][2]), buttons["exit_button"][1])
        screen.blit(buttons["exit_button"][0], (60,790))

        pygame.display.flip()  # Оновлення екрану

