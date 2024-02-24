import pygame
from tools import Vector
import tools
import math
import time

from random import randint,random,choice,shuffle

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
		self.pos = point1.pos
		self.color = average(point1.color,point2.color)

	def draw(self,fenetre,color,pos_cam,scale):
		pp1 = self.p1.get_relative_pos(pos_cam,scale)
		pp2 = self.p2.get_relative_pos(pos_cam,scale)
		size = int(self.width*scale)
		self.color = average(self.p1.color,self.p2.color)
		pygame.draw.line(fenetre,self.color,pp1,pp2,size)

	pass

class Leave:
	pass

class Tree:
	liste = set()
	def __init__(self,angle:tuple,pos,root=None,size=100,time2live=10,scope=70,color=(130,130,130),absolute_scope=(20,-200),tick=1,tolerance=15,chance_of_branch=1):
		Tree.liste.add(self)
		self.root = root
		self.tick = tick
		self.time2live = time2live	
		self.timelived = 0
		self.scope = scope
		self.growing = True
		self.absolute_scope = absolute_scope
		if not tools.is_point_in_set(angle,absolute_scope):
			self.growing = False
		self.tolerance = tolerance
		self.chance_of_branch = chance_of_branch
		self.pos = pos
		

		self.angle = angle
		self.size = size
		self.points = set()
		self.branchs= set()
		self.trees = set()
		self.intermediate = 5


		p1 = Point(self.pos,1,color)
		self.head = p1
		self.points.update({p1})
		self.last_up = time.time()
		self.color = color


		self.augmente_head()

	def get_rects(self,scale:int=1):
		pass

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

		li = [x for x in [int(self.angle-self.scope/2),int(self.angle+self.scope/2)] if tools.is_point_in_set(x,self.absolute_scope) ]
		if random()<self.chance_of_branch and len(self.branchs) !=0:	#create branch new tree
			shuffle(li)
			for a in li:
				color = self.get_variation_color()
				tick = self.get_variation_tick()
				time2live = self.get_varation_time2live()
				scope = self.get_varation_scope()
				t1 = Tree(a,self.head.pos,self,time2live,scope,color,self.absolute_scope,tick,self.tolerance)
				self.trees.add(t1)


		min_angle = int(self.angle-self.scope/2)
		max_angle = int(self.angle+self.scope/2)
		self.augmente_head(randint(min_angle,max_angle))




	def augmente_head(self,angle=None):
		if not angle:
			angle = self.angle

		new_pos = tools.Vector(self.head.pos) +tools.create_vector_angle(self.size,angle)



		if  self.point_collid(new_pos):
			self.dying()
			return 
		
		#create intermediate point for avoid collision on the line
		for k in range(1,self.intermediate):
			inter_pos = tools.Vector(self.head.pos) +tools.create_vector_angle(k*self.size/self.intermediate+1,angle)
			if self.point_collid(inter_pos):
				self.dying()
				return
			else:
				self.points.add(Point(inter_pos))

		
		#-------------------
		if self.point_collid(new_pos):
			self.dying()
			return 
		p1 = Point(new_pos,1,self.color)
		
		new_branch = Branch(p1,self.head,10)

		self.points.add(p1)
		self.branchs.add(new_branch)

		self.head = p1
	
	def point_collid(self,pos,visited=None):
		if visited ==None:
			visited = set()
		visited.add(self)
		
		if any(tools.distance(x.pos, pos) < self.tolerance for x in self.points):

			return True
		for tree in self.trees:
			if tree in visited:			#AVOID INFINIT RECCURTION
				continue
			if tree.point_collid(pos,visited):
				return True
		if self.root and self.root not in visited:
			if self.root.point_collid(pos,visited):
				return True
		return False
		
	def draw(self,*args):
		for branch in self.branchs:
			branch.draw(*args)
		for tree in self.trees:
			tree.draw(*args)


	def dying(self):
		self.growing = False
		for point in self.points:
			#point.color = (255,0,0)
			pass



	def get_variation_color(self):
		return tools.generate_color(self.color,variation=10)
	
	def get_variation_tick(self):
		return self.tick*(0.5+random())
	
	def get_varation_time2live(self):
		return self.time2live/1.2
	
	def get_varation_scope(self):
		return self.scope
	