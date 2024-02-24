
import tools

class World:
	def __init__(self,cam= None,chunk_size=100):
		self.chunk_size = chunk_size
		self.chunks= dict()
		self.cam = cam
	def add_element(self,element):
		num_chunk = tools.get_chunk_number(element.pos,self.chunk_size)
		if num_chunk in self.chunks:
			self.chunks[num_chunk].add_element(element)
		else:
			new_chunk = Chunk(num_chunk,element)
			self.chunks[num_chunk] = new_chunk

	def remove_element(self,element):
		num_chunk = tools.get_chunk_number(element.pos,self.chunk_size)
		if num_chunk not in self.chunks:
			raise IndexError("Chunk infound")
		else:
			self.chunks[num_chunk].remove_element(element)
	
	def move_element(self,element,old_chunk,new_chunk):
		if (old_chunk not in self.chunks):
			raise IndexError("Chunk infound")      
		else:
			self.remove_element(element,old_chunk)
			self.add_element(element,new_chunk)

	#return a list of chunk to fill with element around the position
	def get_loaded_chunks(self,pos:tuple,render_distance:int)-> set:
		output = set()
		center_x,center_y = tools.get_chunk_number(pos,self.chunk_size)
		for x in range(center_x-render_distance, center_x +render_distance+1):
			for y in range(center_y-render_distance, center_y +render_distance+1):
				if (x,y) in self.chunks:
					output.add(self.chunks[(x,y)])
		return output
	
	def get_chunks_around(self,num_chunk,size=1):
		output = set()
		center_x,center_y =num_chunk
		for x in range(center_x-size, center_x +size+1):
			for y in range(center_y-size, center_y +size+1):
				if (x,y) in self.chunks:
					output.add(self.chunks[(x,y)])
		return output
	
	def get_chunk_number(self,pos:tuple)->tuple:
		x, y = pos
		chunk_x = int(x // self.chunk_size)
		chunk_y = int(y // self.chunk_size)
		return (chunk_x, chunk_y)		

class Chunk:
	def __init__(self,num,element=None):
		self.num = num
		self.elements= set()
		if element != None:
			self.add_element(element)

	def add_element(self,element):
		self.elements.add(element)


	def remove_element(self,element):
		self.elements.remove(element)

	def get_all_elements(self):
		return self.elements
	