def has_lift(source):
	return hasattr(source, 'lift') and callable(source.lift)

def operate(init):

	def do_lift(sub, src):
		return init(src, sub)

	def fun(src):
		if has_lift(src):
			return src.lift(do_lift)
		else:
			raise Exception(f'Unable to lift unknown Observable type {src}') 	
	return fun
