import random 
import math

def get_free_tile(world_map, char):
	x,y = 0, 0
	while world_map[x][y] != " ":
	    x = random.randint(0, len(world_map) - 1)
	    y = random.randint(0, len(world_map[0]) - 1)
	world_map[x][y] = char
	return x,y,world_map

def distance(rect1, rect2):
	r1c = rect1.center
	r2c = rect2.center
	return math.sqrt((r1c[0] - r2c[0])**2 + (r1c[1] - r2c[1])**2)
