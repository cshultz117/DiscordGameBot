# bot.py
import random

from game import DiscGame

class ConnectFour(DiscGame):
    def __init__(self) -> None:
        super().__init__()
        self.game_type = 'connect four'

        self.column_emojis = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣']
        self.piece_emojis = ['⚪','🔴','🔵']

        self.player_ids = [None,None]

        self.board_message_1 = None
        self.board_message_2 = None
        self.turn_message = None

        self.COLS = 7
        self.ROWS = 6

        self.game_board = [[0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0]]

    async def run_game(self, emoji, channel):
        #global game_board
        #global turn

        if emoji in self.column_emojis:
            emoji_index = self.get_index_from_emoji(emoji)
            for i in range(5,-1,-1):
                if self.game_board[i][emoji_index] == 0:
                   self.game_board[i][emoji_index] = self.turn%2 + 1
                   break
                if (self.game_board[i][emoji_index] == None):
                    return

        if self.check_win():
            await self.end_game("win", channel)
            return

        #if check_tie(game_board):
        #    await end_game('tie', channel)
        #    return

        self.turn += 1
        if(emoji == 'start'):
            await self.setup_game_board(channel)
        else:
            await self.edit_game_board(channel)

    async def setup_game_board(self,channel):
        #global player_ids
        #global board_message_1
        #global board_message_2
        #global turn_message

        count = 0
        board = ''
        for e in self.game_board:
            for n in e:
                board += self.piece_emojis[n]
            board += '\n'

            count += 1
            if count == 3:
                self.board_message_1 = await channel.send(board)
                board = ''
            if count == 6:
                self.board_message_2 = await channel.send(board)
                board = ''
        self.turn_message =  await channel.send("It's your turn, " + self.piece_emojis[self.turn%2+1] + ' ' + '<@{}>'.format(self.player_ids[self.turn%2]) + " " + self.piece_emojis[self.turn%2+1])
        for e in self.column_emojis:
            await self.turn_message.add_reaction(e)

    async def edit_game_board(self,channel):
        #global board_message_1
        #global board_message_2
        #global turn_message

        count = 0
        board = ''
        for e in self.game_board:
            for n in e:
                board += self.piece_emojis[n]
            board += '\n'

            count += 1
            if count == 3:
                await self.board_message_1.edit(content=board)
                board = ''
            if count == 6:
                await self.board_message_2.edit(content=board)
                board = ''
        if (self.game_in_progress):
            res = "It's your turn, " + self.piece_emojis[self.turn%2+1] + ' ' + '<@{}>'.format(self.player_ids[self.turn%2]) + " " + self.piece_emojis[self.turn%2+1]
            await self.turn_message.edit(content=res)

    def check_win(self):
        current_player = self.turn%2+1

        for c in range(self.COLS - 3):
            for r in range(self.ROWS):
                if(self.game_board[r][c] == current_player) and (self.game_board[r][c+1] == current_player) and (self.game_board[r][c+2] == current_player) and(self.game_board[r][c+3] == current_player):
                    return True

        for c in range(self.COLS):
            for r in range(self.ROWS - 3):
                if(self.game_board[r][c] == current_player) and (self.game_board[r+1][c] == current_player) and (self.game_board[r+2][c] == current_player) and(self.game_board[r+3][c] == current_player):
                    return True

        for c in range(self.COLS - 3):
            for r in range(self.ROWS - 3):
                if(self.game_board[r][c] == current_player) and (self.game_board[r+1][c+1] == current_player) and (self.game_board[r+2][c+2] == current_player) and(self.game_board[r+3][c+3] == current_player):
                    return True

        for c in range(self.COLS - 3):
            for r in range(3,self.ROWS):
                if(self.game_board[r][c] == current_player) and (self.game_board[r-1][c+1] == current_player) and (self.game_board[r-2][c+2] == current_player) and(self.game_board[r-3][c+3] == current_player):
                    return True

    def check_tie(self):
        count = 0
        for r in self.game_board:
            for c in r:
                if self.game_board[r][c] == 0:
                    count += 1
        if count == 0:
            return True

    async def end_game(self, state, channel):
        #global turn_message
        #global game_in_progress

        if state == 'win':
            self.game_in_progress = False
            await self.edit_game_board(channel)
            await self.turn_message.delete()
            await channel.send('👑' + '<@{}>'.format(self.player_ids[self.turn%2]) + '👑' + ' is based')
            await channel.send('😭' + '<@{}>'.format(self.player_ids[(self.turn+1)%2]) + '😭' + ' is dogwater')

        if state == 'tie':
            await channel.send('It is cringe that you both sat here long enough to tie the game.')

        if state == 'override':
            await channel.send('--Game Ending--')
        self.reset_globals()
        return

    def reset_globals(self):
        #global game_in_progress
        #global player_ids
        #global turn
        #global game_board
        #global board_message_1
        #global board_message_2
        #global turn_message

        self.board_message_1 = None
        self.board_message_2 = None
        self.turn_message    = None

        self.game_in_progress = False
        self.player_ids = [None, None]
        self.turn = -1
        self.game_board = [[0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0]]
        return

    def pick_player_order(self):
        #global turn
        n = random.randint(1,2)
        self.turn += n

    def get_index_from_emoji(self,emoji):
        ind = 0
        if emoji in self.column_emojis:
            for e in self.column_emojis:
                if e == emoji:
                    return ind
                ind += 1
            print("Could not find emoji.. somehow?")
        else:
            print("Invalid Emoji Response")