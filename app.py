import pygame
import os
import sys

from random import randint

size = width, height = 1400, 800
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
    return width - pos[0] + 2, height - pos[1] - 120


#Задний фон игры
class Back(pygame.sprite.Sprite):
    image = load_image("forest.jpg")
    image = pygame.transform.scale(image, (width, height))
    def __init__(self, *group):
        super().__init__(*group)
        self.image = Back.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


#Класс поля игры
class Field(pygame.sprite.Sprite):
    image = load_image("field1.png")
    image = pygame.transform.scale(image, (width // 2 - 160, (width // 2 - 160) * 2 - 100))

    #Инициализация поля
    def __init__(self, *group):
        super().__init__(*group)
        self.image = Field.image
        self.rect = self.image.get_rect()
        self.rect.x = 60
        self.rect.y = -160
        self.user = 1

    #Выбор поля игрока (user = 1 или 2)
    def number(self, user):
        if user == 1:
            self.rect.x = 70
            self.rect.y = -160
            self.user = 1
        elif user == 2:
            self.rect.x = 800
            self.rect.y = -160
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
    def __init__(self, size, pos, image_p, attack_r, visual_r, power, hp, speed, units_sprites, user):
        super().__init__(units_sprites)
        self.units_sprites = units_sprites
        self.image = load_image(image_p, colorkey='black')
        self.image = pygame.transform.scale(self.image, size)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.pos = pos

        self.attack_r = attack_r
        self.visual_r = visual_r
        self.power = power
        self.hp = hp
        self.speed = speed

        self.user = user
        self.target = None
        self.target_pos = (-1000, -1000)

    def update(self):
        self.targeting()
        self.moving()

    # Движение к цели и столкновения

    def moving(self):
        if self.speed != 0:
            if self.temp_target_pos:
                self.target_pos = self.temp_target_pos

            # Список объектов, с которыми есть накладывание масок
            collide_list = [spr for spr in pygame.sprite.spritecollide(self, self.units_sprites, False)
                            if self.mask.overlap(spr.mask, (spr.rect.x - self.rect.x - 3, spr.rect.y - self.rect.y - 3))
                            and spr != self]

            # Физика отталкивания от препятствия

            if collide_list:
                for el in collide_list:
                    if self != el.target:
                        dx = el.pos[0] - self.rect.centerx
                        dy = el.pos[1] - self.rect.centery
                        d = (dx ** 2 + dy ** 2) ** 0.5
                        if d != 0:
                            dx /= d
                            dy /= d
                            if el == self.target:
                                dx, dy = -dx, -dy
                            else:
                                if self.pos[0] == el.pos[0] and self.target not in collide_list:
                                    dx += 1
                                elif self.pos[1] == el.pos[1] and self.target not in collide_list:
                                    dy += 1
                                if self.pos[0] > el.pos[0]:
                                    dx -= randint(1, 3)
                                if self.pos[0] < el.pos[0]:
                                    dx += randint(1, 3)
                                if self.pos[1] > el.pos[1]:
                                    dy += randint(1, 3)
                                if self.pos[1] < el.pos[1]:
                                    dy -= randint(1, 3)
                                dx, dy = -dx, dy
                            self.rect.x += dx * self.speed
                            self.rect.y += dy * self.speed
                            self.pos = (self.rect.centerx, self.rect.centery)

            # Движение к цели

            if not pygame.sprite.collide_mask(self, self.target):
                dx = self.target_pos[0] - self.rect.centerx
                dy = self.target_pos[1] - self.rect.centery
                d = (dx ** 2 + dy ** 2) ** 0.5
                if d > 0 or self.temp_target_pos:
                    dx /= d
                    dy /= d
                    self.rect.x += dx * self.speed
                    self.rect.y += dy * self.speed
                    self.pos = (self.rect.centerx, self.rect.centery)

        # Отрисовка второго поля (изображение дублируется)
        screen.blit(self.image, invert((self.rect.right, self.rect.bottom)))

    # Определение цели

    def targeting(self):
        nearest_target = None
        nearest_target_pos = (-1000, -1000)
        nearest_tower = None
        nearest_tower_pos = (-1000, -1000)

        if not self.target or type(self.target) == Tower:
            for el in self.units_sprites:
                if el.user != self.user:
                    if type(el) == Tower:
                        if self.distance(self.pos, el.pos) < self.distance(self.pos, nearest_tower_pos):
                            nearest_tower = el
                            nearest_tower_pos = el.pos
                    if self.distance(self.pos, el.pos) < self.visual_r:
                        if self.distance(self.pos, el.pos) < self.distance(self.pos, nearest_target_pos):
                            nearest_target = el
                            nearest_target_pos = el.pos
            if nearest_target == nearest_tower or not nearest_target:
                self.target = nearest_tower
                self.target_pos = nearest_tower_pos
            else:
                self.target = nearest_target
                self.target_pos = nearest_target_pos

        # Если цель на другой стороне поля, необходимо пройти через ближайший мост (временная цель)
        if type(self) != Tower:
            bridges = [(170, 375), (490, 375)]
            temp_list = [self.rect.centery, self.target.pos[1]]
            if self.user == 2:
                temp_list = temp_list[::-1]
            if temp_list[0] > 375 > temp_list[1]:
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
    def __init__(self, pos, units_sprites, user, image_for_test='Test_tower.png', size=(95, 70)):
        super().__init__(size, pos, image_for_test, 10, 15, 10, 100, 0, units_sprites, user)
        self.pos = pos
        self.user = user


# Тестовый юнит ближнего боя

class Melee(Unit):
    def __init__(self, pos, attack_r, visual_r, power, hp, speed, units_sprites, user, image_for_test='Test_unit.png'):
        super().__init__((60, 50), pos, image_for_test, attack_r, visual_r, power, hp, speed, units_sprites, user)
        self.pos = pos
        self.user = user


#Класс доски на которой отоброжаются игровые юниты
class Deck(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = image = load_image("forest.jpg")
        image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = 60
        self.rect.y = -150
        self.user = 1





#Главное меню игры
def menu():
    all_sprites = pygame.sprite.Group()
    a = Back()
    all_sprites.add(a)
    start = Interactive("play", (width // 2 - 150, 100))
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
    units_sprites = pygame.sprite.Group()
    a = Back()
    all_sprites.add(a)
    user1 = Field()
    user2 = Field()
    user1.number(1)
    user2.number(2)

    all_sprites.add(user1)
    all_sprites.add(user2)

    # Башни 1 поля (1 и 2 игрок)

    all_sprites.add(Tower((169, 580), units_sprites, 1))
    all_sprites.add(Tower((502, 580), units_sprites, 1))
    all_sprites.add(Tower((337, 660), units_sprites, 1, size=(120, 95)))

    all_sprites.add(Tower((166, 100), units_sprites, 2, image_for_test='Test_tower_2.png'))
    all_sprites.add(Tower((502, 100), units_sprites, 2, image_for_test='Test_tower_2.png'))
    all_sprites.add(Tower((335, 23), units_sprites, 2, image_for_test='Test_tower_2.png', size=(120, 95)))

    # Башни 2 поля (1 и 2 игрок)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                # Для тестов: ЛКМ - спавн юнита игрока 1, ПКМ - юнита игрока 2
                # Создание сначала оригинального юнита, затем его клона на другом поле
                if event.button == 1:
                    all_sprites.add(Melee(event.pos, 1, 100, 10, 10, 2, units_sprites, 1))
                elif event.button == 3:
                    all_sprites.add(Melee(invert(event.pos), 1, 100, 10, 10, 2, units_sprites, 2, image_for_test='Test_unit_2.png'))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(60)












if __name__ == '__main__':
    pygame.init()
    running = True
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 50)
    clock = pygame.time.Clock()
    menu()