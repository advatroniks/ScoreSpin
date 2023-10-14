import uuid

from .Tour_Manager import Tournament


TOURNAMENT_BUFFER: dict[int, Tournament] = {}

print(id(TOURNAMENT_BUFFER))
