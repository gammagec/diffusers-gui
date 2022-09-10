class Map:
	def __init__(self, func):
		self.func = func

	def map(self, val):
		ret = self.func(val)
		print(f'mapping {val} to {ret}')
		return ret