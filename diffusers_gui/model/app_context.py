from . import (
	SessionsModel, Config, SelectionModel, RunsModel, ImagesModel, ImageModel,
	RunModel, InputImageModel, ParamsModel, MaskImageModel, SelectedImageModel
)

from ..services.message_service import MessageService
from ..services.diffusers_service import DiffusersService

class AppContext:	
	name = 'app_context'

	def __init__(self):
		self.config = Config()
		self.message_service = MessageService()
		self.diffusers_service = DiffusersService()
		self.selection_model = SelectionModel(self)
		self.sessions_model = SessionsModel(self)	
		self.runs_model = RunsModel(self)	
		self.run_model = RunModel(self)		
		self.images_model = ImagesModel(self)		
		self.input_image_model = InputImageModel(self)	
		self.image_model = SelectedImageModel(self)			
		self.mask_image_model = MaskImageModel(self)
		self.params_model = ParamsModel(self)		