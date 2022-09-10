import os
import yaml

class Config:	
	def __init__(self):
		self.out_dir = ''
		self.embeddings = []

	def load(self, config_path):
		config_path = os.path.join(".", config_path)
		if not os.path.exists(config_path):
			print(f"No {config_path} file found")
			return
		file = open(config_path)		
		config = yaml.load(file, Loader=yaml.UnsafeLoader)					
		self.out_dir = config.out_dir		
		self.embeddings = config.embeddings
		print('loaded config')		
		print(f'out_dir: {self.out_dir}')		