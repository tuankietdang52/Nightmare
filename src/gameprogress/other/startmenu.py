import src.hud.menu.view.startmenuhud as hud_sm
import src.gameprogress.begin.beginning as bg
import src.gameprogress.part as gp
import src.mapcontainer.housenormal as mphouse

from src.pjenum import EState
from src.hud import *
from src.utils import *


class StartMenu(gp.Part):
    def __init__(self, screen: pg.surface.Surface):
        super().__init__(screen)

        self.startmenu = hud_sm.StartMenuHUD(screen)
        self.__hide_player()

        self.__is_open_board = False

    def __hide_player(self):
        gm.Manager.get_instance().player.get_image().set_alpha(0)

    def setup(self):
        self.__setup_map()
        self.__setup_player()

        self.manager.update_UI_ip()
        self.manager.wait(1, False)

    def __draw_start_menu(self):
        elements = self.startmenu.get_elements()

        Effect.fade_in_list(self.screen, elements)
        self.startmenu.init_pointer()

    def __setup_map(self):
        self.manager.set_map(mphouse.HouseNormal(self.screen))
        gamemap = self.manager.gamemap
        gamemap.change_sect("Room")
        gamemap.sect.create()

    def __setup_player(self):
        player = self.manager.player
        gamemap = self.manager.gamemap

        start_point = gamemap.sect.get_start_point()

        player.set_image("sit", (36, 80))
        player.set_position(start_point)
        player.set_state(EState.BUSY)

    def __show_sponsor(self):
        for item in self.startmenu.get_sponsor_list():
            Effect.fade_in_list(self.screen, [item])
            gm.Manager.get_instance().wait(2)

            Effect.fade_out_list(self.screen, [item])
            gm.Manager.get_instance().wait(2)

    def pressing_key(self):
        if not self.can_press_key:
            return

        keys = pg.key.get_pressed()

    def event_action(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

    def __check_choice(self):
        self.startmenu.update()
        choice = self.startmenu.get_choice()

        if choice == 1:
            self.can_press_key = False
            self.next()

        elif choice == 2:
            pass

        elif choice == 3:
            pass

        elif choice == 4:
            sys.exit()

    def update(self):
        if self.get_progress_index() != 3:
            super().update()
        else:
            self.manage_progress()

    def manage_progress(self):
        progress = self.get_progress_index()
        if progress == 0:
            self.__show_sponsor()
            self.next()

        elif progress == 1:
            self.setup()
            self.next()

        elif progress == 2:
            self.__setup_start_menu()
            self.next()

        elif progress == 3:
            self.__check_choice()

        elif progress == 4:
            pg.mixer.music.fadeout(1000)
            self.__destroying()

    def __setup_start_menu(self):
        if not pg.mixer.music.get_busy():
            gm.Manager.play_theme("../Assets/Sound/Other/rain.mp3")

        self.__draw_start_menu()
        self.can_press_key = True

    def __destroy_start_menu(self):
        elements = self.startmenu.get_elements()
        Effect.fade_out_list(self.screen, elements)

    def __destroying(self):
        self.__destroy_start_menu()

        player = self.manager.player

        x, y = player.get_position()

        player.set_position((x - 50, y))
        player.set_image("walk1")
        player.flip_horizontal()

        self.manager.update_UI_ip()
        player.set_state(EState.FREE)

        self.manager.set_part(bg.BeginStory(self.screen))
