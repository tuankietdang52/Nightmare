import pygame


class Area:
    def __init__(self, name, pos, width, height):
        """
        :param tuple[float, float] pos:
        :param float width:
        :param float height:
        """

        self.name = name
        self.x, self.y = pos
        self.width = width
        self.height = height

    def is_overlap(self, rect) -> bool:
        area = pygame.Surface((self.width, self.height))
        _rect = area.get_rect(topleft=(self.x, self.y))

        # pygame.draw.rect(screen, (0, 255, 0), _rect)

        if _rect.colliderect(rect):
            return True

        return False