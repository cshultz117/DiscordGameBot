# bot.py
import os
import discord

from dotenv import load_dotenv

from game_connect_four import *
from game_shardle import *
from game_chess import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

connectFour = None
shardle = None
chess = None
game = None

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    channel = discord.utils.get(guild.channels, id=629524968744681472)

    print('--------------BOT RUNNING--------------')

@client.event
async def on_message(msg):
    global game_in_progress
    global player_ids
    global connectFour
    global shardle
    global game

    if msg.content == '=>play connect4':
        if connectFour == None or (connectFour.game_in_progress == False):
            connectFour = ConnectFour()
            game = connectFour
            pick_msg = await msg.channel.send('Pick the players. Who goes first will be random.')
            await pick_msg.add_reaction('🥇')
            await pick_msg.add_reaction('🥈')
        elif connectFour.game_in_progress == True:
            await msg.channel.send('A game is already being played.')

    elif (msg.content == '=>end connect4') and (msg.author.id in connectFour.player_ids):
        await connectFour.end_game('override',msg.channel)
        connectFour = None

    if msg.content == '=>play shardle':
        if shardle == None or shardle.game_in_progress == False:
            shardle = Shardle()
            game = shardle
            #print(shardle)
            await shardle.start_game(msg.channel)
        elif shardle.game_in_progress == True:
            await msg.channel.send('A game is already being played.')

    elif msg.content.startswith("=>guess"):
        if not(shardle == None):
            if (shardle.game_in_progress == True):
                word_to_guess = str(msg.content.split(' ')[1])
                await shardle.guess(word_to_guess)
            else:
                await msg.channel.send("A game does not exist")
        else:
            await msg.channel.send("A game does not exist")
    elif msg.content == '=>end shardle':
        await shardle.end_game('override')
        shardle = None

@client.event
async def on_reaction_add(reaction, user):
    #global game_in_progress
    #global player_ids
    #global turn
    global game
    global connectFour
    global shardle

    emoji = reaction.emoji
    channel = reaction.message.channel

    if user.bot:
        return


    if game.game_type == "connect four":
        if connectFour.game_in_progress == False:
            if emoji == '🥇':
                if connectFour.player_ids[0] == None:
                    connectFour.player_ids[0] = user.id

            elif emoji == '🥈':
                if connectFour.player_ids[1] == None:
                    connectFour.player_ids[1] = user.id

            elif emoji in connectFour.column_emojis:
                return

            if (not(connectFour.player_ids[0] == None)) and (not(connectFour.player_ids[1] == None)) and (connectFour.turn == -1):
                connectFour.pick_player_order()
                connectFour.game_in_progress = True
                await connectFour.run_game('start', channel)

        if connectFour.game_in_progress == True:
            if (emoji in connectFour.column_emojis) and (user.id == connectFour.player_ids[connectFour.turn%2]):
                await connectFour.run_game(emoji,channel)


    elif game.game_type == "shardle":
        if shardle.game_in_progress == False:
            if emoji in shardle.number_emojis:
                shardle.word_size = shardle.get_index_from_emoji(emoji)
                await shardle.set_word(shardle.word_size)

        elif shardle.game_in_progress == True:
                await channel.send("A shardle game is already in progress")

@client.event
async def on_reaction_remove(reaction, user):
    global connectFour
    emoji = reaction.emoji
    channel = reaction.message.channel

    if connectFour.game_type == 'connect four':
        if connectFour.game_in_progress == True:
            if (emoji in connectFour.column_emojis) and (user.id == connectFour.player_ids[connectFour.turn%2]):
                await connectFour.run_game(emoji,channel)

client.run(TOKEN)