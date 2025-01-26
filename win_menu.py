import pygame  # Імпорт бібліотеки Pygame для роботи з графікою та ігровими елементами

pygame.init()  # Ініціалізація Pygame
pygame.display.set_caption('50 seconds')  # Встановлення заголовка вікна

font = pygame.font.Font("timer_font.otf", 50)  # Завантаження шрифту для використання у грі

def win_screen():  # Оголошення функції для екрану перемоги
    running = True  # Флаг, який вказує на те, що гра продовжується
    screen = pygame.display.set_mode((1600,900))  # Створення вікна гри з розмірами 1600x900
    surface = pygame.Surface((1600,900), pygame.SRCALPHA)  # Створення поверхні для прозорості

    # Створення словника з кнопками: назва кнопки, текст кнопки, обмежувальний прямокутник та прозорість
    buttons = {"play_button": [font.render("ДАЛІ", False, "white"), pygame.Rect(1330, 750, 220, 120), 120],
               "exit_button": [font.render("ВИХІД", False, "white"), pygame.Rect(20, 750, 260, 120), 120]}

    while running:  # Початок головного циклу гри
        mouse_pos = pygame.mouse.get_pos()  # Отримання позиції миші
        events = pygame.event.get()  # Отримання подій від користувача
        screen.fill((0,0,0))  # Заповнення екрана чорним кольором
        screen.blit(surface,(0,0))  # Відображення поверхні на екрані

        for event in events:  # Обробка подій
            if event.type == pygame.QUIT:  # Якщо користувач натиснув на кнопку закриття
                running = False  # Завершення гри
                pygame.quit()  # Вимкнення Pygame
            elif event.type == pygame.MOUSEBUTTONUP:  # Якщо користувач відпустив кнопку миші
                for button in buttons.values():  # Перевірка всіх кнопок
                    if button[1].collidepoint(mouse_pos):  # Якщо миша наведена на кнопку
                        file = open("win_menu_choice.txt", "w")  # Відкриття файлу для запису вибору користувача
                        file.write("play")  # Запис "play" у файл
                        file.close()  # Закриття файлу
                        running = False  # Завершення гри
        screen.blit(font.render("ВИ ДОЙШЛИ ДО СХОВИЩА!", False, "white"), (420, 50))  # Відображення тексту на екрані

        # Відображення кнопки "ДАЛІ" на екрані
        pygame.draw.rect(surface, (220,220,220, buttons["play_button"][2]), buttons["play_button"][1])
        screen.blit(buttons["play_button"][0], (1350,775))

        # Відображення кнопки "ВИХІД" на екрані
        pygame.draw.rect(surface, (220,220,220, buttons["exit_button"][2]), buttons["exit_button"][1])
        screen.blit(buttons["exit_button"][0], (45,780))

        pygame.display.flip()  # Оновлення вікна гри
