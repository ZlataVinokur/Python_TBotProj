from random import choice
from anekdot import anekdots

with open('words.txt', 'r', encoding='utf-8') as f:
    WORDS = [line.strip().lower() for line in f.readlines()]

with open('words_dif.txt', 'r', encoding='utf-8') as f:
    WORDSDIF = [line.strip().lower() for line in f.readlines()]

class HangmanGame:
    def __init__(self):
        self.game_on = False

    def start(self):
        self.game_on = True
        self.used = []
        self.word = choice(WORDS)
        self.so_far = ['_'] * len(self.word)
        self.wrong = 0
        self.max_wrong = len(HANGMANPICS) - 1
        self.anekdot = choice(anekdots)

    def startDif(self):
        self.game_on = True
        self.used = []
        self.word = choice(WORDSDIF)
        self.so_far = ['_'] * len(self.word)
        self.wrong = 0
        self.max_wrong = len(HANGMANPICS) - 1
        self.anekdot = choice(anekdots)

    def info(self):
        msg = HANGMANPICS[self.wrong]
        msg += '\n Вы использовали следующие буквы: \n'
        msg += str(self.used) + '\n'
        msg += ' '.join(self.so_far)
        msg += '\n\n Введите новую букву'
        return msg

    def game_step(self, letter):
        if letter in self.used:
            return 'Вы уже эту букву использовали!'
        else:
            self.used.append(letter)
            if letter in self.word:
                msg = f'\n Дa! \"{letter}\" есть в слове! \n'
                indxs = [i for i in range(len(self.word)) if self.word[i] == letter]
                for indx in indxs:
                    self.so_far[indx] = letter
                if self.so_far.count('_') == 0:
                    congrats = f'\nВау, вы угадали все буквы слова {self.word} \nВаша награда этот анекдот:\n {self.anekdot}'
                    msg += congrats
                    self.game_on = False
                else:
                    msg += self.info()
                return msg
            else:
                msg = f'\n Hе угадали, \"{letter}\" нет в слове! \n'
                self.wrong += 1
                if self.wrong >= self.max_wrong:
                    msg += HANGMANPICS[self.max_wrong]
                    msg = '\n Вас повесили( \n И вы не получите анекдот((('
                    msg += f' \n Правильный ответ: {self.word}'
                    self.game_on = False
                else:
                    msg += self.info()
                return msg

HANGMANPICS = ('''
  +---+
      |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''')