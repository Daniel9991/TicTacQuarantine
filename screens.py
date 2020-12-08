import tkinter as tk
import tkinter.messagebox as msgbox
from styles import BACKGROUND_SCREEN, BACKGROUND_BUTTON, FOREGROUND_BUTTON, FOREGROUND_LABEL
import socket
import random



class InitialScreen(tk.Frame):


	def __init__(self, master, **kwargs):
		"""Creates the initial frame where player has two buttons to decide whether to create or join a game.
		A lambda funtion is used so that we can pass arguments into the called function or method."""

		super().__init__(master, **kwargs)
		self.configure(bg=BACKGROUND_SCREEN)

		#This button indicates that user will create a game and then join it
		self.create_button = tk.Button(self, text="Create game", command=lambda: self.master.pack_info_gathering_screen('create'))
		self.create_button.configure(bg=BACKGROUND_BUTTON, fg=FOREGROUND_BUTTON)
		self.create_button.pack(pady=(20,5), padx=(40,40))

		#This button indicates that the player will join an existing game
		self.join_button = tk.Button(self, text="Join game", command=lambda: self.master.pack_info_gathering_screen('join'))
		self.join_button.configure(bg=BACKGROUND_BUTTON, fg=FOREGROUND_BUTTON)
		self.join_button.pack(pady=(5,20))





class InfoGatheringScreen(tk.Frame):


	def __init__(self, master, mode, **kwargs):
		"""In this screen player has the entry widgets to provide info such as name, ip_address, and port. Depending
		on the mode, the prompt to enter the ip_address and the port will vary."""

		super().__init__(master, **kwargs)
		self.mode = mode
		self.configure(bg=BACKGROUND_SCREEN)

		if mode == 'create': #Player chose to create a game

			ip_address_prompt = "Input your device ip address"
			port_prompt = "Input the port to listen"

		elif mode == 'join': #Player chose to join a game

			ip_address_prompt = "Input the server's ip address"
			port_prompt = "Input the server's listening port"

		self.name_frame = tk.Frame(self, bg=BACKGROUND_SCREEN)
		self.prompt_name_label = tk.Label(self.name_frame, text="Input your name:", bg=BACKGROUND_SCREEN, fg=FOREGROUND_LABEL)
		self.prompt_name_label.pack()
		self.name_entry = tk.Entry(self.name_frame)
		#self.name_entry.insert(0, "Player1")
		self.name_entry.pack(pady=(5,0))

		self.ip_frame = tk.Frame(self, bg=BACKGROUND_SCREEN)
		self.prompt_ip_address_label = tk.Label(self.ip_frame, text=ip_address_prompt, bg=BACKGROUND_SCREEN, fg=FOREGROUND_LABEL)
		self.prompt_ip_address_label.pack()
		self.ip_address_entry = tk.Entry(self.ip_frame)
		#self.ip_address_entry.insert(0, "127.0.0.1")
		self.ip_address_entry.pack(pady=(5,0))

		self.port_frame= tk.Frame(self, bg=BACKGROUND_SCREEN)
		self.prompt_port_label = tk.Label(self.port_frame, text=port_prompt, bg=BACKGROUND_SCREEN, fg=FOREGROUND_LABEL)
		self.prompt_port_label.pack()
		self.port_entry = tk.Entry(self.port_frame)
		#self.port_entry.insert(0, "50002")
		#self.port_entry.focus()
		self.port_entry.pack(pady=(5,0))

		self.name_frame.pack(pady=(20,0))
		self.ip_frame.pack(pady=(20,0))
		self.port_frame.pack(pady=(20,0))

		self.done_button = tk.Button(self, text="Done", command=self.gather_info, bg=BACKGROUND_BUTTON, fg=FOREGROUND_BUTTON)
		self.done_button.pack(pady=(20,30))

		self.port_entry.bind("<Return>", lambda event: self.gather_info())


	def gather_info(self):
		"""Gets info from entries in self.gathering_info_frame and returns it. Port is converted to int so that it can 
		be used later. Might add some input validation, and make sure all entries are filled."""

		name = self.name_entry.get()
		ip_address = self.ip_address_entry.get()
		port = self.port_entry.get()

		if len(name) > 0 and len(ip_address) > 0 and len(port) > 0:
			if port.isdigit() and 50000 < int(port) < 60000:
				command = self.master.create_game if self.mode == 'create' else self.master.join_game
				command(name, ip_address, int(port), self.mode)
			else:
				msgbox.showerror("Error", "Port must be an integer between 50000 and 60000.")
		else:
			msgbox.showerror("Error", "You must fill all three fields.")



class IpWindow(tk.Toplevel):


	def __init__(self, master, **kwargs):

		super().__init__(master, **kwargs)
		self.withdraw()

		info = """
  Hey user!
  This app uses sockets to connect devices.

  If both players are using the same PC, then
  put 127.0.0.1 as your ip address.

  If you are playing across devices, you both need
  to be connected in the same LAN network
  and you don't, then you can use the button below
  to know your ip address. 
  
  If it says 127.0.0.1 then try letting your friend
  create the game. The problem might be that you
  created the hotspot, and since your device is not
  connected to a new network, so it won't display a
  public ip address.
	 
  Also you try using a port between 50000 and 60000,
  just to make sure it doesn't conflict with any
  other app.

  You can use random port button below to get a
  random port that most likely will be safe to use.
			"""

		self.text_area = tk.Text(self, width=53, height=25)
		self.text_area.insert(1.0, info)
		self.text_area.configure(state="disabled", bg=BACKGROUND_SCREEN, fg=FOREGROUND_BUTTON, font=(None, 11))
		self.text_area.pack()

		self.buttons_frame = tk.Frame(self, bg=BACKGROUND_SCREEN)

		self.ipaddress_button = tk.Button(self.buttons_frame, text="My ip address", command=self.get_ipaddress)
		self.ipaddress_button.configure(bg=BACKGROUND_BUTTON, fg=FOREGROUND_BUTTON)
		self.ipaddress_button.pack(pady=(10,10), side=tk.TOP)

		self.random_port_button = tk.Button(self.buttons_frame, text="Random port", command=self.get_random_port)
		self.random_port_button.configure(bg=BACKGROUND_BUTTON, fg=FOREGROUND_BUTTON)
		self.random_port_button.pack(pady=(0,10), side=tk.BOTTOM)

		self.buttons_frame.pack(fill=tk.X)

		self.bind_keys()


	def get_ipaddress(self):
		"""Gets user ipaddres thorugh socket.gethostbyname"""

		ip_address = socket.gethostbyname(socket.gethostname())

		self.ipaddress_label = tk.Label(self.buttons_frame, text=f"Your ip address: {ip_address}")
		self.ipaddress_label.configure(bg=BACKGROUND_SCREEN, fg=FOREGROUND_LABEL)
		self.ipaddress_label.pack(side=tk.TOP, pady=(10,10))
		self.ipaddress_button.pack_forget()

	
	def get_random_port(self):
		"""Gets a random port."""

		random_port = f"Random port: {random.randint(50000, 59999)}"

		self.random_port_label = tk.Label(self.buttons_frame, text=random_port)
		self.random_port_label.configure(bg=BACKGROUND_SCREEN, fg=FOREGROUND_LABEL)
		self.random_port_label.pack(side=tk.BOTTOM, pady=(0,10))
		self.random_port_button.pack_forget()


	def do_nothing(self):
		"""Self-descriptive."""
		pass


	def on_closing(self):
		"""Called when window is closed."""

		self.withdraw()


	def bind_keys(self):
		"""Some key bindings for the window."""

		self.protocol("WM_DELETE_WINDOW", self.on_closing)