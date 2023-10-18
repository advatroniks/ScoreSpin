import uuid

from .Tour_Manager import Tournament


ACTIVE_TOURNAMENTS: dict[int, Tournament] = {}

print(id(ACTIVE_TOURNAMENTS))
