import pytest

from itertools import combinations

from src.api_v1.tournaments.engine.tour_game_iter import IterationGames


players = [
    'pasha', 'vadim', 'oleg', 'anton', 'vladimir',
    'sergey', 'nikita', 'stephan', 'grigory', 'alex',
    'tikhon', 'miron'
]

table_conditions_first = {
    1: ("pasha", "vadim"),
    2: ("oleg", "anton"),
    3: ("vladimir", "sergey"),
    4: ("nikita", "stephan"),
    5: ("grigory", "alex")
}

table_conditions_second = {
    1: ("pasha", "vadim"),
    2: ("oleg", "anton"),
    3: ("vladimir", "sergey"),
    4: ("nikita", "stephan"),
    5: None
}

table_conditions_third = {
    1: None,
    2: None,
    3: None,
    4: None,
    5: None,
}


game_list = [player for player in combinations(players, 2)]


@pytest.mark.parametrize(
    "table_conditions_t, game_list_t, expected_result_t",
    (
            [table_conditions_first, game_list, ('tikhon', 'miron')],
            [table_conditions_second, game_list, ('grigory', 'alex')],
            [table_conditions_third, game_list, ('pasha', 'vadim')],
    )
)
def test_iterator_tournament(
        table_conditions_t,
        game_list_t,
        expected_result_t
):

    assert next(IterationGames(table_conditions_t, game_list_t)) == expected_result_t
