from pyscript.web import dom
from pyscript.web.elements import *
import asyncio

sequence = ["red-btn", "green-btn", "blue-btn", "yellow-btn"]


async def start_game():
    board_events("none")
    await asyncio.ensure_future(run_sequence())
    board_events("all")

def board_events(event):
    dom.find("#simon-board")[0].style["pointer-events"] = event

async def run_sequence():
    for color in sequence:
        btn = dom.find("#" + color)[0]
        btn.id = btn.id + "-highlight"
        await asyncio.sleep(0.7)
        btn.id = btn.id.replace("-highlight", "")
        await asyncio.sleep(0.5)

    

def key_clicked(event):
    print("clicked")

asyncio.ensure_future(start_game())
