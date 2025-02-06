import pygame
import os
import sys

from random import randint
from time import time
from math import atan2, degrees

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


# Задний фон игры
class Back(pygame.sprite.Sprite):
    image = load_image("forest.jpg")
    image = pygame.transform.scale(image, (width, height))
    def __init__(self, *group):
        super().__init__(*group)
        self.image = Back.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


# Класс поля игры
class Field(pygame.sprite.Sprite):
    image = load_image("field1.png")
    image = pygame.transform.scale(image, (width // 2 - 160, (width // 2 - 160) * 2 - 100))

    # Инициализация поля
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


class Deck(pygame.sprite.Sprite):
    image = load_image("desk.png")
    image = pygame.transform.scale(image, (width // 2 - 100, 150))
    def __init__(self, pos, *group):
        super().__init__(*group)
        self.image = Deck.image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]



# Класс надписей в главном меня
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
            self.image = image
            self.sost = 2
        if args and args[0].type == pygame.MOUSEMOTION \
                and not self.rect.collidepoint(args[0].pos) and self.sost == 2:
            image = load_image(self.title + ".png")
            self.image = image
            self.sost = 1


    def text(self, *args):
        if self.sost == 2:
            return True


# класс карт внизу для выбора
class Card(Interactive):
    def __init__(self, title, coord, *group):
        super().__init__(title, coord, *group)
        self.sost = 0
        self.pos = coord
    def upd(self):
        if self.sost == 0:
            image = load_image(self.title + ".png")
            self.image = image
        else:
            image = load_image(self.title + "1.png")
            self.image = image

    # value = 1, если карта выбрана игроком, 0 иначе
    def new_value(self, value):
        self.sost = value
        self.upd()


class Circl(pygame.sprite.Sprite):
    image = load_image("circle.png")
    image = pygame.transform.scale(image, (70, 70))
    def __init__(self, coord, *group):
        super().__init__(*group)
        self.image = Circl.image
        self.rect = self.image.get_rect()
        self.rect.x = coord[0]
        self.rect.y = coord[1]
    def replace(self,coord):
        self.rect.x = coord[0]
        self.rect.y = coord[1]

    def get_coord(self):
        return (self.rect.x, self.rect.y)


# Базовый класс для юнитов
class Unit(pygame.sprite.Sprite):
    def __init__(self, size, pos, image_p, attack_r, visual_r, power, hp, speed, units_sprites, user, all_sprites=None):
        super().__init__(units_sprites)
        self.units_sprites = units_sprites
        self.all_sprites = all_sprites
        self.image = load_image(image_p)
        if image_p[:image_p.index('.')][-1] != '2':
            self.image_2 = load_image(image_p[:image_p.index('.')] + '_2' + image_p[image_p.index('.'):])
        else:
            self.image_2 = load_image(image_p[:image_p.rindex('_')] + image_p[image_p.index('.'):])
        self.image = pygame.transform.scale(self.image, size)
        self.image_2 = pygame.transform.scale(self.image_2, size)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.pos = pos

        self.attack_r = attack_r
        self.visual_r = visual_r
        self.power = power
        self.hp = hp
        self.max_hp = hp
        self.speed = speed

        self.user = user
        self.target = None
        self.target_pos = (-1000, -1000)

        self.last_attack_time = time()

    def update(self):
        self.targeting()
        self.moving()
        self.attacking()
        if self.hp != self.max_hp and self.hp > 0:
            back_image = pygame.Surface([self.image.get_size()[0] * 0.5, 5])
            pos = (self.pos[0] - self.image.get_size()[0] * 0.25, self.rect.y - self.image.get_size()[1] * 0.1)
            screen.blit(back_image, pos)
            screen.blit(back_image, invert((pos[0] + back_image.get_size()[0], pos[1] + self.image.get_size()[1] + self.image.get_size()[1] * 0.2)))
            image = pygame.Surface([self.image.get_size()[0] * 0.5 * (self.hp / self.max_hp) - 1, 5 - 1])
            image.fill(pygame.Color("white"))
            pos = (self.pos[0] - self.image.get_size()[0] * 0.25 + 1, self.rect.y - self.image.get_size()[1] * 0.1)
            screen.blit(image, pos)
            screen.blit(image, (width - pos[0] + 2 - back_image.get_size()[0] + 2, height - pos[1] - 120 - self.image.get_size()[1] - self.image.get_size()[1] * 0.2))

    # Расстояние от одного объекта до другого

    def distance(self, pos1, pos2):
        return ((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2) ** 0.5

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

            if not pygame.sprite.collide_mask(self, self.target) and not self.distance(self.pos, self.target.pos) <= self.attack_r:
                dx = self.target_pos[0] - self.rect.centerx
                dy = self.target_pos[1] - self.rect.centery
                d = (dx ** 2 + dy ** 2) ** 0.5
                if d <= 0 and self.temp_target_pos:
                    self.temp_target_pos = None
                if d > 0 or self.temp_target_pos:
                    dx /= d
                    dy /= d
                    self.rect.x += dx * self.speed
                    self.rect.y += dy * self.speed
                    self.pos = (self.rect.centerx, self.rect.centery)

        # Отрисовка второго поля (изображение дублируется)
        screen.blit(self.image_2, invert((self.rect.right, self.rect.bottom)))

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
            bridges = [(170, 340), (490, 340)]
            temp_list = [self.rect.centery, self.target.pos[1]]
            if self.user == 2:
                temp_list = temp_list[::-1]
            if temp_list[0] > 340 > temp_list[1]:
                self.temp_target_pos = (-1000, -1000)
                for i in range(len(bridges)):
                    if self.distance(self.pos, bridges[i]) < self.distance(self.pos, self.temp_target_pos):
                        self.temp_target_pos = bridges[i]
            else:
                self.temp_target_pos = None

    def attacking(self):
        cur_time = time()
        if self.distance(self.pos, self.target.pos) <= self.attack_r or pygame.sprite.collide_mask(self, self.target):
            if cur_time - self.last_attack_time >= 1:
                self.last_attack_time = cur_time
                if type(self) == Ranged or type(self) == Tower:
                    self.all_sprites.add(Projectile((40, 40), self.pos, 'arrow.png', self.distance(self.pos, self.target.pos) / 20, self.target))
                print(self, 'attacks', self.target)
                self.target.hp -= self.power
                if self.target.hp <= 0:
                    self.target.kill()
                    self.target = None


class Tower(Unit):
    def __init__(self, pos, units_sprites, all_sprites, user, image_for_test='tower.png', size=(100, 100)):
        super().__init__(size, pos, image_for_test, 200, 200, 20, 1000, 0, units_sprites, user, all_sprites=all_sprites)
        self.pos = pos
        self.user = user


# Тестовый юнит ближнего боя
class Melee(Unit):
    def __init__(self, pos, attack_r, visual_r, power, hp, speed, units_sprites, user, image_for_test='Test_unit_2.png'):
        super().__init__((60, 50), pos, image_for_test, attack_r, visual_r, power, hp, speed, units_sprites, user)
        self.pos = pos
        self.user = user


# Тестовый юнит дальнего боя
class Ranged(Unit):
    def __init__(self, pos, attack_r, visual_r, power, hp, speed, units_sprites, all_sprites, user, image_for_test='Test_unit_2.png'):
        super().__init__((50, 40), pos, image_for_test, attack_r, visual_r, power, hp, speed, units_sprites, user, all_sprites=all_sprites)
        self.pos = pos
        self.user = user


# Класс снаряда
class Projectile(pygame.sprite.Sprite):
    def __init__(self, size, pos, image_p, speed, target):
        super().__init__()
        self.image = load_image(image_p)
        self.image = pygame.transform.scale(self.image, size)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.pos = pos

        self.speed = speed
        self.target = target

        self.direction = True

    def update(self):
        if self.target is None or pygame.sprite.collide_mask(self, self.target):
            self.kill()
        dx = self.target.pos[0] - self.rect.centerx
        dy = self.target.pos[1] - self.rect.centery
        d = (dx ** 2 + dy ** 2) ** 0.5
        if d > 0:
            dx /= d
            dy /= d
            if self.direction:
                self.image = pygame.transform.rotate(self.image, degrees(atan2(-dy, dx)) + 90)
                self.rect = self.image.get_rect(center=self.rect.center)
                self.mask = pygame.mask.from_surface(self.image)
                self.direction = False
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
            self.pos = (self.rect.centerx, self.rect.centery)

        screen.blit(pygame.transform.rotate(self.image, 180), invert((self.rect.right, self.rect.bottom)))


# Главное меню игры
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
    cards_sprites = pygame.sprite.Group()
    circleses = pygame.sprite.Group() # Класс с кругами при выставлении юнита
    back = Back()
    all_sprites.add(back)
    user1 = Field()
    user2 = Field()
    user1.number(1)
    user2.number(2)

    all_sprites.add(user1)
    all_sprites.add(user2)

    all_sprites.add(Deck((30, 690)))
    all_sprites.add(Deck((760, 690)))

    # Башни 1 поля
    all_sprites.add(Tower((166, 590), units_sprites, all_sprites, 1, image_for_test='tower_2.png'))
    all_sprites.add(Tower((504, 590), units_sprites, all_sprites, 1, image_for_test='tower_2.png'))
    all_sprites.add(Tower((337, 660), units_sprites, all_sprites, 1, image_for_test='king_tower_2.png', size=(120, 95)))
    # Башни 2 поля
    all_sprites.add(Tower((168, 86), units_sprites, all_sprites, 2))
    all_sprites.add(Tower((506, 86), units_sprites, all_sprites, 2))
    all_sprites.add(Tower((335, 23), units_sprites, all_sprites, 2, image_for_test='king_tower.png', size=(120, 95)))

    # Карты первого игрока(управление WASD)
    cards1 = [Card("card_unit", (-40, 545)), Card("card_unit", (110, 545)), Card("card_unit", (260, 545)), Card("card_unit", (410, 545))]
    cards1[0].new_value(1)
    for el in cards1:
        cards_sprites.add(el)

    # Карты второго игрока(управление стрелками)
    cards2 = [Card("card_unit", (700, 545)), Card("card_unit", (850, 545)), Card("card_unit", (1000, 545)), Card("card_unit", (1150, 545))]
    cards2[0].new_value(1)
    for el in cards2:
        cards_sprites.add(el)

    # Счетчик выбраной карты у игрока 1 и игрока 2
    card_number2 = 0
    card_number1 = 0
    #Состояние игрока(0 - выбор карты, 1 - выставление карты)
    stage1 = 0
    stage2 = 0
    #УПРАВЛЕНИЕ В ИГРЕ НА WASD И СТРЕЛКИ. ПЕРЕМЕЩЕНИЕ МЕЖДУ КАРТАМИ ЭТО НАЖАНИЕ ВЛЕВО ВПРАВО, ВВЕРХ - ВЫБОР КАРТЫ. ОТМЕНА ДЕЙСТВИЯ Q ИЛИ ПРАВЫЙ КОНТРОЛ. ВЫСТАВЛЕНИЕ E ИЛИ ПРАВЫЙ ШИФТ
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if stage1 == 0:
                    if event.key == pygame.K_RIGHT:
                        cards2[card_number2 % 4].new_value(0)
                        card_number2 += 1
                        cards2[card_number2 % 4].new_value(1)
                    if event.key == pygame.K_LEFT:
                        cards2[card_number2 % 4].new_value(0)
                        card_number2 -= 1
                        cards2[card_number2 % 4].new_value(1)
                    if event.key == pygame.K_UP:
                        stage1 = 1
                        circle1 = Circl((1029, 464))
                        circleses.add(circle1)

                if stage2 == 0:
                    if event.key == pygame.K_a:
                        cards1[card_number1 % 4].new_value(0)
                        card_number1 -= 1
                        cards1[card_number1 % 4].new_value(1)
                    if event.key == pygame.K_d:
                        cards1[card_number1 % 4].new_value(0)
                        card_number1 += 1
                        cards1[card_number1 % 4].new_value(1)
                    if event.key == pygame.K_w:
                        stage2 = 1
                        circle2 = Circl((288, 459))
                        circleses.add(circle2)

            if stage1 == 1:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    pos = circle1.get_coord()
                    circle1.replace((max(pos[0] - 7, 795), pos[1]))
                if keys[pygame.K_RIGHT]:
                    pos = circle1.get_coord()
                    circle1.replace((min(pos[0] + 7, 1255), pos[1]))
                if keys[pygame.K_UP]:
                    pos = circle1.get_coord()
                    circle1.replace((pos[0], max(pos[1] - 7, 379)))
                if keys[pygame.K_DOWN]:
                    pos = circle1.get_coord()
                    circle1.replace((pos[0], min(pos[1] + 7, 650)))
                if keys[pygame.K_RCTRL]:
                    stage1 = 0
                    circleses.remove(circle1)
                if keys[pygame.K_RSHIFT]:
                    stage1 = 0
                    circleses.remove(circle1)
                    pos = circle1.get_coord()
                    all_sprites.add(Melee(invert((pos[0] + 25, pos[1] + 25)), 1, 100, 10, 200, 2, units_sprites, 2, image_for_test='Test_unit.png'))

            if stage2 == 1:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    pos = circle2.get_coord()
                    circle2.replace((max(pos[0] - 7, 72), pos[1]))
                if keys[pygame.K_d]:
                    pos = circle2.get_coord()
                    circle2.replace((min(pos[0] + 7, 518), pos[1]))
                if keys[pygame.K_w]:
                    pos = circle2.get_coord()
                    circle2.replace((pos[0], max(pos[1] - 7, 379)))
                if keys[pygame.K_s]:
                    pos = circle2.get_coord()
                    circle2.replace((pos[0], min(pos[1] + 7, 630)))
                if keys[pygame.K_q]:
                    stage2 = 0
                    circleses.remove(circle2)
                if keys[pygame.K_e]:
                    stage2 = 0
                    circleses.remove(circle2)
                    pos = circle2.get_coord()
                    all_sprites.add(Ranged((pos[0] + 25, pos[1] + 25), 100, 200, 15, 50, 2, units_sprites, all_sprites, 1))

        all_sprites.draw(screen)
        all_sprites.update()
        circleses.draw(screen)
        cards_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    running = True
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 100)
    clock = pygame.time.Clock()
    menu()