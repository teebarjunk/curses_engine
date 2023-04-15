from common import add, sub, load_yaml, LEFT, RIGHT, UP, DOWN
import game, keys, view

class Node(object):
	def __init__(self, name="", **kwargs):
		self.yx = (0, 0)
		self.name = name
		self.children = {}
		self.set_properties(**kwargs)
		self.active = True
		self.visible = True
		
	def get_child(self, name):
		if name in self.children:
			return self.children[name]
		return None
	
	def get_descendant(self, name):
		d = self.get_child(name)
		if d:
			return d
		
		for child in self.children.values():
			d = child.get_descendant(name)
			if d:
				return d
		
		return None
	
	def add_child(self, node):
		self.children[node.name] = node
		return node
	
	def remove_child(self, node):
		del self.children[node.name]
		return node
	
	def update(self):
		for child in self.children.values():
			if child.active:
				child.update()
	
	def render(self, yx):
		yx = add(yx, self.yx)
		for child in self.children.values():
			if child.visible:
				child.render(yx)
	
	def set_properties(self, **kwargs):
		for k, v in kwargs.items():
			setattr(self, k, v)

class SymbolNode(Node):
	def __init__(self, **kwargs):
		super(SymbolNode, self).__init__(**kwargs)
		self.symbol = "@"
		self.color = 6
	
	def render(self, yx):
		view.draw(add(self.yx, yx), self.symbol, self.color)
		# Render children on top.
		super(SymbolNode, self).render(yx)
		
class TilesNode(Node):
	def __init__(self, **kwargs):
		super(TilesNode, self).__init__(**kwargs)
		self.tiles = {}
		self.tile_info = {}
		self.tile_info["#"] = { "name": "Wall", "block": True }
		self.bounds = (0, 0, 0, 0)
	
	def is_empty(self, yx):
		if yx in self.tiles:
			tile = self.tiles[yx]
			if tile in self.tile_info:
				if "block" in self.tile_info[tile]:
					return False
		return True
	
	def render(self, yx):
		# Draw map tiles.
		for y in range(view.size[0]):
			for x in range(view.size[1]):
				tile_yx = add(yx, (y,x))
				if tile_yx in self.tiles:
					view.draw(tile_yx, self.tiles[tile_yx])
		
		# Render children on top.
		super(TilesNode, self).render(yx)
	
	def update_bounds(self):
		if len(self.tiles) == 0:
			return (0, 0, 0, 0)
		
		min_x, min_y, max_x, max_y = 9999, 9999, -9999, -9999
		for y,x in self.tiles:
			min_y = min(y, min_y)
			min_x = min(x, min_x)
			max_y = max(y, max_y)
			max_x = max(x, max_x)
		self.bounds = min_x, min_y, max_x, max_y

class PlayerNode(SymbolNode):
	def __init__(self, **kwargs):
		super(PlayerNode, self).__init__(**kwargs)
		self.direction = (0, 0)
	
	def update(self):
		direction = (
			keys.get_axis("w", "s"),
			keys.get_axis("a", "d"))
		
		if direction != (0, 0):
			if direction == self.direction:
				next_pos = add(self.yx, direction)
				if not game.scene.get_collider(next_pos):
					self.yx = next_pos
			
			self.direction = direction
	
	def render(self, yx):
		super(PlayerNode, self).render(yx)
		
		# Direction arrow.
		py, px = self.yx
		dy, dx = self.direction
		if view.tick % 2 == 0:
			arr = "-"
			if self.direction == DOWN: arr = "v"
			elif self.direction == UP: arr = "^"
			elif self.direction == RIGHT: arr = ">"
			elif self.direction == LEFT: arr = "<"
			view.draw(add(add(yx, self.yx), self.direction), arr)
		
		# Determine what is being looked at.
		#msg = ""
		#looking_at = get_at(py+dy, px+dx)
		#if looking_at["type"] == "tile":
			#msg = "[" + str(looking_at["tile"]["name"]) + "]"
		#elif looking_at["type"] == "object":
			#msg = "[" + str(looking_at["object"]["name"]) + "]"
		
		## Draw message at bottom of screen.
		#width, height = view_size
		#extra = (width - len(msg)) // 2
		#msg = " "*extra + msg + " "*extra
		#stdscr.addstr(height, 0, msg)
		
class SceneNode(TilesNode):
	def __init__(self, scene, **kwargs):
		super(SceneNode, self).__init__(**kwargs)
		
		self.colliders = {}
		
		data = load_yaml(scene)
		objs = data["objects"]
		
		# Parse map to tiles and objects.
		rows = data["tiles"].split("\n")
		for y in range(len(rows)):
			cols = rows[y]
			obj_ids = []
			
			# Extract object ids between <>
			if "<" in cols:
				cols, obj_ids = cols.rsplit("<", 1)
				obj_ids = [x.split(":") for x in obj_ids.split(">", 1)[0].strip().split(" ")]
			
			for x in range(len(cols)):
				was_obj_id = False
				for i in range(len(obj_ids)):
					symbol, obj_id = obj_ids[i]
					if cols[x] == symbol:
						node = SymbolNode()
						node.name = obj_id
						node.yx = (y, x)
						node.symbol = cols[x]
						node.set_properties(**objs[obj_id])
						self.add_child(node)
						del obj_ids[i]
						was_obj_id = True
						break
				if was_obj_id:
					continue
				
				if cols[x] == "@":
					player = self.get_child("player")
					if not player:
						player = self.add_child(PlayerNode())
					player.yx = (y, x)
				else:
					if cols[x] == "#":
						self.colliders[(y, x)] = True
					
					self.tiles[(y, x)] = cols[x]
		
		self.update_bounds()
	
	def get_collider(self, yx):
		if yx in self.colliders:
			return self.colliders[yx]
		return False