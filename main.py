from world import *
from camera import Camera_Mouse
from render import start


import tree

FPS = 60
RENDER_DISTANCE=100
STOP = 9 #num for the  key TAB
chunk_size = 300
#map.add_element(self,self.num_chunk)

if __name__ =="__main__":
    cam = Camera_Mouse((-500,-500),1)
    world = World(cam,chunk_size)

    p = tree.Point((0,0),10,(255,0,0))
    p2 = tree.Point((0,100),10,(0,250,0))
    p3 = tree.Point((100,0),10,(0,0,255))

    b1 = tree.Branch(p,p2,10)
    t1 = tree.Tree(-90,(0,0),None,20)

    world.add_element(t1)
    start(world)