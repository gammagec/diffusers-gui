from . import ImageModel

from . import ImageModel
from ..common import Subject

class ReferenceImageModel(ImageModel):

	def __init__(self, app_context):
		super().__init__(app_context)

		self.open_ref_image = Subject(lambda val: self.load_image(val))