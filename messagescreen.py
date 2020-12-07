import tkinter as tk



class MessageScreen(tk.Frame):


	def __init__(self, *args, **kwargs):
		"""This is a Text widget that will inform the user of everything that happens in the game."""

		super().__init__(*args, **kwargs)

		self.text_area = tk.Text(self, bg="white", fg="black")
		self.text_area.configure(height=12, width=40, state="disabled")
		self.scroll_bar = tk.Scrollbar(self, orient="vertical", command=self.scroll_text)
		self.text_area.configure(yscrollcommand=self.scroll_bar.set)

		self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
		self.text_area.pack(side=tk.RIGHT)


	def scroll_text(self, *args):
		"""Handles scrollbar behavior."""

		self.text_area.yview_moveto(args[1])


	def write(self, message):

		self.text_area.configure(state="normal")
		self.text_area.insert(1.0, f"\n    {message}\n")
		self.text_area.configure(state="disabled")