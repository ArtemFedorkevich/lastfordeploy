import pygame
import sys
import random
import time



class Game:
    # timecount используется для того, чтобы в начале игры была пауза в 1 секунду
    # (см функцию refresh_screen)
    timecount = 1

    def __init__(self):
        # задаем размеры экрана
        self.screen_width = 750
        self.screen_height = 450

        # необходимые цвета
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)

        # добавим звук
        pygame.mixer.init()
        pygame.mixer.music.load('intro.mp3')
        pygame.mixer.music.play()

        # Frame per second controller
        # будет задавать количество кадров в секунду
        self.fps_controller = pygame.time.Clock()

        # переменная для оторбражения результата
        self.score = 0

    def show_title(self):
        """Отображение приветственного экрана"""

        self.play_surface.fill(self.white)
        text_massive = ['Hello. You control a small ball in this game. ',
                        'Grow a large ball by eating smaller ones,',
                        'and achieve a result of 50 points.',
                        "Press SPACE to continue."]
        height = self.screen_height / 3
        for i in text_massive:
            go_font = pygame.font.Font('PiecesEight.ttf', 36)
            go_surf = go_font.render(i, True, self.red)
            go_rect = go_surf.get_rect()
            go_rect.midtop = (self.screen_width / 2, height)
            self.play_surface.blit(go_surf, go_rect)
            height += 30

    def next_screen(self):
        """Ожидаем ввода пробела в приветственном окне для запуска игры"""
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        done = True
        pygame.mixer.music.load('musicforgame.ogg')
        pygame.mixer.music.play()

    def init_and_check_for_errors(self):
        """Начальная функция для инициализации и
           проверки как запустится pygame"""
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit()
        else:
            print('Ok')

    def set_surface_and_title(self):
        """Задаем surface(поверхность поверх которой будет все рисоваться)
        и устанавливаем загаловок окна"""
        self.play_surface = pygame.display.set_mode((
            self.screen_width, self.screen_height))
        pygame.display.set_caption('Circles Game')
        
    def event_loop(self, change_to):
        """Функция для отслеживания нажатий клавиш игроком"""
        # запускаем цикл по ивентам
        for event in pygame.event.get():
            # если нажали клавишу
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = "DOWN"
                # нажали escape
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        return change_to

    def refresh_screen(self):
        """Обновляем экран и задаем фпс"""
        pygame.display.flip()
        game.fps_controller.tick(11)
        self.timecount += 1

        # добавил паузу в 1 секунду перед началом игры, чтобы осмотреться
        if self.timecount == 3:
            time.sleep(1)

    def show_score(self, choice=1):
        """Отображение результата"""
        s_font = pygame.font.Font('PiecesEight.ttf', 24)
        s_surf = s_font.render(
            'Score: {0}'.format(self.score), True, self.red)
        s_rect = s_surf.get_rect()
        # дефолтный случай отображаем результат слева сверху
        if choice == 1:
            s_rect.midtop = (80, 10)
        # при game_over отображаем результат по центру
        # под надписью game over
        else:
            s_rect.midtop = (self.screen_width / 2, 120)
        # рисуем прямоугольник поверх surface
        self.play_surface.blit(s_surf, s_rect)

    def game_over(self, t=0):
        """Функция для вывода надписи Game Over и результатов
        в случае завершения игры и выход из игры"""
        if t == 0:
            end = 'Game over'
            music = 'end2.mp3'
        else:
            end = 'You win'
            music = 'win1.mp3'
            self.score = 50
        # заливка белым в начале (чтобы убрать все точки)
        self.play_surface.fill(self.white)
        go_font = pygame.font.Font('PiecesEight.ttf', 72)
        go_surf = go_font.render(end, True, self.red)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (self.screen_width / 2, 15)
        self.play_surface.blit(go_surf, go_rect)
        pygame.display.flip()
        pygame.mixer.music.load(music)
        pygame.mixer.music.play()
        self.show_score(0)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()


class Sphere:
    def __init__(self, sphere_color):
        # важные переменные - позиция позиция точки в начале игры
        self.sphere_head_pos = [100, 50]
        self.sphere_color = sphere_color
        # направление движение змеи, изначально вправо
        self.sphere_radius = 5
        self.direction = "RIGHT"
        # куда будет меняться напрвление точки
        # при нажатии соответствующих клавиш
        self.change_to = self.direction

    def validate_direction_and_change(self):
        """Изменияем направление движения только в том случае,
        если оно не прямо противоположно текущему"""
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):
        """Изменияем положение точки"""
        if self.direction == "RIGHT":
            self.sphere_head_pos[0] += 10
        elif self.direction == "LEFT":
            self.sphere_head_pos[0] -= 10
        elif self.direction == "UP":
            self.sphere_head_pos[1] -= 10
        elif self.direction == "DOWN":
            self.sphere_head_pos[1] += 10

    def sphere_growth_mechanism(
            self, score, food_pos, food_size, screen_width, screen_height):
        # если съели еду
        if (pygame.math.Vector2(self.sphere_head_pos).distance_to(
                pygame.math.Vector2(food_pos)) < self.sphere_radius + food_size):
            # если радиус аватара меньше, чем точки, которую он съедает, наступает game_over
            if self.sphere_radius < food_size:
                time.sleep(1)
                game.game_over()
            else:
                # если съели еду то задаем новое положение еды почти случайным
                # образом и увеличивем score на один, и радиус на 1
                self.sphere_radius += 1
                # может как-то можно упростить
                # e, f, d - маркеры выполнения проверок (не называл их в соответствии со смыслом...)
                e = False
                f = False
                d = False
                while not e or not f or not d:
                    f = False
                    d = False
                    food_size = random.randint(self.sphere_radius - 2, self.sphere_radius + 5)
                    food_pos = [random.randrange(1, screen_width / 10) * 10,
                                random.randrange(1, screen_height / 10) * 10]
                    # проверка, что еда не сливается с другой едой
                    for i in Food.massive_coordinates:
                        if pygame.math.Vector2(food_pos[0], food_pos[1]).distance_to(
                                pygame.math.Vector2(i[0], i[1])) < i[2] + food_size:
                            e = False
                            break
                    else:
                        e = True
                        # проверка, чтобы еда не залазила на аватар
                        if pygame.math.Vector2(food_pos).distance_to(
                                pygame.math.Vector2(self.sphere_head_pos)) < self.sphere_radius + food_size + 10:
                            d = False
                            continue
                        else:
                            d = True
                            # проверка, чтобы еда не выходила за рамки экрана
                            if (food_pos[0] + food_size > screen_width - 10 or food_pos[0] + food_size < 0) \
                                    or (food_pos[1] + food_size > screen_height - 10 or food_pos[1] + food_size < 10):
                                f = False
                            else:
                                f = True

                score += 1

                # при счёте 50 game_over - но при передаче 1 запускается реализация победного экрана.
                if score == 50:
                    time.sleep(1)
                    game.game_over(1)

        return score, food_pos, food_size

    def draw_sphere(self, play_surface, surface_color):
        """Отображаем точку - наш аватар)"""
        play_surface.fill(surface_color)
        pygame.draw.circle(
            play_surface, self.sphere_color, pygame.math.Vector2(self.sphere_head_pos), self.sphere_radius)

    def check_for_boundaries(self, game_over, screen_width, screen_height):
        """Проверка, что столкунлись с концами экрана """
        if any((
                self.sphere_head_pos[0] > screen_width - 10
                or self.sphere_head_pos[0] < 0,
                self.sphere_head_pos[1] > screen_height - 10
                or self.sphere_head_pos[1] < 0
        )):
            time.sleep(1)
            game_over()


class Food:
    # в massive_coordinates хранятся координаты всех точек в формате:
    # список со списками [self.food_pos[0], self.food_pos[1], self.food_size, self.index])
    massive_coordinates = []

    def __init__(self, screen_width, screen_height, sphere_radius, index):
        """Инит еды"""
        # каждая точка индивидуальна - за это отвечает индекс
        self.index = index

        # оттенки красного (255, 0, 0), (227, 38, 54), (144, 0, 32), (196, 30, 58), (150, 0, 24),
        # (222, 49, 99), (205, 92, 92), (220, 20, 60), (128, 24, 24), (255, 0, 255), (255, 0, 144),
        # (128, 0, 0), (224, 176, 255), (199, 21, 133), (183, 65, 14), (204, 136, 153), (255, 36, 0),
        # (227, 66, 52), (229, 43, 80), (255, 0, 127)
        self.food_color = pygame.Color(random.choice(
            [(255, 0, 0), (227, 38, 54), (144, 0, 32), (196, 30, 58), (150, 0, 24), (222, 49, 99), (205, 92, 92),
             (220, 20, 60),
             (128, 24, 24), (255, 0, 255), (255, 0, 144), (128, 0, 0), (224, 176, 255), (199, 21, 133), (183, 65, 14),
             (204, 136, 153), (255, 36, 0),
             (227, 66, 52), (229, 43, 80), (255, 0, 127)]))
        self.food_size = random.randint(1, sphere_radius + 5)
        self.food_pos = [random.randrange(1, screen_width / 10) * 10,
                         random.randrange(1, screen_height / 10) * 10]

        # проверка, что точки не залазят друг на друга при создании
        # b - маркер, если True то цикл закончен и точки не налазят друг на друг
        b = False
        while not b:
            for i in self.massive_coordinates:
                if pygame.math.Vector2(self.food_pos[0], self.food_pos[1]).distance_to(
                        pygame.math.Vector2(i[0], i[1])) < i[2] + self.food_size:
                    self.food_pos = [random.randrange(1, screen_width / 10) * 10,
                                     random.randrange(1, screen_height / 10) * 10]
                    break
            else:
                b = True
        self.massive_coordinates.append([self.food_pos[0], self.food_pos[1], self.food_size, self.index])

    def draw_food(self, play_surface):
        """Отображение еды"""
        pygame.draw.circle(play_surface, self.food_color,
                           pygame.math.Vector2(self.food_pos[0], self.food_pos[1]), self.food_size)


class CommonFood:
    """18 точек"""

    def __init__(self, gamescreen_width, gamescreen_height, sphere_radius):
        self.allfoods = [Food(gamescreen_width, gamescreen_height, sphere_radius, index)
                         for index in range(18)]

    def draw_allfood(self, gameplay_surface):
        for i in self.allfoods:
            i.draw_food(gameplay_surface)

    def check_eatfood(self):
        for i in self.allfoods:
            g = i.food_pos
            game.score, i.food_pos, i.food_size = sphere.sphere_growth_mechanism(
                game.score, i.food_pos, i.food_size, game.screen_width, game.screen_height)
            # i.food_pos, - может измениться, если еду сьели,
            # и тогда нижний код с if будет выполняться,
            # если еду не съели - нижний код не будет выполняться

            # заменил координаты точки которую съели в массиве координат точек
            if g != i.food_pos:
                for j in Food.massive_coordinates:
                    if i.index == j[3]:
                        j[0] = i.food_pos[0]
                        j[1] = i.food_pos[1]
                        j[2] = i.food_size


game = Game()
sphere = Sphere(game.green)
food = CommonFood(game.screen_width, game.screen_height, sphere.sphere_radius)
game.init_and_check_for_errors()
game.set_surface_and_title()
game.show_title()
game.refresh_screen()
game.next_screen()

while True:
    sphere.change_to = game.event_loop(sphere.change_to)
    sphere.validate_direction_and_change()
    sphere.change_head_position()
    food.check_eatfood()
    sphere.draw_sphere(game.play_surface, game.white)
    food.draw_allfood(game.play_surface)
    sphere.check_for_boundaries(
        game.game_over, game.screen_width, game.screen_height)
    game.show_score()
    game.refresh_screen()
