'''
Игра. Space Arcade.
Простая игра созданная как поект для курсов по Python.
Это главный файл. Особо интересного тут ничего нет. Он просто запускает главный цикл и в нем вызвает побочные классы.
'''
import pygame
from render import Render # Импортирование модуля для отображения кадра игры
from constants import * # Импортирование системных констант
from controller import Controller
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT)) # Размер дисплея определяется значениями констант
clock = pygame.time.Clock()
Controller.init(Render(screen)) # Создаем экземпляр класса Rander. Он будет работать с переданным ему состоянием экрана и сразу передаем его в контроллер

while True:

    Controller.update() # Обновляем состояние контроллера
    Controller.evern_handler(pygame.event.get()) # Передаем контроллеру полученные события

    pygame.display.flip()
    clock.tick(60)
