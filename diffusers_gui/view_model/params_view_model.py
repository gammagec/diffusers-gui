from tkinter import StringVar, IntVar
from tkinter import filedialog

from ..common import (
	EqualsObserver, NotObserver, AndObserver, bind_var_to_value_observer,
	ValueSubject, Subject
)

class ParamsViewModel(object):

	def __init__(self, model, app_context):
		self.model = model

		self.seed = ValueSubject(model.seed.get_value())
		self.ddim_steps = ValueSubject('')
		self.n_samples = ValueSubject('')
		self.n_iter = ValueSubject('')
		self.width = ValueSubject('')
		self.height = ValueSubject('')
		self.channels = ValueSubject('')
		self.downsampling = ValueSubject('')
		self.scale = ValueSubject('')		
		self.mask = ValueSubject('')
		self.strength = ValueSubject('')
		self.prompt = StringVar()

		self.load_init_image_clicked = Subject(lambda val: self.on_load_init_image())

		self.run_enabled = NotObserver(
			EqualsObserver(app_context.selection_model.selected_session, None))

		model.seed.subscribe(lambda val: self.seed.set_value(val))				
		self.mask.subscribe(lambda val: self.update_mask_to_model())

		self.update_from_model()

	def on_load_init_image(self):
		result = filedialog.askopenfilename(
				filetypes = [("PNG", "*.png"), ("Jpg", "*.jpg"), ("Jpeg", "*.jpeg")])
		self.model.open_init_image(result)

	def update_mask_to_model(self):
		val = self.mask.get_value()
		self.model.mask.set_value(val if val != '' else None)
	
	def run_clicked(self):
		self.run()

	def run_random_clicked(self):
		self.set_random_seed()
		self.run()

	def run(self):			
		self.params_to_model()
		self.model.on_run()

	def set_random_seed(self):
		self.model.set_random_seed()
		self.seed.set_value(str(self.model.seed.get_value()))

	def params_to_model(self):
		self.model.seed.set_value(int(self.seed.get_value()))
		self.model.ddim_steps = int(self.ddim_steps.get_value())
		self.model.n_samples = int(self.n_samples.get_value())
		self.model.n_iter = int(self.n_iter.get_value())
		self.model.ddim_eta = 0
		self.model.prompt = self.prompt.get()
		self.model.width = int(self.width.get_value())
		self.model.height = int(self.height.get_value())
		self.model.channels = int(self.channels.get_value())
		self.model.downsampling = int(self.downsampling.get_value())
		self.model.scale = float(self.scale.get_value())		
		mask = self.mask.get_value()
		self.model.mask.set_value(mask if mask != '' else None)
		self.model.strength = float(self.strength.get_value())

	def update_from_model(self):
		self.seed.set_value(str(self.model.seed.get_value()))
		self.ddim_steps.set_value(str(self.model.ddim_steps))		
		self.n_samples.set_value(str(self.model.n_samples))
		self.n_iter.set_value(str(self.model.n_iter))
		self.width.set_value(str(self.model.width))
		self.height.set_value(str(self.model.height))		
		self.channels.set_value(str(self.model.channels))
		self.downsampling.set_value(str(self.model.downsampling))
		self.scale.set_value(str(self.model.scale))				
		self.strength.set_value(str(self.model.strength))					