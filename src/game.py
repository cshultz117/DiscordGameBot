class DiscGame:
    def __init__(self) -> None:
        self.game_in_progress = False
        self.game_board = None
        self.turn = -1
        self.game_type = None
        self.player_ids = [None]