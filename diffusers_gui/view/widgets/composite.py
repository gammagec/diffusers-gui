from tkinter import Frame

from . import View

class Composite(View):	
	def __init__(self, layout_manager = None, layout_options = None):
		super().__init__(layout_options)
		self.name = 'container view'
		self.children = []
		self.layout_manager = layout_manager		

	def add_child(self, child):
		self.children.append(child)	
		return self

	def create(self, parent):
		super().create()
		self.frame = Frame(parent)
		for child in self.children:
			child.create(self.frame)

	def get_frame(self):
		return self.frame

	def pack(self, **args):
		self.frame.pack(**args)

	def grid(self, **args):
		self.frame.grid(**args)

	def layout(self):
		for child in self.children:
			if not child.is_created():
				child.create(self.frame)
			if isinstance(child, Composite):
				child.layout()
		if self.layout_manager != None:
			self.layout_manager.layout(self.children)
		else:
			for child in self.children:
				if not child.is_created():
					child.create(self.frame)
				layout_options =child.get_layout_options()
				if layout_options != None:
					print(f'packing child with layout options {layout_options}')
					child.pack(**layout_options)
				else:
					child.pack()
