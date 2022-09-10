class Tap:
	def __init__(self, callback):
		self.callback = callback

	def tap(self, val):
		self.callback(val)