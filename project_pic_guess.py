# TIE-02107 Introduction to Programming
# Student name: Stefanus Wirdatmadja, Student nr: 232722
# A game to guess the picture puzzle the puzzle and questions will
# not be repeated.
# Just run the game, the instruction will be give on the dialog box
# at the beginning of the game.

from tkinter import *
import math
from tkinter import simpledialog
from tkinter import messagebox
import random
import sys


# the amount of squares and it should in integer to the power of 2
SQUARE_NUMBER = 25

class Picturegame:
    def __init__(self):
        # Reads all the input files and put into the lists
        PUZZLE_FILE = './questions/pic_questions.txt'
        QUESTION_FILE = './questions/square_questions.txt'

        with open(PUZZLE_FILE) as file1:
            self.__puzzle_list = file1.readlines()

        with open(QUESTION_FILE) as file2:
            self.__question_list = file2.readlines()

        # deletes the titles
        del self.__puzzle_list[0]
        del self.__question_list[0]

        # Creates the main window
        self.__window = Tk()

        # Gets the requested values of the height and widht.
        windowWidth = self.__window.winfo_reqwidth()
        windowHeight = self.__window.winfo_reqheight()

        # Gets both half the screen width/height and window width/height
        positionRight = int(self.__window.winfo_screenwidth() / 2 - windowWidth)
        positionDown = int(self.__window.winfo_screenheight() / 2 - windowHeight)

        # Positions the window in the center of the page.
        self.__window.geometry("+{}+{}".format(positionRight, positionDown))

        self.__window.title("Guess the picture")
        self.__score = 0

        self.initialize()

        self.__themeLabel = Label(self.__window, text='Theme:')
        self.__themeLabel.grid(row=0, column=0, columnspan=2, sticky=E)

        self.__themeText = Label(self.__window)
        self.__themeText.grid(row=0, column=2, columnspan=self.row_col, sticky=W)

        self.__newgameButton = Button(self.__window, text='New Game',
                                      command=self.newGame)
        self.__newgameButton.grid(row=1, column=self.row_col+2)

        self.__nextquestionButton = Button(self.__window, text='Next Question',
                                           command=self.nextQuestion)
        self.__nextquestionButton.grid(row=2, column=self.row_col+2)

        self.__scoreLabel = Label(self.__window)
        self.__scoreLabel.grid(row=3, column=self.row_col+2)
        self.printScore()

        self.__hintButton = Button(self.__window, text='Hint',
                                   command=self.displayHint)
        self.__hintButton.grid(row=4, column=self.row_col + 2)

        self.__quitButton = Button(self.__window, text='Quit',
                                   command=self.__window.destroy)
        self.__quitButton.grid(row=5, column=self.row_col+2)

        self.__answerLabel = Label(self.__window, text='Answer:')
        self.__answerLabel.grid(row=self.row_col+1, column=0, columnspan=2,
                                sticky=E)

        self.__answerEntry = Entry(self.__window)
        self.__answerEntry.grid(row=self.row_col+1, column=2,
                                columnspan=self.row_col-1, sticky=E+W)

        self.__checkanswerButton = Button(self.__window, text='Check Answer',
                                          command=self.checkAnswer)
        self.__checkanswerButton.grid(row=self.row_col+1, column=self.row_col+2)

        self.__hintLabel = Label(self.__window, text='Hint:')
        self.__hintLabel.grid(row=self.row_col + 2, column=0, columnspan=2,
                              sticky=E)

        self.__hintText = Label(self.__window)
        self.__hintText.grid(row=self.row_col + 2, column=2,
                             columnspan=self.row_col - 1, sticky=W)

        self.__answerButton = Button(self.__window, text='Give up!',
                                     command=self.giveup)
        self.__answerButton.grid(row=self.row_col + 2,
                                 column=self.row_col+2, sticky=E+W)

        self.resetInfo()

        messagebox.showinfo("Instruction", "PICTURE PUZZLE GAME\n"
                                           "Your mission is to guess what picture is hidden\n"
                                           "1. Click one square that you want to reveal. You "
                                           "have to answer the question to reveal the picture "
                                           "underneath. Wrong answer costs you -1 and right "
                                           "answer is rewarded +2.\n"
                                           "2. You can get a HINT, but it will cost you -5. "
                                           "It can only be used once and make sure you have "
                                           "enough points\n"
                                           "3. NEW GAME will reset your score (to zero)\n"
                                           "4. NEXT QUESTION will not reset your score and you"
                                           "continue the game with new puzzle\n"
                                           "5. If you don't know the answer but curious what "
                                           "the answer is, you can GIVE UP, but it will cost "
                                           "you -10 and next game will start automatically.\n"
                                           "6. When you know the answer you can CHECK your "
                                           "ANSWER. If it is wrong, it will cost you -1, but "
                                           "if it is correct, you will be rewarded by +10.\n"
                                           "\n Enjoy your play!!!")

    def questionDestroy(self, questionNumber):
        """
        Gives the question of the corresponding square that is chosen by the
        player and destroys the cover to reveal the picture underneath it

        :param questionNumber: int, number related to the square
        :return: None
        """
        random_value = random.randint(0,
                                      len(self.__question_list)-1)
        question, right_answer = self.__question_list[random_value].split(';')
        answer = simpledialog.askstring("Do you know?", question,
                                        parent=self.__window)

        if answer is not None:
            answer = answer.replace(' ', '')
            right_answer = right_answer.strip().replace(' ', '')
            if answer.lower() == right_answer.lower():
                self.__questionButtons[questionNumber].destroy()
                messagebox.showinfo("Congrats", "Right! +2 for you. Keep it up!")
                self.__score += 2
                self.printScore()
            else:
                if self.__score != 0:
                    messagebox.showinfo("Oops..", "Wrong answer! -1 for you!")
                    self.__score -= 1
                    self.printScore()
                else:
                    messagebox.showinfo("Oops..", "Wrong answer!")

            self.hintPossible()

        del self.__question_list[random_value]
        self.checkDatabase()

    def displayHint(self):
        """
        Displays the hint if the player agree after reconfirmation
        :return: None
        """
        answer = messagebox.askyesno("Think Again!", "Your score will be "
                                        "reduced by 5 points. Are you sure to "
                                        "use this help?")
        if answer:
            self.__hintText.configure(text=self.__hint)
            self.__hintButton.configure(state=DISABLED)
            if self.__score > 4:
                self.__score -= 5
                self.printScore()

    def checkAnswer(self):
        """
        checks the player's answer of what picture underneath the squares and
        gives corresponding score.
        :return: None
        """
        answer = self.__answerEntry.get()
        answer = answer.replace(' ', '')
        answer1 = answer.lower()
        answer2 = self.__answer.replace(' ', '')
        answer2 = answer2.lower()
        if answer1 == answer2:
            # reveals the puzzle picture
            for square in self.__questionButtons:
                square.destroy()
            messagebox.showinfo("Congratulation", "Correct Answer!")
            del self.__puzzle_list[self.__puzzle_random]
            self.__score += 10
            self.hintPossible()
            self.printScore()
            self.destroyPuzzle()
            self.initialize()
            self.resetInfo()
        else:

            self.__answerEntry.delete(0, 'end')
            if self.__score != 0:
                self.__score -= 1
                self.printScore()
                messagebox.showinfo("Sorry", "Wrong Answer. -1 for you. Try Again!")
            else:
                messagebox.showinfo("Sorry", "Wrong Answer. Try Again!")
            self.hintPossible()

    def nextQuestion(self):
        """
        proceeds to the next puzzle if the player decides to continue the game
        but he/she not curious enough to know the current puzzle answer.
        :return: None
        """
        del self.__puzzle_list[self.__puzzle_random]
        self.destroyPuzzle()
        self.initialize()
        self.resetInfo()

    def hintPossible(self):
        """
        checks if the player is possible to use the hint service. This is based
        on the player's score and whether the hint has been revealed or not.
        :return: None
        """
        if self.__score > 4 and self.__hintText['text'] == '':
            self.__hintButton.configure(state=NORMAL)
        else:
            self.__hintButton.configure(state=DISABLED)

    def initialize(self):
        """
        initializes the puzzle picture and the squares covering it
        :return: None
        """
        self.checkDatabase()

        # Gets randomly the puzzle picture, theme, hint, and answer
        self.__puzzle_random = random.randint(0, len(self.__puzzle_list) - 1)
        self.__puzzle_list[self.__puzzle_random] = \
            self.__puzzle_list[self.__puzzle_random].replace('\n', '')
        self.__theme, self.__puz_file, self.__answer, self.__hint = \
            self.__puzzle_list[self.__puzzle_random].split(';')

        # Displays the puzzle pic
        self.row_col = int(math.sqrt(SQUARE_NUMBER))
        self.pic_puzzle = PhotoImage(file='./image/'+self.__puz_file)
        self.__pic_puzzle = Label(self.__window, image=self.pic_puzzle)
        self.__pic_puzzle.grid(row=1, rowspan=self.row_col, column=1,
                               columnspan=self.row_col)

        # Covers the puzzle pic with buttons
        self.__questionButtons = []
        for square in range(0, SQUARE_NUMBER):
            new_button = Button(self.__window,
                                command=lambda a=square: self.questionDestroy(a))
            row_value = int(square // self.row_col) + 1
            column_value = int(square % self.row_col) + 1
            new_button.grid(row=row_value, column=column_value,
                            sticky=N + S + W + E)
            self.__questionButtons.append(new_button)

    def resetInfo(self):
        """
        changes the information about the updated puzzle
        :return: None
        """
        self.__themeText.configure(text=self.__theme)
        self.__hintText.configure(text='')
        self.hintPossible()

    def destroyPuzzle(self):
        """
        destroys the puzzle pictures and squares in order to create new puzzle
        :return: None
        """
        self.__pic_puzzle.destroy()
        self.__answerEntry.delete(0,'end')

    def newGame(self):
        """
        initiates new game where old puzzle will be destroyed and new puzzle
        will be initialized. The score will be reset (to zero)
        :return: None
        """
        answer = messagebox.askyesno("Think Again!", "Your score will be "
                                                     "reset to 0 points. "
                                                     "Are you sure?")
        if answer:
            self.__score = 0
            self.printScore()
            self.destroyPuzzle()
            self.initialize()
            messagebox.showinfo("New Game", "Get Ready!")

    def checkDatabase(self):
        """
        checks if there is still any puzzle or questions left on the database
        :return: None
        """
        if len(self.__puzzle_list) == 0 or len(self.__question_list) == 0:
            messagebox.showinfo("Info", "We are running out of puzzles. "
                                        "Thank you for playing with us!")
            self.__window.destroy()
            sys.exit()

    def giveup(self):
        """
        shows the answer to the player and automatically start next puzzle.
        The score will be deducted by 10 points.
        :return: None
        """
        answer = messagebox.askyesno("Think Again!", "Your score will be "
                                                     "reduced by 10 points and "
                                                     "next game will start "
                                                     "automatically. Are you sure to "
                                                     "give up?")
        if answer:
            self.__score -= 10
            if self.__score < 0:
                self.__score = 0
            # reveals the puzzle picture
            for square in self.__questionButtons:
                square.destroy()
        self.printScore()
        messagebox.showinfo("Answer", "Answer: "+self.__answer)
        self.destroyPuzzle()
        self.initialize()

    def printScore(self):
        """
        updates the scores
        :return: None
        """
        self.__scoreLabel.configure(text='Score: ' + str(self.__score) + ' pts')

    def start(self):
        self.__window.mainloop()

def main():
    ui = Picturegame()
    ui.start()

main()