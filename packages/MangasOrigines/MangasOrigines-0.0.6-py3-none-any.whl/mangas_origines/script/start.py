import inspect
import sys
import os

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(os.path.dirname(current_dir)))

from mangas_origines.script.mangas_origines_script import start

if __name__ == '__main__':
    start()
