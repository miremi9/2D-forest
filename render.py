
import pygame
from pygame.locals import *

from camera import Camera

BLEU = (5,5,30)
RED = (255,0,0)
GREEN = (0,255,0)


def start(world,WIDTH=1000,HEIGHT=1000,FPS=60,RENDER_DISTANCE=100,STOP= pygame.locals.K_TAB,COLOR=BLEU):
    fenetre = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True
    center = WIDTH//2,HEIGHT//2

    while running:
        timer = pygame.time.Clock()

        dt = timer.tick(FPS)/1000

        event_key = list(pygame.event.get())
        if any(filter((lambda x: x.type==KEYDOWN and x.key == STOP), event_key)):
            running = False
        world.cam.update(event_key)
        action2do = set()
        chunks = world.get_loaded_chunks(world.cam.pos,RENDER_DISTANCE)
        for chunk in chunks:
            around_chunks =world.get_chunks_around(chunk.num)
            for element in chunk.get_all_elements():
                action2do.update(element.update(world,event_key,dt,around_chunks))

        for action in action2do:
            action()

        fenetre.fill(BLEU)

        for chunk in sorted(chunks,key=lambda x:x.num):
            #pygame.draw.rect(fenetre,GREEN,chunk.draw(world.cam.get_pos(),center,world.cam.scale),1)  #draw chunk
            for element in chunk.get_all_elements():
                element.draw(fenetre,RED,world.cam.get_pos(),world.cam.scale)

        pygame.display.flip()
    pygame.quit()