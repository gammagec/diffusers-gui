from . import (
	MergeMap, Subscription, Observable, EMPTY_SUBSCRIPTION,
	SubscriptionLike
)

class Subject(Observable, SubscriptionLike):
	def __init__(self, initial_subscribe = None, name = 'Unknown Subject'):	
		super().__init__(self.subscribe_)
		self.name = name		
		self.closed = False
		self.observers = []
		self.is_stopped = False
		self.has_error = False
		if (initial_subscribe != None):
			self.subscribe(initial_subscribe)

	def on_new_subscribe(self, callback):
		pass

	def subscribe_(self, subscriber):		
		if self.is_stopped:
			return EMPTY_SUBSCRIPTION
		self.observers.append(subscriber)					
		def remove_subscription(self, subscriber):
			self.observers.remove(subscriber)
		return Subscription(lambda: remove_observer)	

	def next(self, val = None):		
		if not self.is_stopped and self.observers != None:
			for observer in self.observers:	
				observer.next(val)

	def error(self, err):
		pass

	def complete(self):
		pass

	def unsubscribe(self):
		self.is_stopped = self.closed = True
		self.observers = None
