from pygame.locals import *
LEFT = K_q
UP = K_z
DOWN = K_s
RIGHT = K_d
ACTION = K_e


class Camera:
    def __init__(self,pos,scale):
        self.pos= pos
        self.scale = scale

    def get_pos(self):
        return self.pos
    
    def update(self,*arg):
        pass

class Camera_Mouse(Camera):
    def __init__(self,pos,scale):
        super().__init__(pos,scale)    
        self.draging = False
        self.pos_mouse = 0,0

    def update(self,event_list):
        for event in event_list:
            if event.type == MOUSEMOTION:
                self.pos_mouse = event.pos

            if event.type==MOUSEBUTTONDOWN:
                if event.button==5:
                    self.scale /=1.1

                if event.button==4:
                    self.scale *=1.1
                if event.button==1:
                    self.draging = True
                    self.start_drag = event.pos
            if event.type==MOUSEBUTTONUP:
                if event.button==1:
                    self.draging = False
                    dt_pos = self.start_drag[0]-self.pos_mouse[0],self.start_drag[1]-self.pos_mouse[1]
                    self.pos =  self.pos[0]+dt_pos[0],self.pos[1]+dt_pos[1]

    def get_pos(self):
        if self.draging:
            dt_pos = self.start_drag[0]-self.pos_mouse[0],self.start_drag[1]-self.pos_mouse[1]
            return self.pos[0]+dt_pos[0],self.pos[1]+dt_pos[1]
        else: 
            return self.pos
 
def key_analyse(key):
	move = [0,0]
	output = {}
	for event in key:
		if event.type == KEYDOWN:     #mouv perso
			if event.key == RIGHT:
				move[0] += 1
			if event.key == LEFT:
				move[0] -= 1
			if event.key == UP:
				move[1] -= 1
			if event.key == DOWN:
				move[1] += 1
			if event.key == ACTION:
					output["action"] = False

		elif event.type == KEYUP:
			if event.key==RIGHT:
				move[0] -= 1
			if event.key==LEFT:
				move[0] += 1
			if event.key == UP:
				move[1] += 1
			if event.key == DOWN:
				move[1] -= 1
	output["move"] = move

	return output