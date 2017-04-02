import numpy as np
import pygame
class World():
    height=4
    width=4
    def __init__(self):
        self.states=np.zeros((self.width,self.height,4))
        #X,Y,Index
        self.defaultPosition={
            "agent":(0,1,3),
            "wall":(2,2,2),
            "pit":(2,1,1),
            "goal":(3,3,0)
        }
        self.positions={
            "agent":(self.defaultPosition["agent"][0],self.defaultPosition["agent"][1]),
            "wall":(self.defaultPosition["wall"][0],self.defaultPosition["wall"][1]),
            "pit":(self.defaultPosition["pit"][0],self.defaultPosition["pit"][1]),
            "goal":(self.defaultPosition["goal"][0],self.defaultPosition["goal"][1])
        }
    def clearWorld(self):
        self.states=np.zeros((self.width,self.height,4))

    def getRandomPosition(self):
        return (np.random.randint(0,self.height),np.random.randint(0,self.width))

    def getTypeDefaultPosition(self,type):
        return self.defaultPosition[type]

    def getTypeIndex(self,type):
        return self.defaultPosition[type][2]
    
    def showWorld(self):
        for i in range(self.width):
            line=""
            for j in range(self.height):
                line=line+self.objectOnCoordinates(i,j)
            print(line)
    def getStateArray(self):
        st=np.zeros((self.width,self.height))
        for i in range(self.width):
            for j in range(self.height):
                st[i,j]=self.objectIndexOnCoordinates(i,j)
        return st

    def objectOnCoordinates(self,x,y):
        if self.states[x,y,0]==1:
            return "+"
        elif self.states[x,y,1]==1:
            return "-"
        elif self.states[x,y,2]==1:
            return "W"
        elif self.states[x,y,3]==1:
            return "A"
        else:
            return "_"
    def objectIndexOnCoordinates(self,x,y):
        if self.states[x,y,0]==1:
            return 0 #+
        elif self.states[x,y,1]==1:
            return 1 #-
        elif self.states[x,y,2]==1:
            return 2 #W
        elif self.states[x,y,3]==1:
            return 3 #A
        else:
            return -1

class BasicWorld(World):
    def __init__(self):
        World.__init__(self)
        print("Basic World")
        self.generate()

    def generate(self):
        self.states[self.getTypeDefaultPosition("agent")]=1
        self.states[self.getTypeDefaultPosition("wall")]=1
        self.states[self.getTypeDefaultPosition("pit")]=1
        self.states[self.getTypeDefaultPosition("goal")]=1

class RandomPlayerWorld(World):
    def __init__(self):
        World.__init__(self)
        print("Random Player World")
        self.generate()

    def generate(self):
        self.clearWorld()
        self.states[self.getTypeDefaultPosition("wall")]=1
        self.states[self.getTypeDefaultPosition("pit")]=1
        self.states[self.getTypeDefaultPosition("goal")]=1
        agentPos=self.getRandomPosition()
        self.positions["agent"]=(agentPos[0],agentPos[1])
        if self.objectOnCoordinates(agentPos[0],agentPos[1])!="_":
            self.generate()
        else:
            self.states[agentPos[0],agentPos[1],self.getTypeIndex("agent")]=1
            print(self.positions)
            print(self.states)
class RandomWorld(World):
    def __init__(self):
        World.__init__(self)
        print("Random World")
        self.generate()

    def generate(self):
        self.clearWorld()
        agentPos=self.getRandomPosition()
        wallPos=self.getRandomPosition()
        pitPos=self.getRandomPosition()
        goalPos=self.getRandomPosition()
        if self.objectOnCoordinates(agentPos[0],agentPos[1])!="_":
            self.generate()
        else:
            self.states[agentPos[0],agentPos[1],self.getTypeIndex("agent")]=1

        if self.objectOnCoordinates(wallPos[0],wallPos[1])!="_":
            self.generate()
        else:
            self.states[wallPos[0],wallPos[1],self.getTypeIndex("wall")]=1

        if self.objectOnCoordinates(pitPos[0],pitPos[1])!="_":
            self.generate()
        else:
            self.states[pitPos[0],pitPos[1],self.getTypeIndex("pit")]=1

        if self.objectOnCoordinates(goalPos[0],goalPos[1])!="_":
            self.generate()
        else:
            self.states[goalPos[0],goalPos[1],self.getTypeIndex("goal")]=1

class WorldVisualizer():
    cellSize=50
    def __init__(self, world, screen):
        self.screen=screen
        self.world=world
        self.update()

    def update(self):
        state=self.world.getStateArray()
        print(state)
        for x in range(self.world.width):
            for y in range(self.world.height):
                self.drawCell(x,y)
                self.drawObject(x,y,state[x,y])
        pygame.display.update()

    def drawCell(self,x,y):
        pygame.draw.rect(self.screen,(255,255,255),(x*self.cellSize+1,y*self.cellSize+1,self.cellSize-1,self.cellSize-1))
    
    def drawObject(self,x,y,id):
        myfont = pygame.font.SysFont("Arial", 14)
        txt=""
        if id==0:
            txt="+"
        elif id==1:
            txt="-"
        elif id==2:
            txt="W"
        elif id==3:
            txt="A"
        
        if id!=-1:
            label = myfont.render(txt, 1, (0,0,0))
            self.screen.blit(label, (x*self.cellSize+1+self.cellSize/2-7, y*self.cellSize+1+self.cellSize/2-7))