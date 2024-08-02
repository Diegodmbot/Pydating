from pyscript.web import dom
from pyscript.web.elements import *


def key_clicked(event):
    color_name = event.srcElement.id
    print(color_name)
    output_element = dom.find("#output")[0]
    output_element.append(div(color_name))
