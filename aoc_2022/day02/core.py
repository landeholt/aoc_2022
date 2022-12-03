from collections import defaultdict
from enum import Enum
from functools import reduce
from typing import Dict
from aoc_2022.toolkit import *

data = get_remote_input(2)


class Player(int, Enum):
    rock = 1
    paper = 2
    scissor = 3

    lose = 0
    draw = 30
    win = 60


    @property
    def win_table(self):
        return {
                Player.rock   : Player.scissor,
                Player.scissor: Player.paper,
                Player.paper  : Player.rock
            }
    
    @property
    def lose_table(self):
        return {
            Player.scissor: Player.rock,
            Player.paper  : Player.scissor,
            Player.rock   : Player.paper
        }
            
    @staticmethod
    def convert(*tokens):
        rules = {'X': Player.rock, 'Y': Player.paper, 'Z': Player.scissor, 'A': Player.rock, 'B': Player.paper, 'C': Player.scissor}
        return [rules[t] for t in tokens]
    
    def score(self, opponent: "Player", allow_cheat=False):

        if allow_cheat:
            self = self.cheat(opponent)

        if self == opponent:
            return self.draw.value // 10 + self.value
        if self.win_table[self] == opponent:
            return self.win.value // 10 + self.value
        return self.value

    def cheat(self, opponent: "Player"):
        strategy: Dict[Player, Player] = {Player.rock: Player.lose, Player.paper: Player.draw, Player.scissor: Player.win}

        if strategy[self] == Player.draw:
            return opponent
        elif strategy[self] == Player.win:
            return self.lose_table[opponent]
        else:
            return self.win_table[opponent]


def reducer(allow_cheat = False):
    def wrapper(acc, it):
        opponent, player = Player.convert(*it)
        acc += player.score(opponent, allow_cheat=allow_cheat)
        return acc
    return wrapper

def parse(data):
    import re
    return re.findall(r"(A|B|C)\s+(Y|X|Z)", data)
    

def first(data: str):
    scores = reduce(reducer(allow_cheat=False),parse(data), 0)
    return scores

def second(data: str):
    return reduce(reducer(allow_cheat=True),parse(data), 0)
