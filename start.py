# Імпорт бібліотек та ініціалізація Pygame

import pygame
import random
import json
from pygame.time import get_ticks

pygame.init()
pygame.display.set_caption('50 seconds')

# Завантаження шрифту та музики, налаштування ігрового екрану

font = pygame.font.Font("timer_font.otf", 50)
bg_music_start = pygame.mixer.Sound("sounds\\start.mp3")

# Основна функція гри
def play():
    
    bg_music_start.play(-1)
    escape_zone = pygame.Rect(752, 619, 160, 135)
    picked_items = {}
    coordinates = [(670, 703),(591, 644),(765, 454),(1231, 641),(523, 276),(873, 345),(1057, 569), (1094, 694), (1332, 625), (364, 275), (625, 340), (604, 554), (469, 639), (771, 118), (783, 252), (1093, 303), (1015, 377), (820, 201), (634, 437)]

    item_images = {"book": 1, "cards": 1, "axe": 2, "masha_head": 2, "posion": 1, 
                    "radio": 2, "rifle": 2, "dima_head": 2, "map":1,"dasha_head": 2, "mask": 1, "medkit": 1, "food_can": 1, "water_bottle": 1}
    
    # Клас прдеметів які можна підібрати
    class CollectableSprite(pygame.sprite.Sprite):
        def __init__(self, name, space,image, x, y):
            super().__init__()
            self.space = space
            self.image = image
            self.name = name
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    # Клас гравця
    class Player(pygame.sprite.Sprite):
        def __init__(self, image, x, y):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (45, 40))
            
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.counter = 0
            self.speed = 2
        
        # Метод для руху гравця
        def move(self):
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w] and not self.check(self.rect.x, self.rect.y - self.speed, walls):
                self.rect.y -= self.speed
                self.animation("go_up")

            elif keys[pygame.K_s] and not self.check(self.rect.x, self.rect.y + self.speed, walls):
                self.rect.y += self.speed
                self.animation("go_back")
            
            elif keys[pygame.K_d] and not self.check(self.rect.x + self.speed, self.rect.y, walls):
                self.rect.x += self.speed
                self.animation("go_right")
                
            elif keys[pygame.K_a] and not self.check(self.rect.x - self.speed, self.rect.y, walls):
                self.rect.x -= self.speed
                self.animation("go_left")

        # Метод для анімації руху гравця
        def animation(self, kind):
            if kind == "go_up":
                self.counter+=1
                if 0 <= self.counter < 10:
                    self.image = pygame.transform.scale(pygame.image.load("images\\forward_left_leg.png").convert_alpha(), (45, 40))
                elif 10 <= self.counter < 20:
                    self.image  = pygame.transform.scale(pygame.image.load("images\\forward_right_leg.png").convert_alpha(), (45, 40))
                
                if self.counter >= 20:
                    self.counter = 0
            
            elif kind == "go_back":
                self.counter+=1
                if 0 <= self.counter < 10:
                    self.image = pygame.transform.scale(pygame.image.load("images\\back_left_leg.png").convert_alpha(), (45, 40))
                elif 10 <= self.counter < 20:
                    self.image  = pygame.transform.scale(pygame.image.load("images\\back_right_leg.png").convert_alpha(), (45, 40))
                
                if self.counter >= 20:
                    self.counter = 0
            
            elif kind == "go_left":
                self.counter+=1
                if 0 <= self.counter < 10:
                    self.image = pygame.transform.scale(pygame.image.load("images\\left_left_leg.png").convert_alpha(), (45, 40))
                elif 10 <= self.counter < 20:
                    self.image  = pygame.transform.scale(pygame.image.load("images\\left_right_leg.png").convert_alpha(), (45, 40))
                
                if self.counter >= 20:
                    self.counter = 0
            
            elif kind == "go_right":
                self.counter+=1
                if 0 <= self.counter < 10:
                    self.image = pygame.transform.scale(pygame.image.load("images\\right_left_leg.png").convert_alpha(), (45, 40))
                elif 10 <= self.counter < 20:
                    self.image  = pygame.transform.scale(pygame.image.load("images\\right_right_leg.png").convert_alpha(), (45, 40))
                
                if self.counter >= 20:
                    self.counter = 0

        # Метод для перевірки чи не врізається гравець у хітбокси
        def check(self, x, y, barriers):
            for barrier in barriers:
                if barrier.collidepoint(x, y):
                    return True
            return False

    # Словник інвентаря
    inventory = {}        

    hand_x_coordinate = 600

    count_picked_items = 0
    item_place = 0

    transperency = 0
    item_width = 60
    item_height = 90
    

    screen = pygame.display.set_mode((1600, 900))
    surface = pygame.Surface((1600, 900), pygame.SRCALPHA)

    # Завантаження картинки для заднього фону
    bg = pygame.image.load("images\\house.png").convert()
    resized_bg = pygame.transform.scale(bg, (1600, 1400))

    # Відображення Заднього фону
    screen.blit(bg, (0, 0))

    # Екземпляр класу гравця
    player = Player("images\\forward_right_leg.png",  800, 550)

    player_group = pygame.sprite.GroupSingle(player)
    collectables = pygame.sprite.Group()

    # Спавн предметів 
    for item in item_images.keys():
        if item == "food_can" or item == "water_bottle":
            for i in range(3):
                image = pygame.image.load(f"images\\{item}.png").convert_alpha()
                resized_image = pygame.transform.scale(image, (25, 30))
                coord = random.choice(coordinates)
                sprite = CollectableSprite(item, item_images[item], resized_image, coord[0], coord[1])
                coordinates.remove(coord)
                collectables.add(sprite)
        else:
            image = pygame.image.load(f"images\\{item}.png").convert_alpha()
            resized_image = pygame.transform.scale(image, (25, 30))
            coord = random.choice(coordinates)
            sprite = CollectableSprite(item, item_images[item], resized_image, coord[0], coord[1])
            coordinates.remove(coord)
            collectables.add(sprite)

    # Список хітбоксів 
    walls = [pygame.Rect(306, 183, 13, 600), pygame.Rect(722, 20, 13, 310), pygame.Rect(722, 394, 13, 148), 
            pygame.Rect(933, 20, 13, 312), pygame.Rect(933, 414, 13, 126), pygame.Rect(933, 615, 13, 233), pygame.Rect(722, 613, 13, 233), pygame.Rect(1154, 247, 13, 250),
            pygame.Rect(1370, 495, 13, 250), pygame.Rect(940, 495, 480, 11), pygame.Rect(940, 700, 480, 11), pygame.Rect(940, 246, 480, 11), pygame.Rect(316, 495, 480, 11), 
            pygame.Rect(250, 703, 480, 11), pygame.Rect(500, 33, 480, 11), pygame.Rect(250, 187, 480, 11), pygame.Rect(500, 839, 480, 11), pygame.Rect(735, 640, 51, 12), 
            pygame.Rect(888, 640, 51, 12), pygame.Rect(869, 178, 70, 12), pygame.Rect(729, 178, 70, 12), pygame.Rect(377, 385, 135, 61), pygame.Rect(382, 327, 120, 50), 
            pygame.Rect(382, 453, 122, 50), pygame.Rect(326, 582, 62, 48), pygame.Rect(323, 655, 33, 27), pygame.Rect(330, 669, 115, 50), pygame.Rect(373, 505, 100, 28), 
            pygame.Rect(902, 101, 40, 53), pygame.Rect(770, 42, 128, 36), pygame.Rect(310, 197, 410, 37), pygame.Rect(774, 818, 100, 28), pygame.Rect(776, 644, 113, 80), 
            pygame.Rect(947, 635, 30, 75), pygame.Rect(1030, 505, 130, 23), pygame.Rect(972, 256, 45, 40), pygame.Rect(1091, 376, 100, 120), pygame.Rect(969, 467, 70, 28), 
            pygame.Rect(1184, 540, 120, 54)]

    running = True
    clock = pygame.time.Clock()

    game_start = 180
    main_timer = 3060

    # Заповнення інвентарю
    def filling_inventory():
        nonlocal inventory
        nonlocal hand_x_coordinate
        for i in range(4):
            if len(inventory) < 4:
                inventory[f"hand{i}"] = hand_x_coordinate
                hand_x_coordinate+=150

    # Цикл гри
    while running:
        events = pygame.event.get()
        for event in events:
            # Перевірка чи хоче гравець вийти з гри
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        # Відображення заднього фону
        screen.blit(resized_bg, (120, -550))
        screen.blit(surface, (0, 0))

        filling_inventory()

        # Додавання премету до інвентаря
        for item in inventory.keys():
            temp = item.replace(item[-1], "")
            itm = pygame.image.load(f"images\\{temp}.png")
            resized_itm = pygame.transform.scale(itm, (item_width, item_height)).convert_alpha()
            screen.blit(resized_itm, (inventory[item], 750))
        
        # Відмальовування хітбоксів
        for wall in walls:
            pygame.draw.rect(surface, (255, 0, 0, transperency), wall)
        pygame.draw.rect(surface, (255, 255, 0, transperency), escape_zone)
        
        # Перевірка чи торкнувся гравец предмету, і якщо так, то предмет додається до інвентарю
        for coll in collectables:
            if player.rect.colliderect(coll.rect) and count_picked_items + coll.space <= 4:
                temp = 0
                for item in inventory.keys():
                    if temp < coll.space:
                        inventory[coll.name + str(item_place)] = inventory[item]

                        itm = pygame.image.load(f"images\\hand.png")
                        resized_itm = pygame.transform.scale(itm, (item_width, item_height)).convert_alpha()
                        resized_itm.set_alpha(255)
                        screen.blit(resized_itm, (inventory[item], 750))

                        del inventory[item]
                        temp += 1
                        item_place += 1
                        count_picked_items += 1
                    else:
                        break
                coll.kill()
        
        game_start -= 1
        # Запуск таймеру
        if game_start >= 0:
            count_down = int((game_start + 60) / 60)
            if count_down in range(1,4):
                pygame.draw.rect(screen, (133, 37, 51), pygame.Rect(825, 419, 80, 135))
                text_surface = font.render(str(count_down), False, "white")
                screen.blit(text_surface, (825, 419))
            else:
                pygame.draw.rect(screen, (133, 37, 51), pygame.Rect(825, 419, 80, 135))

        player_group.draw(screen)
        collectables.draw(screen)
        
        if game_start < 0:
            player.move()
            main_timer -= 1
            # Запуск основного таймеру
            if main_timer >= 0:
                count_down_main = int((main_timer) / 60)
                if count_down_main in range(1, 51):
                    pygame.draw.rect(screen, (34, 177, 76), pygame.Rect(0, 0, 80, 135))
                    text_surface_main = font.render(str(count_down_main), False, "white")
                    screen.blit(text_surface_main, (0, 0))
                else:
                    pygame.draw.rect(screen, (34, 177, 76), pygame.Rect(0, 0, 80, 135))

            # Перевірка чи дотикається гравець до жовтої зони, і якщо так, то предмети з інвентарю переходять у словник для збереження 
            if player.rect.colliderect(escape_zone):

                # Перевірка, чи скінчився таймер і гравець у жовтій зоні, якщо так, то усі предмети зберігаютсья у json файл, і вікно гри змінюєтсья, а якщо ні, то гравець програє
                if main_timer <= 0:
                    data = {}
                    picked_items['oleg_head'] = 1
                    data["items"] = picked_items
                    with open('saving_file.json', 'w') as js:
                        json.dump(data, js)
                    file = open("win_lose.txt", "w")
                    file.write("win")
                    file.close()
                    running = False
                else:
                    for item in inventory.keys():
                        corrected_item = item.replace(item[-1], "")
                        if corrected_item != "hand":
                            if corrected_item in picked_items and item_images[corrected_item] == 1:
                                picked_items[corrected_item] += 1
                            else:
                                picked_items[corrected_item] = 1
                    
                    count_picked_items = 0
                    item_place = 0
                    hand_x_coordinate = 600
                    inventory.clear()
                    filling_inventory()

            elif not player.rect.colliderect(escape_zone) and main_timer <= 0:
                file = open("win_lose.txt", "w")
                file.write("lose")
                file.close()
                running = False

        pygame.display.update()
        clock.tick(60)
    # Припинення програвання саундтреку
    bg_music_start.stop()