from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        """"""


class AddCommand(Command):
    def __call__(self, *args, **kwargs):
        return


class SubCommand(Command):
    def __call__(self, *args, **kwargs):
        pass


class DivCommand(Command):
    def __call__(self, *args, **kwargs):
        pass


class MulCommand(Command):
    def __call__(self, *args, **kwargs):
        pass


class ACCommand(Command):
    def __call__(self, *args, **kwargs):
        pass


class DelCommand(Command):
    def __call__(self, *args, **kwargs):
        pass