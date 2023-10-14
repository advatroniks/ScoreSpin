import pytest

from src.api_v1.tournaments.service_tournament.Tour_process import TournamentEngine, TableOperator
from src.api_v1.tournaments.service_tournament.Tour_Manager import Tournament


@pytest.fixture()
def create_tournament_instance():
    return Tournament()