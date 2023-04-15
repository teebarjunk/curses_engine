from nodes import Node
from common import add, sub, clamp
import keys, view

class Menu(Node):
	def __init__(self, options=[], **kwargs):
		super(Menu, self).__init__(**kwargs)
		self.options = options
		self.current = -1
	
	def update(self):
		self.current = clamp(self.current + keys.get_up_down(), 0, len(self.options)-1)
		super(Menu, self).update()
	
	def render(self, yx):
		yx = add(yx, self.yx)
		
		for i in range(len(self.options)):
			if i == self.current:
				view.draw_local(add(yx, (i, 0)), "[O] " + self.options[i]["text"])
			else:
				view.draw_local(add(yx, (i, 0)), "[ ] " + self.options[i]["text"])
		
		super(Menu, self).render(yx)