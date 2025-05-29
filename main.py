import os
import eel

eel.init("www")  #frontend code is present in this directory

os.system('start msedge.exe --app="http://localhost:8000/index.html"')

eel.start('index.html', mode=None, host='localhost', block=True)
