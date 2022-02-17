import random
import re

from game import DiscGame

class Shardle(DiscGame):
    def __init__(self) -> None:
        super().__init__()
        self.game_type = "shardle"


        #white - green - yellow - black
        self.shardle_emojis = ['⬜','🟩','🟨','⬛']
        self.number_emojis = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣']
        self.letter_emojis = ['🇦 ','🇧 ','🇨 ','🇩 ','🇪 ','🇫 ','🇬 ','🇭 ','🇮 ','🇯 ','🇰 ','🇱 ','🇲 ','🇳 ','🇴 ','🇵 ','🇶 ','🇷 ','🇸 ','🇹 ','🇺 ','🇻 ','🇼 ','🇽 ','🇾 ','🇿 ']


        self.game_board = []
        self.guess_board = []

        self.board_message_1 = None
        self.board_message_2 = None
        self.channel = None

        self.word = None
        self.word_hash = {}

        self.word_size = None
        self.pick_msg = None
        self.guess_msg_1 = None
        self.guess_msg_2 = None
        self.info_msg    = None

        self.banned_letters = []
        self.required_letters = []

    async def start_game(self, channel):
        self.channel = channel
        self.pick_msg = await self.channel.send('How many letters should the word have?')
        for e in self.number_emojis:
            await self.pick_msg.add_reaction(e)

    async def set_word(self,size):
        for i in range(6):
            g = [0 for j in range(size+1)]
            self.game_board.append(g)

        for i in range(6):
            g = [-1 for j in range(size+1)]
            self.guess_board.append(g)

        with open('data/words.txt','r') as file:
            all_words = ''.join(line for line in file)


            if size == 0:
                words_of_size = re.findall(r'\b[a-zA-Z]{1}\b',all_words)
            elif size == 1:
                words_of_size = re.findall(r'\b[a-zA-Z]{2}\b',all_words)
            elif size == 2:
                words_of_size = re.findall(r'\b[a-zA-Z]{3}\b',all_words)
            elif size == 3:
                words_of_size = re.findall(r'\b[a-zA-Z]{4}\b',all_words)
            elif size == 4:
                words_of_size = re.findall(r'\b[a-zA-Z]{5}\b',all_words)
            elif size == 5:
                words_of_size = re.findall(r'\b[a-zA-Z]{6}\b',all_words)
            elif size == 6:
                words_of_size = re.findall(r'\b[a-zA-Z]{7}\b',all_words)
            elif size == 7:
                words_of_size = re.findall(r'\b[a-zA-Z]{8}\b',all_words)

            rand = random.randint(0,len(words_of_size))
            self.word = words_of_size[rand]
            for i in self.word:
                self.word_hash[str(i)] = 0

        for j in self.word:
            self.word_hash[str(j)] += 1
        self.turn = 0
        self.game_in_progress = True
        await self.print_game_board()

    async def guess(self, guess):
        guess = guess.lower()
        guess_hash = {}

        for i in guess:
            guess_hash[str(i)] = 0

        if len(guess) == self.word_size+1:
            for i in range(len(guess)):
                if guess[i] in self.banned_letters:
                    await self.info_msg.edit(content=f'You cannot use {guess[i]} in your word')
                    return
            for i in range(self.word_size+1):
                if self.word[i] == guess[i]:
                    self.game_board[self.turn][i] = 1
                    guess_hash[str(guess[i])] += 1
            for i in range(self.word_size+1):
                if (guess[i] in self.word) and (self.game_board[self.turn][i] == 0) and (guess_hash[str(guess[i])] < self.word_hash[str(guess[i])]):
                    guess_hash[str(guess[i])] += 1
                    self.game_board[self.turn][i] = 2
            for i in range(self.word_size+1):
                if(self.game_board[self.turn][i] == 0):
                    if not (guess[i] in self.word_hash.keys()):
                        self.banned_letters.append(guess[i])
                    self.game_board[self.turn][i] = 3

            for i in range(len(guess)):
                self.guess_board[self.turn][i] = ord(guess[i]) - 97

            self.turn += 1
            await self.edit_game_board()
            if(guess == self.word):
                await self.end_game("win")
            if(self.turn == 6):
                await self.end_game('lose')
        else:
            await self.info_msg.edit(content="Invalid word")

    async def print_game_board(self):
        #print(f'the shardle is: {self.word}')
        count = 0
        board = ''
        for e in self.game_board:
            for n in e:
                board += self.shardle_emojis[n] + ' '
            board += '\n'

            count += 1
            if count == 3:
                self.board_message_1 = await self.channel.send(board)
                board = ''
            if count == 6:
                self.board_message_2 = await self.channel.send(board)
                board = ''

        self.guess_msg_1 =  await self.channel.send("-> ")
        self.guess_msg_2 =  await self.channel.send("-> ")
        self.info_msg    =  await self.channel.send("Make your guesses with =>guess <word>")

    async def edit_game_board(self):
        count = 0
        board = ''
        guess_letters = ''

        for e,l in zip(self.game_board, self.guess_board):
            for n in e:
                board += self.shardle_emojis[n] + ' '

            for m in l:
                if m == -1:
                    guess_letters += ''
                else:
                    guess_letters += self.letter_emojis[m]

            board += '\n'
            guess_letters += '\n'
            count += 1

            if count == 3:
                await self.board_message_1.edit(content=board)
                await self.guess_msg_1.edit(content=guess_letters)
                board = ''
                guess_letters = ''
            if count == 6:
                await self.board_message_2.edit(content=board)
                if not (guess_letters.isspace()):
                    await self.guess_msg_2.edit(content=guess_letters)
                board = ''
                guess_letters = ''

    async def end_game(self,status):
        if status == 'win':
            await self.info_msg.edit(content='You are based and also pog')
            self.reset_globals()

        elif status == 'lose':
            await self.info_msg.edit(content=f'You are cringe. The word is {self.word}')
            self.reset_globals()

        elif status == 'override':
            await self.info_msg.edit(content=f"You're a beezy for giving up. The word is {self.word}")
            self.reset_globals()

    def reset_globals(self):
        self.game_in_progress = False
        self.turn = -1
        self.game_type = None
        self.game_board = []
        self.guess_board = []

        self.board_message_1 = None
        self.board_message_2 = None
        self.channel = None

        self.word = None
        self.word_hash = {}

        self.word_size = None
        self.pick_msg = None
        self.guess_msg = None

        self.banned_letters = []
        self.required_letters = []
        return

    def get_index_from_emoji(self,emoji):
        ind = 0
        if emoji in self.number_emojis:
            for e in self.number_emojis:
                if e == emoji:
                    return ind
                ind += 1
            print("Could not find emoji.. somehow?")
        else:
            print("Invalid Emoji Response")