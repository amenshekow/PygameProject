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
    return width - pos[0], height - pos[1] + 50


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
    def __init__(self, title, coord,  unit, cost, pos, name, attack_r, visual_r, power, hp, speed, units_sprites, all_sprites, user, assets, *group):
        super().__init__(title, coord, *group)
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.cost = cost
        self.unit = unit
        self.pos = pos
        self.name = name
        self.attack_r = attack_r
        self.visual_r = visual_r
        self.power = power
        self.hp = hp
        self.speed = speed
        self.units_sprites = units_sprites
        self.all_sprites = all_sprites
        self.user = user
        self.assets = assets
        self.sost = 0

    def upd(self):
        if self.sost == 0:
            image = load_image(self.title + ".png")
            image = pygame.transform.scale(image, (200, 200))
            self.image = image
        else:
            image = load_image(self.title + "1.png")
            image = pygame.transform.scale(image, (200, 200))
            self.image = image

    # value = 1, если карта выбрана игроком, 0 иначе
    def new_value(self, value):
        self.sost = value
        self.upd()

    def get_info(self):
        return [self.sost,
                self.unit, self.cost, self.pos,
        self.name,
        self.attack_r,
        self.visual_r,
        self.power,
        self.hp,
        self.speed,
        self.units_sprites,
        self.all_sprites,
        self.user,
        self.assets]


class Elecsir(pygame.sprite.Sprite):
    image0 = load_image("elec0.png")
    image1 = load_image("elec1.png")
    image2 = load_image("elec2.png")
    image3 = load_image("elec3.png")
    image4 = load_image("elec4.png")
    image5 = load_image("elec5.png")
    image6 = load_image("elec6.png")
    image7 = load_image("elec7.png")
    image8 = load_image("elec8.png")
    image9 = load_image("elec9.png")
    image10 = load_image("elec10.png")
    image0 = pygame.transform.scale(image0, (195, 720))
    image1 = pygame.transform.scale(image1, (195, 720))
    image2 = pygame.transform.scale(image2, (195, 720))
    image3 = pygame.transform.scale(image3, (195, 720))
    image4 = pygame.transform.scale(image4, (195, 720))
    image5 = pygame.transform.scale(image5, (195, 720))
    image6 = pygame.transform.scale(image6, (195, 720))
    image7 = pygame.transform.scale(image7, (195, 720))
    image8 = pygame.transform.scale(image8, (195, 720))
    image9 = pygame.transform.scale(image9, (195, 720))
    image10 = pygame.transform.scale(image10, (195, 720))
    def __init__(self, pos, *group):
        super().__init__(*group)
        self.image = Elecsir.image0
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.pos = pos
    def new_value(self, value):
        pos = self.pos
        if value == 0:
            self.image = Elecsir.image0
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        if value == 1:
            self.image = Elecsir.image1
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        if value == 2:
            self.image = Elecsir.image2
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        if value == 3:
            self.image = Elecsir.image3
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        if value == 4:
            self.image = Elecsir.image4
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        if value == 5:
            self.image = Elecsir.image5
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        if value == 6:
            self.image = Elecsir.image6
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        if value == 7:
            self.image = Elecsir.image7
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        if value == 8:
            self.image = Elecsir.image8
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        if value == 9:
            self.image = Elecsir.image9
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        if value == 10:
            self.image = Elecsir.image10
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos[1]


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
    def __init__(self, size, pos, name, attack_r, visual_r, power, hp, speed, units_sprites, all_sprites, user, assets):
        super().__init__(units_sprites)
        self.units_sprites = units_sprites
        self.all_sprites = all_sprites
        self.assets = assets

        self.name = name
        print(self.name)
        self.user = user
        self.size = size
        self.update_speed = None
        self.dir = 1
        self.pos = pos
        if self.user == 2:
            self.dir = 5
        self.status = 0
        self.cut_sheet()
        self.cur_frame = 0
        self.rev = False
        self.image = self.frames[self.cur_frame]
        self.image_2 = self.frames2[self.cur_frame]
        self.image = pygame.transform.scale(self.image, size)
        self.image_2 = pygame.transform.scale(self.image_2, size)
        if self.rev:
            self.image = pygame.transform.flip(self.image, True, False)
            self.image_2 = pygame.transform.flip(self.image_2, True, False)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]


        self.attack_r = attack_r
        self.visual_r = visual_r
        self.power = power
        self.hp = hp
        self.max_hp = hp
        self.speed = speed

        self.target = None
        self.target_pos = (-1000, -1000)

        self.last_attack_time = time()
        self.last_update_time = 0
        self.last_move_time = 0

        if type(self) == Building:
            self.cannon_base = load_image('cannon_base.png')
            self.cannon_base = pygame.transform.scale(self.cannon_base, (80, 80))

    def cut_sheet(self):
        self.frames = []
        self.frames2 = []
        columns = self.assets[self.name][0][self.status][0]
        rows = self.assets[self.name][0][self.status][1]
        self.update_speed = self.assets[self.name][0][2]

        sheet = self.assets[self.name][self.dir][0 + self.status]
        sheet2 = self.assets[self.name][self.dir][2 + self.status]
        if self.user == 2:
            sheet = sheet[:-1] + 'r'
            sheet2 = sheet2[:-1] + 'b'
        for el in sheet, sheet2:
            temp = el
            el = el + '.png'
            if el[0] == '-':
                el = el[1:]
                el = pygame.transform.flip(load_image(self.name + '\\' + el), True, False)
            else:
                el = load_image(self.name + '\\' + el)

            rect = pygame.Rect(self.pos[0], self.pos[1], el.get_width() // columns,
                                    el.get_height() // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (rect.w * i, rect.h * j)
                    frame = el.subsurface(pygame.Rect(frame_location, rect.size))
                    if temp == sheet:
                        self.frames.append(frame)
                    else:
                        self.frames2.append(frame)

    def update(self):
        if self.target not in self.all_sprites:
            self.target = None
        self.targeting()

        self.last_update_time += 1
        if self.last_update_time == self.update_speed:
            self.last_update_time = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image_2 = self.frames2[self.cur_frame]
            self.image = pygame.transform.scale(self.image, self.size)
            self.image_2 = pygame.transform.scale(self.image_2, self.size)
            if self.rev:
                self.image = pygame.transform.flip(self.image, True, False)
                self.image_2 = pygame.transform.flip(self.image_2, True, False)
            self.mask = pygame.mask.from_surface(self.image)

        if self.status == 0:
            self.last_move_time += 1
            if self.last_move_time == 5:
                self.last_move_time = 0
                self.moving()
        else:
            self.last_move_time = 0

        status = self.status
        self.attacking()
        if self.status != status:
            # if type(self) == Princess and self.status == 1:
            #     self.pos = (self.pos[0] - 50, self.pos[1] - 30)
            self.cut_sheet()
            self.cur_frame = 0

        self.hp_check()

        self.reflection()

        if type(self) == Building:
            screen.blit(self.cannon_base, self.pos)
            screen.blit(self.cannon_base, invert(self.pos))

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
                                    dx += randint(-1, 1)
                                elif self.pos[1] == el.pos[1] and self.target not in collide_list:
                                    dy += randint(-1, 1)
                                if self.pos[0] > el.pos[0]:
                                    dx -= randint(-1, 3)
                                if self.pos[0] < el.pos[0]:
                                    dx += randint(-1, 3)
                                if self.pos[1] > el.pos[1]:
                                    dy += randint(-1, 3)
                                if self.pos[1] < el.pos[1]:
                                    dy -= randint(-1, 3)
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

        rev = False
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        d = (dx ** 2 + dy ** 2) ** 0.5
        if d > 0:
            dx /= d
            dy /= d
        if self.visual_r >= d or type(self.target) == Princess:
            dir = 0
            rev = False

            if abs(dx) > abs(dy):  # Движение по X
                if dx > 0:
                    dir = 3
                else:
                    dir = 3
                    rev = True
            elif abs(dy) > abs(dx):  # Движение по Y
                if dy > 0:
                    dir = 5
                else:
                    dir = 1
            if dx > 0 and dy > 0 and abs(dx) > 0.3:
                dir = 4
            elif dx > 0 and dy < 0 and abs(dx) > 0.3:
                dir = 2
            elif dx < 0 and dy > 0 and abs(dx) > 0.3:
                dir = 4
                rev = True
            elif dx < 0 and dy < 0 and abs(dx) > 0.3:
                dir = 2
                rev = True

            if (self.dir != dir or rev != self.rev) and dir != 0:
                self.dir = dir
                self.rev = rev
                self.cut_sheet()
                self.cur_frame = 0

    # Определение цели

    def targeting(self):
        nearest_target = None
        nearest_target_pos = (-1000, -1000)
        nearest_tower = None
        nearest_tower_pos = (-1000, -1000)

        if not self.target or type(self.target) == Princess:
            for el in self.units_sprites:
                if el.user != self.user:
                    if type(el) == Princess:
                        if self.distance(self.pos, el.pos) < self.distance(self.pos, nearest_tower_pos):
                            nearest_tower = el
                            nearest_tower_pos = el.pos
                    if self.distance(self.pos, el.pos) < self.visual_r:
                        if self.distance(self.pos, el.pos) < self.distance(self.pos, nearest_target_pos):
                            nearest_target = el
                            nearest_target_pos = el.pos
            if (nearest_target == nearest_tower or not nearest_target) or type(self) == Siege:
                self.target = nearest_tower
                self.target_pos = nearest_tower_pos
            else:
                self.target = nearest_target
                self.target_pos = nearest_target_pos

        # Если цель на другой стороне поля, необходимо пройти через ближайший мост (временная цель)
        if type(self) != Princess:
            bridges = [(160, 340), (510, 340)]
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
        if self.distance(self.pos, self.target.pos) <= self.attack_r or pygame.sprite.collide_mask(self, self.target) \
                or type(self.target) == Princess and pygame.sprite.collide_mask(self, self.target.tower):
            self.status = 1
            if cur_time - self.last_attack_time >= 1:
                print(self, 'attacks', self.target)
                self.last_attack_time = cur_time
                if type(self) == Ranged or type(self) == Princess:
                    self.all_sprites.add(Projectile((40, 40), self.pos, 'arrow.png', self.distance(self.pos, self.target.pos) / 20, self.target))
                if type(self) == Building:
                    self.all_sprites.add(Projectile((40, 40), self.pos, 'cannon_ball.png', self.distance(self.pos, self.target.pos) / 20, self.target))
                self.target.hp -= self.power
        else:
            self.status = 0

    def hp_check(self):
        if self.hp != self.max_hp and self.hp > 0:
            colors = ['lightblue', 'pink']
            if self.user == 2:
                colors.reverse()

            back_image = pygame.Surface([self.mask.get_size()[0] * 0.25, 5])
            pos = (self.pos[0] - self.mask.get_size()[0] * 0.20, self.rect.y + self.mask.get_size()[1] * 0.1)
            screen.blit(back_image, pos)
            screen.blit(back_image, invert((pos[0] + back_image.get_size()[0] + 10, pos[1] + self.mask.get_size()[1] + self.mask.get_size()[1] * 0.9 + 10)))

            image = pygame.Surface([self.mask.get_size()[0] * 0.25 * (self.hp / self.max_hp) - 1, 5 - 1])
            image.fill(pygame.Color(colors[0]))
            pos = (self.pos[0] - self.mask.get_size()[0] * 0.20 + 1, self.rect.y + self.mask.get_size()[1] * 0.1)
            screen.blit(image, pos)
            image.fill(pygame.Color(colors[1]))
            screen.blit(image, invert((pos[0] + back_image.get_size()[0] + 10, pos[1] + self.mask.get_size()[1] + self.mask.get_size()[1] * 0.9 + 10)))

        if self.hp <= 0:
            self.kill()

    # Отрисовка второго поля (изображение дублируется)
    def reflection(self):
        screen.blit(self.image_2, invert((self.rect.right - 10, self.rect.bottom + 195)))

    def new_coord(self, pos):
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]


class Princess(Unit):
    def __init__(self, pos, name, units_sprites, all_sprites, user, assets, tower, size=(120, 120), king=None):
        super().__init__(size, pos, name, 200, 200, 20, 1000, 0, units_sprites, all_sprites, user, assets)
        self.pos = pos
        self.user = user
        self.tower = tower
        self.king = king
        all_sprites.add(self.tower)
        if self.king:
            all_sprites.add(self.king)

    def hp_check(self):
        if self.hp != self.max_hp and self.hp > 0:
            colors = ['lightblue', 'pink']
            if self.user == 2:
                colors.reverse()

            back_image = pygame.Surface([self.mask.get_size()[0] * 0.5, 10])
            pos = (self.pos[0] - self.mask.get_size()[0] * 0.20 - 5, self.rect.y + self.mask.get_size()[1] * 1.2)
            screen.blit(back_image, pos)
            screen.blit(back_image, invert((pos[0] + back_image.get_size()[0] - 3,
                                            pos[1] + self.mask.get_size()[1] + self.mask.get_size()[1] * 0.9)))

            image = pygame.Surface([self.mask.get_size()[0] * 0.50 * (self.hp / self.max_hp) - 1, 10 - 1])
            image.fill(pygame.Color(colors[0]))
            pos = (self.pos[0] - self.mask.get_size()[0] * 0.20 - 5 + 1, self.rect.y + self.mask.get_size()[1] * 1.2)
            screen.blit(image, pos)
            image.fill(pygame.Color(colors[1]))
            screen.blit(image, invert((pos[0] + back_image.get_size()[0] - 5,
                                       pos[1] + self.mask.get_size()[1] + self.mask.get_size()[1] * 0.9)))

        if self.hp <= 0:
            self.kill()
            self.tower.kill()
            if self.king:
                self.king.kill()

    def reflection(self):
        screen.blit(self.image_2, invert((self.rect.right - 5, self.rect.bottom + 260)))


# Юнит ближнего боя
class Melee(Unit):
    def __init__(self, pos, name, attack_r, visual_r, power, hp, speed, units_sprites, all_sprites, user, assets):
        super().__init__((160, 160), pos, name, attack_r, visual_r, power, hp, speed, units_sprites, all_sprites, user, assets)
        self.pos = pos
        self.user = user


def create_Melee(pos, name, attack_r, visual_r, power, hp, speed, units_sprites, all_sprites, user, assets):
    return Melee(pos, name, attack_r, visual_r, power, hp, speed, units_sprites, all_sprites, user, assets)


# Юнит дальнего боя
class Ranged(Unit):
    def __init__(self, pos, name, attack_r, visual_r, power, hp, speed, units_sprites, all_sprites, user, assets):
        super().__init__((90, 90), pos, name, attack_r, visual_r, power, hp, speed, units_sprites, all_sprites, user, assets)
        self.pos = pos
        self.user = user


def create_Ranged(pos, name, attack_r, visual_r, power, hp, speed, units_sprites,  all_sprites, user, assets):
    return Ranged(pos, name, attack_r, visual_r, power, hp, speed, units_sprites, all_sprites, user, assets)


# Юнит осады
class Siege(Unit):
    def __init__(self, pos, name, attack_r, visual_r, power, hp, speed, units_sprites, all_sprites, user, assets):
        super().__init__((160, 160), pos, name, attack_r, visual_r, power, hp, speed, units_sprites, all_sprites, user, assets)
        self.pos = pos
        self.user = user


def create_Siege(pos, name, attack_r, visual_r, power, hp, speed, units_sprites, all_sprites, user, assets):
    return Siege(pos, name, attack_r, visual_r, power, hp, speed, units_sprites, all_sprites, user, assets)


# Юнит-здание
class Building(Unit):
    def __init__(self, pos, name, attack_r, visual_r, power, hp, speed, units_sprites, all_sprites, user, assets):
        super().__init__((80, 80), pos, name, attack_r, visual_r, power, hp, speed, units_sprites, all_sprites, user, assets)
        self.pos = pos
        self.user = user


def create_Building(pos, name, attack_r, visual_r, power, hp, speed, units_sprites, all_sprites, user, assets):
    return Building(pos, name, attack_r, visual_r, power, hp, speed, units_sprites, all_sprites, user, assets)


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

        screen.blit(pygame.transform.rotate(self.image, 180), invert((self.rect.right, self.rect.bottom + 200)))


class Tower(pygame.sprite.Sprite):
    def __init__(self, size, pos, image_p, user):
        super().__init__()
        self.image = load_image(image_p)
        self.image = pygame.transform.scale(self.image, size)
        if user == 1:
            self.image_2 = load_image(image_p[:-5] + 'r.png')
        else:
            self.image_2 = load_image(image_p[:-5] + 'b.png')
        self.image_2 = pygame.transform.scale(self.image_2, size)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.pos = pos

    def update(self):
        screen.blit(self.image_2, invert((self.rect.right - 3, self.rect.bottom + 143)))


class King(pygame.sprite.Sprite):
    def __init__(self, size, pos, image_p, user):
        super().__init__()
        self.image = load_image(image_p)
        self.image = pygame.transform.scale(self.image, size)
        if user == 1:
            self.image_2 = load_image(image_p[:-5] + 'r.png')
        else:
            self.image_2 = load_image(image_p[:-5] + 'b.png')
        self.image_2 = pygame.transform.scale(self.image_2, size)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.pos = pos

    def update(self):
        screen.blit(self.image_2, invert((self.rect.right - 3, self.rect.bottom + 230)))


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
    circleses = pygame.sprite.Group()  # Класс с кругами при выставлении юнита
    back = Back()
    elec_sprite1 = Elecsir((555, 40))
    all_sprites.add(back)
    all_sprites.add(elec_sprite1)
    circleses.add(elec_sprite1)
    elec_sprite2 = Elecsir((670, 40))
    all_sprites.add(elec_sprite2)
    circleses.add(elec_sprite2)
    user1 = Field()
    user2 = Field()
    user1.number(1)
    user2.number(2)
    all_sprites.add(user1)
    all_sprites.add(user2)

    all_sprites.add(Deck((30, 690)))
    all_sprites.add(Deck((760, 690)))

    # Подгрузка списков ассетов юнитов
    units_assets = dict()
    with open('units_info.txt', mode='r') as f:
        a = []
        for _ in range(int(f.readline()) * 6):
            a.append(f.readline().split())
        for el in a:
            if el[0] not in units_assets.keys():
                units_assets[el[0]] = [(tuple(list(map(int, list(el[1])))[:2]), tuple(list(map(int, list(el[1])))[2:-1]), list(map(int, list(el[1])))[-1])]
            else:
                units_assets[el[0]].append(tuple(el[1:]))
        for key, value in units_assets.items():
            print(key, value)

    # Башни 1 игрока
    all_sprites.add(Princess((167, 540), 'princess', units_sprites, all_sprites, 1, units_assets, Tower((200, 200), (167, 595), 'princess_tower_b.png', 1)))
    all_sprites.add(Princess((502, 540), 'princess', units_sprites, all_sprites, 1, units_assets, Tower((200, 200), (503, 595), 'princess_tower_b.png', 1)))
    all_sprites.add(Princess((337, 630), 'princess', units_sprites, all_sprites, 1, units_assets, Tower((260, 260), (337, 675), 'king_tower_b.png', 1), size=(120, 95), king=King((200, 200), (337, 620), 'king_b.png', 1)))

    # Башни 2 игрока
    all_sprites.add(Princess((170, 50), 'princess', units_sprites, all_sprites, 2, units_assets, Tower((200, 200), (170, 112), 'princess_tower_r.png', 2)))
    all_sprites.add(Princess((510, 50), 'princess', units_sprites, all_sprites, 2, units_assets, Tower((200, 200), (507, 112), 'princess_tower_r.png', 2)))
    all_sprites.add(Princess((335, -40), 'princess', units_sprites, all_sprites, 2, units_assets, Tower((260, 260), (335, 33), 'king_tower_r.png', 2), size=(120, 95), king=King((200, 200), (335, 0), 'king_r.png', 2)))


    # Карты первого игрока(управление WASD)
    cards1 = [
        Card("knight", (-13, 590), create_Melee, 4, (1000,1000), "knight", 1, 200, 100, 300, 2, units_sprites, all_sprites, 1, units_assets),
        Card("archer", (137, 590), create_Ranged, 3, (1000,1000), "archer", 200, 300, 50, 150, 3, units_sprites, all_sprites, 1, units_assets),
        Card("giant", (287, 590), create_Siege, 5, (1000,1000), "giant", 3, 200, 150, 500, 1, units_sprites, all_sprites, 1, units_assets),
        Card("cannon", (437, 590), create_Building, 2, (1000,1000), "cannon", 200, 300, 150, 300, 0, units_sprites, all_sprites, 1, units_assets)]
    cards1[0].new_value(1)
    for el in cards1:
        cards_sprites.add(el)

    # Карты второго игрока(управление стрелками)
    cards2 = [Card("knight", (740, 590), create_Melee, 4, (1000, 1000), "knight", 1, 200, 100, 300, 2, units_sprites, all_sprites, 2, units_assets),
        Card("archer", (890, 590), create_Ranged, 3, (1000, 1000), "archer", 200, 300, 50, 150, 3, units_sprites, all_sprites, 2, units_assets),
        Card("giant", (1040, 590), create_Siege, 5, (1000, 1000), "giant", 3, 200, 150, 500, 1, units_sprites, all_sprites, 2, units_assets),
        Card("cannon", (1190, 590), create_Building, 2, (1000, 1000), "cannon", 200, 300, 150, 300, 0, units_sprites, all_sprites, 2, units_assets)]
    cards2[0].new_value(1)
    for el in cards2:
        cards_sprites.add(el)

    elecsir1 = 2
    elecsir2 = 2
    MYEVENTTYPE1 = pygame.USEREVENT + 2
    pygame.time.set_timer(MYEVENTTYPE1, 60)

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
            if event.type == MYEVENTTYPE:
                if elecsir1 != 10:
                    elecsir1 = min(elecsir1 + 1, 10)
                    elec_sprite1.new_value(elecsir1)
                if elecsir2 != 10:
                    elecsir2 = min(elecsir2 + 1, 10)
                    elec_sprite2.new_value(elecsir2)

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
                    pos = circle1.get_coord()
                    for el in cards2:
                        inf = el.get_info()
                        if inf[0] == 1:
                            if elecsir2 >= inf[2]:
                                inf[1] = inf[1](inf[3], inf[4], inf[5], inf[6], inf[7], inf[8], inf[9], inf[10],
                                                inf[11], inf[12], inf[13])
                                elecsir2 -= inf[2]
                                inf[1].new_coord(invert((pos[0], pos[1] + 195)))
                                all_sprites.add(inf[1])
                                elec_sprite2.new_value(elecsir2)
                                stage1 = 0
                                circleses.remove(circle1)
                            break

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
                    pos = circle2.get_coord()
                    for el in cards1:
                        inf = el.get_info()
                        if inf[0] == 1:
                            if elecsir1 >= inf[2]:
                                inf[1] = inf[1](inf[3], inf[4], inf[5], inf[6], inf[7], inf[8], inf[9], inf[10],
                                                inf[11], inf[12], inf[13])
                                inf[1].new_coord((pos[0] + 25, pos[1] + 15))
                                elecsir1 -= inf[2]
                                all_sprites.add(inf[1])
                                elec_sprite1.new_value(elecsir1)
                                stage2 = 0
                                circleses.remove(circle2)
                            break

        all_sprites.draw(screen)
        all_sprites.update()
        circleses.draw(screen)
        cards_sprites.draw(screen)
        circleses.update()
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    running = True
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 2000)
    clock = pygame.time.Clock()
    menu()