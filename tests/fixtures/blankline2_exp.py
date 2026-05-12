import os
import sys
a = 1
b = 1


# lol

# lol
def outer_scope():
    class LocalState:
        def __init__(self):
            self.value = 1

        @property
        def data(self):
            return self.value

    def helper():
        pass
    return LocalState()


class PrimaryController:
    a = 1
    b = 1

    def handle(self):
        def sub_logic():
            pass
        return True

    @staticmethod
    def log():
        pass


def global_runner():
    x = 1
    if a:
        pass

    class RunnerConfig:
        def __init__(self):
            pass
    return x + y


x = 100


@decorator
class FinalEntity:
    pass
