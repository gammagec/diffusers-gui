import gc, torch, random, os, yaml
from torch import autocast

from ..common import BehaviorSubject, Subject, Namespace

class ParamsModel:
	name = 'params_model'

	def __init__(self, app_context):
		self.seed = BehaviorSubject(42)
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
		self.strength = 0.3		
		self.selection_model = app_context.selection_model
		self.config = app_context.config
		self.runs_model = app_context.runs_model
		self.image_model = app_context.image_model		
		self.config = app_context.config
		self.diffusers_service = app_context.diffusers_service
		self.image_model.copy_seed.subscribe(lambda _: self.on_copy_seed())
		self.input_image_model = app_context.input_image_model
		self.mask_image_model = app_context.mask_image_model

	def on_copy_seed(self):
		img = self.selection_model.selected_image
		img = img[6:-4]
		self.seed.next(img)

	def set_random_seed(self):
		self.seed.next(random.randint(0, 4294960000))

	def after_run(self):
		print('doing after run')
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
				seed = self.seed.get_value(),
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
				), file)

		seed = self.seed.get_value()
		out_dir = run_path

		if self.input_image_model.image.get_value() == None:
			image = self.diffusers_service.run_txt2img(
				run_path, 
				seed,
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
				embeddings = self.config.embeddings		
			)
			base_count = len(os.listdir(out_dir))
			path = os.path.join(out_dir, f"{base_count:05}-{seed}.png")
			image.save(path)
			self.after_run()

		elif self.mask_image_model.image.get_value() != None:
			image = self.diffusers_service.run_inpaint(
				run_path, 
				self.seed.get_value(), 
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
				self.input_image_model.image.get_value(),
				self.strength,
				self.mask_image_model.mask.get_value(),
				session,
				lambda: self.after_run(),
				embeddings = self.config.embeddings		
				)		
			base_count = len(os.listdir(out_dir))
			path = os.path.join(out_dir, f"{base_count:05}-{seed}.png")
			image.save(path)
			self.after_run()
		else:
			image = self.diffusers_service.run_img2img(
				run_path, 
				self.seed.get_value(), 
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
				self.input_image_model.image.get_value(),
				self.strength,
				session,
				lambda: self.after_run(),
				embeddings = self.config.embeddings		
				)		
			base_count = len(os.listdir(out_dir))
			path = os.path.join(out_dir, f"{base_count:05}-{seed}.png")
			image.save(path)
			self.after_run()
			