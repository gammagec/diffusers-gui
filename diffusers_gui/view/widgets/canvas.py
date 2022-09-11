from tkinter import Canvas as TkCanvas, NW
from PIL import ImageTk

from . import View

class Canvas(View):

	def __init__(self, image, width, height):
		super().__init__()
		image.subscribe(lambda val: self.update_image(val))
		self.tk_image = None
		self.width = width
		self.height = height

	def update_image(self, val):
		if val != None:
			self.tk_image = ImageTk.PhotoImage(val)
			self.render(self.tk_image)
		else:
			self.tk_image = None		
			self.clear()

	def create(self, parent):
		super().create()
		self.canvas = TkCanvas(parent, width = self.width, height = self.height)
		if self.tk_image:
			self.render(self.tk_image)

	def get_frame(self):
		return self.canvas

	def clear(self):
		self.canvas.delete('all')

	def render(self, image):
		self.canvas.create_image(0, 0, anchor = NW, image = image)