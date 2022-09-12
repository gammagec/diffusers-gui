from PIL import Image

from .image_model import ImageModel

from ..common import BehaviorSubject, Subject

class MaskImageModel(ImageModel):
	name = 'mask_image_model'

	def __init__(self, app_context):
		super().__init__(app_context)		
		self.mask = BehaviorSubject(None)
		self.input_image_model = app_context.input_image_model
		self.open_mask_image = Subject(lambda val: self.load_image(val))
		self.clear_mask_image = Subject(lambda val: self.load_image(None))

	def load_image(self, path):
		print(f'load image for {path}')
		if (path == None):
			self.image.next(None)
			self.mask.next(None)
			return

		print(f'loading image {path}')
		mask_image = Image.open(path)
		self.mask.next(mask_image)

		init_img = self.input_image_model.image.get_value().copy()
		if (init_img == None):
			print('showing mask only')
			# if no init image, show the mask only
			self.image.next(mask_image)
			return
		mask = mask_image.convert("RGBA")	
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
		self.image.next(init_img)