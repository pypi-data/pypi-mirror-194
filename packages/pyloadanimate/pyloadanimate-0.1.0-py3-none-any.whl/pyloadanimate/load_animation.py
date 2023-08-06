import sys
import time
import itertools
import threading
from threading import Event
event = Event()
t = threading.Thread()

def start_animation(loading_symbols=None):
   t.__init__(target=animate,args=(event,loading_symbols))
   t.start()

def stop_animation():
    event.set()
    t.join()


def animate(event, animation=None):
    if not animation: 
        animation = ["/","-","\\","|"]
    # itertools cycle will continously cycle through list
    for c in itertools.cycle(animation):
        # checking if event variable raise to set
        if event.is_set():
            break
        sys.stdout.flush()
        sys.stdout.write("\r Loading "+c )
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.flush()
    sys.stdout.write('\rDone!')
    sys.stdout.flush()

