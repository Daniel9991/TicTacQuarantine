"""This is tic tac toe to play across devices. One player has to create a game (create a client server
to listen to messages from own device and the other device) and the other one joins the game. Both players
must know the ip address and the listening port of the client server to connect to it."""



import tkinter as tk
import tkinter.messagebox as msgbox
import threading
from queue import LifoQueue as Stack #put() and get()
import time
from pathlib import Path
import os

from player_model import PlayerModel
from player_frame import PlayerFrame
from player_controller import PlayerController
from networking import Server, PlayerClient
from screens import InitialScreen, InfoGatheringScreen, IpWindow
from styles import FOREGROUND_BUTTON, BACKGROUND_BUTTON, BACKGROUND_SCREEN



class App(tk.Tk):

	def __init__(self):
		"""Create the app."""

		super().__init__()

		self.configure_window()

		self.screen_stack = Stack() #Here the window will save a reference and order of the screens that it has packed
									#So that they can unpacked accordingly.
		self.pack_help_frame() #This frame provides help and a button to go to the previous window
		self.pack_initial_screen() #Calling method to setup the initial screen


	def configure_window(self):
		"""Defines some elements for the main window"""

		self.title("TicTacStayOverThere")
		self.configure(bg=BACKGROUND_SCREEN)
		icon_path = Path(os.getcwd(), "res", "icon.png")
		icon = tk.PhotoImage(file=icon_path)
		self.iconphoto(False, icon)
		self.bind_keys()


	def pack_help_frame(self):
		"""Here the bottom frame of the app is packed. It contains a button to go back,
		as well as stuff on how to connect and others."""

		self.help_frame = tk.Frame(self, bg=BACKGROUND_SCREEN)
		self.help_frame.pack(side=tk.BOTTOM)

		#This is a Toplevel window that will give users info on how to connect
		self.how_to_connect_window = IpWindow(self)
		self.focus()

		my_credits = lambda: msgbox.showinfo("Credits", "Created by Daniel. 2020")
		self.credits_button = tk.Button(self.help_frame, text="Credits", command=my_credits)
		self.credits_button.configure(bg=BACKGROUND_BUTTON, fg=FOREGROUND_BUTTON)
		self.credits_button.pack(side=tk.RIGHT, pady=(10,10), padx=(5,10))

		self.how_to_connect_button = tk.Button(self.help_frame, text="How to connect")
		self.how_to_connect_button.configure(bg=BACKGROUND_BUTTON, fg=FOREGROUND_BUTTON, command=lambda: self.how_to_connect_window.deiconify())
		self.how_to_connect_button.pack(side=tk.RIGHT, pady=(10,10), padx=(5,0))

		self.back_button = tk.Button(self.help_frame, text="Go back", command=self.go_to_previous_screen)
		self.back_button.configure(bg=BACKGROUND_BUTTON, fg=FOREGROUND_BUTTON, disabledforeground=FOREGROUND_BUTTON, state="disabled")
		self.back_button.pack(side=tk.LEFT, pady=(10,10), padx=(10,0))


	def pack_initial_screen(self):

		self.first_screen = InitialScreen(self)
		self.mount_screen(self.first_screen)


	def pack_info_gathering_screen(self, mode):
		
		self.info_screen = InfoGatheringScreen(self, mode)
		self.mount_screen(self.info_screen)
		self.back_button.configure(state="normal")


	def mount_screen(self, new_screen):
		"""Packs new screen as the current screen and adds it to the screen stack."""

		if type(new_screen) == InitialScreen:
			new_screen.pack(fill=tk.X)
			self.current_screen = new_screen
		else:
			self.current_screen.pack_forget()
			self.screen_stack.put(self.current_screen)
			self.current_screen = new_screen
			self.current_screen.pack(fill=tk.X)


	def go_to_previous_screen(self, send_closing=True):
		"""Handles changing screens (from one to the previous)"""

		if not self.screen_stack.empty():

			if type(self.current_screen) == PlayerFrame: #Player is on the game screen a clicks on the back button.
				if hasattr(self.player_controller, "player_client"):
					if send_closing:
						self.player_controller.player_client.send_message("CLOSING")
					self.player_controller.player_client.client.close()
				if hasattr(self, "server"):
					self.server.client.close()

			self.current_screen.pack_forget()
			self.current_screen = self.screen_stack.get()
			self.current_screen.pack()

			if type(self.current_screen) == InitialScreen: #If user returns to the first screen, disable back button
				self.back_button.configure(state="disabled")

		else: #It will never enter here since the back button is disabled in when the first screen is active
			pass


	def create_game(self, name, ip_address, port, mode):
		"""Player must create game, that is, a server client is created and it is set to listen for players in a new thread,
		so that current flow can create player instance and connect to server."""

		try:
			self.server = Server(ip_address, port)
		except Exception as e:
			msgbox.showerror("Error creating the server", f"The following error happened when creating the server.\n{e}")
		else:
			threading.Thread(target=self.server.accept_players).start()
			self.join_game(name, ip_address, port, mode)


	def join_game(self, name, ip_address, port, mode):
		"""Player connects to the server client, sends name over and creates the frame."""

		model = PlayerModel(name, ip_address, port, mode)
		frame = PlayerFrame(self)
		self.mount_screen(frame)
		self.player_controller = PlayerController(model, frame)


	def bind_keys(self):
		"""Some key bindings for the window."""

		self.protocol("WM_DELETE_WINDOW", self.on_closing)


	def on_closing(self):
		"""App resolves issues before closing the app."""

		if hasattr(self, "player_controller"):
			self.player_controller.player_client.client.close()
		if hasattr(self, "server"):
			self.server.client.close()
		self.destroy()



if __name__ == "__main__":

	app = App()
	app.mainloop()