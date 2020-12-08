import tkinter as tk
import tkinter.messagebox as msgbox
from pathlib import Path
import os

from messagescreen import MessageScreen
from styles import BACKGROUND_SCREEN, BACKGROUND_BUTTON, FOREGROUND_LABEL, FOREGROUND_BUTTON



class PlayerFrame(tk.Frame):

	def __init__(self, master, **kwargs):

		super().__init__(master, **kwargs)
		self.controller = None
		self.configure(bg=BACKGROUND_SCREEN)

		self.setup_connection_screen()


	def setup_connection_screen(self):
		"""Sets up screen to inform users about connection."""

		self.connecting_label = tk.Label(self, text="Trying to connect to server...", fg=FOREGROUND_LABEL, bg=BACKGROUND_SCREEN)
		self.connecting_label.pack(pady=(10,0), padx=(10,10))


	def display_connection_error(self, error, connection_info):
		"""Displays connection error information to the user."""

		self.connecting_label.configure(text="Failed conenction at:")

		ip_address, port = connection_info

		self.connection_info_label = tk.Label(self, text=f"{ip_address}     {port}", fg=FOREGROUND_LABEL, bg=BACKGROUND_SCREEN)
		self.connection_info_label.pack(padx=(10,10), pady=(0,10))

		self.learn_more_button = tk.Button(self, text="Learn more", command=lambda: msgbox.showerror("Error connecting", error))
		self.learn_more_button.configure(fg=FOREGROUND_BUTTON, bg=BACKGROUND_BUTTON)
		self.learn_more_button.pack(pady=(10,10), padx=(10,10))


	def display_connection_accepted(self, connection_info):
		"""Displays connection success information to the user."""

		self.connecting_label.configure(text="Succesfully connected at:")

		ip_address, port = connection_info

		self.connection_info_label = tk.Label(self, text=f"{ip_address}     {port}", fg=FOREGROUND_LABEL, bg=BACKGROUND_SCREEN)
		self.connection_info_label.pack(padx=(10,10), pady=(0,10))

		self.current_player_label = tk.Label(self, text="Waiting to begin the game...", fg=FOREGROUND_LABEL, bg=BACKGROUND_SCREEN)
		self.current_player_label.pack(padx=(10,10), pady=(10,20))

		self.setup_game_screen()


	def setup_game_screen(self):

		self.load_images()
		self.setup_grid()

		self.restart_button = tk.Button(self, text="Restart", fg=FOREGROUND_BUTTON, bg=BACKGROUND_BUTTON)
		self.restart_button.configure(state="disabled", command=self.on_restart)
		self.restart_button.pack(pady=(10,10), padx=(10,10))

		self.message_screen = MessageScreen(self)
		self.message_screen.pack(pady=(5,5), padx=(5,5))


	def load_images(self):
		"""Loads images used in the game grid cells."""

		self.X_IMAGE = tk.PhotoImage(file=Path(os.getcwd(), 'res', 'X.png'))
		self.O_IMAGE = tk.PhotoImage(file=Path(os.getcwd(), 'res', 'O.png'))
		self.BLANK_IMAGE = tk.PhotoImage(file=Path(os.getcwd(), 'res', 'blank.png'))


	def setup_grid(self):
		"""Sets up the game grid."""

		self.grid = []

		self.first_grid_row = CellRow(self)
		self.second_grid_row = CellRow(self)
		self.third_grid_row = CellRow(self)

		for i in range(9):

			if i in (0,1,2):
				row = self.first_grid_row
			elif i in (3,4,5):
				row = self.second_grid_row
			else:
				row = self.third_grid_row

			cell = CellButton(row, i, image=self.BLANK_IMAGE, state="disabled")
			self.grid.append(cell)
			cell.pack(side=tk.LEFT)
		
		self.first_grid_row.pack()
		self.second_grid_row.pack()
		self.third_grid_row.pack()


	def setup_game(self, current_player_name):
		"""Sets all necessary things to start a game."""

		for c in self.grid:
			c.configure(image=self.BLANK_IMAGE, state="disabled", token=None)


	def prepare_to_play(self, available_cells):
		"""Makes the available cell clickable for the player."""

		self.current_player_label.configure(text="It's your turn.")

		for cell in available_cells:
			self.grid[cell.index].configure(state="normal")

		self.restart_button.configure(state="normal")


	def prepare_to_wait_turn(self, rival_name, available_cells):
		"""Disables all cells in the grid as well as the restart button."""

		self.current_player_label.configure(text=f"It's {rival_name}'s turn")

		for cell in available_cells:
			self.grid[cell.index].configure(state="disabled")

		self.restart_button.configure(state="disabled")


	def player_played(self, index, token):
		"""Updates the game screen after a play."""

		self.grid[index].token = token
		image = self.X_IMAGE if token == 'X' else self.O_IMAGE
		self.grid[index].configure(image=image, state="disabled")


	def game_over(self, header, message, available_cells):
		"""Display some message to the user once the game is over."""

		for cell in available_cells:

			self.grid[cell.index].configure(state="disabled")

		msgbox.showinfo(header, message)


	def notify_rival_closing(self):
		"""Method called when the rival player sends a CLOSING message to notify player."""

		self.message_screen.write("Rival has left the game")
		msgbox.showinfo("Last Man Standing", "Rival left the game")


	def on_cell_pressed(self, cell):
		"""Receives the instance of the cell that was pressed."""

		self.controller.player_client.send_message(f"PLAYED {cell.index}")

	
	def on_restart(self):
		"""Method called when the restart button is pressed."""

		self.controller.player_client.send_message("RESTART")
		self.message_screen.write("You restarted the game")



class CellRow(tk.Frame):

	def __init__(self, master, **kwargs):

		super().__init__(master, **kwargs)



class CellButton(tk.Button):

	def __init__(self, master, index, **kwargs):
		"""The command is set in the cell's constructor, since each button will call a method from the master
		widget passing its reference as an argument. This assignment can't be done in the master widget inside
		a loop, since all buttons seem to call the method giving the reference of the last cell."""

		super().__init__(master, **kwargs)
		#The cells master is a frame, and the frame's master is the screen tha tcontains the method.
		self.configure(command=lambda: self.master.master.on_cell_pressed(self))

		self.index = index
		self.token = None