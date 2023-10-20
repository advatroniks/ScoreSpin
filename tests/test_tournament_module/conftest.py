import pytest

from src.api_v1.tournaments.engine.tour_engine import TournamentEngine, TableOperator
from src.api_v1.tournaments.engine.tour_manager import Tournament


@pytest.fixture()
def create_tournament_instance():
    return Tournament()