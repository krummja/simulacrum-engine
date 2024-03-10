import sys
import pygame as pyg


class Game:

    def load(self) -> None:
        pass

    def update(self) -> None:
        pass

    def run(self) -> None:
        self.load()
        while True:
            self.update()

    def quit(self) -> None:
        pyg.quit()
        sys.exit()
