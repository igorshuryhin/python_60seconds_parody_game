import pygame

pygame.init()
pygame.display.set_caption('50 seconds')

font = pygame.font.Font("timer_font.otf", 50)

def gameover_screen():
    running = True
    screen = pygame.display.set_mode((1600,900))
    surface = pygame.Surface((1600,900), pygame.SRCALPHA)

    buttons = {"menu_button": [font.render("ДО ГОЛОВНОГО МЕНЮ", False, "white"), pygame.Rect(480, 750, 760, 120), 120],
               "exit_button": [font.render("ВИХІД", False, "white"), pygame.Rect(20, 750, 260, 120), 120]}
    

    while running:
        mouse_pos = pygame.mouse.get_pos()
        events = pygame.event.get()
        screen.fill((0,0,0))
        screen.blit(surface,(0,0))
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in buttons.values():
                    if button[1].collidepoint(mouse_pos):
                        file = open("game_over_choice.txt", "w")
                        file.write("menu")
                        file.close()
                        running = False
        screen.blit(font.render("ВИ ПРОГРАЛИ!", False, "white"), (520, 50))
            
        pygame.draw.rect(surface, (220,220,220, buttons["menu_button"][2]), buttons["menu_button"][1])
        screen.blit(buttons["menu_button"][0], (500,775))

        pygame.draw.rect(surface, (220,220,220, buttons["exit_button"][2]), buttons["exit_button"][1])
        screen.blit(buttons["exit_button"][0], (45,780))

        pygame.display.flip()