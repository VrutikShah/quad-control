import time
import numpy as np
import cv2
from utils import *
import math
from scipy.integrate import quad

dim_x = 600
dim_y = 400
frame = np.ones((dim_y,dim_x,3),np.uint8)*255
a = 0
l = 50
x,y = 100,100 #center
x1 = x-l
x2 = x+l
y1 = y
y2 = y


grav = 9.8


class quad:
    def __init__(self):
        self.l = 50
        self.thc = 3

        self.x = 200
        self.y = 300
        self.x1 = self.x-self.l
        self.y1 = self.y
        self.x2 = self.x+self.l
        self.y2 = self.y
        
        self.Phi = 0

        self.f1 = 0
        self.f2 = 0

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

    def getPhi(self):
        return self.Phi

    def moveY(self,frame,units):
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(255,255,255),self.thc)
        self.y1-=units
        self.y2-=units
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(255,0,0),self.thc)
    
    def moveX(self,frame,units):
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(255,255,255),self.thc)
        self.x1+=units
        self.x2+=units
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(255,0,0),self.thc)
    
    def rotate(self,frame,degrees):
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(255,255,255),self.thc)
        self.Phi += degrees
        self.Phi %= 360

        # rad = deg2rad(degrees)
        rad = deg2rad(self.Phi)
        # x1 = round((self.x1 - self.x) * math.cos(rad) - (self.y1 - self.y) * math.sin(rad) + self.x)
        # x2 = round((self.x2 - self.x) * math.cos(rad) - (self.y2 - self.y) * math.sin(rad) + self.x)
        # y1 = round((self.x1 - self.x) * math.sin(rad) + (self.y1 - self.y) * math.cos(rad) + self.y)
        # y2 = round((self.x2 - self.x) * math.sin(rad) + (self.y2 - self.y) * math.cos(rad) + self.y)

        x1 = round(- self.l * math.cos(rad) + self.x)
        x2 = round(+ self.l * math.cos(rad) + self.x)
        y1 = round(+ self.l * math.sin(rad) + self.y)
        y2 = round(- self.l * math.sin(rad) + self.y)
        
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
    
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(255,0,0),self.thc)
    
obj = quad()

text = 'phi: ' + str(obj.getPhi())
cv2.putText(frame,text,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),1)

cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),3)
deg = 1
count = 0

def netThrust():
    return obj.f1 + obj.f2 - grav

def update():
    thrust = netThrust()
    y_vel = 


while True:
    # if obj.getPhi() <= 89:
    cv2.putText(frame,text,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),1)
    text = 'phi: ' + str(obj.getPhi())
    cv2.putText(frame,text,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),1)
    obj.moveY(frame,2)
    obj.moveX(frame,1)
    obj.rotate(frame,1)
    # time.sleep(0.1)
    cv2.imshow('an',frame)
    
    k = cv2.waitKey(10)
    if k ==27:
        break

cv2.destroyAllWindows()
