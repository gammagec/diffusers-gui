class MergeMap:
	def __init__(self, subject):
		self.subject = subject

	def merge_map(self, value):
		self.subject.next(value)