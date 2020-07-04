from tkinter import *
from game import *
from functools import partial

class App(object):

    def __init__(self):
        self.game = Game()
        self.root = Tk()
        self.root.geometry("+650+100")
        self.root.title('SET')
        self.instructions_frame = Frame(self.root, 
                                        bg = 'gray', 
                                        borderwidth = 10, 
                                        relief = SUNKEN, 
                                        width = 400)
        self.instructions_frame.grid(row = 1, column = 1, columnspan = 3)
        instructions_text = 'Instructions\n' \
                            'Click to select 3 cards that are either all same or all different\n' \
                            'for each of the following properties:\n' \
                            '1. Color\n2. Number\n3. Shape\n4. Shading'
        self.instructions_label = Label(self.instructions_frame, text = instructions_text)
        self.instructions_label.grid(row = 1, column = 1, columnspan = 3)
        self.board_images = [PhotoImage(file = 'images\\' 
                                        + str(elem.get_index()) 
                                        + '.png').zoom(2, 2) 
                            for elem in self.game.board]
        self.board_frames = [Frame(self.root, bg = 'black', borderwidth = 5) for elem in self.game.board]
        self.board_buttons = []
        self.selected = [False] * 12
        index = 0
        for i in range(4):
            for j in range(3):
                self.board_frames[index].grid(row = i + 2, column = j + 1)
                command_with_args = partial(self.select_card, index)
                self.board_buttons.append(Button(self.board_frames[index], 
                                            image = self.board_images[index], 
                                            command = command_with_args))
                self.board_buttons[index].grid(row = i + 2, column = j + 1)
                index += 1
        self.new_game_frame = Frame(self.root, bg = 'black', borderwidth = 5)
        self.new_game_frame.grid(row = 6, column = 1, columnspan = 2)
        self.new_game_button = Button(self.new_game_frame, text = 'New Game', command = self.restart)
        self.new_game_button.grid(row = 6, column = 1, columnspan = 2)
        self.hint_frame = Frame(self.root, bg = 'cyan', borderwidth = 5)
        self.hint_frame.grid(row = 6, column = 2, columnspan = 2)
        self.hint_button = Button(self.hint_frame, text = 'Find Set', command = self.hint)
        self.hint_button.grid(row = 6, column = 2, columnspan = 2)
        self.root.mainloop()

    def restart(self):
        self.root.destroy()
        self.__init__()

    def hint(self):
        while self.game.set:
            self.selected[self.game.board.index(self.game.set[0])] = False
            self.board_frames[self.game.board.index(self.game.set[0])].config(bg = 'black')
            self.game.remove_from_set(self.game.set[0])
        for possible_set in self.game.possible_sets:
            if self.game.check_set(possible_set) and all([card in self.game.board for card in possible_set]):
                # Highlight the cards that can be selected
                for card in possible_set:
                    self.board_frames[self.game.board.index(card)].config(bg = 'cyan')
                return

    def select_card(self, index):
        if self.game.board[index] in self.game.set:
            self.game.remove_from_set(self.game.board[index])
            self.board_frames[index].config(bg = 'black')
            self.selected[index] = False
        else:
            self.game.add_to_set(self.game.board[index])
            self.board_frames[index].config(bg = 'red')
            self.selected[index] = True
        if len(self.game.set) == 3:
            self.update()

    def update(self):
        if self.game.check_set(self.game.set):
            self.game.clear_set()
            # Update the board
            for elem in self.board_frames:
                elem.config(bg = 'black')
            # There are no more cards in the deck
            # Remove GUI elements for the cards removed
            if len(self.game.board) < 12:
                for i in range(len(self.selected) - 1, -1, -1):
                    if self.selected[i]:
                        self.board_frames[i].grid_forget()
                        self.board_frames.remove(self.board_frames[i])
                        self.board_buttons[i].grid_forget()
                        self.board_buttons.remove(self.board_buttons[i])
                self.selected = [False] * len(self.game.board)
                for i in range(len(self.selected)):
                    self.board_buttons[i].grid_forget()
                    self.board_frames[i].grid_forget()
                self.board_images = [PhotoImage(file = 'images\\' 
                                        + str(elem.get_index()) 
                                        + '.png').zoom(2, 2) 
                            for elem in self.game.board]
                self.board_frames = [Frame(self.root, bg = 'black', borderwidth = 5) for elem in self.game.board]
                self.board_buttons = []
                index = 0
                for i in range(3):
                    for j in range(3):
                        self.board_frames[index].grid(row = i + 2, column = j + 1)
                        command_with_args = partial(self.select_card, index)
                        self.board_buttons.append(Button(self.board_frames[index], 
                                                    image = self.board_images[index], 
                                                    command = command_with_args))
                        self.board_buttons[index].grid(row = i + 2, column = j + 1)
                        index += 1
            # Remove the cards in the set
            # Update self.board_buttons
            else:
                for index in range(len(self.game.board)):
                    if self.selected[index] == True:
                        self.selected[index] = False
                        self.board_images[index] = PhotoImage(file = 'images\\' 
                                            + str(self.game.board[index].get_index()) 
                                            + '.png').zoom(2, 2)
                        self.board_buttons[index].config(image = self.board_images[index])
                        self.board_frames[index].config(bg = 'black')
        # A set was not selected
        else:
            for elem in self.board_frames:
                elem.config(bg = 'black')
                for elem in self.game.set:
                    self.game.remove_from_set(elem)

app = App()
