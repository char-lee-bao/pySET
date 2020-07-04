import random
from card import *

class Deck(object):

    def __init__(self):
        self.order = []
        self.assemble()
        self.shuffle()

    def __repr__(self):
        return str([elem.__repr__() for elem in self.order])

    def assemble(self):
        index = 0
        for color in ['Red', 'Green', 'Purple']:
            for shading in ['Open', 'Striped', 'Solid']:
                for shape in ['Diamond', 'Oval', 'Squiggle']:
                    for number in [1, 2, 3]:
                        self.order.append(
                            Card(number, shape, shading, color, index))
                        index += 1

    def shuffle(self):
        random.shuffle(self.order)

    def remove_card(self):
        return self.order.pop()
