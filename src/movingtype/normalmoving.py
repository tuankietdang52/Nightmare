import heapq
import pygame as pg
import numpy as np
import src.entity.thealternate.enemy as enenemy
import src.movingtype.movement as mv
import src.gamemanage.game as gm
import src.gamemanage.physic as gp


class Cell:
    def __init__(self, f: float, g: float, h: float, position: mv.IntVector2, parent: mv.IntVector2):
        self.f = f
        self.g = g
        self.h = h

        self.position = position
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def __eq__(self, other):
        return self.f == other.f


class NormalMovement(mv.Movement):
    def __init__(self, enemy: enenemy.Enemy):
        self.owner = enemy
        self.manager = gm.Manager.get_instance()
        self.player = self.manager.player

    def moving(self):
        rect = self.owner.get_rect()
        player_rect = self.player.get_rect()
        player_position = self.player.get_position()

        if gp.Physic.is_collide(player_rect, rect):
            return

        direction = self.owner.calculate_direction(player_position)
        velocity = direction * self.owner.get_speed()

        if self.owner.can_move(self.owner.get_position() + velocity):
            self.__chase(velocity)

        else:
            self.__bypass_to_player()

        self.manager.update_UI_ip()

    __ways = list()

    def __chase(self, velocity: pg.math.Vector2):
        self.__ways.clear()

        position = self.owner.get_position() + velocity
        self.owner.set_position(position)

    def __bypass_to_player(self):
        player_position = self.player.get_position()
        src = self.owner.position
        dest = player_position

        if len(self.__ways) == 0:
            self.__ways = self.__find_way(src, dest)

        speed = self.owner.get_speed()
        position = 0

        for step in range(int(speed)):
            if len(self.__ways) == 0:
                break

            position = self.__ways.pop(0)
            self.owner.calculate_direction(position)

        self.owner.set_position(position)

    # A STAR PATHFINDING

    def __check_valid_dest(self, dest: pg.math.Vector2):
        if self.owner.can_move(dest):
            return True

        return False

    def __find__valid_dest(self, dest: pg.math.Vector2) -> pg.math.Vector2:
        left, right = dest.x, dest.x
        up, down = dest.y, dest.y

        while True:
            left -= 1
            right += 1
            up -= 1
            down += 1

            if self.owner.can_move(pg.math.Vector2(left, dest.y)):
                return pg.math.Vector2(left, dest.y)
            elif self.owner.can_move(pg.math.Vector2(right, dest.y)):
                return pg.math.Vector2(right, dest.y)
            elif self.owner.can_move(pg.math.Vector2(dest.x, up)):
                return pg.math.Vector2(dest.x, up)
            elif self.owner.can_move(pg.math.Vector2(dest.x, down)):
                return pg.math.Vector2(dest.x, down)

    def __find_way(self, src: pg.math.Vector2, dest: pg.math.Vector2) -> list:
        src_int = mv.IntVector2(src)

        if not self.__check_valid_dest(dest):
            dest = self.__find__valid_dest(dest)

        dest_int = mv.IntVector2(dest)

        detail = self.__a_star_search(src_int, dest_int)

        if detail is None:
            return [src]

        return self.__trace_path(detail, dest_int)

    def __trace_path(self, detail: list, dest: mv.IntVector2) -> list:
        path = list()
        x, y = dest.x, dest.y

        while detail[y][x].parent.x != x or detail[y][x].parent.y != y:
            path.append(pg.math.Vector2(x, y))
            tempx, tempy = detail[y][x].parent.x, detail[y][x].parent.y
            x, y = tempx, tempy

        path.reverse()
        return path

    def __a_star_search(self, src: mv.IntVector2, dest: mv.IntVector2):
        screen = self.manager.screen

        col = screen.get_width() * 2
        row = screen.get_height() * 2

        detail = np.ndarray((row, col), dtype=np.object_)
        closed_list = set()

        start = Cell(0, 0, 0, src, src)
        x, y = src.x, src.y
        detail[y][x] = start

        open_list = [start]

        return self.__searching(dest, open_list, detail, closed_list)

    def __searching(self,
                    dest: mv.IntVector2,
                    open_list: list,
                    detail,
                    closed_list: set) -> list | None:

        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        while len(open_list) > 0:
            p = heapq.heappop(open_list)
            cur = p.position

            closed_list.add((cur.x, cur.y))

            for di in directions:
                nx_pos = mv.IntVector2(cur.x + di[0], cur.y + di[1])

                if self.__is_in_dest(nx_pos, dest):
                    detail[nx_pos.y][nx_pos.x] = Cell(0, 0, 0, nx_pos, cur)
                    return detail

                if not self.__is_valid(nx_pos) or self.__is_closed(nx_pos, closed_list):
                    continue

                g_new = detail[cur.y][cur.x].g + 1.0
                h_new = self.__get_heuristic(nx_pos, dest)
                f_new = g_new + h_new

                new_cell = Cell(f_new, g_new, h_new, nx_pos, cur)

                if detail[nx_pos.y][nx_pos.x] is None or detail[nx_pos.y][nx_pos.x].f > f_new:
                    heapq.heappush(open_list, new_cell)
                    detail[nx_pos.y][nx_pos.x] = new_cell
                    # pg.draw.circle(self.screen, (0, 0, 150), (nx_pos.x, nx_pos.y), 5)
                    # pg.display.update()

        return None

    def __is_valid(self, cur: mv.IntVector2) -> bool:
        cur = pg.math.Vector2(cur.x, cur.y)
        if self.owner.can_move(cur):
            return True

        return False

    def __is_closed(self, pos: mv.IntVector2, closed_list: set) -> bool:
        if (pos.x, pos.y) in closed_list:
            return True

        return False

    def __is_in_dest(self, cur: mv.IntVector2, dest: mv.IntVector2) -> bool:
        if cur.x == dest.x and cur.y == dest.y:
            return True

        return False

    def __get_heuristic(self, cur: mv.IntVector2, dest: mv.IntVector2) -> float:
        return abs(cur.x - dest.x) + abs(cur.y - dest.y)