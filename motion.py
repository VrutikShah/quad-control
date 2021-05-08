from scipy.integrate import quad, dblquad
import matplotlib.pyplot as plt
p = 0
v = 0
accn = 2
t = 0
plt.axis([0,10,0,1])

def integrand(x,val):
    return val

def vel(accn,t1,t2):
    return quad(integrand,t1,t2,args=(accn))

def pos(p,t1,t2):
    return dblquad(integrand,t1,t2,,args=(p))

def update(accn,p,v,t1):
    v_temp,_ = vel(accn,t1,t1+0.1)
    v += v_temp
    x_temp,_ = pos(p,t1,t1+0.1)
    p += x_temp
    return p


t = 0
while t<10:
    p = update(accn,p,v,t)
    plt.scatter(t,p)
    plt.pause(0.05)
    t+=0.1

plt.show()