"""This is tic tac toe to play across devices. One player has to create a game (create a client server
to listen to messages from own device and the other device) and the other one joins the game. Both players
must know the ip address and the listening port of the client server to connect to it."""



import tkinter as tk



class App(tk.Tk):

	def __init__(self):
		"""Create the app."""

		super().__init__()

		self.title("TicTacStayOverThere")

		self.pack_initial_frame() #Calling method to setup the initial screen


	def pack_initial_frame(self):
		"""Creates the initial frame where player has two buttons to decide whether to create or join a game."""

		self.first_frame = tk.Frame(self)

		#This button indicates that user will create a game and then join it
		self.create_button = tk.Button(self.first_frame, text="Create game", command=lambda: self.pack_info_gathering_frame('create'))
		self.create_button.pack()

		#This button indicates that the player will join an existing game
		self.join_button = tk.Button(self.first_frame, text="Join game", command=lambda: self.pack_info_gathering_frame('join'))
		self.join_button.pack()

		self.first_frame.pack()


	def pack_info_gathering_frame(self, mode):
		"""In this screen player has the entry widgets to provide info such as name, ip_address, and port. Depending
		on the mode, the prompt to enter the ip_address and the port will vary."""

		pass


	def create_game(self):
		"""Player must create game, that is, a server client is created and it is set to listen for players in a new thread,
		so that current flow can create player instance and connect to server."""

		pass


	def join_game(self, name, ip_address, port):
		"""Player connects to the server client, sends name over and creates the frame."""

		pass


if __name__ == "__main__":

	app = App()
	app.mainloop()