import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from diffusers import StableDiffusionImg2ImgPipeline
from diffusers import StableDiffusionInpaintPipeline
import os
import PIL
from PIL import Image
import numpy as np

from ..common import Observable

def preprocess(image):
	w, h = image.size
	w, h = map(lambda x: x - x % 32, (w, h))  # resize to integer multiple of 32
	image = image.resize((w, h), resample=PIL.Image.LANCZOS)
	image = np.array(image).astype(np.float32) / 255.0
	image = image[None].transpose(0, 3, 1, 2)
	image = torch.from_numpy(image)
	return 2.0 * image - 1.0

class DiffusersService:

	def __init__(self):
		self.txt2img_pipe = None
		self.img2img_pipe = None
		self.inpaint_pipe = None

	def run_txt2img(self, out_dir, seed, 
		ddim_steps, n_samples, n_iter, prompt, ddim_eta, H, W,
		C, f, scale, session_name, device = "cuda", precision = "autocast"):
		print('Run txt2img!')

		def do_txt2img():	
			if self.txt2img_pipe == None:
				self.txt2img_pipe = StableDiffusionPipeline.from_pretrained(
					"stable-diffusion-v1-4", revision="fp16", 
					torch_dtype=torch.float16, use_auth_token=False)

			generator = torch.Generator(device).manual_seed(seed)
			pipe = self.txt2img_pipe.to(device)
			with autocast(device):
				image = pipe(prompt, generator = generator)["sample"][0]

			base_count = len(os.listdir(out_dir))
			path = os.path.join(out_dir, f"{base_count:05}-{seed}.png")
			image.save(path)

		return Observable(lambda _: do_txt2img())


	def run_img2img(self, out_dir, seed,
		ddim_steps, n_samples, n_iter, prompt, ddim_eta, H, W,
		C, f, scale, init_img, 
		strength, session_name, after_run, device = "cuda",  precision = "autocast"):
		print('Run img2img!')

		if self.img2img_pipe == None:
			self.img2img_pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
			"stable-diffusion-v1-4", revision="fp16", 
			torch_dtype=torch.float16, use_auth_token=False)
		init_image = init_img.convert("RGB")
		generator = torch.Generator(device).manual_seed(seed)
		pipe = self.img2img_pipe.to(device)
		with autocast(device):
			image = pipe(prompt, 
				init_image = preprocess(init_image), 
				strength = strength, 
				generator = generator)["sample"][0]

		base_count = len(os.listdir(out_dir))
		path = os.path.join(out_dir, f"{base_count:05}-{seed}.png")
		image.save(path)
		after_run()

	def run_inpaint(self, out_dir, seed,
		ddim_steps, n_samples, n_iter, prompt, ddim_eta, H, W,
		C, f, scale, init_img,
		strength, mask_img, session_name, after_run, device = "cuda",  precision = "autocast"):
		print('Run inpaint!')
		print(f'Prompt is: {prompt}')

		if self.inpaint_pipe == None:
			self.inpaint_pipe = StableDiffusionInpaintPipeline.from_pretrained(
			"stable-diffusion-v1-4", revision="fp16", 
			torch_dtype=torch.float16, use_auth_token=False)

		pipe = self.inpaint_pipe.to(device)
		with autocast(device):
			init_img = init_img.convert("RGB")
			generator = torch.Generator(device).manual_seed(seed)
			image = pipe(
				prompt = prompt, 
				init_image = init_img, 
				mask_image = mask_img, 
				generator = generator,
				guidance_scale = 7.5,
				strength = strength)["sample"][0]		

		base_count = len(os.listdir(out_dir))
		path = os.path.join(out_dir, f"{base_count:05}-{seed}.png")
		image.save(path)
		after_run()