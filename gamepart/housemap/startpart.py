import sys

import hud.startmenu as hud_sm
import gamemanage.effect as ge
import gamemanage.game as gm
import gamepart.housemap.firstpart as fp
import gamepart.part as gp

from pjenum import EState
from view.player.playerview import *
from hud import *


class Start(gp.Part):
    def __init__(self, screen, gamemap):
        self.screen = screen
        self.gamemap = gamemap

        self.player = PlayerView.get_instance()

        pg.mixer.music.load("Assets/Sound/rain.mp3")

        self.startmenu = hud_sm.StartMenu(screen)
        self.title_start = self.startmenu.get_start_title()
        self.elements = self.startmenu.get_elements()

        self.nextpart = fp.FirstPart(self.screen, self.gamemap)

        self.alpha = 0
        self.choice = 1

    def __setup(self):
        gamemap = self.gamemap
        player = self.player

        gamemap.sect.create()

        try:
            start_point = gamemap.sect.get_spawn_point()
        except AttributeError:
            start_point = gamemap.sect.get_start_point()

        player.set_position(start_point)

        player.presenter.set_state(EState.BUSY)
        player.presenter.set_img("sitleft")

        player.update()

        pg.display.update()
        pg.time.wait(1000)

    def __fade_in(self, ls):
        if self.alpha == 255:
            return

        self.alpha += 1
        ge.Effect.set_opacity(self.screen, ls, self.alpha)

    def __redraw_other(self):
        gm.Manager.update_UI()

    def __fade_out(self, ls):
        if self.alpha <= 0:
            return

        if self.gamemap.sect.is_created:
            gm.Manager.update_UI()

        self.alpha -= 1
        ge.Effect.set_opacity(self.screen, ls, self.alpha)

    def pressing_key(self):
        if not self.can_press_key:
            return

        keys = pg.key.get_pressed()

        if keys[pg.K_ESCAPE]:
            if self.is_open_board:
                self.__closing_board()

    def __open_board(self):
        self.is_open_board = True
        load_board = Board(self.screen, (400, 400), (700, 600))
        load_board.draw()

    def __closing_board(self):
        self.is_open_board = False
        self.__redraw_other()
        self.startmenu.draw_elements()
        self.startmenu.change_choice(2)

    def event_action(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if not self.can_press_key:
                    return

                key = event.key
                self.__move_cur(key)

    def __move_cur(self, key):
        if self.is_open_board:
            return

        if key == pg.K_RETURN:
            self.startmenu.pointer.play_choose_sound()
            self.__check_choice()
            return

        elif key == pg.K_w:
            if self.choice == 1:
                return
            self.choice -= 1

        elif key == pg.K_s:
            if self.choice == 3:
                return
            self.choice += 1

        else:
            return

        self.__redraw_other()
        self.startmenu.draw_elements()
        self.startmenu.change_choice(self.choice)

    def __check_choice(self):
        if self.choice == 1:
            self.can_press_key = False
            self.next()

        elif self.choice == 2:
            self.__open_board()

        elif self.choice == 3:
            sys.exit()

    def update(self):
        self.manage_progess()

    def manage_progess(self):
        progess = self.get_progess_index()
        if progess == 0:
            self.begin()

        elif progess == 1:
            self.__to_start_menu()

        elif progess == 2:
            self.__setup()
            self.next()

        elif progess == 3:
            self.__setup_start_menu()

        elif progess == 4:
            self.__fade_out(self.elements.values())
            pg.mixer.music.fadeout(1000)
            if self.alpha <= 0:
                self.__destroying()

    def begin(self):
        self.__fade_in([self.title_start])
        if self.alpha == 255:
            self.next()

    def __to_start_menu(self):
        self.screen.fill((0, 0, 0))
        self.__fade_out([self.title_start])
        if self.alpha <= 0:
            self.alpha = 0
            self.next()

    def __setup_start_menu(self):
        if not pg.mixer.music.get_busy():
            pg.mixer.music.play(True)
        self.__fade_in(self.elements.values())

        if self.alpha == 255 and not self.startmenu.pointer.is_set:
            self.startmenu.change_choice(1)
            self.can_press_key = True

    def __destroying(self):
        self.is_changing_part = True

        x, y = self.player.get_position()

        self.player.set_position((x - 50, y))
        self.player.presenter.set_img("left1")

        gm.Manager.update_UI_ip()
        self.player.presenter.set_state(EState.FREE)
