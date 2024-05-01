import pygame as pg
import src.gamemanage.game as gm
import src.hud.playerhud as plhud


from src.pjenum.estate import EState
from src.utils import *


class Player(pg.sprite.Sprite):
    _instance = None
    __path = "../Assets/Ally/Viole/"
    animatepth = "walk0"
    __frame = 0

    def __init__(self, screen: pg.surface.Surface, groups: pg.sprite.Group):
        super().__init__(groups)
        self.screen = screen
        self.__state = EState.FREE

        self.size = 36, 80
        self.__speed = 1.5
        self.position = pg.math.Vector2()

        self.image = pg.image.load(f"{self.__path + self.animatepth}.png").convert_alpha()
        self.set_size(self.size)
        self.rect = self.image.get_rect()

        self.direction = "left"

        self.hungry_bar: plhud.HungryBar | None = None

    def init_hud(self, hud_groups: pg.sprite.Group):
        self.hungry_bar = plhud.HungryBar(self, hud_groups)

    # Get Set #
    def set_image(self, image: str | pg.surface.Surface, size: tuple[float, float] = None):
        size = self.get_size() if size is None else size

        if type(image) is str:
            self.image = pg.image.load(f"{self.__path + image}.png").convert_alpha()
        else:
            self.image = image

        self.set_size(size)

    def get_image(self) -> pg.surface.Surface:
        return self.image

    def flip_horizontal(self):
        self.image = pg.transform.flip(self.image, True, False)

    def get_state(self) -> EState:
        return self.__state

    def set_state(self, state: EState):
        self.__state = state
        if self.__state == EState.DEAD:
            self.dying()

    def set_position(self, pos: tuple[float, float] | pg.math.Vector2):
        if type(pos) is pg.math.Vector2:
            self.position = pos
        else:
            self.position = pg.math.Vector2(pos)

        self.rect = self.image.get_rect(center=self.position)

    def get_position(self) -> pg.math.Vector2:
        return self.position

    def set_speed(self, speed: float):
        self.__speed = speed

    def get_speed(self) -> float:
        return self.__speed

    def set_size(self, size: tuple[int, int]):
        self.image = pg.transform.scale(self.image, size)

    def get_size(self) -> tuple[int, int]:
        return self.image.get_size()

    def get_rect(self) -> pg.rect.Rect:
        return self.get_image().get_rect(center=self.get_position())

    def get_voice(self, voice: str) -> pg.mixer.Sound:
        path = f"../Assets/Sound/VioleVoice/{voice}.wav"
        return pg.mixer.Sound(path)

    # Movement #
    def __get_reverse_animate(self) -> str:
        direction_tuple = [
            ["down", "up"],
            ["left", "right"]
        ]

        for di in direction_tuple:
            if self.direction == di[0]:
                return di[1]

            elif self.direction == di[1]:
                return di[0]

        return ""

    def handle_moving(self, keys: pg.key.ScancodeWrapper):
        if self.__state != EState.FREE and self.__state != EState.PANIC:
            return

        speed = self.get_speed()
        velocity = pg.math.Vector2()

        if keys[pg.K_w]:
            velocity.y = -speed
            self.direction = "up"

        elif keys[pg.K_d]:
            velocity.x = speed
            self.direction = "right"

        elif keys[pg.K_a]:
            velocity.x = -speed
            self.direction = "left"

        elif keys[pg.K_s]:
            velocity.y = speed
            self.direction = "down"

        else:
            return

        manager = gm.Manager.get_instance()

        if not self.can_move(velocity):
            return

        if self.__state == EState.PANIC:
            self.direction = self.__get_reverse_animate()
            velocity = velocity[0] * -1, velocity[1] * -1

        self.moving(velocity)
        self.moving_animation(self.direction)
        manager.update_UI_ip()

    def can_move(self, velocity: pg.math.Vector2) -> bool:
        next_pos = self.position + velocity

        rect = self.image.get_rect(center=next_pos)

        if Physic.is_collide_wall(rect):
            return False

        return True

    def moving(self, velocity: pg.math.Vector2):
        position = self.get_position() + velocity
        self.set_position(position)

        self.hungry_bar.decrease_amount(0.1)

    def moving_animation(self, direction):
        if self.__frame < 20:
            index = 1

        else:
            index = 0

        self.__frame += 1
        if self.__frame > 40:
            self.__frame = 0
            SoundUtils.play_sound("../Assets/Sound/Other/footstep.mp3")

        if direction == "left" or direction == "right":
            name_animate = "walk"
        else:
            name_animate = direction

        self.set_image(name_animate + str(index))
        if direction == "left":
            self.flip_horizontal()

    def dying(self):
        pos = self.get_position()
        self.set_image("dead", (203, 51))
        self.set_position(pos)

    def reset(self):
        self.set_image("walk0", (36, 80))
        self.set_state(EState.FREE)
        self.direction = "left"
        self.set_speed(1.5)

