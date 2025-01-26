import pygame
from abc import ABC, abstractmethod

# Ініціалізація Pygame
pygame.init()

# Завантаження звукових ефектів
leaf_sfx = pygame.mixer.Sound("sounds\\leaf.mp3")
picking_items = pygame.mixer.Sound("sounds\\picking_item.mp3")

# Абстрактний клас для об'єктів гри
class Object(ABC):
    @abstractmethod
    def update(self, events):
        pass

# Клас для предметів "їжа/вода"
class FoodWater(Object, pygame.sprite.Sprite):
    def __init__(self, x, y, name, image, func):
        super().__init__()
        # Ініціалізація властивостей предмета
        self.name = name
        self.amount = 1
        self.image_name = image
        self.image = pygame.image.load(f"images\\{self.image_name}.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.callback = func

    def update(self, events):
        # Оновлення стану предмета залежно від подій
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(mouse_pos):
                    self.callback(self.name, self.rect.x, self.rect.y)

# Клас для клікабельних спрайтів
class ClickableSprite(Object, pygame.sprite.Sprite):
    def __init__(self, x, y, name, image, func):
        super().__init__()
        # Ініціалізація властивостей клікабельного спрайту
        self.name = name
        self.image = pygame.image.load(f"images\\{image}.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.callback = func

    def update(self, events):
        # Оновлення стану клікабельного спрайту залежно від подій
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(mouse_pos):
                    self.callback(self.name, self.rect.x, self.rect.y)

# Клас для журнальних спрайтів
class JournalSprite(Object, pygame.sprite.Sprite):
    def __init__(self, x, y, image, func):
        super().__init__()
        # Ініціалізація властивостей журнального спрайту
        self.image = pygame.image.load(f"images\\{image}.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if func:
            self.callback = func

    def update(self, events):
        # Оновлення стану спрайту
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(mouse_pos):
                    self.callback()

# Клас для кнопок
class Button(Object, pygame.sprite.Sprite):
    def __init__(self, x, y, image, transperency, journal_group, buttons_group, func=None, extra_argument=None, width=None, height=None):
        super().__init__()
        # Ініціалізація властивостей кнопки
        self.image_name = image 
        self.image = pygame.image.load(f"images\\{self.image_name}.png").convert_alpha()
        if width and height:
            self.image = pygame.transform.scale(self.image, (width, height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked_times = 0
        self.transperency = transperency
        self.image.set_alpha(self.transperency)
        self.extra_argument = extra_argument
        self.callback = func
        self.journal_group = journal_group
        self.buttons_group = buttons_group
    
    def update(self, events):
        # Оновлення стану кнопки залежно від подій
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(mouse_pos) and self.callback:
                    self.clicked_times += 1
                    self.image.set_alpha([self.transperency, 255][self.clicked_times % 2])
                    if self.callback.__name__ == "close_button":
                        self.callback(self.journal_group, self.buttons_group)
                        picking_items.play()
                    elif self.callback.__name__ in ["on_click_journal_icon", "next_button", "back_button"]:
                        leaf_sfx.play()
                        self.callback()
                    else: 
                        self.callback(self)
                        picking_items.play()

# Клас персонажа
class Character(Object, pygame.sprite.Sprite):
    def __init__(self, x, y, name, image, func):
        super().__init__()
        # Ініціалізація властивостей персонажа
        self.hunger = 100
        self.thirst = 100
        self.hunger_status = None
        self.thirst_status = None
        self.name = name
        self.image_name = image
        self.image = pygame.image.load(f"images\\{self.image_name}.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.callback = func

    def minus_hunger_thirst(self):
        self.hunger -= 10
        self.thirst -= 20

    def eat(self):
        if self.hunger + 40 <= 100:
            self.hunger += 40
        else:
            self.hunger = 100

    def drink(self):
        if self.thirst + 40 <= 100:
            self.thirst += 40
        else:
            self.thirst = 100

    def update(self, events):
        # Оновлення стану персонажа залежно від подій
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(mouse_pos):
                    self.callback(self.name, [self.thirst_status, self.hunger_status], self.rect.x, self.rect.y)

    def update_status(self):
        # Оновлення статусу персонажа в залежності від значень голоду та спраги
        if self.hunger <= 60:
            self.hunger_status = "Голодування"
        if self.thirst <= 40:
            self.thirst_status = "Зневоднення"
        elif self.thirst <= 60:
            self.thirst_status = "Спрага"

        if self.thirst >= 100:
            self.thirst_status = None
        if self.hunger >= 100:
            self.hunger_status = None

# Клас для предметів їжі/води в журналі
class FoodWaterJournal(Object, pygame.sprite.Sprite):
    def __init__(self, x, y, whome, image, transperency, func):
        super().__init__()
        # Ініціалізація властивостей предмету їжі/води в журналі
        self.whome = whome
        self.image_name = image
        self.image = pygame.transform.scale(pygame.image.load(f"images\\{self.image_name}.png"), (20, 40)).convert_alpha()
        self.image.set_alpha(transperency)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked_times = 0
        self.callback = func
    
    def update(self, events):
        # Оновлення стану предмету їжі/води в журналі залежно від подій
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(mouse_pos):
                    picking_items.play()
                    self.clicked_times += 1
                    self.callback(self)

# Клас для голови персонажа у блокноті
class Head(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        # Ініціалізація властивостей голови персонажа
        self.image = pygame.transform.scale(pygame.image.load(f"images\\{image}.png"), (50, 70))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Клас для зображення в журналі
class JournalImage(pygame.sprite.Sprite):
    def __init__(self, x, y, image, width, height):
            super().__init__()
            # Ініціалізація властивостей зображення в журналі
            self.image = pygame.transform.scale(pygame.image.load(f"images\\{image}.png"), (width, height)).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y


