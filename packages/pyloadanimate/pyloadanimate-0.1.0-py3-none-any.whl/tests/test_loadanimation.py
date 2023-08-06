import threading, time
from pyloadanimate import load_animation
from threading import Event

load_animation.start_animation()

for i in range(3):
    time.sleep(1)

load_animation.stop_animation()