'''
Класс отвечает за отрисовку кадра игры.
Вся отрисовка графики инкапсулирована в него.
'''
import pygame
from constants import * # Импортируем константы

class Render:
    def __init__(self, screen) -> None:
        '''
          При инициализации принимает объект класса Surface из библиотеки pygame.  
        '''
        self.screen = screen
        self.font = pygame.font.SysFont(None, SCREEN_HEIGHT//20) # Размер шрифта зависит от размера экрана
        self.frame_size = SCREEN_WIDTH // 3 # Вычисляем размер единичного фрейма. Они всегда квадратные

    def draw_game_frame(self, frames, score = 0):
        '''
        Функция отвечает за отрисовку кадра геймплея и очков.
        На входе она принимает список списков.
        Каждый элемент списка состоит из изображения типа Surface и двух координат 
        Кроме того, который отвечает за отображение игровых очков.
        '''
        for frame in frames: # Проходимся циклам по полученному списку
            image = pygame.transform.scale(frame[0], (self.frame_size, self.frame_size)) # Сразу даем понятные имена полученным данным
            x = frame[1]
            y = frame[2]

            self.screen.blit(image,(x, y)) 

        pygame.draw.rect(self.screen, GRAY, pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT//20)) # для панели счета делаем подложку.
        text_img = self.font.render(f"SCORE: {score}", True, BLACK)
        self.screen.blit(text_img,(0,0))

    def draw_text(self, text, start_position = SCREEN_HEIGHT//2): 
        '''
        Функция для вывода текста на экран. Предполагается для использования в стартовом меню и меня конца игры.
        На входе принимает текст(Может быть разделен знаком '\\n' для вывода нескольких сток)
        Необязательный параметр start_position позиция от верхней части экрана. По умолчанию центр.
        '''
        self.screen.fill(BLACK)

        indent = SCREEN_HEIGHT // 20 # Вычисляем отступ

        for message in text.split('\n'): # Если есть несколько строк, то разбиваем на подстроки.
            text_img = self.font.render(message, True, WHITE)
            text_width = SCREEN_WIDTH // 2 - text_img.get_width() // 2 # Центрируем, исходя из ширины самой строки
            self.screen.blit(text_img,(text_width,start_position))
            start_position += indent
