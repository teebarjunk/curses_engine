import curses
import keys
from common import add, sub

REFRESH_RATE = 500
MAX_WIDTH = 64
MAX_HEIGHT = 32
WIPE_CHAR = " " # If this is set, it will wipe the screen with this char. (Slightly slow.)

tick = 0
stdscr = None
yx = (0, 0)
size = (MAX_HEIGHT, MAX_WIDTH)

def init():
	global stdscr
	stdscr = curses.initscr()
	stdscr.timeout(REFRESH_RATE)
	curses.noecho()
	curses.cbreak()
	curses.start_color()
	curses.use_default_colors()
	for i in range(0, curses.COLORS):
		curses.init_pair(i + 1, i, -1)
	stdscr.keypad(True)

def update():
	global yx, size, tick
	
	yx = add(yx, keys.get_arrows())
	
	max_y, max_x = stdscr.getmaxyx()
	size = min(MAX_HEIGHT, max_y-2), min(MAX_WIDTH, max_x-2)
	
	# Wipe the screen?
	if WIPE_CHAR:
		for y in range(size[0]):
			for x in range(size[1]):
				stdscr.addstr(y, x, WIPE_CHAR)
	
	tick += 1

def is_inside(yx):
	y, x = yx
	h, w = size
	return y >= 0 and x >= 0 and y < h and x < w
	#return 0 < yx[0] > size[0] and 0 < yx[1] > size[1]
	#return size[0] < yx[0] >= 0 and size[1] < yx[1] >= 0

def draw(dyx, st, clr=-1):
	dyx = sub(dyx, yx)
	if is_inside(dyx):
		clr = curses.color_pair(clr) if clr != -1 else 0
		y, x = dyx
		stdscr.addstr(y, x, st, clr)

def draw_local(dyx, st, clr=-1):
	if is_inside(dyx):
		clr = curses.color_pair(clr) if clr != -1 else 0
		y, x = dyx
		stdscr.addstr(y, x, st, clr)
	
def terminate():
	curses.nocbreak()
	stdscr.keypad(False)
	curses.echo()
	curses.endwin()
