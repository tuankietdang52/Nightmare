import src.utils.effect as ge
import src.hud.menu.presenter.menupresenter as smpr
import src.hud.menu.model.menumodel as smm


from src.hud.menu.contract import *


class BaseMenuView(MenuContract.IView, pg.sprite.Sprite):
    FONTPATH = "../Assets/Font/Crang.ttf"

    def __init__(self, screen, max_choice: int, groups: pg.sprite.Group):
        super().__init__(groups)

        self.image = None
        self.rect = None

        self.screen = screen
        self.presenter = smpr.MenuPresenter(self, smm.MenuModel(max_choice))
        self.elements: list[tuple[pg.surface.Surface, pg.rect.Rect]] = list()

    def __write_text(self, text: str, size: int) -> pg.surface.Surface:
        font = pg.font.Font(self.FONTPATH, size)
        text_surf = ge.Effect.create_text_outline(font,
                                                  text,
                                                  (255, 255, 255),
                                                  3,
                                                  (255, 0, 0))

        return text_surf

    def create_txt_element(self,
                           text: str,
                           size: int,
                           pos: tuple[float, float]) -> tuple[pg.surface.Surface, pg.rect.Rect]:
        title = self.__write_text(text, size)

        title_rect = title.get_rect(center=pos)
        return title, title_rect

    def update(self):
        pass

    def setup(self):
        pass

    def get_elements(self):
        pass

    def get_screen(self):
        pass

    def set_choice(self, choice: int):
        pass

    def get_choice(self) -> int:
        pass

    def __init_elements(self):
        pass

    def __draw_elements(self):
        for item in self.elements:
            self.image.blit(item[0], item[1])

    def draw(self):
        self.__draw_elements()
        pointer = self.presenter.get_pointer()
        pointer.draw()

    def destroy(self):
        self.kill()
        self.presenter.get_pointer().destroy()
