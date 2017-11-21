from curses import wrapper
from game import Game
import time
import sys

def main(stdscreen):
    g = Game(stdscreen)
    g.start()

if __name__ == '__main__':
    sys.stdout.write("\x1b[8;33;70t")
    sys.stdout.flush()
    time.sleep(.05)
    wrapper(main)