from tkinter import LEFT

class RowLayout:
	def layout(self, children):
		for child in children:
			child.pack(side = LEFT)		