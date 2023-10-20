import uuid

from .tour_manager import Tournament


ACTIVE_TOURNAMENTS: dict[int, Tournament] = {}

print(id(ACTIVE_TOURNAMENTS))
