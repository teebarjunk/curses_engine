from nodes import SceneNode

scene = None

def set_scene(name):
	global scene
	scene = SceneNode("map")

def update():
	scene.update()
	scene.render((0, 0))