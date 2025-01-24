import pygame
import os
import sys


size = width, height = 1225, 700
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


#Задний фон игры
class Back(pygame.sprite.Sprite):
    image = load_image("forest.jpg")
    image = pygame.transform.scale(image, (1225, 700))
    def __init__(self, *group):
        super().__init__(*group)
        self.image = Back.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


#Класс поля игры
class Field(pygame.sprite.Sprite):
    image = load_image("field1.png")
    image = pygame.transform.scale(image, (400, 800))

    #Инициализация поля
    def __init__(self, *group):
        super().__init__(*group)
        self.image = Field.image
        self.rect = self.image.get_rect()
        self.rect.x = 60
        self.rect.y = -70
        self.user = 1

    #Выбор поля игрока (user = 1 или 2)
    def number(self, user):
        if user == 1:
            self.rect.x = 90
            self.rect.y = -70
            self.user = 1
        elif user == 2:
            self.rect.x = 730
            self.rect.y = -70
            self.user = 2
        else:
            raise Exception("Введен неверный номер игрового поля")


#Класс надписей в главном меня
class Interactive(pygame.sprite.Sprite):
    #Инициализация класса, где title это название файла с изображением текста
    #Файлы должны быть в виде name.png и name1.png(name - обычный, name1 - при выборе)
    #coord координаты надписи
    def __init__(self, title, coord, *group):
        super().__init__(*group)
        self.title = title
        self.sost = 1
        self.x = coord[0]
        self.y = coord[1]
        image = load_image(title + ".png")
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = coord[0]
        self.rect.y = coord[1]

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION \
                and self.rect.collidepoint(args[0].pos) and self.sost == 1:
            image = load_image(self.title + "1.png")
            print(self.title + "1.png")
            self.image = image
            self.sost = 2
        if args and args[0].type == pygame.MOUSEMOTION \
                and not self.rect.collidepoint(args[0].pos) and self.sost == 2:
            print("bb")
            image = load_image(self.title + ".png")
            self.image = image
            self.sost = 1


    def text(self, *args):
        if self.sost == 2:
            return True




#Главное меню игры
def menu():
    all_sprites = pygame.sprite.Group()
    a = Back()
    all_sprites.add(a)
    start = Interactive("play", (440, 100))
    all_sprites.add(start)
    all_sprites.draw(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                all_sprites.update(event)
                all_sprites.draw(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start.text(event):
                    game()
                    running = False
        pygame.display.flip()




#Создание игрового поля в начале игры
def game():
    all_sprites = pygame.sprite.Group()
    a = Back()
    all_sprites.add(a)
    user1 = Field()
    user2 = Field()
    user1.number(1)
    user2.number(2)
    all_sprites.add(user1)
    all_sprites.add(user2)
    all_sprites.draw(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()












if __name__ == '__main__':
    pygame.init()
    running = True
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 50)
    menu()