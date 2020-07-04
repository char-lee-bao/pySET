from deck import *
from itertools import combinations

class Game(object):

    def __init__(self):
        self.deck = Deck()
        self.board = []
        self.complete_sets = []
        self.set = []
        self.possible_sets = []
        self.set_board()
        self.get_possible_sets()

    def set_board(self):
        for i in range(12):
            self.board.insert(0, self.deck.remove_card())

    def get_possible_sets(self):
        self.possible_sets = [list(possible_set) for possible_set in list(combinations(self.board, 3))]

    def add_to_board(self, index):
        self.board.insert(index, self.deck.remove_card())

    def remove_from_board(self, card):
        self.board.remove(card)

    def add_to_set(self, card):
        self.set.append(card)

    def remove_from_set(self, card):
        self.set.remove(card)

    def check_set(self, possible_set):
        return ((self.check_different("Number", possible_set) or self.check_same("Number", possible_set)) and
                    (self.check_different("Shape", possible_set) or self.check_same("Shape", possible_set)) and
                    (self.check_different("Shading", possible_set) or self.check_same("Shading", possible_set)) and
                    (self.check_different("Color", possible_set) or self.check_same("Color", possible_set)))

    def clear_set(self):
        self.complete_sets.append(self.set)
        # Ensure the next three cards will guarantee a set
        potential_board = [elem for elem in self.board if elem not in self.set] + self.deck.order[-3:]
        while not any([self.check_set(list(possible_set)) for possible_set in list(combinations(potential_board, 3))]):
            if len(self.deck.order) <= 3:
                break
            self.deck.shuffle()
            potential_board = [elem for elem in self.board if elem not in self.set] + self.deck.order[-3:]
        while self.set:
            # Add a new card if possible
            if len(self.deck.order) > 0:
                self.add_to_board(self.board.index(self.set[0]))
            # Remove the original card
            self.remove_from_board(self.set[0])
            self.set.remove(self.set[0])
        self.get_possible_sets()

    def check_different(self, feature, possible_set):
        if feature == "Number":
            return len(set([elem.get_number() for elem in possible_set])) == 3
        elif feature == "Shape":
            return len(set([elem.get_shape() for elem in possible_set])) == 3
        elif feature == "Shading":
            return len(set([elem.get_shading() for elem in possible_set])) == 3
        else:
            return len(set([elem.get_color() for elem in possible_set])) == 3

    def check_same(self, feature, possible_set):
        if feature == "Number":
            return len(set([elem.get_number() for elem in possible_set])) == 1
        elif feature == "Shape":
            return len(set([elem.get_shape() for elem in possible_set])) == 1
        elif feature == "Shading":
            return len(set([elem.get_shading() for elem in possible_set])) == 1
        else:
            return len(set([elem.get_color() for elem in possible_set])) == 1