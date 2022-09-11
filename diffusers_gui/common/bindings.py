
from tkinter import DISABLED, NORMAL, END, INSERT

def bind_enabled_to_value_observer(obj, val_obs, widget):	
	def on_enabled(enabled):
		name = widget.name if hasattr(widget, 'name') else 'unknown widget'
		print(f'val obs enabled {enabled} for widget {name}')
		widget.configure(state = NORMAL if enabled else DISABLED)	
	val_obs.subscribe(lambda enabled: on_enabled(enabled))

def bind_enabled_to_intvar(widget, var):	
	def on_enabled(var_name, index, mode):
		widget.configure(state = NORMAL if var.get() else DISABLED)
	var.trace('w', on_enabled)	

def bind_scrolledtext_to_stringvar(text, var):
	def update():
		#print(f'got update {text.get(1.0, END)}')
		var.set(text.get(1.0, END))
	text.bind('<KeyRelease>', lambda k: update())

def bind_stringvar_to_scrolled_text(text, var):
	def update():
		#print(f'got update {text.get(1.0, END)}')
		was_disabled = text.cget('state') == DISABLED
		if was_disabled:
			text.configure(state = NORMAL)
		text.delete(1.0, END)		
		val = var.get()
		if(val != None):
			text.insert(INSERT, val)				
		if was_disabled:
			text.configure(state = DISABLED)
	var.trace('w', lambda a, b, c: update())

def bind_visible_to_observer(obj, val_obs, widget, vis_options):
	def on_visible(visible):
		if visible:
			widget.pack(vis_options)
		else:
			widget.pack_forget()
	val_obs.subscribe(lambda visible: on_visible(visible))

def bind_visible_to_intvar(widget, var, vis_options):
	def on_visible(var_name, index, mode):
		if var.get():
			widget.pack(**vis_options)
		else:
			widget.pack_forget()
	var.trace('w', on_visible)

def bind_var_to_value_observer(obj, var, obs):
	def on_change(val):
		var.set(val)
	obs.subscribe(on_change)