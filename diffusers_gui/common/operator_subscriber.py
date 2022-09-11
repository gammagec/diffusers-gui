from . import Subscriber

def create_operator_subscriber(
		destination, on_next, on_complete = None, on_error = None, on_finalize = None):
	return OperatorSubscriber(destination, on_next, on_complete, on_error, on_finalize)

class OperatorSubscriber(Subscriber):

	def __init__(self, destination, on_next, on_complete, on_error, on_finalize):
		super().__init__(destination)
		self.next_ = on_next
		self.error_ = on_error
		self.complete_ = on_complete
		self.finalize_ = on_finalize

	def unsubscribe():
		super().unsubscribe()