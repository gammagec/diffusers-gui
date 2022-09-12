from tkinter import Canvas as TkCanvas, NW
from PIL import ImageTk

from . import View

class Canvas(View):

	def __init__(self, image, width, height, mouse_handler = None):
		super().__init__()
		image.subscribe(lambda val: self.update_image(val))
		self.tk_image = None
		self.width = width
		self.height = height
		self.mouse_handler = mouse_handler

	def update_image(self, val):
		if self.is_created():
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
		if self.mouse_handler:
			self.canvas.bind('<Button-1>', lambda evt: self.mouse_handler.down(evt.x, evt.y))
			self.canvas.bind('<B1-Motion>', lambda evt: self.mouse_handler.drag(evt.x, evt.y))

	def get_frame(self):
		return self.canvas

	def clear(self):
		if self.is_created():
			self.canvas.delete('all')

	def render(self, image):
		if self.is_created():
			self.canvas.create_image(0, 0, anchor = NW, image = image)