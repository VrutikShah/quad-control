import time
import numpy as np
import cv2
from utils import *
import math




class quad:
    def __init__(self):
        self.l = 50
        self.thc = 3
        self.m = 0.18
        self.grav = 9.8
        self.I = 2.5*1e-4

        self.x = 300
        self.y = 200
        self.x1 = self.x-self.l
        self.y1 = self.y
        self.x2 = self.x+self.l
        self.y2 = self.y
        
        self.Phi = -20

        self.f1 = 0.5
        self.f2 = 0.5

        self.u2 = self.f2*self.l - self.f1*self.l
        self.u1 = self.f1 + self.f2

        # Linear velocities
        self.v = 0          #Lateral velocity
        self.w = 0          #Normal velocity

        # Rotational velocities
        self.p = 0          #Roll rate

        self.vdot = 0
        self.wdot = 0
        self.pdot = 0

        self.xdot = math.cos(deg2rad(self.Phi)) * self.w - math.sin(deg2rad(self.Phi)) * self.v
        self.ydot = - math.sin(deg2rad(self.Phi)) * self.v - math.cos(deg2rad(self.Phi)) * self.w

    
    def newState(self,frame):
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(255,255,255),self.thc)
        self.Phi %= 360
        rad = deg2rad(self.Phi)
        x1 = round(- self.l * math.cos(rad) + self.x)
        x2 = round(+ self.l * math.cos(rad) + self.x)
        y1 = round(+ self.l * math.sin(rad) + self.y)
        y2 = round(- self.l * math.sin(rad) + self.y)
        
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
    
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(255,0,0),self.thc)
    

    
    def getPhi(self):
        return self.Phi

    def moveY(self,frame,units):
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(255,255,255),self.thc)
        self.y1-=units
        self.y2-=units
        self.y = (self.y1+self.y2)/2
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(255,0,0),self.thc)
    
    def moveX(self,frame,units):
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(255,255,255),self.thc)
        self.x1+=units
        self.x2+=units
        self.x = (self.x1+self.x2)/2
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(255,0,0),self.thc)

    def rotate(self,frame,degrees):
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(255,255,255),self.thc)
        self.Phi += degrees
        self.Phi %= 360

        # rad = deg2rad(degrees)
        rad = deg2rad(self.Phi)
        x1 = round(- self.l * math.cos(rad) + self.x)
        x2 = round(+ self.l * math.cos(rad) + self.x)
        y1 = round(+ self.l * math.sin(rad) + self.y)
        y2 = round(- self.l * math.sin(rad) + self.y)
        
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
    
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(255,0,0),self.thc)
    
        # x1 = round((self.x1 - self.x) * math.cos(rad) - (self.y1 - self.y) * math.sin(rad) + self.x)
        # x2 = round((self.x2 - self.x) * math.cos(rad) - (self.y2 - self.y) * math.sin(rad) + self.x)
        # y1 = round((self.x1 - self.x) * math.sin(rad) + (self.y1 - self.y) * math.cos(rad) + self.y)
        # y2 = round((self.x2 - self.x) * math.sin(rad) + (self.y2 - self.y) * math.cos(rad) + self.y)

    



def normalForces(obj):
    return -(obj.f1 + obj.f2)/obj.m + obj.grav * math.cos(deg2rad(obj.Phi)) - obj.p * obj.v

def lateralForces(obj):
    return obj.grav * math.sin(deg2rad(obj.Phi)) + obj.p * obj.w

def update(obj,t):
    obj.v = t * lateralForces(obj) + obj.v
    obj.w = t * normalForces(obj) + obj.w
    obj.p = t * obj.u2 / obj.I + obj.p
    obj.Phi = obj.p * t + obj.Phi

    obj.xdot = -math.cos(deg2rad(obj.Phi)) * obj.v + math.sin(deg2rad(obj.Phi)) * obj.w
    obj.ydot = math.sin(deg2rad(obj.Phi)) * obj.v + math.cos(deg2rad(obj.Phi)) * obj.w

    obj.y = obj.ydot * t + obj.y
    obj.x = obj.xdot * t + obj.x

    obj.newState(frame)
    # obj.Phi -= 0.2
    print('w: {}, v: {}, xdot: {}'.format(obj.w,obj.v,obj.xdot))


def statUpdate(frame,obj,text1,text2):
    cv2.putText(frame,text1,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),1)
    text1 = 'phi: ' + str(obj.getPhi())
    cv2.putText(frame,text1,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),1)

    cv2.putText(frame,text2,(10,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),1)
    text2 = 'y: ' + str(obj.y)
    cv2.putText(frame,text2,(10,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),1)
    
    return text1,text2
    

dim_x = 600
dim_y = 700
frame = np.ones((dim_y,dim_x,3),np.uint8)*255
grav = 9.8

obj = quad()

text1 = 'phi: ' + str(obj.getPhi())
text2 = 'y: 0'

t = 0




while t<30:
    # if obj.getPhi() <= 89:
    # cv2.putText(frame,text,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),1)
    # text = 'phi: ' + str(obj.getPhi())
    # cv2.putText(frame,text,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),1)
    # y_vel,y_pos = basic_update(0.1,accn,y_pos,y_vel)
    
    text1,text2 = statUpdate(frame,obj,text1,text2)
    
    update(obj,0.1)
    t+=.1

    time.sleep(0.02)
    cv2.imshow('an',frame)
    k = cv2.waitKey(10)
    if k ==27:
        break

while True:
    k = cv2.waitKey(10)
    if k ==27:
        break

cv2.destroyAllWindows()
