import uuid


class IterationGames:
    def __init__(
            self,
            tables_conditions: dict[int, [uuid.UUID, uuid.UUID]],
            game_list: list,
    ):
        self.game_list = game_list
        self.table_conditions = tables_conditions
        self.result_players_list = self.get_online_players_list()

    def get_online_players_list(self):
        result_player_list = []
        for key, value in self.table_conditions.items():
            if value is not None:
                result_player_list.extend(value)
        return result_player_list

    def __iter__(self):
        return self

    def __next__(self) -> tuple:
        for game in self.game_list:
            # print(game, self.result_players_list, "_NEXT_ ITERATROR!!!") uncomment for debug mode
            if not set(game) & set(self.result_players_list):
                print("ITERATOR RETURN GAME!!!!!", game)
                return game

        raise StopIteration("NOT FREE TABLES")