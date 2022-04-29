from tkinter import *
from tkinter.messagebox import *
from random import randint
import re

# Variable global, la palabra a adivinar
game_word = ''

# Lista de palabras para modo aleatorio
words_list = ('casa', 'apendice', 'monitor', 'hipopotomostrosesquidepaliofobia', 'Electroencefalografista',
              'Otorrinolaringologo', 'Caleidoscopio', 'Arteriosclerosis', 'Electrocardiograma', 'Electrodoméstico',
              'Lactovegetarianismo', 'Desacostumbradamente', 'Seudohermafroditismo', 'Antitauromaquia',
              'Contrarrevolucionariamente', 'Desindustrialización', 'Incomprehensibilidad', 'Equisatisfactibilidad',
              'Androide', 'Mantener', 'Tristeza', 'Kimono', 'Taekwondo', 'Guirnalda', 'Situación', 'Recordar',
              'Entonces', 'Inconmensurable', 'Indiscutible', 'Sempiterno', 'Nauseabundo', 'Programacion', 'Contruccion',
              'petricor', 'luminiscencia', 'infinito', 'construir', 'martillo', 'melancolia', 'futbol', 'rugby',
              'tenis', 'nefelibata', 'elocuencia', 'elocuente')

# Variable para almacenar la cantidad de palabras aleatorias
words_list_quantity = -1

# Variables globales para almacenar la cantidad de juegos ganados y perdidos
winned_games = 0
losed_games = 0

# Actualizar cantidad de palabras aleatorias
for words in words_list:
    words_list_quantity = words_list_quantity + 1


# Ventana principal, menu de inicio
class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title('Juego: Ahorcadito')
        self.master.geometry('500x400')
        self.master.resizable(False, False)
        # self.master.iconbitmap('ahorcado_game.ico')
        self.widgets()

    # Mostrar widgets
    def widgets(self):
        title = Label(self.master, text='JUEGO DEL AHORCADO',
                      font=('calibri', 20, 'bold'),
                      pady=10,
                      anchor=CENTER
                      )
        title.pack()

        word_label = Label(self.master, text='Ingrese una palabra para jugar:',
                           font=('calibri', 15)
                           )
        word_label.pack()

        self.word_entry = Entry(self.master,
                                width=100,
                                justify='center',
                                show='*')
        self.word_entry.pack()

        play_button = Button(self.master, text='JUGAR!',
                             width=50,
                             pady=20,
                             command=lambda: self.play_game())
        play_button.pack()

        seeword_button = Button(self.master, text='Mostrar/ocultar palabra',
                                width=50,
                                pady=20,
                                command=lambda: self.show_word())
        seeword_button.pack()

        random_word_label = Label(self.master, text='O, puede jugar con una palabra aleatoria:',
                                  font=('calibri', 15)
                                  )
        random_word_label.pack()

        random_play_button = Button(self.master, text='JUGAR MODO ALEATORIO!',
                                    width=50,
                                    pady=20,
                                    command=lambda: self.play_random_game())
        random_play_button.pack()

        self.winned_games_label = Label(self.master, text=f'Partidas ganadas: {winned_games}',
                                        font=('calibri', 15)
                                        )
        self.winned_games_label.pack()

        self.losed_games_games_label = Label(self.master, text=f'Partidas perdidas: {losed_games}',
                                             font=('calibri', 15)
                                             )
        self.losed_games_games_label.pack()  # # Most

    # Metodo para revelar u ocultar la palabra que ingresa el usuario
    def show_word(self):
        if self.word_entry.cget('show') == '*':
            self.word_entry.config(show='')
            self.word_entry.pack()
        else:
            self.word_entry.config(show='*')
            self.word_entry.pack()

    # Metodo para jugar con palabra personalizada
    def play_game(self):
        if self.word_entry.get().isspace() or self.word_entry.get() == '':
            showerror(title='Error',
                      message='No ha introducido ninguna palabra')
        elif not self.word_entry.get().isalpha():
            showerror(title='Error',
                      message='Solo se pueden introducir letras')
        else:
            global game_word
            game_word = self.word_entry.get()
            game_window = Toplevel(self.master)
            game_window.grab_set()
            Game(game_window)

    # Metodo para jugar con palabra aleatoria
    def play_random_game(self):
        global game_word
        game_word = words_list[(randint(0, words_list_quantity))]
        game_window = Toplevel(self.master)
        game_window.grab_set()
        Game(game_window)

    # Metodo para actualizar la cantidad de juegos ganados y perdidos
    def update_lives(self):
        self.winned_games_label.config(text=f'Partidas ganadas: {winned_games}')

        self.losed_games_games_label.config(text=f'Partidas perdidas: {losed_games}')


# Ventana de juego
class Game:
    # Variable que almacena la cantidad de vidas
    lives = 6

    def __init__(self, master):
        # super().__init__(master)
        self.master = master
        self.master.title = 'Ahorcadito'
        # self.master.geometry('500x500')
        self.master.resizable(False, False)
        # self.master.iconbitmap('ahorcado_game.ico')
        self.widgets()

    # Metodo para crear los botones
    def create_button(self, letter, rows, columns):
        self.btn = Button(self.master, text=letter, font=('arial', 15, 'bold'),
                          command=lambda: [self.check_letter(letter), self.disable_button(letter, rows, columns)])
        self.btn.grid(row=rows, column=columns)

    # Metodo para mostrar los widgets
    def widgets(self):
        self.lifes_label = Label(self.master, text=f'Vidas restantes: {self.lives}', font=15,
                                 fg='red')
        self.lifes_label.grid(row=0, column=0, columnspan=10)

        global game_word
        game_word = game_word.upper()

        wtg_label = Label(self.master, text='PALABRA A ADIVINAR:', font=('calibri', 20, 'italic'))
        wtg_label.grid(row=1, column=0, columnspan=10)

        self.censored_word = Label(self.master, text=re.sub('[QWERTYUIOPASDFGHJKLZXCVBNM]', '*', game_word),
                                   font=('arial', 25, 'bold'))
        self.censored_word.grid(row=2, column=0, columnspan=10)

        self.a = self.create_button('A', 3, 0)
        self.b = self.create_button('B', 3, 1)
        self.c = self.create_button('C', 3, 2)
        self.d = self.create_button('D', 3, 3)
        self.e = self.create_button('E', 3, 4)
        self.f = self.create_button('F', 3, 5)
        self.g = self.create_button('G', 3, 6)
        self.h = self.create_button('H', 3, 7)
        self.i = self.create_button('I', 3, 8)
        self.j = self.create_button('J', 3, 9)
        self.k = self.create_button('K', 4, 0)
        self.l = self.create_button('L', 4, 1)
        self.m = self.create_button('M', 4, 2)
        self.n = self.create_button('N', 4, 3)
        self.o = self.create_button('O', 4, 4)
        self.p = self.create_button('P', 4, 5)
        self.p = self.create_button('Q', 4, 6)
        self.r = self.create_button('R', 4, 7)
        self.s = self.create_button('S', 4, 8)
        self.t = self.create_button('T', 4, 9)
        self.u = self.create_button('U', 5, 0)
        self.v = self.create_button('V', 5, 1)
        self.w = self.create_button('W', 5, 2)
        self.x = self.create_button('X', 5, 3)
        self.y = self.create_button('Y', 5, 4)
        self.z = self.create_button('Z', 5, 5)

    # Metodo para deshabilitar el boton una vez pulsado
    def disable_button(self, letter, rows, columns):
        self.btn = Button(self.master, text=letter, font=30, state=DISABLED, disabledforeground='black', bg='black')
        self.btn.grid(row=rows, column=columns)

    # Metodo para comprobar si la letra ingresada se encuentra en la palabra a adivinar
    @staticmethod
    def letter_match(letter):
        return letter in game_word

    # Metodo para perder una vida
    def lose_live(self):
        self.lives = self.lives - 1

        self.lifes_label = Label(self.master, text=f'Vidas restantes: {self.lives}', font=15,
                                 fg='red')
        self.lifes_label.grid(row=0, column=0, columnspan=10)

    # Metodo para encontrar la posicion de la letra especificada en la palabra a adivinar
    def find_letter(self, letter):
        self.positions = []
        for letters in game_word:
            if letters == letter:
                if not self.positions:
                    letter_position = game_word.find(letter)
                    self.positions.append(letter_position)
                else:
                    letter_position = game_word.find(letter, (self.positions[-1]) + 1)
                    self.positions.append(letter_position)
        print(self.positions)

    # Metodo para revelar la letra ingresada, si es que se encuentra en la palabra a adivinar
    def reveal_letters(self, letter):
        uncensored_word = self.censored_word.cget('text')
        uncensored_word_list = []

        for censored in uncensored_word:
            uncensored_word_list.append(censored)

        for positions in self.positions:
            uncensored_word_list[positions] = letter

        uncensored_word = ''
        for letters in uncensored_word_list:
            uncensored_word = uncensored_word + letters

        self.censored_word = Label(self.master, text=uncensored_word,
                                   font=('arial', 25, 'bold'))
        self.censored_word.grid(row=2, column=0, columnspan=10)

    # Metodo para comprobar si se ha ganado la partida
    def check_win(self):
        check_win = self.censored_word.cget('text')
        return check_win.find('*') == -1

    # Metodo para indicar que se ha ganado el juego
    def game_winned(self):
        global winned_games
        error_window = Toplevel()
        error_window.grab_set()
        error_window.withdraw()
        showinfo(title='Ganaste!',
                 message=f'Has ganado el juego! La palabra era "{game_word}". Volviendo al menu principal...')
        winned_games = winned_games + 1
        MainWindow.update_lives(game)
        self.lives = 6
        error_window.destroy()
        self.master.destroy()

    # Metodo para indicar que se ha perdido el juego
    def losed_game(self):
        global losed_games
        error_window = Toplevel()
        error_window.grab_set()
        error_window.withdraw()
        showerror(title='Has perdido',
                  message=f'Has perdido, la palabra era "{game_word}". Volveras al menu de inicio')
        losed_games = losed_games + 1
        MainWindow.update_lives(game)
        self.lives = 6
        error_window.destroy()
        self.master.destroy()

    # Metodo principal. Usa todos los anteriores para que el juego se lleve a cabo.
    def check_letter(self, letter):
        if self.lives > 1:
            if self.letter_match(letter):
                self.find_letter(letter)
                self.reveal_letters(letter)
                if self.check_win():
                    self.game_winned()
            else:
                self.lose_live()
        else:
            if self.letter_match(letter):
                self.find_letter(letter)
                self.reveal_letters(letter)
                if self.check_win():
                    self.game_winned()
            else:
                self.losed_game()



# Instanciar la clase MainWindow para crear una ventana
game = MainWindow(Tk())
game.master.mainloop()
