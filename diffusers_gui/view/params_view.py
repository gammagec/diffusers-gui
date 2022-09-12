from tkinter import WORD, LEFT, Frame, scrolledtext, Checkbutton
from tkinter import LEFT, END, DISABLED, NORMAL, W, E

from ..common import (
	bind_enabled_to_value_observer, bind_scrolledtext_to_stringvar,
	bind_enabled_to_intvar
)

from .widgets import (
	Composite, LoadFileView, Label, TextBox, 
	Button, ScrolledText
)

from .layout import grid_layout_options, GridLayout

class ParamsView(Composite):
	name = 'params_view'

	def __init__(self, view_model):
		super().__init__(GridLayout())
		self.view_model = view_model

	def create(self, parent):
		super().create(parent)
		row = 0		
		self.add_child(Label(var = "Params",
			layout_options = grid_layout_options(row = row, column = 0)))
		row += 1
		
		self.add_child(Label(var = "Prompt:", 
			layout_options = grid_layout_options(
				row = row, column = 0, columnspan = 3, sticky = W
			)))			
		row += 1

		self.add_child(ScrolledText(self.view_model.prompt,
			layout_options = grid_layout_options(row = row, column = 0, columnspan = 3)))		
		row += 1

		#self.add_child(Button('Load Init Image', 
		#	lambda: self.view_model.load_init_image_clicked.next(),
		#	layout_options = grid_layout_options(row = row, column = 0, columnspan = 2)))
		#row += 1

		#self.add_child(Button('Load Mask Image',
		#	lambda: self.view_model.load_mask_image_clicked.next(),
		#	layout_options = grid_layout_options(row = row, column = 0, columnspan = 2)))		
		#row += 1
		
		self.add_child(Label(var = 'Strength:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))			
		self.add_child(TextBox(var = self.view_model.strength,
			layout_options = grid_layout_options(row = row, column = 1)))		
		row += 1

		self.add_child(Label(var = "Seed:",
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))		
		self.add_child(TextBox(var = self.view_model.seed,
			layout_options = grid_layout_options(row = row, column = 1)))					
		row += 1

		self.add_child(Label(var = 'DDIM Steps:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))		
		self.add_child(TextBox(var = self.view_model.ddim_steps,
			layout_options = grid_layout_options(row = row, column = 1)))		
		row += 1

		self.add_child(Label(var = '# Samples:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))		
		self.add_child(TextBox(var = self.view_model.n_samples,
			layout_options = grid_layout_options(row = row, column = 1)))		
		row += 1

		self.add_child(Label(var = '# Iterations:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))		
		self.add_child(TextBox(var = self.view_model.n_iter,
			layout_options = grid_layout_options(row = row, column = 1)))		
		row += 1

		self.add_child(Label(var = 'Width:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))		
		self.add_child(TextBox(var = self.view_model.width,
			layout_options = grid_layout_options(row = row, column = 1)))						
		row += 1

		self.add_child(Label(var = 'Height:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))
		self.add_child(TextBox(var = self.view_model.height,
			layout_options = grid_layout_options(row = row, column = 1)))						
		row += 1

		self.add_child(Label(var = 'Channels:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))		
		self.add_child(TextBox(var = self.view_model.channels,
			layout_options = grid_layout_options(row = row, column = 1)))		
		row += 1

		self.add_child(Label(var = 'Downsampling:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))		
		self.add_child(TextBox(var = self.view_model.downsampling,
			layout_options = grid_layout_options(row = row, column = 1)))		
		row += 1

		self.add_child(Label(var = 'Scale:',
			layout_options = grid_layout_options(row = row, column = 0, sticky = E)))		
		self.add_child(TextBox(var = self.view_model.scale,
			layout_options = grid_layout_options(row = row, column = 1)))		
		row += 1	

		self.add_child(Button(var = 'Run', 
			handler = lambda: self.view_model.run_clicked.next(),
			enabled_value = self.view_model.run_enabled,
			layout_options = grid_layout_options(row = row, column = 0)))

		self.add_child(Button(var = 'Run Random Seed', 
			handler = lambda: self.view_model.run_random_clicked.next(),
			enabled_value = self.view_model.run_enabled,
			layout_options = grid_layout_options(row = row, column = 1)))

		
	
