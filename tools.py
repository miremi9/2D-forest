import math
import pygame
import random

def distance(x,y):
	s = 0
	for i in range(len(x)):
		s += math.pow(x[i]-y[i],2)
	return math.sqrt(s)

def get_chunk_number(pos:tuple,chunk_size)->tuple:
	x, y = pos
	chunk_x = int(x // chunk_size)
	chunk_y = int(y // chunk_size)
	return (chunk_x, chunk_y)

def get_elements_from_chunks(chunks:set)->set:
	out = set()
	for chunk in chunks:
		out.update(chunk.elements)
	return out

def get_solide_elements_from_chunks(chunks:set)->set:
	out = set()
	for chunk in chunks:
		out.update(chunk.elements_solide)
	return out

def get_vecteur(pos1: tuple, pos2: tuple, lenght=1.0) -> tuple:
	# Calcul des composantes du vecteur
	delta_x = pos2[0] - pos1[0]
	delta_y = pos2[1] - pos1[1]

	# Calcul de la norme du vecteur
	norm = math.sqrt(delta_x ** 2 + delta_y ** 2)

	# Calcul des composantes du vecteur normalisé
	if norm != 0:
		normalized_x = delta_x / norm
		normalized_y = delta_y / norm
	else:
		normalized_x = 0
		normalized_y = 0
		
	result_x = normalized_x * lenght
	result_y = normalized_y * lenght

	return (result_x, result_y)

def get_clique(event_key):
	for event in event_key:
		if event.type==pygame.MOUSEBUTTONDOWN:

			if event.button==1:
				return event.pos


def addtuple(*tuples):
	n = len(tuples[0])
	out = [0 for _ in range(n)]
	for tu in tuples:
		for i,num in enumerate(tu):
			out[i] +=num
	return out
def is_iterable(obj):
	try:
		iter(obj)
		return True
	except TypeError:
		return False
	

def get_ig_pos(pos_mouse,cam,mid):

	pos = (Vector(pos_mouse)-cam.get_pos())*cam.scale+mid
	return pos





class Vector(tuple):
	def __add__(self,other):
		if is_iterable(other):
			return Vector((x+y for x,y in zip(self,other)))
		else:
			return Vector((x+other for x in self))
	def __sub__(self,other):
		if is_iterable(other):
			return Vector((x-y for x,y in zip(self,other)))
		else:
			return Vector((x-other for x in self))        
	def __mul__(self, value):
		return Vector((x*value for x in self))
	def __truediv__(self, value):
		return Vector((x/value for x in self))
	def __neg__(self):
		return Vector((-x for x in self))
	def __abs__(self):
		return Vector((abs(x) for x in self))
	def __iadd__(self, other):
		if is_iterable(other):
			return Vector((x+y for x,y in zip(self,other)))
		else:
			return Vector((x+other for x in self))
	def __isub__(self, other):
		return Vector((x-y for x,y in zip(self,other)))
	def __imul__(self,value):
		return Vector((x*value for x in self))
	

def create_vector_angle(size, angle_degrees):
	angle_radians = math.radians(angle_degrees)
	x = size * math.cos(angle_radians)
	y = size * math.sin(angle_radians)
	return Vector((x,y))

def generate_color(color,variation):
	n_color = list()
	for k in color:
		x = (k+random.randint(-1,1)*variation)%256
		n_color.append(x)
	return n_color
#input x , lim lim tuple of 2 float, output : x if x in lim right border else:
#exemple = -1 , (0,10) -> 0
# 1 , (0,10) -> 1
def is_point_in_set(pos,lim):
		if pos< min(lim):
			return False
		elif pos > max(lim):
			return False
		return True
		
	