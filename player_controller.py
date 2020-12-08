from dataclasses import make_dataclass
import socket
import threading
from networking import PlayerClient



Cell = make_dataclass("Cell", ("index", "token"))



class PlayerController:

	def __init__(self, player_model, player_frame):

		self.player_model = player_model
		self.player_frame = player_frame
		self.player_frame.controller = self

		#These are the cell combination where each cell would be involved in for a victory.
		self.cell_combinations = {
			0: ((0,1,2), (0,3,6), (0,4,8)),
			1: ((0,1,2), (1,4,7)),
			2: ((0,1,2), (2,5,8), (6,4,2)),
			3: ((0,3,6), (3,4,5)),
			4: ((3,4,5), (1,4,7), (0,4,8), (6,4,2)),
			5: ((3,4,5), (2,5,8)),
			6: ((0,3,6), (6,7,8), (6,4,2)),
			7: ((6,7,8), (1,4,7)),
			8: ((6,7,8), (0,4,8), (2,5,8)),
		}

		self.possible_messages = {
			"NAME": None,
			"CREATE": None,
			"PLAYED": None,
			"CLOSING": None
		}

		self.create_client()


	def create_client(self):

		try:
			self.player_client = PlayerClient(self.player_model.ip_address, self.player_model.port, self.react_to_messages)
			self.player_client.connect_to_server()
		except Exception as e:
			self.player_frame.display_connection_error(e, (self.player_model.ip_address, self.player_model.port))
		else:
			self.player_frame.display_connection_accepted((self.player_model.ip_address, self.player_model.port))


	def react_to_messages(self, message):

		if message == "NAME": #Server is requesting player's name
			self.received_NAME()

		elif message[:6] == "CREATE": #Server instructs to create a new game
			self.received_CREATE(message)

		elif message[:6] == "PLAYED":
			self.received_PLAYED(message)

		elif message == "CLOSING":
			self.received_CLOSING()

		else:
			pass


	def check_for_win(self, index):
		"""Checks if last move is a winning move."""

		possible_comb = self.cell_combinations[index]

		for comb in possible_comb:

			tokens = []
			tokens.append(self.player_model.grid[comb[0]].token)
			tokens.append(self.player_model.grid[comb[1]].token)
			tokens.append(self.player_model.grid[comb[2]].token)

			if all([token == self.player_model.current_player.token for token in tokens]):

				return True

		return False

	
	def check_for_tie(self):
		"""Checks if there is any available cell."""

		if len(self.player_model.available_cells) > 0:
			return False
		else:
			return True


	def create_game(self):
		"""Gives player frame instructions to create the game."""

		self.player_model.grid = []
		self.player_model.available_cells = []

		for i in range(9):
			c = Cell(i, None)
			self.player_model.grid.append(c)
			self.player_model.available_cells.append(c)

		self.player_frame.setup_game(self.player_model.current_player.name)


	def play(self):
		"""Sets app for the player to make a move."""

		self.player_model.current_player = self.player_model.player
		self.player_frame.prepare_to_play(self.player_model.available_cells)


	def wait_to_play(self):
		"""Sets the app for the player to wait its turn."""

		self.player_model.current_player = self.player_model.rival_player
		self.player_frame.prepare_to_wait_turn(self.player_model.rival_player.name, self.player_model.available_cells)


	def received_NAME(self, message=None):
		"""Called when server asks NAME"""

		self.player_client.send_message(self.player_model.player.name)


	def received_CREATE(self, message):
		"""Called when server says to CREATE"""

		_, rival_name, order = message.split(' ')

		player_token = "X" if order == "first" else "O"
		rival_token = "O" if order == "first" else "X"

		self.player_model.player.token = player_token

		#Initializing rival player
		self.player_model.rival_player.name = rival_name
		self.player_model.rival_player.token = rival_token
		self.player_model.current_player = self.player_model.player if order == "first" else self.player_model.rival_player

		self.create_game()

		if order == "first":
			self.play()

		else:
			self.wait_to_play()

		self.player_frame.message_screen.write(f"New game against {rival_name}")
		self.player_frame.message_screen.write(f"You go {order}")


	def received_PLAYED(self, message):
		"""Called when client receives a PLAYED message."""

		_, index = message.split(' ')
		index = int(index)

		played_cell = self.player_model.grid[index]
		self.player_model.available_cells.remove(played_cell)
		played_cell.token = self.player_model.current_player.token

		self.player_frame.player_played(index, self.player_model.current_player.token)

		won = self.check_for_win(index)

		if won:

			if self.player_model.current_player == self.player_model.player:
				header = "Congratulations"
				message = "You won!"
			else:
				header = "Game Over"
				message = "You lost"

			self.player_frame.game_over(header, message, self.player_model.available_cells)
			self.player_frame.message_screen.write(message)
			
		else:
			tied = self.check_for_tie()

			if tied:
				header = "Tied Game"
				message = "At least you didn't lose"
				self.player_frame.game_over(header, message, [])
				self.player_frame.message_screen.write("You tied the game")
			else:
				if self.player_model.player == self.player_model.current_player:
					self.wait_to_play()
				else:
					self.play()


	def received_CLOSING(self):
		"""Called when received CLOSING message"""

		self.player_frame.notify_rival_closing()
		self.player_frame.master.go_to_previous_screen(False)