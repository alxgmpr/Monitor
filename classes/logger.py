# coding = utf-8

from termcolor import colored


class Logger:
    def __init__(self, name=None):
        self.name = name

    def log(self, text, color=None):
        print(colored('[{}] || {}'.format(self.name, text), color))
