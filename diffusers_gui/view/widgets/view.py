from tkinter import Tk, Frame

class View(object):	
	def __init__(self, layout_options = None):		
		self.name = 'view'
		self.created = False
		self.layout_options = layout_options

	def create(self):
		if self.created: return
		self.created = True

	def is_created(self):
		return self.created

	def after_create(self):
		pass

	def get_frame(self):
		return None

	def pack(self, **args):
		self.get_frame().pack(**args)

	def grid(self, **args):
		self.get_frame().grid(**args)

	def get_layout_options(self):
		return self.layout_options
