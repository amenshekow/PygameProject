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


# Зеркальные координаты для другого поля

def invert(pos):
    return width - pos[0], height - pos[1] - 10


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


# Базовый класс для юнитов

class Unit(pygame.sprite.Sprite):
    def __init__(self, size, pos, image_p, attack_r, power, hp, speed, all_sprites, user, field):
        super().__init__()
        self.all_sprites = all_sprites
        self.image = load_image(image_p, colorkey='black')
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.pos = pos
        self.field = field

        self.attack_r = attack_r
        self.power = power
        self.hp = hp
        self.speed = speed

        self.user = user
        self.target = None
        self.target_pos = (-1000, -1000)

    def update(self):
        self.targeting()
        self.moving()

    # Движение к цели

    def moving(self):
        if self.speed != 0:
            if self.temp_target_pos:
                self.target_pos = self.temp_target_pos
            dx = self.target_pos[0] - self.rect.centerx
            dy = self.target_pos[1] - self.rect.centery
            d = (dx ** 2 + dy ** 2) ** 0.5
            if d > 0:
                dx /= d
                dy /= d
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed

    # Определение цели

    def targeting(self):
        # Если цели нет, то цель по умолчанию - ближайшая башня
        if not self.target or type(self.target) == Tower:
            for el in self.all_sprites:
                if type(el) == Tower and el.user != self.user and el.field == self.field:
                    if self.distance(self.pos, el.pos) < self.distance(self.pos, self.target_pos):
                        self.target = el
                        self.target_pos = self.target.pos
        self.target_pos = self.target.pos

        # Если цель на другой стороне поля, необходимо пройти через ближайший мост (временная цель)
        if type(self) != Tower:
            bridges = [(160, 325), (410, 325)]
            temp_list = [self.rect.centery, self.target.pos[1]]
            if self.field == 2:

                bridges = [(802, 325), (1050, 325)]
            if self.user != self.field:
                temp_list = temp_list[::-1]
            if temp_list[0] > 325 > temp_list[1]:
                self.temp_target_pos = (-1000, -1000)
                for i in range(len(bridges)):
                    if self.distance(self.pos, bridges[i]) < self.distance(self.pos, self.temp_target_pos):
                        self.temp_target_pos = bridges[i]
            else:
                self.temp_target_pos = None

    # Расстояние от одного объекта до другого
    def distance(self, pos1, pos2):
        return ((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2) ** 0.5


class Tower(Unit):
    def __init__(self, pos, all_sprites, user, field, image_p='Test_tower.png', size=(60, 50)):
        super().__init__(size, pos, image_p, 10, 15, 100, 0, all_sprites, user, field)
        self.pos = pos
        self.user = user
        self.field = field


# Тестовый юнит ближнего боя

class Melee(Unit):
    def __init__(self, pos, attack_r, power, hp, speed, all_sprites, user, field):
        super().__init__((60, 50), pos, 'Test_unit.png', attack_r, power, hp, speed, all_sprites, user, field)
        self.pos = pos
        self.user = user
        self.field = field



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
    # user1_sprites = pygame.sprite.Group()
    # user2_sprites = pygame.sprite.Group() # Как вариант, можно в будущем при необходимости ввести
    a = Back()
    all_sprites.add(a)
    user1 = Field()
    user2 = Field()
    user1.number(1)
    user2.number(2)

    all_sprites.add(user1)
    all_sprites.add(user2)

    # Башни 1 поля (1 и 2 игрок)

    all_sprites.add(Tower((162, 536), all_sprites, 1, 1))
    all_sprites.add(Tower((410, 536), all_sprites, 1, 1))
    all_sprites.add(Tower((287, 601), all_sprites, 1, 1, size=(80, 65)))

    all_sprites.add(Tower((162, 143), all_sprites, 2, 1))
    all_sprites.add(Tower((413, 143), all_sprites, 2, 1))
    all_sprites.add(Tower((287, 78), all_sprites, 2, 1, size=(80, 65)))

    # Башни 2 поля (1 и 2 игрок)

    all_sprites.add(Tower((802, 143), all_sprites, 1, 2))
    all_sprites.add(Tower((1053, 143), all_sprites, 1, 2))
    all_sprites.add(Tower((927, 78), all_sprites, 1, 2, size=(80, 65)))

    all_sprites.add(Tower((802, 536), all_sprites, 2, 2))
    all_sprites.add(Tower((1050, 536), all_sprites, 2, 2))
    all_sprites.add(Tower((927, 601), all_sprites, 2, 2, size=(80, 65)))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Для тестов: ЛКМ - спавн юнита игрока 1, ПКМ - юнита игрока 2
                # Создание сначала оригинального юнита, затем его клона на другом поле
                if event.button == 1:
                    all_sprites.add(Melee(event.pos, 10, 10, 10, 1, all_sprites, 1, 1))
                    all_sprites.add(Melee(invert(event.pos), 10, 10, 10, 1, all_sprites, 1, 2))
                elif event.button == 3:
                    all_sprites.add(Melee(event.pos, 10, 10, 10, 1, all_sprites, 2, 2))
                    all_sprites.add(Melee(invert(event.pos), 10, 10, 10, 1, all_sprites, 2, 1))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()












if __name__ == '__main__':
    pygame.init()
    running = True
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 50)
    menu()