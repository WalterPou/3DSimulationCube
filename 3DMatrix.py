import pygame as pyg
from pygame.locals import *
import math
import numpy as np
import threading

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
    def __init__(self,vertices,edges,w,h):
        self.vertices=vertices
        self.edges=edges
        self.width=w
        self.height=h

    def calculateX(self,t):
        return np.array([
            [1,0,0],
            [0,math.cos(t),-math.sin(t)],
            [0,math.sin(t),math.cos(t)]
        ])

    def calculateY(self,t):
        return np.array([
            [math.cos(t),0,math.sin(t)],
            [0,1,0],
            [-math.sin(t),0,math.cos(t)]
        ])
    
    def calculateZ(self,t):
        return np.array([
            [math.cos(t),-math.sin(t),0],
            [math.sin(t),math.cos(t),0],
            [0,0,1]
        ])

    def computeDeg(self,rtx,rty,rtz):
        rX=self.calculateX(rtx)
        rY=self.calculateY(rty)
        rZ=self.calculateZ(rtz)
        prV=np.dot(self.vertices,rX)
        prV=np.dot(prV,rY)
        prV=np.dot(prV,rZ)
        return prV
    
    def projection(self,vertex,fov,scale):
        z=vertex[2]+fov
        x=vertex[0]*scale/z+self.width//2
        y=vertex[1]*scale/z+self.height//2
        return int(x),int(y)

class GraphicsEngine:
    def __init__(self,screen,vertices,edges,fov,scale,w,h):
        self.screen=screen
        self.fov=fov
        self.scale=scale
        self.vertices=vertices
        self.edges=edges
        self.width=w
        self.height=h
        self.RotC=RotationCalculator(self.vertices,self.edges,self.width,self.height)

    def render(self,rtx,rty,rtz):
        loc=self.RotC.computeDeg(rtx,rty,rtz)
        pV=[self.RotC.projection(v,self.fov,self.scale) for v in loc]
        for edge in edges:
            start=pV[edge[0]]
            end=pV[edge[1]]
            pyg.draw.line(self.screen,(255,255,255),start,end,4)

class Main:
    def __init__(self,w,h,fov,fps,vertices,edges,scale,rtx,rty,rtz,speed):
        pyg.init()
        self.speed=speed
        self.width=w
        self.height=h
        self.fov=fov
        self.fps=fps
        self.vertices=vertices
        self.edges=edges
        self.scale=scale
        self.rtx=rtx
        self.rty=rty
        self.rtz=rtz
        self.font=pyg.font.SysFont(None,24)
        self.rX=self.font.render("[0,0,0][0,0,0][0,0,0]", False, (255,255,255))
        self.rY=self.font.render("[0,0,0][0,0,0][0,0,0]", False, (255,255,255))
        self.rZ=self.font.render("[0,0,0][0,0,0][0,0,0]", False, (255,255,255))
        self.rad=self.font.render("radX:0 radY:0 radZ:0", False, (255,255,255))
        self.deg=self.font.render("degX:0 degY:0 degZ:0", False, (255,255,255))
        self.screen=pyg.display.set_mode((self.width,self.height))
        pyg.display.set_caption("Floating 3D Object")
        self.GE=GraphicsEngine(
            self.screen,self.vertices,
            self.edges,self.fov,
            self.scale,self.width,
            self.height
        )
        self.RotC=RotationCalculator(self.vertices,self.edges,self.width,self.height)

    def CustomRotation(self):
        print("Load Degree")
        while True:
            try:
                dX=float(input("X: "))
                dY=float(input("Y: "))
                dZ=float(input("Z: "))
                self.rtx=dX/180*math.pi
                self.rty=dY/180*math.pi
                self.rtz=dZ/180*math.pi
            except ValueError:
                print("Invalid Degrees")

    def run(self):
        running=True
        thread=threading.Thread(target=self.CustomRotation)
        thread.start()
        while running:
            self.screen.fill((0,0,0))
            self.screen.blit(self.rad,(50,50))
            self.screen.blit(self.deg,(50,70))
            self.screen.blit(self.rX,(50,170+self.height//2))
            self.screen.blit(self.rY,(50,190+self.height//2))
            self.screen.blit(self.rZ,(50,210+self.height//2))
            self.GE.render(self.rtx,self.rty,self.rtz)
            for event in pyg.event.get():
                if event.type==pyg.QUIT:
                    running=False
            keys=pyg.key.get_pressed()
            if keys[K_w]:
                self.rtx-=self.speed
            if keys[K_s]:
                self.rtx+=self.speed
            if keys[K_a]:
                self.rty-=self.speed
            if keys[K_d]:
                self.rty+=self.speed
            if keys[K_q]:
                self.rtz+=self.speed
            if keys[K_e]:
                self.rtz-=self.speed
            pyg.display.update()
            self.rX=self.font.render(f"[1,0,0] [0,{float(math.cos(self.rtx)):.2f},{float(-math.sin(self.rtx)):.2f}] [0,{float(math.sin(self.rtx)):.2f},{float(math.cos(self.rtx)):.2f}]=Rx", False, (255,255,255))
            self.rY=self.font.render(f"[{float(math.cos(self.rty)):.2f},0,{float(math.sin(self.rty)):.2f}] [0,1,0] [{float(-math.sin(self.rty)):.2f},0,{float(math.cos(self.rty)):.2f}]=Ry", False, (255,255,255))
            self.rZ=self.font.render(f"[{float(math.cos(self.rtz)):.2f},{float(-math.sin(self.rtz)):.2f},0] [{float(math.sin(self.rtz)):.2f},{float(math.cos(self.rtz)):.2f},0] [0,0,0]=Rz", False, (255,255,255))
            self.rad=self.font.render(f"radX:{self.rtx:.2f} radY:{self.rty:.2f} radZ:{self.rtz:.2f}", False, (255,255,255))
            self.deg=self.font.render(f"degX:{int(self.rtx*180//math.pi)} degY:{int(self.rty*180//math.pi)} degZ:{int(self.rtz*180//math.pi)}", False, (255,255,255))
            pyg.time.Clock().tick(self.fps)

if __name__ == '__main__':
    main=Main(800,600,4,240,vertices,edges,300,0.01,0.01,0.01,0.01)
    main.run()
