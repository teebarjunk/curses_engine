import yaml

DOWN = (1, 0)
UP = (-1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

# Load data from YAML file.
def load_yaml(path):
	with open(path + ".yaml", "r") as f:
		yaml_data = yaml.safe_load(f)
	return yaml_data

def clamp(x, minn, maxx):
	return max(minn, min(maxx, x))

# Add tuple values.
def add(t0, t1):
	return (t0[0]+t1[0], t0[1]+t1[1])

# Subtract tuple values.
def sub(t0, t1):
	return (t0[0]-t1[0], t0[1]-t1[1])