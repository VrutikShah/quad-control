# PID class
import time

class PID:
    def __init__(self,current_time=None):
        self.Kp = 0.0
        self.Ki = 0.0
        self.Kd = 0.0

        self.prev_time = 0.0
        self.curr_time = current_time if current_time is not None else time.time()

        self.clear()
    
    def clear(self):
        self.dest = 0.0
        
        self.p = 0.0
        self.i = 0.0
        self.d = 0.0

        self.prev_error = 0.0
        self.output = 0.0

    def setKp(self,Kp):
        self.Kp = Kp

    def setKi(self,Ki):
        self.Ki = Ki
    
    def setKd(self,Kd):
        self.Kd = Kd

    def setDest(self,dest):
        self.dest = dest
    
    def update(self,curr_val):
        error = self.dest - curr_val
        delta_error = error - self.prev_error
        
        self.current_time = current_time if current_time is not None else time.time()
        delta_time = self.current_time - self.prev_time

        self.p = self.Kp * error
        self.i += error * delta_time

        #TODO Add windup_guard condition here

        self.d = 0.0
        self.d = delta_error / delta_time
        
        self.prev_time = self.curr_time
        self.prev_error = error

        self.output = self.p + (self.i * self.Ki) + (self.d * self.Kd)
