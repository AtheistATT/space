'''
Классы содержащие игровые объекты. По идее должны содержать только данные. За обработку отвечает контроллер.
'''
import pygame

class GameObject:
    def __init__(self, image : str, x : int, y : int) -> None:
        '''
       При инициализации объет получает параметры: image - путь к файлу изобрахения, не разбитого на отдельные кадры, x и y это координаты отрисовки спрайта.
        '''

        self.frames = []
        self.x = x
        self.y = y
        self.current_frame = 0

        full_image = pygame.image.load(image) # Загружаем изображение

        image_width, image_hight = full_image.get_size()
        number_of_frames = image_hight // image_width
        
        for i in range(number_of_frames): # Разбиваем файл на кадры и добавляем их в список кадров.
            frame = full_image.subsurface(pygame.Rect(0, i * image_width, image_width, image_width))
            self.frames.append(frame)

    def get_render_data(self):
        '''
        Возвращает данные в формате, который обрабатывает рендер.
        '''
        return [self.frames[self.current_frame], self.x, self.y]

