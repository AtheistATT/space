'''
Класс игрового контроллера. 
Отвечает за всю логику игры и обрабатывает нажатие клавиш.
Задуман как подобие статического класса.
'''
import pygame
from render import Render
from constants import *
import objects
import random

class Controller:

    @classmethod
    def init(cls, game_render : Render):
        '''
        Метод инициализации. Должен быть вызван до начала работы класса. Принимает как аргумент экземпляр класса Render.
        '''
        cls.game_render : Render = game_render
        cls.background = []
        #cls.tick = 0
        cls.score = 0 # Счетчик очков
        cls.asteroids = []
        cls.fall_speed = SCREEN_HIGHT // 160 # Начальная скорость падения астеройдов
        cls.max_speed = SCREEN_HIGHT // 40 # максимальная скорость
        cls.hitbox_redution = 0.4 # Переменная отвечает за уменьшение хитбокса. На большой скорости коллизии резковаты.
        cls.gams_state = "START"

        pygame.mixer.music.load("resource/magic sky.ogg") # Загружаем музыку

        for col in range(5): # Создаем задний фон
            for row in range(3):
                bf = objects.GameObject("resource/background.png", 0, 0)

                bf.current_frame = random.choice(range(len(bf.frames)))
                bf.x = row * (SCREEN_WIDTH // 3)
                bf.y = col * (SCREEN_WIDTH // 3)

                cls.background.append(bf)
                cls.frame_size = SCREEN_WIDTH // 3
                

                cls.player = objects.GameObject("resource/player.png", 1 * cls.frame_size, 4 * cls.frame_size) # Создаем корабль игрока

    @classmethod
    def update(cls):
        '''
        Метод страбатывающий на каждой итерации игрового цикла. Отвечает за логику работы программы.
        '''
        
        match cls.gams_state:
            case "START":
                cls.game_render.draw_text("Добро пожаловать!\nSPACE ARCADE\nНажмите пробел...")
            case "PLAY":

                cls.player.current_frame = random.randint(0, len(cls.player.frames) - 1) # Анимация огня

                if len(cls.asteroids) == 0: # Спаун астеройдов. Происходит когда их список пуст.
                    free_space = random.randint(0,2)# Определяем позицию без астеройда.
                    for i in range(3):
                        if i == free_space:
                            continue
                        else:
                            ast = objects.GameObject("resource/asteroid.png", i * cls.frame_size, -cls.frame_size)
                            ast.current_frame = random.randint(0, len(ast.frames) - 1)
                            cls.asteroids.append(ast)
                
                for ast in cls.asteroids:# Двигаем астеройды вниз.
                    ast.y += cls.fall_speed

                if cls.check_collision(): # Проверяем коллизии
                    pygame.mixer.music.stop()
                    cls.gams_state = "END"

                asteroids_new_list = [ast for ast in cls.asteroids if ast.y < 5 * cls.frame_size] # Создаем список астеройдов за исключением тех что вышли за экран.

                if len(asteroids_new_list) != len(cls.asteroids): # Если есть астоеройды за экраном.
                    cls.score += 1 # Добавляем игроку очко
                    if cls.max_speed > cls.fall_speed: # Проверяем что скорость не достигла максимума.
                        cls.fall_speed += 1 # Увеличиваем скорость
                    cls.asteroids = asteroids_new_list # Удаляем лишние астеройды

                background = [x.get_render_data() for x in cls.background] # Преобразуем задний фон в списки для вывода на экран
                asteroids = [x.get_render_data() for x in cls.asteroids] # Преобразуем астеройды в списки вывода на экран
                cls.game_render.draw_game_frame(background + [cls.player.get_render_data()] + asteroids, cls.score) # Передаем объекты в объект рендер для отрисовки

                #cls.tick += 1
            case "END":
                cls.game_render.draw_text(f"Игра окончена.\n Ваш счет: {cls.score}\nНажмите пробел...")
    
    @classmethod
    def check_collision(cls): # Просверка на столкновение.
        for ast in cls.asteroids:
            if cls.player.x == ast.x:
                if ast.y + cls.frame_size > cls.player.y + cls.frame_size * cls.hitbox_redution and ast.y < cls.player.y + cls.frame_size * cls.hitbox_redution:
                    return True
        return False

    @classmethod
    def evern_handler(cls, events):
        '''
        Метод обработки игровых событий.
        '''
        for event in events:
            match event.type:
                case pygame.QUIT:
                    exit()
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE:
                            exit()
                        case pygame.K_LEFT:
                            cls.player.x = 0
                        case pygame.K_RIGHT:
                            cls.player.x = 2 * cls.frame_size
                        case pygame.K_SPACE:
                            if cls.gams_state == "START":
                                pygame.mixer.music.play(-1)
                                cls.gams_state = "PLAY"
                            elif cls.gams_state == "END":
                                exit()
                case pygame.KEYUP:
                    cls.player.x = 1 * cls.frame_size
