import time
import numpy as np
import cv2
from utils import *
import math


class stats:
    def __init__(self):
        self.phi = ''
        self.y = ''
        self.x = ''
        self.f1 = ''
        self.f2 = ''
    
    def statUpdate(self,frame,quad_quad_obj):
        cv2.putText(frame,self.phi,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(254,254,254),1)
        self.phi = 'phi: ' + str(quad_quad_obj.getPhi())
        cv2.putText(frame,self.phi,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1)

        cv2.putText(frame,self.y,(10,50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(254,254,254),1)
        self.y = 'y: ' + str(quad_quad_obj.y)
        cv2.putText(frame,self.y,(10,50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1)
        
        cv2.putText(frame,self.x,(10,70),cv2.FONT_HERSHEY_SIMPLEX,0.5,(254,254,254),1)
        self.x = 'x: ' + str(quad_quad_obj.x)
        cv2.putText(frame,self.x,(10,70),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1)

        # cv2.putText(frame,self.y,(10,90),cv2.FONT_HERSHEY_SIMPLEX,0.5,(254,254,254),1)
        # self.f1 = 'f1: ' + str(quad_quad_obj.f1)
        # cv2.putText(frame,self.y,(10,90),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1)

        # cv2.putText(frame,self.y,(10,110),cv2.FONT_HERSHEY_SIMPLEX,0.5,(254,254,254),1)
        # self.f2 = 'f2: ' + str(quad_quad_obj.f2)
        # cv2.putText(frame,self.y,(10,110),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1)

class quad:
    def __init__(self):
        self.l = 50
        self.thc = 3
        self.m = 0.18
        self.grav = 1.5
        self.I = 2.5*1e-4

        self.x = 300
        self.y = 400
        self.x1 = self.x-self.l
        self.y1 = self.y
        self.x2 = self.x+self.l
        self.y2 = self.y
        
        self.Phi = 30

        self.f1 = 0.5
        self.f2 = 0.5

        self.u2 = self.f2*self.l - self.f1*self.l
        self.u1 = self.f1 + self.f2

        # Linear velocities
        self.v = 0          #Lateral velocity
        self.w = 0          #Normal velocity

        # Rotational velocities
        self.p = -.2         #Roll rate

        self.vdot = 0
        self.wdot = 0
        self.pdot = 0

        self.xdot = 0
        self.ydot = 0

    
    def newState(self,frame,frame2):
        
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(254,254,254),self.thc)
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

        self.y = (self.y1+self.y2)/2
        self.x = (self.x1+self.x2)/2

        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(254,0,0),self.thc)
        cv2.circle(frame2, (round(self.x),round(self.y2)), radius=0, color=(0, 0, 255), thickness=5)
    

    
    def getPhi(self):
        return self.Phi

    def moveY(self,frame,units):
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(254,254,254),self.thc)
        self.y1-=units
        self.y2-=units
        self.y = (self.y1+self.y2)/2
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(254,0,0),self.thc)
    
    def moveX(self,frame,units):
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(254,254,254),self.thc)
        self.x1+=units
        self.x2+=units
        self.x = (self.x1+self.x2)/2
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(254,0,0),self.thc)

    def rotate(self,frame,degrees):
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(254,254,254),self.thc)
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
    
        cv2.line(frame,(self.x1,self.y1),(self.x2,self.y2),(254,0,0),self.thc)
    
        # x1 = round((self.x1 - self.x) * math.cos(rad) - (self.y1 - self.y) * math.sin(rad) + self.x)
        # x2 = round((self.x2 - self.x) * math.cos(rad) - (self.y2 - self.y) * math.sin(rad) + self.x)
        # y1 = round((self.x1 - self.x) * math.sin(rad) + (self.y1 - self.y) * math.cos(rad) + self.y)
        # y2 = round((self.x2 - self.x) * math.sin(rad) + (self.y2 - self.y) * math.cos(rad) + self.y)

    



def normalForces(quad_obj):
    return +(quad_obj.f1 + quad_obj.f2) - quad_obj.grav * math.cos(deg2rad(quad_obj.Phi)) + quad_obj.p * quad_obj.v

<<<<<<< HEAD
# def update():
#     thrust = netThrust()
#     y_vel = 
=======
def lateralForces(quad_obj):
    return -quad_obj.grav * math.sin(deg2rad(quad_obj.Phi)) - quad_obj.p * quad_obj.w
>>>>>>> 3512ef97c4d896a15729250a280637d31f2bd950

def update(quad_obj,t):
    quad_obj.v = t * lateralForces(quad_obj) + quad_obj.v
    quad_obj.w = t * normalForces(quad_obj) + quad_obj.w
    quad_obj.p = t * quad_obj.u2 / quad_obj.I + quad_obj.p
    quad_obj.Phi = quad_obj.p * t + quad_obj.Phi

    quad_obj.xdot = +math.cos(deg2rad(quad_obj.Phi)) * quad_obj.v - math.sin(deg2rad(quad_obj.Phi)) * quad_obj.w
    quad_obj.ydot = -math.sin(deg2rad(quad_obj.Phi)) * quad_obj.v - math.cos(deg2rad(quad_obj.Phi)) * quad_obj.w

    quad_obj.y = quad_obj.ydot * t + quad_obj.y
    quad_obj.x = quad_obj.xdot * t + quad_obj.x

    quad_obj.newState(frame,frame2)
    # quad_obj.Phi += 0.2
    # quad_obj.f1 += 0.01
    # quad_obj.f2 += 0.01
    print('p: {}, w: {}, v: {}, xdot: {}, ydot: {}'.format(quad_obj.p, quad_obj.w,quad_obj.v,quad_obj.xdot,quad_obj.ydot))


def statUpdate(frame,quad_obj,text1,text2):
    cv2.putText(frame,text1,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(254,254,254),1)
    text1 = 'phi: ' + str(quad_obj.getPhi())
    cv2.putText(frame,text1,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),1)

    cv2.putText(frame,text2,(10,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(254,254,254),1)
    text2 = 'y: ' + str(quad_obj.y)
    cv2.putText(frame,text2,(10,50),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),1)
    
    return text1,text2
    

dim_x = 600
dim_y = 700
frame = np.ones((dim_y,dim_x,3),np.uint8)*254
frame2 = np.ones((dim_y,dim_x,3),np.uint8)*1
quad_obj = quad()
stat_obj = stats()
t = 0

# text1 = 'phi: ' + str(quad_obj.getPhi())
# text2 = 'y: 0'

while t<500:
    # text1,text2 = statUpdate(frame,quad_obj,text1,text2)

    stat_obj.statUpdate(frame,quad_obj)
    update(quad_obj,0.1)
    t+=.1

    # time.sleep(0.02)
    cv2.imshow('an',frame+frame2)
    k = cv2.waitKey(10)
    if k ==27:
        break

while True:
    k = cv2.waitKey(10)
    if k ==27:
        break

cv2.destroyAllWindows()
