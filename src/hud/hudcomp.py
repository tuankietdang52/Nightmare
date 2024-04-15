import pygame as pg
import src.gamemanage.game as gm


class Pointer:
    """Position by topleft"""
    size = (20, 30)

    def __init__(self, screen: pg.surface.Surface):
        self.image = pg.image.load("../Assets/HUD/pointer.png").convert_alpha()

        self.image = pg.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()

        self.screen = screen
        self.is_set = False

    def set_position(self, pos: tuple[float, float]):
        self.play_select_sound()
        self.rect = self.image.get_rect(topleft=pos)

        self.is_set = True

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def flip_horizontal(self):
        self.image = pg.transform.flip(self.image, True, False)

    def play_select_sound(self):
        pg.mixer.Sound("../Assets/Sound/Other/select.mp3").play()

    def play_choose_sound(self):
        pg.mixer.Sound("../Assets/Sound/Other/choose.mp3").play()


class Board:
    """Position by center"""

    def __init__(self, screen: pg.surface.Surface, pos: tuple[float, float], size: tuple[float, float]):
        self.screen = screen

        self.surf = pg.Surface(size)

        self.surf.fill((0, 0, 0))
        self.surf.set_alpha(100)

        self.rect = self.surf.get_rect(center=pos)

        self.content: list[tuple[pg.surface.Surface, pg.rect.Rect]] = list()

    def draw(self):
        self.screen.blit(self.surf, self.rect)

        points = [
            self.rect.topleft,
            self.rect.topright,
            self.rect.bottomright,
            self.rect.bottomleft
        ]

        pg.draw.lines(self.screen, (0, 0, 0), True, points, 7)

        self.__draw_content()

    def __draw_content(self):
        for item in self.content:
            inside_rect = item[1].clamp(self.rect)
            rect = inside_rect.move(inside_rect.x, 20)

            self.screen.blit(item[0], rect)

    def insert_content(self, content: pg.surface.Surface, rect: pg.rect.Rect):
        self.content.append((content, rect))


class StoryText:
    """Position by topleft"""
    fontpath = "../Assets/Font/Crang.ttf"

    def __init__(self, screen: pg.surface.Surface, text: str, size: int, board: Board):
        """
        Write text to board
        New line: ' |sometext'
        """
        self.screen = screen

        self.text = text
        self.size = size

        self.space_distance = self.size / 3

        self.board = board

        self.write()

    def write(self):
        words = self.text.split()

        font = pg.font.Font(self.fontpath, self.size)

        start = self.board.rect.topleft
        width = self.board.rect.width

        pos = start

        end = (start[0] + width) / 2.2

        for word in words:
            pos = self.__get_position_word(word, pos, start[0], end)

            for char in word:
                if char == '|':
                    continue

                surf = font.render(char, 1, (255, 255, 255))
                rect = surf.get_rect(topleft=pos)

                self.board.insert_content(surf, rect)
                pos = self.__spacing(char, pos, self.space_distance)

    def __get_position_word(self,
                            word: str,
                            cur: tuple[float, float],
                            start_x: float,
                            end_x: float) -> tuple[float, float]:
        if cur[0] != start_x:
            cur = self.__spacing(' ', cur, self.space_distance)
        pos = cur

        i = 0
        while i < len(word):
            if word[i] == '|':
                cur = start_x, cur[1] + self.space_distance * 4
                return cur

            elif cur[0] >= end_x:
                cur = start_x, cur[1] + self.space_distance * 4
                return cur

            cur = self.__spacing(word[i], cur, self.space_distance)
            i += 1

        return pos

    def __spacing(self, word: str, pos: tuple[float, float], space: float) -> tuple[float, float]:
        word_extra_space = {'n'}
        word_extra_space_x2 = {'M', 'm', 'N'}
        word_decrease_space = {'I', 'i'}

        if word in word_decrease_space:
            pos = pos[0] + space / 2, pos[1]

        elif word in word_extra_space:
            pos = pos[0] + space + 1, pos[1]

        elif word in word_extra_space_x2:
            pos = pos[0] + space + 3, pos[1]

        else:
            pos = pos[0] + space, pos[1]

        return pos


class BoardText:
    def __init__(self,
                 screen: pg.surface.Surface,
                 text: str,
                 fontsize: int,
                 pos: tuple[float, float],
                 size: tuple[float, float]):
        """
        :param pos: position of board
        :param size: size of board
        """
        self.board = Board(screen, pos, size)
        self.txt = StoryText(screen, text, fontsize, self.board)

        self.rect = self.board.rect

    def draw(self):
        self.board.draw()


class AcceptBoard:
    def __init__(self,
                 screen: pg.surface.Surface,
                 pos: tuple[float, float],
                 size: tuple[float, float]):
        self.board_txt = BoardText(screen, "yes | |no", 25, pos, size)
        self.board = self.board_txt.board

        self.pointer = Pointer(screen)
        self.pointer.flip_horizontal()

        self.screen = screen
        self.rect = self.board.rect

        self.yes_choice = True

    def __setup_pointer(self):
        pos = self.board.rect.topleft
        pointer_pos = pos[0] + 100, pos[1] + 20

        self.pointer.set_position(pointer_pos)
        self.pointer.draw()

    def draw(self):
        self.board.draw()
        self.__setup_pointer()

    def __move_cur(self, y):
        pointer_pos = self.pointer.rect.x, self.pointer.rect.y
        self.pointer.set_position((pointer_pos[0], pointer_pos[1] + y))

        gm.Manager.update_UI()
        self.board.draw()
        self.pointer.draw()
        pg.display.flip()

    def changing_choice(self):
        keys = pg.key.get_pressed()

        new_y = self.board_txt.txt.space_distance * 8

        if keys[pg.K_w]:
            if self.yes_choice:
                return

            self.yes_choice = True
            self.__move_cur(-new_y)

        elif keys[pg.K_s]:
            if not self.yes_choice:
                return

            self.yes_choice = False
            self.__move_cur(new_y)
