import os, cv2
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet
from PIL import Image
import numpy as np
from gfpgan import GFPGANer

class RealEsrganService():

	def __init__(self):
		self.upsampler = None


	def initialize(self):
		if self.upsampler == None:
			#model_name = 'RealESRGAN_x4plus'
			model = RRDBNet(num_in_ch = 3, num_out_ch = 3, num_feat = 64,
				num_block = 23, num_grow_ch = 32, scale = 4)
			model_path = os.path.join(
				'src/realesrgan/experiments/pretrained_models/RealESRGAN_x4plus.pth')
			# get from here
			# https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth
			# or here?
			# https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth
			self.upsampler = RealESRGANer(
				scale = 4,
				model_path = model_path,
				model = model,
				tile = 0,
				tile_pad = 10,
				pre_pad = 0,
				half = True,
				gpu_id = None 
			)
			self.face_enhancer = GFPGANer(
				model_path = 'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth',
				upscale = 4,
				arch='clean',
				channel_multiplier = 2,
				bg_upsampler = self.upsampler)

	def process(self, input):
		if not self.upsampler:
			self.initialize()
		img = np.asarray(input) 
		img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
		#if len(img.shape) == 3 and img.shape[2] == 4:
		#   img_mode = 'RGBA'
		#else:
		#   img_mode = None

		#output, _ =  self.upsampler.enhance(img, outscale = 4)
		_, _, output = self.face_enhancer.enhance(
			img, has_aligned=False, only_center_face=False, paste_back=True)
		return Image.fromarray(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
