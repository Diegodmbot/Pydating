import random
import asyncio
from enum import Enum
from pyscript.web import dom
# from pyscript.web.elements import *

# define a enum of the game states


class GameState(Enum):
    OFF = 0
    WIN = 1
    LOSE = 2


COLORS = ["red-btn", "green-btn", "blue-btn", "yellow-btn"]
sequence = []
user_sequence = []
game_state = GameState.OFF


async def start_game():
    global game_state
    level = 1
    level_label = dom.find("#level")[0]
    while game_state != GameState.WIN or game_state != GameState.LOSE:
        level_label.text = "Level: " + str(level)
        board_events("none")
        sequence.append(COLORS[random.randint(0, 3)])
        await asyncio.ensure_future(run_sequence())
        board_events("all")
        # wait for the user input sequence
        user_sequence.clear()
        while len(user_sequence) < len(sequence):
            await asyncio.sleep(0.3)
            if game_state == GameState.LOSE:
                return
        print(f"Game state: {game_state}")
        if level == 3:
            game_state = GameState.WIN
            break
        level += 1
        await asyncio.sleep(1)


# Activate or deactivate the click event on the simon buttons
def board_events(event):
    dom.find("#simon-board")[0].style["pointer-events"] = event


async def run_sequence():
    for color in sequence:
        btn = dom.find("#" + color)[0]
        await highlight_key(btn)
        await asyncio.sleep(0.5)


def display_result():
    if game_state == GameState.WIN:
        dom.find("#result")[0].text = "You Win!"
    if game_state == GameState.LOSE:
        dom.find("#result")[0].text = "Game Over!"


async def start_clicked(event):
    sequence.clear()
    user_sequence.clear()
    dom.find("#result")[0].text = ""
    global game_state
    game_state = GameState.OFF
    event.srcElement.disabled = True
    await asyncio.ensure_future(start_game())
    display_result()
    event.srcElement.disabled = False
    board_events("none")


async def key_clicked(event):
    button_pressed = event.srcElement
    await highlight_key(button_pressed)
    user_sequence.append(event.srcElement.id)
    user_sequence_len = len(user_sequence)
    global game_state
    if user_sequence[user_sequence_len - 1] != sequence[user_sequence_len - 1]:
        game_state = GameState.LOSE


async def highlight_key(btn):
    btn.id = btn.id + "-highlight"
    await asyncio.sleep(0.4)
    btn.id = btn.id.replace("-highlight", "")


def main():
    board_events("none")


main()
