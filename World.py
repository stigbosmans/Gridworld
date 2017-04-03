import numpy as np
import pygame
class World():
    height=4
    width=4
    score=0
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
            "goal":(self.defaultPosition["goal"][0],self.defaultPosition["goal"][1]),
            "pit":(self.defaultPosition["pit"][0],self.defaultPosition["pit"][1]),
            "wall":(self.defaultPosition["wall"][0],self.defaultPosition["wall"][1]),
            "agent":(self.defaultPosition["agent"][0],self.defaultPosition["agent"][1])
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
        for y in range(self.height):
            line=""
            for x in range(self.width):
                line=line+self.objectOnCoordinates(x,y)
            print(line)
            
    def getStateArray(self):
        st=np.zeros((self.width,self.height))
        for x in range(self.height):
            for y in range(self.width):
                st[y,x]=self.objectIndexOnCoordinates(x,y)
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
    def objectIndexOnCoordinates(self,row,col):
        if self.states[row,col,0]==1:
            return 0 #+
        elif self.states[row,col,1]==1:
            return 1 #-
        elif self.states[row,col,2]==1:
            return 2 #W
        elif self.states[row,col,3]==1:
            return 3 #A
        else:
            return -1

    def moveAgent(self,action):
        agentPos=self.positions["agent"]
        (newx,newy)=agentPos
        if action==0:
            if newy-1>=0:
                newy=newy-1
        elif action==1:
            if newy+1<self.height:
                newy=newy+1
        elif action==2:
            if newx-1>=0:
                newx=newx-1
        elif action==3:
            if newx+1<self.width:
                newx=newx+1
        
        (wallx,wally)=self.positions["wall"]
        (pitx,pity)=self.positions["pit"]
        (goalx,goaly)=self.positions["goal"]
        if newx==wallx and newy==wally:
            newx=agentPos[0]
            newy=agentPos[1]
        elif newx==pitx and newy==pity:
            self.score=self.score-10
        elif newx==goalx and newy==goaly:
            self.score=self.score+10
        self.positions["agent"]=(newx,newy)
        self.__updateStates()
    
    def __updateStates(self):
        self.clearWorld()
        
        for obj in self.positions:
            (x,y)=self.positions[obj]
            index=-1
            if obj=="goal":
                index=0
            elif obj=="pit":
                index=1
            elif obj=="wall":
                index=2
            elif obj=="agent":
                index=3
            self.states[x,y,index]=1

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
        for x in range(self.world.width):
            for y in range(self.world.height):
                self.drawCell(x,y)
                self.drawObject(x,y,state[y,x])
        self.drawText("Score:"+str(self.world.score),0,self.world.height*self.cellSize+10)
        print(self.world.score)
        pygame.display.update()

    def drawCell(self,x,y):
        pygame.draw.rect(self.screen,(255,255,255),(x*self.cellSize+1,y*self.cellSize+1,self.cellSize-1,self.cellSize-1))
    
    def drawText(self,text,x,y):
        myfont = pygame.font.SysFont("Arial", 14)
        label = myfont.render(text, 1, (255,255,255))
        self.screen.blit(label, (x,y))

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