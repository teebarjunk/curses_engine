
def call_str(lines):
	for line in lines.split("\n"):
		if line.strip():
			eval(line)

# Main loop.
import game, keys, view
game.set_scene("map")

import nodes_gui
menu = nodes_gui.Menu([
{"text": "New Game"},
{"text": "Load"},
{"text": "Quit"}
])
menu.yx = (5, 5)
game.scene.add_child(menu)

def run():
	view.init()
	
	# Q to quit.
	while keys.last != ord('q'):
		keys.last = view.stdscr.getch()
		
		# P to screenshot.
		if keys.was("p"):
			view.screenshot()
		
		view.update()
		
		game.update()
		
		#stdscr.addch(20,25,last_key)
		#stdscr.addstr(0, 0, str(view_yx))
		view.draw_local((0, 0), str(view.tick))
		view.draw_local((1, 0), str(keys.last))
		#tick += 1
		#stdscr.refresh()
	
	view.terminate()

run()