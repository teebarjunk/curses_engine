import view
from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT
last = -1

#def update():
	#global last
	
def was(key):
	key = ord(key) if isinstance(key, str) else key
	return last == key

def get_arrows():
	return (
		get_axis(KEY_UP, KEY_DOWN),
		get_axis(KEY_LEFT, KEY_RIGHT)
	)

def get_up_down():
	return get_axis(KEY_UP, KEY_DOWN)

def get_left_right():
	return get_axis(KEY_LEFT, KEY_RIGHT)

# Returns -1, 0, or 1 depending on if direction keys are pressed.
def get_axis(pos, neg):
	pos = ord(pos) if isinstance(pos, str) else pos
	neg = ord(neg) if isinstance(neg, str) else neg
	return -1 if last == pos else 1 if last == neg else 0
