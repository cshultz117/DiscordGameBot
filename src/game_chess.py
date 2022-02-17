from game import DiscGame

class Chess(DiscGame):
    def __init__(self) -> None:
        super().__init__()
        self.game_type = "chess"
        self.player_ids = [None,None]
        self.ROWS = 8
        self.COLS = 8

        self.valid_moves = {}