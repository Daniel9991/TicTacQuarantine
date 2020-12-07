from dataclasses import make_dataclass

Player = make_dataclass("Player", ("name", "token"))



class PlayerModel:

	def __init__(self, name, ip_address, port, mode):

		self.player = Player(name, None)
		self.rival_player = Player(None, None)
		self.ip_address = ip_address
		self.port = port
		self.mode = mode
		self.current_player = None
		self.grid = []
		self.available_cells = []