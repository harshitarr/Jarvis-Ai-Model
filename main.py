import os
import eel

from engine.features import *
from engine.command import *

eel.init("www")  #frontend code is present in this directory

playAssistantSound()

os.system('start msedge.exe --app="http://localhost:8000/index.html"')

eel.start('index.html', mode=None, host='localhost', block=True) # eel library converts it into desktop formate
