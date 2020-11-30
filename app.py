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
		"""Creates the initial frame where player has two buttons to decide whether to create or join a game.
		A lambda funtion is used so that we can pass arguments into the called function or method."""

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

		if mode == 'create': #Player chose to create a game

			ip_address_prompt = "Input your device ip address"
			port_prompt = "Input the port to listen"

		elif mode == 'join': #Player chose to join a gama

			ip_address_prompt = "Input the server's ip address"
			port_prompt = "Input the server's listening port"

		else:

			print("What just happened?")

		self.gather_info_frame = tk.Frame(self)

		self.prompt_name_label = tk.Label(self.gather_info_frame, text="Input your name:")
		self.prompt_name_label.pack()
		self.name_entry = tk.Entry(self.gather_info_frame)
		self.name_entry.pack()

		self.prompt_ip_address_label = tk.Label(self.gather_info_frame, text=ip_address_prompt)
		self.prompt_ip_address_label.pack()
		self.ip_address_entry = tk.Entry(self.gather_info_frame)
		self.ip_address_entry.pack()

		self.prompt_port_label = tk.Label(self.gather_info_frame, text=port_prompt)
		self.prompt_port_label.pack()
		self.port_entry = tk.Entry(self.gather_info_frame)
		self.port_entry.pack()

		#Depending on what the user chose to do, the creating or joining method will be called.
		command = self.create_game if mode == 'create' else self.join_game

		self.done_button = tk.Button(self.gather_info_frame, text="Done", command=command)
		self.done_button.pack()

		self.first_frame.pack_forget()
		self.gather_info_frame.pack()


	def create_game(self):
		"""Player must create game, that is, a server client is created and it is set to listen for players in a new thread,
		so that current flow can create player instance and connect to server."""

		pass


	def join_game(self, name, ip_address, port):
		"""Player connects to the server client, sends name over and creates the frame."""

		pass


	def gather_info(self):
		"""Gets info from entries in self.gathering_info_frame and returns it. Port is converted to int so that it can 
		be used later. Might add some input validation, and make sure all entries are filled."""

		name = self.name_entry.get()
		ip_address = self.ip_address_entry.get()
		port = int(self.port_entry.get())

		return name, ip_address, port


if __name__ == "__main__":

	app = App()
	app.mainloop()