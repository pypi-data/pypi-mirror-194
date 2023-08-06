# -*- coding: utf-8 -*-
"""Ceruleanbot GUI
~~~~~~~~~~~~~~~~~~~~~"""

import tkinter as tk
from tkinter import ttk
#import sv_ttk

if __name__ == "__main__":
	from core import diff
else:
	from .core import diff


'''window = tk.Tk()

window.title('LightWikibot')
window.geometry("640x400")'''
#window.resizable(False, False)


class Textarea:
	def __init__(self, window):
		self.root = tk.Text(window)
		self.pack = self.root.pack

	def get_text(self) -> str:
		print(self.root.get(1.0, "end"))
		return self.root.get(1.0, "end")


class SubmitDialog(tk.Tk):
	def __init__(self, title: str = ""):
		tk.Tk.__init__(self)
		if title != "":
			self.title('text input')
		self.geometry("640x400")

		self.entry = Textarea(self)
		self.entry.pack(side="left")

		#ttk.Style(window).theme_use()
		#sv_ttk.set_theme("light")

		self.button = ttk.Button(self, command=self.entry.get_text, text="")
		self.button.pack(side="right")


dialog = SubmitDialog()

dialog.mainloop()
