from types import SimpleNamespace
import torch
from collections import OrderedDict
from torch import autocast
from diffusers import (
	StableDiffusionPipeline, StableDiffusionImg2ImgPipeline, StableDiffusionInpaintPipeline
)
from transformers import CLIPTokenizer, CLIPTextModel
import os, gc 
import PIL
from PIL import Image
import numpy as np

from diffusers.pipelines.stable_diffusion.safety_checker import StableDiffusionSafetyChecker

from ..common import Observable

def preprocess(image):
	w, h = image.size
	w, h = map(lambda x: x - x % 32, (w, h))  # resize to integer multiple of 32
	image = image.resize((w, h), resample=PIL.Image.LANCZOS)
	image = np.array(image).astype(np.float32) / 255.0
	image = image[None].transpose(0, 3, 1, 2)
	image = torch.from_numpy(image)
	return 2.0 * image - 1.0

pretrained_model_path = "stable-diffusion-v1-4"

class DummySafetyChecker(StableDiffusionSafetyChecker):
	def __init__(self):
		self._modules = OrderedDict()
		self._parameters = OrderedDict()
		self._buffers = OrderedDict()
		self._backward_hooks = OrderedDict()
		self._forward_hooks = OrderedDict()
		self._forward_pre_hooks = OrderedDict()
	def forward(self, clip_input, images):
		return images, False
	def forward_onnx(self, clip_input, images):
		return images, False

class DiffusersService:

	def __init__(self):
		self.txt2img_pipe = None
		self.img2img_pipe = None
		self.inpaint_pipe = None
		self.tokenizer = None
		self.text_encoder = None
		self.safety_checker = DummySafetyChecker()

	def create_tokenizer(self):
		self.tokenizer = CLIPTokenizer.from_pretrained(pretrained_model_path + '/tokenizer',
			revision = "fp16")
		self.text_encoder = CLIPTextModel.from_pretrained(pretrained_model_path + '/text_encoder',
			revision = "fp16")

	def load_embeddings(self, embeddings):
		if embeddings != None:
			for embedding in embeddings:
				path = embedding['file']
				new_token = embedding['token']
				if path.endswith('.pt'):
					print(f'loading embedding at {path}')
					loaded_embeds = torch.load(path, map_location="cpu")
					string_to_token = loaded_embeds['string_to_token']
					string_to_param = loaded_embeds['string_to_param']
					token = list(string_to_token.keys())[0]
			
					embeds = string_to_param[token]
					dtype = self.text_encoder.get_input_embeddings().weight.dtype
					embeds.to(dtype)

					token = new_token
					print(f'storing to token {token}')
					num_added_tokens = self.tokenizer.add_tokens(token)
					if num_added_tokens == 0:
						raise ValueError(f'tokenizer already contains the token {token}')
					self.text_encoder.resize_token_embeddings(len(self.tokenizer))
					token_id = self.tokenizer.convert_tokens_to_ids(token)
					self.text_encoder.get_input_embeddings().weight.data[token_id] = embeds
				elif path.endswith('.bin'):
					print(f'loading embedding at {path}')
					loaded_learned_embeds = torch.load(path, map_location="cpu")
					# separate token and the embeds
					trained_token = list(loaded_learned_embeds.keys())[0]
					embeds = loaded_learned_embeds[trained_token]

  					# cast to dtype of text_encoder
					dtype = self.text_encoder.get_input_embeddings().weight.dtype
					embeds.to(dtype)

					# add the token in tokenizer
					token = new_token 
					num_added_tokens = self.tokenizer.add_tokens(token)
					if num_added_tokens == 0:
						raise ValueError(f"The tokenizer already contains the token {token}. Please pass a different `token` that is not already in the tokenizer.")
  
  					# resize the token embeddings
					self.text_encoder.resize_token_embeddings(len(self.tokenizer))
  
					# get the id for the token and assign the embeds
					token_id = self.tokenizer.convert_tokens_to_ids(token)
					self.text_encoder.get_input_embeddings().weight.data[token_id] = embeds


	def run_txt2img(self, out_dir, seed, 
		ddim_steps, n_samples, n_iter, prompt, ddim_eta, H, W,
		C, f, scale, session_name, device = "cuda", precision = "autocast", embeddings = None):
		print('Run txt2img!')
		print(f'Prompt is: {prompt}')

		if self.tokenizer == None and embeddings != None and len(embeddings) > 0:
			self.create_tokenizer()
			self.load_embeddings(embeddings)
		gc.collect()
		torch.cuda.empty_cache()

		def do_txt2img():	
			if self.txt2img_pipe == None:
				if self.tokenizer != None:
					self.txt2img_pipe = StableDiffusionPipeline.from_pretrained(
						pretrained_model_path, revision="fp16", 
						torch_dtypel = torch.float16, 
						tokenizer = self.tokenizer,
						text_encoder = self.text_encoder,
						safety_checker = self.safety_checker
					)
				else:
					self.txt2img_pipe = StableDiffusionPipeline.from_pretrained(
						pretrained_model_path, revision="fp16", 
						torch_dtypel = torch.float16, 
						safety_checker = self.safety_checker
					)
			gc.collect()
			torch.cuda.empty_cache()

			generator = torch.Generator(device).manual_seed(seed)
			pipe = self.txt2img_pipe.to(device)
			pipe.enable_attention_slicing()
			with autocast(device):
				image = pipe(
					prompt, 
					generator = generator,
					height = H,
					width = W,
					eta = ddim_eta,
					num_inference_steps = ddim_steps,
					guidance_scale = f
				)["sample"][0]
				return image

		return do_txt2img()

	def run_img2img(self, out_dir, seed,
		ddim_steps, n_samples, n_iter, prompt, ddim_eta, H, W,
		C, f, scale, init_img, 
		strength, session_name, after_run, device = "cuda",  precision = "autocast",
		embeddings = None):

		print('Run img2img!')
		print(f'Prompt is: {prompt}')

		if self.tokenizer == None and embeddings != None and len(embeddings) > 0:
			self.create_tokenizer()
			self.load_embeddings(embeddings)
		gc.collect()
		torch.cuda.empty_cache()

		if self.img2img_pipe == None:
			if self.tokenizer != None:
				self.img2img_pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
					pretrained_model_path, revision="fp16", 
					torch_dtype=torch.float16, use_auth_token=False,
					tokenizer = self.tokenizer,
					text_encoder = self.text_encoder,
					safety_checker = self.safety_checker
				)
			else:
				self.img2img_pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
					pretrained_model_path, revision="fp16", 
					torch_dtype=torch.float16, use_auth_token=False,
					safety_checker = self.safety_checker
				)
		gc.collect()
		torch.cuda.empty_cache()

		init_image = init_img.convert("RGB")
		generator = torch.Generator(device).manual_seed(seed)
		pipe = self.img2img_pipe.to(device)
		pipe.enable_attention_slicing()
		with autocast(device):
			image = pipe(prompt, 
				init_image = preprocess(init_image), 
				strength = strength, 
				generator = generator)["sample"][0]

			return image

	def run_inpaint(self, out_dir, seed,
		ddim_steps, n_samples, n_iter, prompt, ddim_eta, H, W,
		C, f, scale, init_img,
		strength, mask_img, session_name, after_run, device = "cuda",  precision = "autocast",
		embeddings = None):

		print('Run inpaint!')
		print(f'Prompt is: {prompt}')

		if self.tokenizer == None and embeddings != None and len(embeddings) > 0:
			self.create_tokenizer()
			self.load_embeddings(embeddings)
		gc.collect()
		torch.cuda.empty_cache()

		if self.inpaint_pipe == None:
			if self.tokenizer != None:
				self.inpaint_pipe = StableDiffusionInpaintPipeline.from_pretrained(
					pretrained_model_path, revision="fp16", 
					torch_dtype=torch.float16, use_auth_token=False,
					tokenizer = self.tokenizer,
					text_encoder = self.text_encoder,
					safety_checker = self.safety_checker
				)
			else:
				self.inpaint_pipe = StableDiffusionInpaintPipeline.from_pretrained(
					pretrained_model_path, revision="fp16", 
					torch_dtype=torch.float16, use_auth_token=False,
					safety_checker = self.safety_checker
				)
		gc.collect()
		torch.cuda.empty_cache()

		pipe = self.inpaint_pipe.to(device)
		pipe.enable_attention_slicing()
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
			return image