from PIL import Image, ImageDraw

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
		self.input_image_model.image.subscribe(lambda val: self.render_mask())
		self.mask_fill = (255, 255, 255, 255)

	def paint_mask_at(self, x, y):
		print(f'painting mask at {x} {y}')
		radius = 10
		draw = ImageDraw.Draw(self.mask.get_value())
		dx = x - radius - 7
		dy = y - radius - 7
		draw.ellipse((dx, dy, x + radius * 2, y + radius * 2), fill = self.mask_fill)
		self.render_mask()

	def set_erase(self):
		self.mask_fill = (255, 255, 255, 255)
	
	def set_restore(self):
		self.mask_fill = (0, 0, 0, 255)

	def reset_mask_image(self):
		self.mask.next(Image.new("RGBA", (512, 512), (0, 0, 0, 255)))
		self.render_mask()

	def render_mask(self):
		print('rendering mask')
		if self.mask == None:
			return
		init_img = self.input_image_model.image.get_value()
		if (init_img == None):
			print('showing mask only')
			# if no init image, show the mask only
			self.image.next(self.mask.get_value())
			return
		init_img = init_img.copy()
		mask = self.mask.get_value().copy()
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

	def load_image(self, path):
		print(f'load image for {path}')
		if (path == None):
			self.image.next(None)
			self.mask.next(None)
			return

		print(f'loading image {path}')
		mask_image = Image.open(path).convert("RGBA")

		self.mask.next(mask_image)
		self.render_mask()
