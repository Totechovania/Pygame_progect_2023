import pygame as pg
from IFrame import IFrame
from Signals import KillEntireApp
from utilities import load_image

pg.init()
info = pg.display.Info()
w = info.current_w
h = info.current_h - 50
screen = pg.display.set_mode((w, h))
all_buttons_cords = []
event = ''


class MainMenu(IFrame):
    def __init__(self):
        self.all_sprites = pg.sprite.Group()
        screen.fill(pg.Color('white'))
        self.start_window()

    def update(self):
        global event
        for event in pg.event.get():
            if event.type == pg.QUIT:
                raise KillEntireApp
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = event.pos
                for x_start, x_end, y_start, y_end, name in all_buttons_cords:
                    if x_start < x < x_end and y_start < y < y_end:
                        all_buttons_cords.clear()
                        self.all_sprites.empty()
                        if name == 'leave':
                            raise KillEntireApp
                        if name == 'settings':
                            self.draw_settings()
                        if name == 'back':
                            self.start_window()
                        if name == 'game':
                            self.draw_game()
                        if name == 'fight':
                            self.draw_fight_menu()
                        if name == 'redactor':
                            self.draw_redactor_menu()
                        if name == 'campany':
                            self.draw_campany_menu()
                        if name == 'download':
                            self.draw_download_menu()
                        break
        self.all_sprites.draw(screen)
        self.all_sprites.update()
        pg.display.flip()

    def draw_redactor_menu(self):
        self.draw_fon()

        Button(self.all_sprites, 'back.png', 0, 0, int(0.04 * w), int(0.04 * w), 'back')
        Button(self.all_sprites, 'leave_button.png', w * 0.96, 0, int(0.04 * w), int(0.04 * w), 'leave')

    def draw_campany_menu(self):
        self.draw_fon()

        Button(self.all_sprites, 'back.png', 0, 0, int(0.04 * w), int(0.04 * w), 'back')
        Button(self.all_sprites, 'leave_button.png', w * 0.96, 0, int(0.04 * w), int(0.04 * w), 'leave')

    def draw_download_menu(self):
        self.draw_fon()

        Button(self.all_sprites, 'back.png', 0, 0, int(0.04 * w), int(0.04 * w), 'back')
        Button(self.all_sprites, 'leave_button.png', w * 0.96, 0, int(0.04 * w), int(0.04 * w), 'leave')

    def draw_fight_menu(self):
        self.draw_fon()

        Button(self.all_sprites, 'back.png', 0, 0, int(0.04 * w), int(0.04 * w), 'back')
        Button(self.all_sprites, 'leave_button.png', w * 0.96, 0, int(0.04 * w), int(0.04 * w), 'leave')

    def draw_game(self):
        self.draw_fon()

        Button(self.all_sprites, 'back.png', 0, 0, int(0.04 * w), int(0.04 * w), 'back')
        Button(self.all_sprites, 'leave_button.png', w * 0.96, 0, int(0.04 * w), int(0.04 * w), 'leave')

        Button(self.all_sprites, 'rectangle.png', w * 0.4, h * 0.1, int(w * 0.2), int(w * 0.08), 'fight')
        self.draw_text('Сражение', w // 2.35, h // 6.3, '#08E8DE', 155)
        Button(self.all_sprites, 'rectangle.png', w * 0.4, h * 0.25, int(w * 0.2), int(w * 0.08), 'redactor')
        self.draw_text('Редактор', w // 2.35, h // 3.25, '#08E8DE', 155)
        Button(self.all_sprites, 'rectangle.png', w * 0.4, h * 0.4, int(w * 0.2), int(w * 0.08), 'campany')
        self.draw_text('Кампания', w // 2.35, h // 2.15, '#08E8DE', 155)
        Button(self.all_sprites, 'rectangle.png', w * 0.4, h * 0.55, int(w * 0.2), int(w * 0.08), 'download')
        self.draw_text('Загрузить', w // 2.35, h // 1.62, '#08E8DE', 155)

    def draw_settings(self):
        self.draw_fon()

        Button(self.all_sprites, 'back.png', 0, 0, int(0.04 * w), int(0.04 * w), 'back')
        Button(self.all_sprites, 'leave_button.png', w * 0.96, 0, int(0.04 * w), int(0.04 * w), 'leave')

    def start_window(self):
        self.draw_fon()

        self.draw_text('MyAntiyoy', w // 2.58, h // 4.25, '#00FF7F', 200)

        Button(self.all_sprites, 'game_start_button.png', w * 0.46, h * 0.5, int(0.08 * w), int(0.08 * w), 'game')
        Button(self.all_sprites, 'settings_button.png', 0, 0, int(0.04 * w), int(0.04 * w), 'settings')
        Button(self.all_sprites, 'leave_button.png', w * 0.96, 0, int(0.04 * w), int(0.04 * w), 'leave')

    def draw_text(self, text, x, y, color, size=50):
        font = pg.font.Font(None, size)
        to_print = font.render(text, True, pg.Color(color))
        screen.blit(to_print, (x, y))

    def draw_fon(self):
        image = load_image('fon_menu.png')
        image = pg.transform.scale(image, (w, h))
        screen.blit(image, (0, 0))


class Button(pg.sprite.Sprite):
    def __init__(self, group, filename, x, y, new_size_w=500, new_size_h=500, name=''):
        super().__init__(group)
        image = load_image(filename)
        image = pg.transform.scale(image, (new_size_w, new_size_h))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        all_buttons_cords.append((x, x + new_size_w, y, y + new_size_h, name))

    def update(self, *args):
        pass
