import pygame as pyg
from pygame.locals import *
import numpy as np
import math as m

width,height=800,600
vertices=np.array([
    [-1,-1,-1],
    [1,-1,-1],
    [1,1,-1],
    [-1,1,-1],
    [-1,-1,1],
    [1,-1,1],
    [1,1,1],
    [-1,1,1]
])

edges=[
    (0,1),(1,2),(2,3),(3,0),
    (4,5),(5,6),(6,7),(7,4),
    (0,4),(1,5),(2,6),(3,7)
]

class RotationCalculator:
    def __init__(self,fov,scale,w,h):
        self.fov=fov
        self.scale=scale
        self.w=w
        self.h=h

    def calculateX(self,t):
        return np.array([
            [1,0,0],
            [0,m.cos(t),-m.sin(t)],
            [0,m.sin(t),m.cos(t)]
        ])

    def calculateY(self,t):
        return np.array([
            [m.cos(t),0,m.sin(t)],
            [0,1,0],
            [-m.sin(t),0,m.cos(t)]
        ])

    def calculateZ(self,t):
        return np.array([
            [m.cos(t),-m.sin(t),0],
            [m.sin(t),m.cos(t),0],
            [0,0,1]
        ])

    def project(self,vertex):
        z=vertex[2]+self.fov
        x=vertex[0]*self.scale/z+self.w//2
        y=vertex[1]*self.scale/z+self.h//2
        return int(x),int(y)

class GraphicsEngine:
    def __init__(self,calc,vertices,edges,screen):
        self.calc=calc
        self.vertices=vertices
        self.edges=edges
        self.screen=screen

    def computeDeg(self,rtx,rty,rtz):
        rX=self.calc.calculateX(rtx)
        rY=self.calc.calculateY(rty)
        rZ=self.calc.calculateZ(rtz)
        prV=np.dot(self.vertices,rX)
        prV=np.dot(prV,rY)
        prV=np.dot(prV,rZ)
        return prV

    def drawGraphics(self,rtx,rty,rtz):
        prV=self.computeDeg(rtx,rty,rtz)
        xfl=[self.calc.project(vertex) for vertex in prV]
        for edge in self.edges:
            start=xfl[edge[0]]
            end=xfl[edge[1]]
            pyg.draw.line(self.screen,(255,255,255),start,end,4)

class Application:
    def __init__(self,rtx,rty,rtz,vertices,edges,fps,fov,scale,w,h,skip):
        pyg.init()
        self.skip=skip
        self.rtx=rtx
        self.rty=rty
        self.rtz=rtz
        self.vertices=vertices
        self.edges=edges
        self.screen=pyg.display.set_mode((w,h))
        self.fps=fps
        self.calc=RotationCalculator(fov,scale,w,h)
        self.GE=GraphicsEngine(self.calc,self.vertices,self.edges,self.screen)
        pyg.display.set_caption("3D Object")
        self.font=pyg.font.SysFont(None,24)
        self.text=self.font.render("degX:0 degY:0 degZ:0",False,(255,255,255))

    def run(self):
        running=True
        while running:
            self.screen.fill((0,0,0))
            self.screen.blit(self.text,(50,50))
            self.GE.drawGraphics(self.rtx,self.rty,self.rtz)
            for event in pyg.event.get():
                if event.type==pyg.QUIT:
                    running=False
            keys=pyg.key.get_pressed()
            if keys[K_w]:
                self.rtx-=self.skip
            if keys[K_s]:
                self.rtx+=self.skip
            if keys[K_a]:
                self.rty-=self.skip
            if keys[K_d]:
                self.rty+=self.skip
            if keys[K_q]:
                self.rtz-=self.skip
            if keys[K_e]:
                self.rtz+=self.skip
            self.text=self.font.render(f"degX:{self.rtx:.2f} degY:{self.rty:.2f} degZ:{self.rtz:.2f}",False,(255,255,255))
            #print(f"Rotation Angles: {self.rtx}, {self.rty}, {self.rtz}")
            pyg.display.update()
            pyg.time.Clock().tick(self.fps)

if __name__ == '__main__':
    app=Application(0.01,0.01,0.01,vertices,edges,120,4,300,800,600,0.01)
    app.run()
