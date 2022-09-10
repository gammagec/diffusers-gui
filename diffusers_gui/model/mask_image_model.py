from PIL import Image
import numpy as np

from .image_model import ImageModel

from ..common.subject import Subject

class MaskImageModel(ImageModel):
	name = 'mask_image_model'

	def __init__(self, app_context):
		super().__init__(app_context)		
		self.params_model = app_context.params_model
		self.params_model.mask.register(self, lambda val: self.load_image())		

	def get_processed_image(self, image):

		selected_img = self.params_model.init_image.get_value()
		if (selected_img == None):
			print('showing mask only')
			# if no init image, show the mask only
			return image
		init_img = Image.open(selected_img)
		mask = image.convert("RGBA")	
		datas = mask.getdata()

		newData = []
		for item in datas:
			if item[0] < 100 and item[1] < 100 and item[2] < 100:
				# black
				newData.append((0, 0, 0, 0))
			else:				
				newData.append((255, 255, 255, 128))

		mask.putdata(newData)
		
		init_img.paste(mask, (0, 0), mask)
		#return Image.composite(init_img, mask.convert('L'), mask.convert('L'))
		return init_img

	def get_image_path(self):
		return self.params_model.mask.get_value()