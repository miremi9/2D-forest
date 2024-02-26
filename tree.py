import pygame
import math
import time
from random import randint,random,choice,shuffle,choices

from tools import Vector
import tools
from tools_tree import *

import world

AUTO = -1

def minus_cam(pos,cam_pos):
	return pos[0]-cam_pos[0],pos[1]-cam_pos[1] 
def average(a,b):
	c = list()
	for i ,x in enumerate(a):
		c.append((x+b[i])/2)
	return c


class Element:
	def __init__(self,pos:tuple,size:tuple):
		self.size = size
		self.pos = pos

	def update(self,world,event_key,dt,chunks_around):
		return {}

	def draw(self,center,mid,scale=1):
		if scale ==1:
			return self.surface,(Vector(self.rect_surface.topleft)-center+mid)
		else:
			temp_size = Vector(self.size)*scale
			temp_surface = pygame.transform.scale(self.surface, temp_size)
			temp_pos = (Vector(self.rect_surface.topleft)-center)*scale+mid

			return temp_surface,temp_pos

		
class Point(Element):
	def __init__(self,pos:tuple,diametre=1,color=(255,255,255)):
		super().__init__(pos,(diametre,diametre))
		self.color = color
		self.x = pos[0]
		self.y = pos[1]
	
	def draw(self,fenetre,color,pos_cam,scale):
		pos = self.get_relative_pos(pos_cam,scale)
		size = self.size[0]
		size *=scale
		pygame.draw.circle(fenetre,self.color,pos,int(size/2))
	
	def get_relative_pos(self,pos_cam,scale):
		pos = Vector(self.pos)
		pos -= pos_cam
		pos *=scale
		return pos



class Branch(Element):
	def __init__(self,point1:Point,point2:Point,width:int=1):
		self.p1 = point1
		self.p2 = point2
		#angle
		self.width = width/2
		self.pos = self.get_mid()
		self.color = average(point1.color,point2.color)

	def draw(self,fenetre,color,pos_cam,scale):
		pp1 = self.p1.get_relative_pos(pos_cam,scale)
		pp2 = self.p2.get_relative_pos(pos_cam,scale)
		size = int(self.width*scale)
		self.color = average(self.p1.color,self.p2.color)
		pygame.draw.line(fenetre,self.color,pp1,pp2,size)

	def get_mid(self):
		return average(self.p1.pos,self.p2.pos)
	
	def get_angle(self):
		x1, y1 = self.p1.pos
		x2, y2 = self.p2.pos
		angle_radians = math.atan2(y2 - y1, x2 - x1)

		return math.degrees(angle_radians)



	
class Tree:
	liste = set()
	world = world.World(None,150)
	def __init__(self,angle:tuple,pos:tuple,root=None,size:int=100,time2live:int=10,
			  scope:int=70,color:tuple=(130,130,130),absolute_scope:tuple=(20,-200),tick:float=1,
			  mini_radius:float=15,chance_of_branch:float=1,chance_of_leave:float=0.5):
		
		

		Tree.liste.add(self)
		self.root = root
		self.tick = tick
		self.time2live = time2live	
		self.timelived = 0
		self.scope = scope
		self.growing = True
		self.absolute_scope = absolute_scope
		if not is_point_in_scope(angle,absolute_scope):
			self.growing = False
		
		self.chance_of_branch = chance_of_branch
		self.chance_of_leave = chance_of_leave
		self.pos = pos
		

		self.angle = angle
		self.size = size
		self.points = set()
		self.branchs= set()
		self.trees = set()
		self.leaves = set()
		self.nb_branch = 2


		if max(color) > 255 or min(color) < 0 or len(color) != 3:
			raise ValueError(f"color {color} must be a tuple of 3 float beetween 0 and 255")


		p1 = Point(self.pos,1,color)
		self.head = p1
		self.points.update({p1})
		self.last_up = time.time()
		self.color = color


		self.augmente_head(self.angle)

	def get_seed(self):
		if self.root ==None:
			return self.pos
		else:
			return self.root.get_seed()

	def update(self,world,keys:list,dt:float,chunks_around:list):
		for tree in self.trees:
			tree.update(world,keys,dt,chunks_around)
		
		if time.time()-self.last_up > self.tick and self.growing:
			self.grow()
			self.last_up = time.time()
		return set()
	
	def grow(self):
		self.timelived +=1
		if self.time2live <=self.timelived :
			self.dying()
			return

		if random.random()<self.chance_of_branch and len(self.branchs) >0:	#create branch new tree
			self.grow_branch()

		self.augmente_head()

	def grow_branch(self):
		li = [x for x in [int(self.angle-self.scope/2),int(self.angle+self.scope/2)] if is_point_in_scope(x,self.absolute_scope) ]
		shuffle(li)
		for a in li[:self.nb_branch]:
			color = self.get_variation_color()
			tick = self.get_variation_tick()
			time2live = self.get_varation_time2live()
			scope = self.get_varation_scope()
			t1 = Tree(a,self.head.pos,self,self.size,time2live,scope,color,self.absolute_scope,tick,mini_radius=AUTO)
			self.trees.add(t1)


	def augmente_head(self,angle= None):

		if not angle:
			min_angle = int(self.angle-self.scope/2)
			max_angle = int(self.angle+self.scope/2)
			angle = randint(min_angle,max_angle)

		new_pos = tools.Vector(self.head.pos) +tools.create_vector_angle(self.size,angle)

		new_point = Point(new_pos,1,self.color)

		new_branch = Branch(new_point,self.head,10)

		if self.is_branch_collid(new_branch):
			self.dying()
			return 

		self.points.add(new_point)
		self.branchs.add(new_branch)
		Tree.world.add_element(new_branch)

		
		if random.random() < self.chance_of_leave and self.root!=None:
			self.grow_sub_tree(new_branch)
			#self.grow_leaves(new_branch)
		self.head = new_point
	

	def grow_leaves(self,branch:Branch):
		mid = branch.get_mid()
		angle = self.angle+choice([-45,45])
		distance = self.size/2
		new_pos = tools.Vector(mid)+ tools.create_vector_angle(distance,angle)
		leave = Leave(mid,self,new_pos,self.head.color)
		self.leaves.add(leave)

	def grow_sub_tree(self,branch:Branch):

		color = self.get_variation_color()
		tick = self.get_variation_tick()
		time2live = self.get_varation_time2live()
		scope = self.get_varation_scope()
		scale = self.get_varation_scale()
		mid = branch.get_mid()
		nb_sub = 2
		for rel_angle in choices([-45,45],k=nb_sub):
			angle = self.angle+rel_angle
			distance = self.size/2	
			
			t1 = Tree(angle,mid,self,self.size*scale,time2live,scope,color,self.absolute_scope,tick,AUTO,self.chance_of_branch,self.chance_of_leave)
			self.trees.add(t1)


	def is_branch_collid(self,branch,visited=None):
		num_chunk = Tree.world.get_chunk_number(branch.pos)
		chunks = Tree.world.get_chunks_around(num_chunk)
		for chunk in chunks:
			if any(branch_intersect(branch,x) for x in chunk.get_all_elements()):
				return True
			
		return False

		
	def draw(self,*args):
		for branch in self.branchs:
			branch.draw(*args)
		for tree in self.trees:
			tree.draw(*args)
		for leave in self.leaves:
			leave.draw(*args)
		for leave in self.points:
			leave.draw(*args)


	def dying(self):
		self.growing = False
		for point in self.points:
			#point.color = (255,0,0)
			pass



	def get_variation_color(self):
		return generate_color(self.color,variation=10)
	
	def get_variation_tick(self):
		return self.tick
		return 0.1+10/self.size
	
	def get_varation_time2live(self):
		if tools.distance(self.get_seed(),self.head.pos) > 1000:
			return 0
		else:
			return 10
		return self.time2live/1.2
	
	def get_varation_scope(self):
		return self.scope
	
	def get_varation_scale(self):
		return 0.5

class Leave:
	def __init__(self,origine:tuple,root:Tree,center:tuple,color:tuple=(255,255,255)) -> None:
		self.p_origine = Point(origine,1,color)
		self.p_center = Point(center,30,color)
		self.branche = Branch(self.p_center,self.p_origine,10)
	def draw(self,*args):
		self.branche.draw(*args)
		self.p_center.draw(*args)