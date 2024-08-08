from pyscript.web import dom
from pyscript.web.elements import *
import random
import asyncio

colors = ["red-btn", "green-btn", "blue-btn", "yellow-btn"]
sequence = []
user_sequence = []
state = "off"

async def start_game():
    global state
    level = 1
    level_label = dom.find("#level")[0]
    while state != "win" or state != "lose":
        level_label.text = "Level: " + str(level)
        board_events("none")
        sequence.append(colors[random.randint(0, 3)])
        await asyncio.ensure_future(run_sequence())
        board_events("all")
        # wait for the user input sequence
        user_sequence.clear()
        while len(user_sequence) < len(sequence):
            await asyncio.sleep(1)
        level += 1
        if level > 3:
            state = "win"
            break
    display_result()

def board_events(event):
    dom.find("#simon-board")[0].style["pointer-events"] = event

async def run_sequence():
    for color in sequence:
        btn = dom.find("#" + color)[0]
        btn.id = btn.id + "-highlight"
        await asyncio.sleep(0.7)
        btn.id = btn.id.replace("-highlight", "")
        await asyncio.sleep(0.5)

def start_clicked(event):
    asyncio.ensure_future(start_game())
    event.srcElement.disabled = True

def key_clicked(event):
    user_sequence.append(event.srcElement.id)
    user_sequence_len = len(user_sequence)
    global state
    if user_sequence[user_sequence_len-1] != sequence[user_sequence_len-1]:
        user_sequence.clear()
        state = "lose"

def display_result():
    if state == "win":
        dom.find("#result")[0].text = "You Win!"
    if state == "lose":
        dom.find("#result")[0].text = "Game Over!"
    dom.find("#start")[0].disabled = False

def main():
    board_events("none")
    
main()
    
