from . import operate, create_operator_subscriber

def map(project):
	index = 0
	def do_operate(source, subscriber):
		global index
		index = 0
		def next_and_inc(val):		
			global index	
			subscriber.next(project(val, index))
			index += 1
		source.subscribe(create_operator_subscriber(subscriber, next_and_inc))
	return operate(do_operate)
