
def call_str(lines):
	for line in lines.split("\n"):
		if line.strip():
			eval(line)

# Main loop.
import game, keys, view
game.set_scene("map")

def run():
	view.init()
	
	while keys.last != ord('q'):
		keys.last = view.stdscr.getch()
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