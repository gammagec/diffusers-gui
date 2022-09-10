from tkinter import Canvas, NW

from . import View

class CanvasView(View):

	def __init__(self, width, height):
		super().__init__()
		self.width = width
		self.height = height

	def create(self, parent):
		super().create()
		self.canvas = Canvas(parent, width = self.width, height = self.height)

	def get_frame(self):
		return self.canvas

	def clear(self):
		self.canvas.delete('all')

	def render(self, image):
		self.canvas.create_image(0, 0, anchor = NW, image = image)