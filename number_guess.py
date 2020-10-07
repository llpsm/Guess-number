# import modules
from tkinter import *
from tkinter.ttk import *
import random

# adding a menu to entry widget
class EntryPlus(Entry):
	def __init__(self, *args, **kwargs):
		Entry.__init__(self, *args, **kwargs)
		_rc_menu_install(self)
		self.bind("<Button-3><ButtonRelease-3>", self.rmenu)

	def rmenu(self, e):
		self.tk.call("tk_popup", self.menu, e.x_root, e.y_root)

def _rc_menu_install(w):
	w.menu = Menu(w, tearoff=0)
	w.menu.add_command(label="Cut")
	w.menu.add_command(label="Copy")
	w.menu.add_command(label="Paste")
	w.menu.add_separator()
	w.menu.add_command(label="Select all")		

	w.menu.entryconfigure("Cut", command=lambda: w.focus_force() or w.event_generate("<<Cut>>"))
	w.menu.entryconfigure("Copy", command=lambda: w.focus_force() or w.event_generate("<<Copy>>"))
	w.menu.entryconfigure("Paste", command=lambda: w.focus_force() or w.event_generate("<<Paste>>"))
	w.menu.entryconfigure("Select all", command=lambda: w.focus_force() or w.event_generate("<Control-a>"))

# main window
root = Tk()
root.title('Number Guess')
root.resizable(0,0)

class Guess():
	score = IntVar() # variable for store score
	score.set(100)
	num = random.randint(10,99) # generating a number to guess
	hints = [] # list for storing hints
	number_str = StringVar()
	number_str.set('???')

	# creating main ui widgets
	def __init__(self):
		self.menu = Menu(root)
		self.menu_cont() # contents of the menu
		self.label1 = Label(root, text='Number', font=('Cooper', 18), width=40, anchor='center')
		self.num_lbl = Label(root, textvariable=Guess.number_str, font=('Cooper', 20), background='#34897f', width=20, anchor='center')
		self.guess_lbl = Label(root, text='Enter your guess', anchor='center', font=('Cooper', 15))
		self.guess_ent = EntryPlus(root, font=('Cooper', 20))
		self.check_btn = Button(root, text='Check', command=self.check)
		self.hint_btn = Button(root, text='Hint', command=self.hint_window)
		self.score_lbl = Label(root, text='Score', font=('Cooper', 18), anchor='center', background='#84a5aa')
		self.score = Label(root, textvariable=Guess.score, font=('Cooper', 25), anchor='center', foreground='red')

		self.label1.grid(row=0, column=0, padx=50, pady=30)
		self.num_lbl.grid(row=1, column=0,padx=50, ipady=10)
		self.guess_lbl.grid(row=2, column=0, padx=50, pady=20)
		self.guess_ent.grid(row=3, column=0, padx=75, ipady=20, sticky='wens')
		self.check_btn.grid(row=4, column=0, pady=20, padx=75, sticky='ens')
		self.hint_btn.grid(row=4, column=0, pady=20, sticky='ns')
		self.score_lbl.grid(row=5, column=0,padx=75)
		self.score.grid(row=6, column=0,padx=75, pady=20)

		self.hint() # generating hints and storing them in hints attribute

	# contents of the main menu
	def menu_cont(self):
		menu = Menu(self.menu, tearoff=0)
		menu.add_command(label='How to play?')
		menu.add_command(label='Hint')
		menu.add_command(label='Highscores')
		menu.add_command(label='Quit')
		menu.entryconfigure('How to play?', command=self.help)
		menu.entryconfigure('Hint', command=self.hint_window)
		menu.entryconfigure('Highscores', command=self.hscore)
		menu.entryconfigure('Quit', command=self.quit)
		self.menu.add_cascade(label='Menu', menu=menu)
		root.config(menu=self.menu)

	# contents of how to play window
	def help(self):
		helpwin = Toplevel(root)
		helpwin.title('How to play?')
		# rules for playing the game
		text = 'blah'
		label = Label(helpwin, text=text, anchor='center')
		button = Button(helpwin, text='OK', command=helpwin.destroy)
		label.grid(row=0, column=0, padx=10, pady=10)
		button.grid(row=1, column=0, sticky='e')

	# generating hints for storing in the hints attribute
	def hint(self):
		# check if the number is odd or even
		def odd_even(num):
			if num % 2 == 0:
				return 'even'
			else:
				return 'odd'

		# finding numbers that can be divided by
		def divisible(num):
			l1 = []
			for x in range(10,100):
				if num % x == 0:
					l1.append(x)
			return l1

		# check if it is a square number
		def square(num):
			square = [16,25,36,49,64,81]
			if Guess.num in square:
				return True

		# check if it is a triangular number
		def triangular(num):
			tri = [10,15,21,28,36,45,55,66,78,91]
			if Guess.num in tri:
				return True

		# check if it is a prime number
		def prime(num):
			prime = [11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
			if num in prime:
				return True

		# calling the functions and appending hints to the hints arribute
		Guess.hints.insert(0,f'It is a {odd_even(Guess.num)} number')
		ind = 1
		for num in divisible(Guess.num):
			Guess.hints.insert(ind,f'It is divisible by {num}')
			ind+=1
		if square(Guess.num) == True:
			Guess.hints.insert(ind,'It is a square number')
		else:
			Guess.hints.insert(ind,'It is not a square number')
		if triangular(Guess.num) == True:
			Guess.hints.insert(ind+1,'It is a triangular number')
		else:
			Guess.hints.insert(ind+1,'It is not a triangular number')
		if prime(Guess.num) == True:
			Guess.hints.insert(ind+2,'It is a prime number')
		else:
			Guess.hints.insert(ind+2,'It is not a prime number')

	# creating a new window to display hints
	def hint_window(self):
		hint = Toplevel(root)
		hint.resizable(0,0)
		hint.title('Hint')
		if Guess.hints != []:
			label = Label(hint, text=Guess.hints.pop(0), anchor='center', font=('Arial', 15))
			print(Guess.hints)
			label.update()
			Guess.score.set(Guess.score.get()-5)
		else:
			label = Label(hint, text='No more hints!', anchor='center', font=('Arial', 15))
		btn = Button(hint, text='OK', command=hint.destroy)

		label.grid(row=0, column=0, padx=10, pady=10, sticky='esnw')
		btn.grid(row=1, column=0, padx=10, pady=10, sticky='esn')

	# store and display highscores (not created yet)
	def hscore(self):
		print('hscore')

	# function to ask for permission when quitting
	def quit(self):
		warn = Toplevel(root)
		# warn.geometry('250x100')
		warn.resizable(0,0)
		label = Label(warn, text='Are you sure?', font=('Arial', 14))
		ybtn = Button(warn, text='Yes', command=root.quit)
		nbtn = Button(warn, text='No', command=warn.destroy)

		label.grid(row=0, column=1, columnspan=3,padx=100, pady=10, sticky='nesw')
		ybtn.grid(row=1, column=1, padx=10, pady=10, sticky='e')
		nbtn.grid(row=1, column=2, padx=10, pady=10, sticky='e')

	# check if the player guessed the correct number
	def check(self):
		if self.guess_ent.get() == str(Guess.num):
			Guess.number_str.set(str(Guess.num))
			win = Toplevel(root)
			win.resizable(0,0)
			label = Label(win, font=('Cooper', 24), background='#ff6a6a', text=f'Congratulations!!\nYou have won the game!\nYour score is {Guess.score.get()}', anchor='center')
			label.grid(row=0, column=0, padx=10, pady=10)
		else:
			Guess.number_str.set('Try Again!!')
			Guess.score.set(Guess.score.get()-1)



Guess()

root.mainloop()
