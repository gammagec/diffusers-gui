import gc
import torch
from torch import autocast
import random
import os
import yaml

from ..common.namespace import Namespace
from ..common.subject import Subject
from ..common.value_subject import ValueSubject

class ParamsModel:
	name = 'params_model'

	def __init__(self, app_context):
		self.seed = 42	
		self.ddim_steps = 50
		self.n_samples = 1
		self.n_iter = 1
		self.ddim_eta = 0
		self.prompt = 'a gorilla drinking a soda'
		self.width = 512
		self.height = 512
		self.channels = 4
		self.downsampling = 8
		self.scale = 7.5
		self.init_image = ValueSubject('init_image', None)
		self.strength = 0.3		
		self.selection_model = app_context.selection_model
		self.config = app_context.config
		self.mask = ValueSubject('mask', None)

		self.runs_model = app_context.runs_model
		self.image_model = app_context.image_model
		self.seed_changed = Subject('seed-changed')
		self.config = app_context.config
		self.diffusers_service = app_context.diffusers_service

		self.image_model.copy_seed_value.register(self, lambda: self.on_copy_seed())
		self.image_model.use_image_value.register(self, lambda: self.on_use_image())

	def on_copy_seed(self):
		img = self.selection_model.selected_image
		img = img[6:-4]
		self.seed = img
		self.seed_changed.dispatch()

	def on_use_image(self):
		path = os.path.join(self.config.out_dir)
		path = os.path.join(path, 'sessions')
		path = os.path.join(path, self.selection_model.selected_session.get_value())
		path = os.path.join(path, self.selection_model.selected_run)
		path = os.path.join(path, self.selection_model.selected_image)
		self.init_image.set_value(path)

	def set_random_seed(self):
		self.seed = random.randint(0, 4294960000)

	def after_run(self):
		self.runs_model.after_new_run()

	def on_run(self):
		gc.collect()
		torch.cuda.empty_cache()

		session = self.selection_model.selected_session.get_value()
		sample_path = os.path.join(self.config.out_dir, "sessions")
		os.makedirs(sample_path, exist_ok=True)
		session_parent = os.path.join(sample_path, f"{session}")
		run_path = os.path.join(session_parent, "0")
		n = 1
		while os.path.exists(run_path):
			run_path = os.path.join(session_parent, f"{n}")
			n += 1
		os.makedirs(run_path, exist_ok=True)
		config_path = os.path.join(run_path, "config.yaml")
		with open(config_path, 'w') as file:
			yaml.dump(Namespace(
				seed = self.seed,
				ckpt = self.config.ckpt_loc,
				config = self.config.config_file,
				ddim_steps = self.ddim_steps,
				n_samples = self.n_samples,
				n_iter = self.n_iter,
				prompt = self.prompt,
				ddim_eta = self.ddim_eta,
				height = self.height,
				width = self.width,
				channels = self.channels,
				f = self.downsampling,				
				session_name = session,
				outdir = self.config.out_dir,
				scale = self.scale,
				strength = self.strength,
				init_img = self.init_image.get_value(),
				), file)

		if self.init_image.get_value() == None:
			self.diffusers_service.run_txt2img(
				run_path, 
				self.seed, 
				self.config.ckpt_loc, 
				self.config.config_file, 
				self.ddim_steps, 
				self.n_samples,
				self.n_iter, 
				self.prompt, 
				self.ddim_eta, 
				self.height, 
				self.width, 
				self.channels, 
				self.downsampling, 
				self.scale, 
				session,
				lambda: self.after_run())
		elif self.mask.get_value() != None:
			self.diffusers_service.run_inpaint(
				run_path, 
				self.seed, 
				self.config.ckpt_loc, 
				self.config.config_file, 
				self.ddim_steps, 
				self.n_samples,
				self.n_iter, 
				self.prompt, 
				self.ddim_eta, 
				self.height, 
				self.width, 
				self.channels, 
				self.downsampling, 
				self.scale,
				self.init_image.get_value(),
				self.strength,
				self.mask.get_value(),
				session,
				lambda: self.after_run())		
		else:
			self.diffusers_service.run_img2img(
				run_path, 
				self.seed, 
				self.config.ckpt_loc, 
				self.config.config_file, 
				self.ddim_steps, 
				self.n_samples,
				self.n_iter, 
				self.prompt, 
				self.ddim_eta, 
				self.height, 
				self.width, 
				self.channels, 
				self.downsampling, 
				self.scale,
				self.init_image.get_value(),
				self.strength,
				session,
				lambda: self.after_run())		