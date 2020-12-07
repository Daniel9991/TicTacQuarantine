import socket
import time
import threading
import random



class Server():

	
	def __init__(self, ip_address, port):

		self.ip_address = ip_address
		self.port = port
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates the server client
		self.client.bind((self.ip_address, self.port))
		self.client.listen() #Makes the server listen for incoming stuff

		self.player_clients = []
		self.player_names = []


	def accept_players(self):
		"""Accepts two players, and saves their names and addresses, and creates a thread to listen to each one."""

		while len(self.player_clients) < 2:

			client, address = self.client.accept() #Players connect and information is saved.
			print(f"Joined {client} with {address}")
			time.sleep(0.5)
			self.send_message(client, "NAME")
			name = client.recv(1024).decode("ascii")
			self.player_clients.append(client)
			self.player_names.append(name)
			print(f"Server accepted player {name}")

		#Starts two threads to listen to each player's individual messages.
		threading.Thread(target=self.listen_for_messages, args=(self.player_clients[0], self.player_clients[1])).start()
		threading.Thread(target=self.listen_for_messages, args=(self.player_clients[1], self.player_clients[0])).start()

		self.setup_game()


	def setup_game(self):
		"""Decides which player will begin and sends each player the 'CREATE rival_name order' message"""

		first = random.choice(self.player_clients)
		second = self.player_clients[1] if first == self.player_clients[0] else self.player_clients[0]

		first_name = self.player_names[self.player_clients.index(first)]
		second_name = self.player_names[self.player_clients.index(second)]

		try:
			self.send_message(first, f"CREATE {second_name} first")
		except Exception as e:
			print(f"Couldn't send create message to {first_name}")
			first.close()
			self.player_clients.remove(first)
			raise e

		try:
			self.send_message(second, f"CREATE {first_name} second")
		except Exception as e:
			print(f"Couldn't send create message to {second_name}")
			second.close()
			self.player_clients.remove(second)
			raise e


	def send_message(self, client, message):
		"""Handles sending a message to a client"""

		if bytes != type(message):
			message = message.encode("ascii")

		try:
			client.send(message)
		except Exception as e:
			print(f"Couldn't send message {message.decode('ascii')} to {client}")
			client.close()
			print(e)

	
	def listen_for_messages(self, client, other_client):

		while True:

			try:
				message = client.recv(1024)
			except Exception as e:
				print("Something went wrong when receiving message from a client. Client was removed.")
				client.close()
				self.player_clients.remove(client)
				print(e)
				break

			message = message.decode("ascii")

			if message == "CLOSING": #Player is leaving the game
				self.client.close()
				self.send_message(other_client, message)

			elif message[:7] == "RESTART": #Player restarted game. Send both the 'CREATE rival_name order' message
				self.setup_game()

			elif message[:6] == "PLAYED": #Player played. Send both the 'PLAYED cell_index' message
				self.send_message(client, message)
				self.send_message(other_client, message)

			else:
				pass
			


class PlayerClient:


	def __init__(self, ip_address, port, calling_method):
		"""Create the player client that will connect to the server client and allow communication.
		The ip address and port that it gets is from the server. Calling_method is a method form PlayerFrame
		classs that will be called whenever a new message comes in."""

		self.ip_address = ip_address
		self.port = port
		self.calling_method = calling_method

		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		

	def listen_to_incoming_messages(self):
		"""This method runs on a separate thread and will be listening for any message that the server client sends,
		then calls the calling_method passing such message as an argument."""
		
		while True:
			try:
				message = self.client.recv(1024).decode("ascii")
				self.calling_method(message)
			except Exception:
				self.client.close()
				break


	def connect_to_server(self):
		"""Connects to the server on the given ip address and port."""

		try:
			self.client.connect((self.ip_address, self.port))
			threading.Thread(target=self.listen_to_incoming_messages).start()
		except Exception as e:
			self.client.close()
			raise e


	def send_message(self, message):
		"""Sends the message to the server."""

		try: 
			if bytes != type(message):
				message = message.encode("ascii")
		except Exception as e:
			raise e

		try:
			self.client.send(message)
		except Exception as e:
			self.client.close()
			raise e