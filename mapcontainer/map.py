import abc
import os

import pygame
import pytmx

from tilemap import Area, Tile


class Map(abc.ABC):
    path = ""
    screen = None
    sect = None

    def change_sect(self, name: str):
        pass


class Sect:
    walls = list()

    CAM_OFFSETX = 0
    """Higher = Left, Lower = Right"""

    CAM_OFFSETY = 0
    """Higher = Up, Lower = Down"""

    size = 64

    def __init__(self, screen, prev_sect=None):
        self.screen = screen

        self.map = None
        self.areas = []
        self.back_point = {}
        self.tilegroup = pygame.sprite.Group()
        self.is_created = False

        if prev_sect is not None:
            self.prev_sect = prev_sect

    def init_OFFSET(self, offset, offsetfullscr):
        if self.screen.get_size() == (800, 800):
            self.CAM_OFFSETX, self.CAM_OFFSETY = offset

        else:
            self.CAM_OFFSETX, self.CAM_OFFSETY = offsetfullscr

    def load(self, path):
        if os.getcwd() == "C:\\Users\\ADMIN\\PycharmProjects\\Nightmare":
            self.map = pytmx.load_pygame(path)

    def set_pre_sect(self, prev_sect: str):
        self.prev_sect = prev_sect

    def get_start_point(self) -> tuple[float, float] | None:
        if self.prev_sect != "" and self.prev_sect is not None:
            start_area = self.prev_sect
        else:
            start_area = "Start"

        for area in self.areas:
            if area.name == start_area:
                return area.x, area.y

        return None

    def create(self):
        self.walls.clear()
        self.areas.clear()
        self.tilegroup.empty()

        self.is_created = True

        for layer in self.map.layers:
            if hasattr(layer, "data"):
                self.__draw_tile(layer)

            if isinstance(layer, pytmx.TiledObjectGroup):
                self.__init_areas(layer)

    def __draw_tile(self, layer):
        for x, y, surf in layer.tiles():
            pos = x * self.size - self.CAM_OFFSETX, y * self.size - self.CAM_OFFSETY

            tilesize = self.size, self.size

            surf = pygame.transform.scale(surf, tilesize)

            tile = Tile(surf, pos, layer.name, layer.id, self.screen)
            self.tilegroup.add(tile)

            if "Wall" in layer.name or layer.name == "Object":
                self.walls.append(tile)

            self.screen.blit(tile.image, tile.rect)

    def __init_areas(self, layer):
        for area in layer:
            pos = (area.x / 16 * self.size - self.CAM_OFFSETX,
                   area.y / 16 * self.size - self.CAM_OFFSETY)

            width = area.width / 16 * self.size
            height = area.height / 16 * self.size

            tileobj = Area(area.name, pos, width, height)

            self.areas.append(tileobj)

    def in_area(self, rect) -> str | None:
        for area in self.areas:
            if area.is_overlap(rect):
                return area.name

        return None

    def redraw(self):
        group = self.tilegroup

        group.draw(self.screen)
