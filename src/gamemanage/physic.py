import src.gamemanage.game as gm
import pygame as pg


class Physic:
    def __init__(self):
        pass

    @staticmethod
    def is_collide_wall(rect: pg.rect.Rect) -> bool:
        """
        :param rect: Next rect
        """
        manager = gm.Manager.get_instance()

        if manager.gamemap is None:
            return False

        bottom_left = rect.bottomleft
        bottom_right = rect.bottomright
        top = rect.midbottom[0], rect.midbottom[1] - 10

        walls = manager.gamemap.sect.walls
        if (top in walls
                or bottom_right in walls
                or bottom_left in walls):
            return True

        return False

    @staticmethod
    def is_collide(rect1: pg.rect.Rect, rect2: pg.rect.Rect) -> bool:
        top = rect1.center
        if rect2.collidepoint(top):
            return True

        return False
