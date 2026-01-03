from abc import ABC

from src.commands import Command


class Executor(ABC):
    pass

class DevCalc(Executor):
    def __init__(self):
        self._number = 0

    def update(self, command : Command):
        command()
