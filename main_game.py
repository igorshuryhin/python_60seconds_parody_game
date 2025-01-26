
# Імпорт неоюхідних для роботи коду бібліотек
import pygame
import json
import math
import random

# Імпорт класів з файлу entities
from entities import *

# Імпорт тексту для сторінок блакноту
from journal_notes import journal_pages_text

pygame.init()
pygame.display.set_caption("50 seconds")

# Створення фонової музики
bg_music = pygame.mixer.Sound("sounds\\basement.mp3")

# Основний ігровий цикл
def gameplay():
    
    # Створення різних шрифтів
    font = pygame.font.Font("Propysy-Bold.otf", 15)
    notes_font = pygame.font.Font("Propysy-Bold.otf", 9)
    days_font = pygame.font.Font("days_font.otf", 80)

    # Увімкнення музики у грі
    bg_music.play(-1)

    # Виставлення розміру дісплею 
    screen = pygame.display.set_mode((1600, 900))

    # Словник з назвами предметів із значеннями у вигляді списку з елементами: ім'я предмету, список з його координатами, де 0 індекс це х, а 1 індекс це у
    # Приклад: {"назва_предмету": ["ім'я_предмету", [координта_за_х, координата_за_у]]}
    items_info = {"oleg": ["Олег", [710, 380]], "dima": ["Діма", [336, 460]], "masha": ["Маша", [490, 356]],
                  "dasha": ["Даша", [1030, 280]], "mask": ["Протигаз", [1340, 318]],
                  "rifle": ["Гвинтівка", [631, 285]], "book": ["Бойскаутський довідник", [35, 295]],
                  "cards": ["Карти", [954, 730]], "map": ["Мапа", [430, 220]], "radio": ["Радіо", [300, 429]],
                  "medkit": ["Аптечка", [1421, 316]], "posion": ["Спрей", [984, 500]], "axe": ["Сокира", [70, 525]],
                  "food_box": ["Суп", [1230, 600]], "jug": ["Вода", [1370, 630]]}
    
    # Вигруження даних з файлу збереження
    file = open("saving_file.json", "r")
    data = json.load(file)
    file.close()

    # Створення словнику з метою записування даних у файл збереження
    data_for_saving = {}

    # Створення необхідних для минання помилок ключів словника data
    data["feeding_watering"] = {}
    data["feeding_watering"]["dima"] = {"food_can": False, "water_bottle": False}
    data["feeding_watering"]["oleg"] = {"food_can": False, "water_bottle": False}
    data["feeding_watering"]["dasha"] = {"food_can": False, "water_bottle": False}
    data["feeding_watering"]["masha"] = {"food_can": False, "water_bottle": False}
    
    # Передача у словник items_data інформацію про кількість кожного предмета
    items_data = data["items"]

    # Функція яка використовується при натисканні на їжу/воду при вибору кому давати їжу
    def click_foodwater_journal(foodwater):
        # Об'явлення змінних з основної функції, для зміни даних у них
        nonlocal data
        nonlocal food

        # Змінна для перевірки чи був знайдений шуканий предмет
        item_found = None

        # Перевірка чи є кількість їжі/води більше нулю,
        if items_data[foodwater.image_name] > 0:
            # Передача у змінну clckd_times кількість натискань на картинку води/їжі, а також перевірка кількості натискань,
            # якщо кількість натискань парна, то прозорість дорівнює 120, а якщо непарна, то прозорість дорівнює 255
            clckd_times = foodwater.clicked_times
            foodwater.image.set_alpha([120, 255][clckd_times%2])
            # Якщо предмет натиснут непарну кількість раз, то temp_variabal = True, а якщо парну False
            temp_variable = [False, True][clckd_times%2]
            data["feeding_watering"][foodwater.whome][foodwater.image_name] = temp_variable
            
            # Перевірка що це за предмет, якщо вода, то кількість віднімається від води, якщо їжа, то від їжі
            if foodwater.image_name == "food_can":
                food.sprites()[len(food)-1].amount -= [-0.25, 0.25][clckd_times%2]
                item_found = "food_can"

            elif foodwater.image_name == "water_bottle":
                water.sprites()[len(water)-1].amount -= [-0.25, 0.25][clckd_times%2]
                item_found = "water_bottle"
            
            # Запис оновленної кількості предмету у словник
            data["items"][item_found] -= [-0.25, 0.25][clckd_times%2]  

    # Функція для очищення блакноту від не потрібних кнопок
    def deleting_unnecessary_buttons():
        # Список потрібних кнопок
        btns_functions = ["close_button", "back_button", "next_button"]

        # Перечислення кожної кнопки у группі buttons_group
        for btn in buttons_group:
            try:
                # Якщо кнопка не є потрібною, то її видаляють
                if btn.callback.__name__ not in btns_functions:
                    btn.kill()
            except AttributeError:
                btn.kill()

    # Функція яка використовується при натисканні на іконку блакноту
    def on_click_journal_icon():
        nonlocal journal_open

        # Додавання необхідних кнопок у блакнот
        buttons_group.add(button_next)
        journal_group.add(journal)
        buttons_group.add(button_close)
        
        journal_open = True

    # Списки для додавання або віднімання предметів при відповідному івенті
    taken_items_list = []
    given_items_list = []

    # Функція для відмальовування тексту у блакноті 
    def draw_page_text():

        # Об'явлення змінних з основної функції з метою їх подальшого змінення
        nonlocal taken_items_list
        nonlocal given_items_list
        nonlocal buttons_group
        nonlocal running
        nonlocal callback
        nonlocal days_count
        nonlocal characters 

        texts = []
        start_y = 190

        # Функція для відображення тексту
        def write_lines():
            nonlocal start_y
            for text in texts:
                screen.blit(text, (690, start_y))
                start_y+=30

        try:
            # Перевірка чи не є цей день кінцевим
            if showing_days_text != "КІНЕЦЬ":

                # Якщо екпідиція не спланована, то кнопка для початку експідиції з'являється
                if journal_pages_text[page_count][posts[page_count]]["type"] == "expedition_plan":
                    for txt in range(len(journal_pages_text[page_count][posts[page_count]]["text"])):
                        texts.append(notes_font.render(journal_pages_text[page_count][posts[page_count]]["text"][txt], False, (0, 0, 0)))
                    
                    write_lines()

                    buttons_group.add(button_expedition)
                
                # Якщо тип тексту на відповідній сторінці дорівнює "feed_water"
                elif journal_pages_text[page_count][posts[page_count]]["type"] == "feed_water":
                    for txt in range(len(journal_pages_text[page_count][posts[page_count]]["text"])):
                        texts.append(notes_font.render(journal_pages_text[page_count][posts[page_count]]["text"][txt], False, (0, 0, 0)))

                    write_lines()

                    # Перевірка хто з персонажів ще є у грі
                    if "oleg_head" in data["items"].keys():
                        buttons_group.add(oleg_head_journal)
                        buttons_group.add(oleg_food)
                        buttons_group.add(oleg_water)

                    if "dasha_head" in data["items"].keys():
                        buttons_group.add(dasha_head_journal)
                        buttons_group.add(dasha_food)
                        buttons_group.add(dasha_water)

                    if "masha_head" in data["items"].keys():
                        buttons_group.add(masha_head_journal)
                        buttons_group.add(masha_food)
                        buttons_group.add(masha_water)
                    
                    if "dima_head" in data["items"].keys():
                        buttons_group.add(dima_food)
                        buttons_group.add(dima_water)
                        buttons_group.add(dima_head_journal)

                    # Додавання спрайтів біля которих написана їх кількість
                    buttons_group.add(food_journal_sprite)
                    buttons_group.add(water_journal_sprite)

                    # Відображення тексту із кількістю води/їжі
                    try:
                        food_amount_title = font.render(f":  "+str(data["items"]["food_can"]), False, (0, 0, 0))
                    except KeyError:
                        data["items"]["food_can"] = 0
                        food_amount_title = font.render(f":  "+str(data["items"]["food_can"]), False, (0, 0, 0))
                    try:
                        water_amount_title = font.render(f":  "+str(data["items"]["water_bottle"]), False, (0, 0, 0))
                    except KeyError:
                        data["items"]["water_bottle"] = 0
                        water_amount_title = font.render(f":  "+str(data["items"]["water_bottle"]), False, (0, 0, 0))
                    screen.blit(food_amount_title, (820, 450))
                    screen.blit(water_amount_title, (820, 570))

                # Якщо тип тексту є expedition_character_choice, то виконується певних алгоритм дій
                elif journal_pages_text[page_count][posts[page_count]]["type"] == "expedition_character_choice":
                    for txt in range(len(journal_pages_text[page_count][posts[page_count]]["text"])):
                        texts.append(notes_font.render(journal_pages_text[page_count][posts[page_count]]["text"][txt], False, (0, 0, 0)))
                    
                    write_lines()

                    # Перевірка хто з персонажів ще є у грі
                    if "oleg_head" in data["items"].keys():
                        buttons_group.add(button_oleg)

                    if "dasha_head" in data["items"].keys():
                        buttons_group.add(button_dasha)

                    if "masha_head" in data["items"].keys():
                        buttons_group.add(button_masha)
                    
                    if "dima_head" in data["items"].keys():
                        buttons_group.add(button_dima)

                # Якщо тип початок типу тексту є event, то додаються кнопки для відповідей(так або ні)
                elif journal_pages_text[page_count][posts[page_count]]["type"][:5] == "event" and journal_pages_text[page_count][posts[page_count]]["type"][-1:] not in event_answers:
                    for txt in range(len(journal_pages_text[page_count][posts[page_count]]["text"])):
                        texts.append(notes_font.render(journal_pages_text[page_count][posts[page_count]]["text"][txt], False, (0, 0, 0)))
                    
                    write_lines()
                    
                    buttons_group.add(button_answer_yes)
                    buttons_group.add(button_answer_no)
                
                # Якщо тип тексту є відповіддю на подію, то виконується певний алгорітм
                elif journal_pages_text[page_count][posts[page_count]]["type"][:5] == "event" and journal_pages_text[page_count][posts[page_count]]["type"][-1:] in event_answers:
                    for txt in range(len(journal_pages_text[page_count][posts[page_count]]["text"])):
                        texts.append(notes_font.render(journal_pages_text[page_count][posts[page_count]]["text"][txt], False, (0, 0, 0)))
                    
                    write_lines()

                    # Список ключів на певній сторінці
                    key_list = list(journal_pages_text[page_count][posts[page_count]].keys())

                    # Перевірка чи ваша реакція на подію дала, або відняла у вас якісь предмети
                    if "taken_items" in key_list:
                        for item in journal_pages_text[page_count][posts[page_count]]["taken_items"].keys():
                            if item not in taken_items_list and data["items"][item]-1 >= 0:
                                data["items"][item] -= journal_pages_text[page_count][posts[page_count]]["taken_items"][item]
                                taken_items_list.append(item)
                
                    if "given_items" in key_list:
                        for item in journal_pages_text[page_count][posts[page_count]]["given_items"].keys():
                            if item not in given_items_list:
                                data["items"][item] += journal_pages_text[page_count][posts[page_count]]["given_items"][item]
                                given_items_list.append(item)

                # Якщо тип тексту є якісь іншим, то він просто вімальовується
                else:
                    for txt in range(len(journal_pages_text[page_count][posts[page_count]]["text"])):
                        texts.append(notes_font.render(journal_pages_text[page_count][posts[page_count]]["text"][txt], False, (0, 0, 0)))
                    
                    write_lines()
            
            # Якщо це кінцевий день, до видається помилка
            else:
                raise IndexError()

        # Якщо сторінки блокноту підійшли до кінця, то виконуєтсья певний алгорітм
        except IndexError:

            # Якщо це не кінцевий день, то перевіряється чи кормили ви персонажів, і до кількості днів додається +1, а також персонажі втрачають трішки голоду та спраги
            if showing_days_text != "КІНЕЦЬ":
                callback = "next_day"
                days_count+=1
                
                for character in characters:
                    if data["feeding_watering"][character.image_name.replace("_default", "")]["food_can"]:
                        character.eat()
                    if data["feeding_watering"][character.image_name.replace("_default", "")]["water_bottle"]:
                        character.drink()
                    character.minus_hunger_thirst()
            
            # Якщо це кінцевий день, то у файл main_game_final записується кількість прожитих днів і чи є цей день кінцевим
            else:
                file = open("main_game_final.json", "w")
                json.dump({"days": days_count, "callback": "end"}, file)
                file.close()
            
            # Припинення програвання музики
            bg_music.stop() 

            # Припинення гравого циклу
            running = False

            # Збереження прогресу
            saving_progress()

    # Функція для кнопки незгоди при події
    def agree_button(btn):
        nonlocal event_choice
        nonlocal button_answer_no

        button_answer_no.clicked_times+=1
        button_answer_no.image.set_alpha(120)
        
        # Якщо кількість натискань непарна, то записується реакція на подію
        event_choice = [{"type": None, "day": days_count}, {"type": btn.extra_argument, "day": days_count}][btn.clicked_times%2]

    # Функція для кнопки згоди при події
    def disagree_button(btn):
        nonlocal button_answer_yes
        nonlocal event_choice

        button_answer_yes.clicked_times+=1
        button_answer_yes.image.set_alpha(120)

        # Якщо кількість натискань непарна, то записується реакція на подію
        event_choice = [{"type": None, "day": 0}, {"type": btn.extra_argument, "day": days_count}][btn.clicked_times%2]

    # Функція для зариття блакноту
    def close_button(journal_grp, buttons):
        nonlocal journal_open, page_count
        
        # Видалення з екрану усіх кнопок та блакноту
        for journal in journal_grp:
            journal.kill()
            
        for button in buttons:
            button.kill()
        
        page_count = 0
        journal_open = False
    
    # Функція для повернення на минулу сторінку блакноту
    def back_button():
        nonlocal page_count

        # Оновлення змінною page_count
        page_count -= 1
        if page_count == 2:
            buttons_group.add(button_next)

        # Відмальовування сторінки блакноту
        deleting_unnecessary_buttons()

    # Функція для повернення на перелистування блакноту
    def next_button():
        nonlocal page_count

        # Оновлення змінною page_count
        page_count += 1
        # Відмальовування сторінки блакноту
        deleting_unnecessary_buttons()

    # Функція для натискання на персонажа
    def on_click_character(name, statuses, x, y):

        # Відмальовування ім'я персонажа
        text = font.render(name, False, (255, 255, 255))
        name_x = x + 35
        name_y = y - 35
        stats_y_start = name_y + 35
        stats_text = []

        # Відмальовування статусу персонажа

        for status in statuses:
            if status:
                stats_text.append(font.render(status, False, (204, 102, 0)))
        other.draw(screen)
        food.draw(screen)
        water.draw(screen)
        characters.draw(screen)
        journal_icon_group.draw(screen)
        journal_group.draw(screen)
        buttons_group.draw(screen)

        if len(stats_text) > 0:
            for i in stats_text:
                screen.blit(i, (name_x, stats_y_start))
                stats_y_start += 35

        screen.blit(text, (name_x, name_y))
        pygame.display.update()
        # Затримка перед зниканням тексту
        pygame.time.delay(1200)

    # Функція для натискання на предмети
    def on_click(name, x, y):

        text = font.render(name, False, (255, 255, 255))

        other.draw(screen)
        food.draw(screen)
        water.draw(screen)
        characters.draw(screen)
        journal_icon_group.draw(screen)
        journal_group.draw(screen)
        buttons_group.draw(screen)

        # Відмальовування назви предмету
        screen.blit(text, (x + 35, y - 35))

        pygame.display.update()
        # Затримка перед зниканням тексту
        pygame.time.delay(1200)
    
    # Функція для натискання на кнопку планування експідиції
    def expedition(btn):
        nonlocal expedition_variable

        # Змінення даних змінної expedition_variable
        expedition_variable["status"] = [False, True][btn.clicked_times % 2]
        expedition_variable["duration"] = [0, random.randint(4, 7)][btn.clicked_times % 2]
        expedition_variable["duration"] = expedition_variable["duration"]+days_count

    # Функція для додавання спрайтів до груп
    def create_sprites():
        nonlocal food_start_x
        nonlocal water_start_x

        # Перелік усіх предметів
        for item in items_data.keys():
            # Якщо прдеметом є їжа/вода, то воно перевіряє чи є кількість йього предмету більше за 5, і
            # якщо так, то на екрані з'являються тільки 5 банок/пляшок
            if item == "food_can":
                if items_data[item] <= 5:
                    for i in range(math.ceil(items_data[item])):
                        soup = FoodWater(food_start_x, 320, "Суп", "food_can", on_click)
                        food.add(soup)
                        food_start_x += 60
                else:
                    for i in range(5):
                        soup = FoodWater(food_start_x, 320, "Суп", "food_can", on_click)
                        food.add(soup)
                        food_start_x += 60

                food_start_x = 935

            elif item == "water_bottle":
                if items_data[item] <= 5:
                    for i in range(math.ceil(items_data[item])):
                        watr = FoodWater(water_start_x, 185, "Вода", "water_bottle", on_click)
                        water.add(watr)
                        water_start_x += 60
                else:
                    for i in range(5):
                        watr = FoodWater(water_start_x, 185, "Вода", "water_bottle", on_click)
                        water.add(watr)
                        water_start_x += 60

                water_start_x = 935

            # Якщо назва предмету закінчується на _head, то це персонаж
            elif item[-5:] == "_head":
                corrected_item = item.replace(item[-5:], "")
                char = Character(items_info[corrected_item][1][0], items_info[corrected_item][1][1],
                                items_info[corrected_item][0], corrected_item + "_default", on_click_character)
                
                try:             
                    char.hunger_status = data[item]["status"]["hunger"]
                    char.thirst_status = data[item]["status"]["thirst"]
                    char.hunger = data[item]["hunger"]
                    char.thirst = data[item]["thirst"]
                except KeyError:
                    pass

                characters.add(char)
            # Якщо щось інше, то це просто предмет
            else:
                itm = ClickableSprite(items_info[item][1][0], items_info[item][1][1], items_info[item][0], item, on_click)
                other.add(itm)

    # Створення контейнерів для їжі/води
    def create_containers():
        nonlocal data

        try:
            # Перевірка чи є кількість їжі більше за 5, і якщо так, то на екрані створюється коробка з їжею
            if items_data["food_can"] > 5:
                data["items"]["food_box"] = 1
            else:
                try:
                    del data["items"]["food_box"]
                except KeyError:
                    pass
            # Перевірка чи є кількість води більше за 5, і якщо так, то на екрані створюється кувшин з водою
            if items_data["water_bottle"] > 5:
                data["items"]["jug"] = 1
            else:
                try:
                    del data["items"]["jug"]
                except KeyError:
                    pass
        except KeyError:
            pass
    
    # Функція для збереження прогресу 
    def saving_progress():
        nonlocal data_for_saving

        # Запис даних у словник data_for_saving
        data_for_saving["items"] = data["items"]
        data_for_saving["days"] = days_count

        data_for_saving["expedition"] = expedition_variable
        data_for_saving["event_choice"] = event_choice
        data_for_saving["taken_posts_page_0"] = taken_posts_page_0

        for character in characters:
            data_for_saving[character.image_name.replace("default", "head")] = {"status": {"hunger": character.hunger_status, "thirst": character.thirst_status}, 
                                                                        "hunger": character.hunger, "thirst": character.thirst}

        # Запис цих даний у json файл
        file = open("saving_file.json", "w")
        json.dump(data_for_saving, file)
        file.close()
    
    # Функція для натискання на персонажа при виборі кого послати на експедицію
    def on_click_journal_head(head):
        nonlocal expedition_variable
        nonlocal data
        
        # Оновлення інформації у змінній expedition_variable
        expedition_variable["day"] = days_count
        expedition_variable["character"] = [None, head.image_name.replace("_head", "")][head.clicked_times % 2]
        expedition_variable["status"] = [False, True][head.clicked_times % 2]
        expedition_variable["duration"] = data["expedition"]["duration"]

        if head.clicked_times % 2 == 1:    
            del data["items"][head.image_name]
        else:
            data["items"][head.image_name] = 1

        for head_char in buttons_group:
            if head_char.callback.__name__ == "on_click_journal_head" and head_char.image_name != head.image_name:
                head_char.clicked_times+=1
                head_char.image.set_alpha(120)

    # Створення відповідних змінних і перевірки чи є вони у словнику data
    try:

        days_count = data["days"]

    except KeyError:

        days_count = 1
    
    try:

        expedition_variable = data["expedition"]

    except KeyError:

        expedition_variable = {"status": False, "character": None, "day": 0, "duration": 0}
        print(expedition_variable)
    
    try:

        event_choice = data["event_choice"]

    except KeyError:

        event_choice = {"type": None, "day": 0}
    
    # Усі текстові пости на першій сторінці
    text_posts_page_0 = []
    for i in journal_pages_text[0]:
        if i["type"] == "text":
            text_posts_page_0.append(i)

    # Усі текстові пости на третій сторінці
    text_posts_page_2 = []
    for i in journal_pages_text[0]:
        if i["type"] == "text":
            text_posts_page_2.append(i)

    # Створення списків із вже використанними постами
    try:

        taken_posts_page_0 = data["taken_posts_page_0"]

        if len(taken_posts_page_0) >= len(text_posts_page_0):
            raise KeyError("Too many taken posts")

    except KeyError:

        taken_posts_page_0 = []
    
    try:

        taken_posts_page_2 = data["taken_posts_page_0"]

        if len(taken_posts_page_2) >= len(text_posts_page_2):
            raise KeyError("Too many taken posts")

    except KeyError:

        taken_posts_page_2 = []
    
    file.close()

    # Змінна для з'ясування на якій ви сторінці
    page_count = 0

    # Передвання у словник posts рандомні значення, а ключі це номери сторінок
    posts = {key: random.randint(0, len(journal_pages_text[key])-1) for key in range(len(journal_pages_text))}
    event_answers = ["y", "n"]
    event_text = False


    # Перевірка коли був здійснений івент
    if days_count - event_choice["day"] > 1:
        event_choice = {"type": None, "day": 0}
        event_text = False

    try:
        if journal_pages_text[0][posts[0]]["type"][:5] == "event" and not data["event_choice"]["type"]:
            for post in range(len(journal_pages_text[0])):
                if journal_pages_text[0][post] not in taken_posts_page_0:
                    posts[0] = post
                    event_text = True
                    
    except KeyError:
        pass

    try:
        # Якщо персонаж у словнику expedition_variable є None
        if not expedition_variable["character"]:
            # Перевірка чи планувалась вже експідиція, якщо ні, то вона буде плануватись на 2 сторінці, якщо так, то на 2 сторінці будуть обирати, хто на неї піде
            if (journal_pages_text[2][posts[2]]["type"] != "expedition_plan")and not expedition_variable["status"]:
                print(f"1: {posts}")
                for post in range(len(journal_pages_text[2])):
                    if journal_pages_text[2][post]["type"] == "expedition_plan":
                        posts[2] = post
                        break      

            elif (journal_pages_text[2][posts[2]]["type"] != "expedition_character_choice") and expedition_variable["status"]:
                print(f"2: {posts}")
                for post in range(len(journal_pages_text[2])):
                    if journal_pages_text[2][post]["type"] == "expedition_character_choice":
                        posts[2] = post
                        break
        # Якщо персонаж для експідиція вже іде, то на сторінку з експідицію, просто додаєтьс язвичайний текст
        else:
            for post in range(len(journal_pages_text[2])):
                if (journal_pages_text[2][post] not in taken_posts_page_2) and journal_pages_text[2][post]["type"] == "text":
                    posts[2] = post
                    break
    
    except KeyError:
        pass
    
    # Додавання у список зайнятого поста потс на першій сторінці
    for post in range(len(journal_pages_text[0])):
        if journal_pages_text[0][post] not in taken_posts_page_0 and journal_pages_text[0][post]["type"] == "text" and not event_text:
            posts[0] = post
            taken_posts_page_0.append(journal_pages_text[0][post])
            break

    try:
        # Якщо ви дали відповідь на івент, то наслідок цього вибору відобразиться на першій сторінці
        if data["event_choice"]["type"]:
            if data["event_choice"]["type"][-1:] in event_answers:
                for post in range(len(journal_pages_text[0])):
                    if journal_pages_text[0][post]["type"] == data["event_choice"]["type"]:
                        posts[0] = post
    except KeyError:
        pass
    
    # Перевірка чи завершилась експідиція, якщо так, то додається рандомна кількість води і їжі
    if expedition_variable["status"] and expedition_variable["character"] and (expedition_variable["duration"] - days_count <= 0):
        expedition_variable["status"] = False
        data["items"][expedition_variable["character"]+"_head"] = 1
        random_food_plus = random.randint(1,4)
        random_water_plus = random.randint(1,4)

        # Перевірка кількості води і їжі, якщо вони більше за 9, то їх кількість просто буде дорівнювати 9
        if data["items"]["food_can"]+random_food_plus > 9:
            data["items"]["food_can"] = 9
        else:
            data["items"]["food_can"] += random_food_plus
        
        if data["items"]["water_bottle"]+random_water_plus > 9:
            data["items"]["water_bottle"] = 9
        else:
            data["items"]["water_bottle"] += random_food_plus

        # Відображення поста пропевного персонажа, який повернувся з експідиції
        for post in range(len(journal_pages_text[2])):
            if journal_pages_text[2][post]["type"] == "expedition_end_"+expedition_variable["character"]:
                posts[2] = post
                break
        
        # Зміна даних словника щою обозначити, що експідиція завершилась, і можна починати нову
        expedition_variable["character"] = None
        expedition_variable["day"] = 0
        expedition_variable["duration"] = 0

    food_start_x = 935
    water_start_x = 935

    bg = pygame.image.load("images\\basement.png")

    clock = pygame.time.Clock()

    days_title = font.render(f"День  "+str(days_count), False, (0, 0, 0))

    running = True
    appeared_days_text = False
    journal_open = False

    # Створення спрайтів
    buttons_group = pygame.sprite.Group()
    journal_group = pygame.sprite.GroupSingle()
    journal_icon_group = pygame.sprite.GroupSingle()
    characters = pygame.sprite.Group()
    food = pygame.sprite.Group()
    water = pygame.sprite.Group()
    other = pygame.sprite.Group()

    journal_icon = JournalSprite(1400, 750, "notebook", on_click_journal_icon)
    journal = JournalSprite(500, 20, "opened_notebook", None)
    button_next = Button(1035, 750, "next_page", 255, journal_group, buttons_group, func = next_button)
    button_back = Button(685, 750, "past_page", 255, journal_group, buttons_group, func = back_button)
    button_close = Button(1116, 154, "close_notebook", 255, journal_group, buttons_group, func=close_button)
    button_expedition = Button(880, 672, "backpack", 120, journal_group, buttons_group, func=expedition)
    button_answer_no = Button(900, 590, "disagree", 120, journal_group, buttons_group, func=disagree_button, extra_argument=journal_pages_text[-1][posts[3]]["type"]+"_n")
    button_answer_yes = Button(790, 574, "agree", 120, journal_group, buttons_group, func=agree_button, extra_argument=journal_pages_text[-1][posts[3]]["type"]+"_y")
    button_oleg = Button(720, 574, "oleg_head", 120, journal_group, buttons_group, func=on_click_journal_head, width=50, height=70)
    button_dima = Button(840, 574, "dima_head", 120, journal_group, buttons_group, func=on_click_journal_head, width=50, height=70)
    button_dasha = Button(960, 574, "dasha_head", 120, journal_group, buttons_group, func=on_click_journal_head, width=50, height=70)
    button_masha = Button(1080, 574, "masha_head", 120, journal_group, buttons_group, func=on_click_journal_head, width=50, height=70)

    oleg_head_journal = Head(720, 258, "oleg_head")
    dima_head_journal = Head(840, 258, "dima_head")
    dasha_head_journal = Head(960, 258, "dasha_head")
    masha_head_journal = Head(1080, 258, "masha_head")

    oleg_water = FoodWaterJournal(750, 340, "oleg", "water_bottle", 120, click_foodwater_journal)
    oleg_food = FoodWaterJournal(710, 340, "oleg", "food_can", 120, click_foodwater_journal)

    dima_water = FoodWaterJournal(870, 340, "dima", "water_bottle", 120, click_foodwater_journal)
    dima_food = FoodWaterJournal(830, 340, "dima", "food_can", 120, click_foodwater_journal)

    dasha_water = FoodWaterJournal(1000, 340, "dasha", "water_bottle", 120, click_foodwater_journal)
    dasha_food = FoodWaterJournal(960, 340, "dasha", "food_can", 120, click_foodwater_journal)

    masha_water = FoodWaterJournal(1120, 340, "masha", "water_bottle", 120, click_foodwater_journal)
    masha_food = FoodWaterJournal(1080, 340, "masha", "food_can", 120, click_foodwater_journal)

    food_journal_sprite = JournalImage(700, 430, "food_can", 70, 90)
    water_journal_sprite = JournalImage(700, 550, "water_bottle", 70, 90)

    journal_icon_group.add(journal_icon)

    create_containers()
    create_sprites()

    # Зміна яка буде відображатись на початку дня
    showing_days_text = f"{days_count} ДЕНЬ"

    # Перевірка голоду і спраги пресонажів
    for character in characters:

        # Якщо спрага, або голод меньше або дорівнюють 0, то персонажі видаляються з словнику для збереження, і виведеться відповідний пост
        if character.thirst <= 0:
            del data["items"][character.image_name.replace("default", "head")]
            character.kill()
            for post in range(len(journal_pages_text[0])):
                if journal_pages_text[0][post]["type"] == character.image_name.replace("_default", "")+"_0_thirst":
                    posts[0] = post
                    break

        elif character.hunger <= 0:
            del data["items"][character.image_name.replace("default", "head")]
            character.kill()
            for post in journal_pages_text[0]:
                if post["type"] == character.image_name.replace("_default", "")+"_0_hunger":
                    posts[0] = post
                    break
    
    # Якщо кількість персонажів мень або дорівнює 0, то відображаємий текст дорівнює "КІНЕЦЬ"
    if len(characters) <= 0:
        showing_days_text = "КІНЕЦЬ"

    event_choice = {"type": None, "day": 0}
    callback = "quit"

    # Основний цикл гри
    while running:
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            # Перевірка чи хоче гравець вийти з гри
            if event.type == pygame.QUIT:
                callback = "quit"
                file = open("main_game_final.json", "w")
                json.dump({"days": days_count, "callback": "quit"}, file)
                file.close()
                bg_music.stop()
                saving_progress()
                running = False
        
        if page_count > 0:
            buttons_group.add(button_back)
        else:
            button_back.kill()

        if page_count == 3 and button_answer_no.extra_argument[:4] != "text":
            if button_answer_yes.clicked_times%2 == 1 or button_answer_no.clicked_times%2 == 1:
                buttons_group.add(button_next)
            else:
                button_next.kill()
        
        # Відображення заднього фону
        screen.blit(bg, (0, 0))

        # Відображення тексту на початку дня
        if not appeared_days_text:
            screen.fill((0, 0, 0))
            text = days_font.render(showing_days_text, False, (255, 255, 255))
            screen.blit(text, (700, 400))
            pygame.display.update()
            pygame.time.delay(1900)
            appeared_days_text = True
        
        # Оновлення статусу персонажів
        for character in characters:
            character.update_status()

        # Відмальовування спрайтів
        other.draw(screen)
        food.draw(screen)
        water.draw(screen)
        characters.draw(screen)

        # Перевірка чи є блокнот відкритим
        if not journal_open:
            other.update(events)
            food.update(events)
            water.update(events)
            characters.update(events)

            journal_icon_group.draw(screen)
            journal_icon_group.update(events)
        else:
            
            buttons_group.update(events)
            journal_group.draw(screen)
            buttons_group.draw(screen)
            screen.blit(days_title, (850, 130))
            draw_page_text()

        pygame.display.update()
        clock.tick(60)

    # Якщо гравець не закривав гру, а просто почався новий день, то функція запускає сама себе
    if callback != "quit":
        gameplay()