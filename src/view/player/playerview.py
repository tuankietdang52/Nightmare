import pygame as pg
import src.mapcontainer.map as mp
import src.presenter.player.playerpresenter as playerpr
import src.view.baseview as vw


class PlayerView(vw.BaseView):
    """Position by topleft"""
    _instance = None
    screen = None
    gamemap = None

    def __init__(self):
        """
        Call init() instead.
        :exception RuntimeError: when calling
        """
        pg.sprite.Sprite.__init__(self)
        raise RuntimeError("Please call init() when init instance")

    # Singleton init #

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise TypeError("Must init instance first")

        return cls._instance

    @classmethod
    def init(cls, screen: pg.Surface, health: float):
        """
        Init instance for Player
        """

        if cls._instance is not None:
            print("Player is created before")
            return cls._instance

        cls._instance = cls.__new__(cls)
        pg.sprite.Sprite.__init__(cls.get_instance())

        cls.screen = screen

        cls.presenter = playerpr.PlayerPresenter(cls, screen, health)

        return cls._instance

    def set_position(self, pos: tuple[int, int] | pg.math.Vector2):
        self.presenter.set_position(pos)

    def get_position(self) -> pg.math.Vector2:
        return self.presenter.get_position()

    def set_size(self, size: tuple[int, int]):
        self.presenter.set_size(size)

    def get_size(self) -> tuple[int, int]:
        return self.presenter.get_size()

    def set_speed(self, speed: int):
        self.presenter.set_speed(speed)

    def get_speed(self) -> int:
        return self.get_speed()

    def get_rect(self) -> pg.rect.Rect:
        return self.presenter.get_rect()

    def set_image(self, image: str | pg.surface.Surface):
        self.presenter.set_image(image)

    def get_image(self) -> pg.surface.Surface:
        return self.presenter.get_image()

    def get_voice(self, voice: str) -> pg.mixer.Sound:
        """
        passing name of voice file (not path) into this function

        wav file required
        """
        return self.presenter.get_voice(voice)

    def update(self):
        self.draw()
        # pg.draw.rect(self.screen, (0, 255, 0), self.get_rect())

    def draw(self):
        image = self.presenter.get_image()
        rect = self.presenter.get_rect()

        self.screen.blit(image, rect)

    def moving(self, keys):
        self.presenter.handle_moving(keys)