import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from src.ui.console_ui import ConsoleUI

if __name__ == "__main__":
    ConsoleUI().run()
