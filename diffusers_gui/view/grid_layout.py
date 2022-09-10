class GridLayout:

	def layout(self, children):
		for child in children:
			layout_options = child.get_layout_options()
			if layout_options:
				child.grid(**layout_options)		
			else:
				child.grid()