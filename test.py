from decimal import *
from cmath import acos, atan, pi, sqrt, tan
from math import atan2
from sympy import Symbol, init_printing, solve, sin, cos, symbols, simplify, trigsimp
from sympy.simplify.fu import fu, L, TR0, TR10, TR3, TR8, TR9, TR10i, TR11
import numpy as np
import craig as cg
#import warnings

#warnings.filterwarnings('ignore')
#from inverse_kinematic import trig_equ
dh_tbl=np.array([[0,0,0],
                    [np.deg2rad(-90), -30, 0],
                    [0, 340, 0],
                    [np.deg2rad(-90), -40, 338],
                    [np.deg2rad(90), 0, 0],
                    [np.deg2rad(-90),0,0]])

cg.setDhTbl(dh_tbl)
#getcontext().prec=2
#getcontext().rounding = ROUND_UP

ty = np.deg2rad(-60) # rotate y axis
tcup_0_2s = np.array([[cos(ty), 0, sin(ty), 330], [0, 1, 0, 372],
                          [-sin(ty), 0, cos(ty), 367], [0, 0, 0, 1]])
Tcup_6 = np.array([[0, 0, 1, 0], [0, -1, 0, 0], [1, 0, 0, 206],
                       [0, 0, 0, 1]])
tcup_0_2s = np.array([[cos(ty), 0, sin(ty), 330], [0, 1, 0, 372],
                          [-sin(ty), 0, cos(ty), 367], [0, 0, 0, 1]])

init_printing(use_unicode=True)
np.set_printoptions(precision=3, suppress=True)

t6_0 = tcup_0_2s @ np.linalg.inv(Tcup_6)
print('t6_0', t6_0)
#p4_0_org=P6_0_org
(x,y,z)=t6_0[0:3, 3]
print('4-0-org:', x,y,z)

t4_3=cg.get_ti2i_1(4)
# returns the 3rd col
p4_3_org=t4_3[:, 3]
print('p4_3:', p4_3_org)
t2_1= cg.get_ti2i_1(2)
t3_2= cg.get_ti2i_1(3)

g3_equ=z
p4_0_org= t2_1@t3_2@p4_3_org
print('p4_0:', p4_0_org)
g1=p4_0_org[0]
g3=p4_0_org[2]
g1=trigsimp(g1)
g3=trigsimp(g3)
num=-cg.extract_num(str(g1))
g1+=num
g1_equ=sqrt(x**2+y**2)+num

#print('trigsimp_g1:', g1)
#print('trigsimp_g3:', trigsimp(g3))

a1 = -30
print((227)**2 + (372)**2 + 188.6**2 + 2 * (227 + 372) * 30 + 30**2)
print((435.79 - a1)**2 + 188.6**2)
c = (252530 - 40**2 - 338**2 - 340**2) / (2 * 340)
print('c', c)
a = -40
b = 338

(q3_1, q3_2)= cg.trig_equ(a, b, c)
# print('q3_1, q3_2:', (q31 * 180 / pi), q32 * 180 / pi)
print('q3:', np.rad2deg(q3_1), np.rad2deg(q3_2))

r_equ=g1_equ**2+g3_equ**2
r = trigsimp((g1**2).expand()+(g3**2).expand())
r+=(-r_equ)
q3=Symbol('q3')
print('r:', r)
sol=solve(r, q3)
print('sol_q3:', sol[0]*180/pi, sol[1]*180/pi)

# send caculated q3 to ti_2_i-1
t3_2= cg.get_ti2i_1(3, q3_1)
#g3_equ=z
p4_0_org= t2_1@t3_2@p4_3_org
g3=p4_0_org[2]-z
#g3=g3.find(lambda x: x.replace('cos(q3)',c3))
# g3=TR9(g3)-z
print('g3:', g3)
q2=Symbol('q2')
sol=solve(g3, q2)

# expr=(40*(sin(x)*c3+cos(x)*s3)-338*(cos(x)*c3-sin(x)*s3)-340*sin(x)-188.6)
#sol=solve(expr, x)
#print(expr)
print('q2:', sol[0]*180/pi, 180-sol[1]*180/pi)

q1=atan2(y, x)
print('q1:', np.rad2deg(q1))


# https://zhuanlan.zhihu.com/p/440748878
(alp4, a4, d5)=cg.dh_tbl[4, :]
(alp3, a3, d4)=cg.dh_tbl[3, :]
(alp2, a2, d3)=cg.dh_tbl[2, :]
(alp1, a1, d2)=cg.dh_tbl[1, :]
q1=atan2(d3, abs(sqrt(x+y+z-d3*d3)))+atan2(y,x)
print('q1', np.rad2deg(q1))

#https://zhuanlan.zhihu.com/p/440748878
k3= ((a1-cos(q1)*x-sin(q1)*y)**2+z**2-(a3**2+d4**2+a2**2))/(2*a2)
s = sqrt(a3**2+d4**2-k3**2)
print('s:', s)
q3 = atan(k3/s) + atan(a3/d4)
print('q3:', q3*180/pi)

g=cos(q1)*x+sin(q1)*y -a1
e=a3*cos(q3)+d4*sin(q3)+a2
f=a3*sin(q3)-d4*cos(q3)
q2=atan(z*e-g*f/g*e+z*f)
print('q2:', q2*180/pi)


# ti_i-1
'''
def get_ti2i_1(i):
    np.set_printoptions(precision=2, suppress=True)
    # fill in dh tbl wrt robot arms' dh params
    dh_tbl=np.array([[0,0,0],
                    [np.deg2rad(-90), -30, 0],
                    [0, 340, 0],
                    [np.deg2rad(-90), -40, 338],
                    [np.deg2rad(90), 0, 0],
                    [np.deg2rad(-90),0,0]])
    # array idx starts frm 0, so i-1
    (alp, ai, di)=dh_tbl[i-1, :]
    ci = Symbol('c'+str(i))
    si = Symbol('s'+str(i))
    t=np.array([[ci, -si, 0, round(ai)],
                    [si*round(cos(alp),2), ci*round(cos(alp),2), round(-sin(alp)), round(-sin(alp)*di)],
                    [si*round(sin(alp),2), ci*round(sin(alp),2), round(cos(alp)), round(cos(alp)*di)],
                    [0,0,0,1]
                    ])
    print(t)
    return(t)
'''

def getT4_0_org():
    np.set_printoptions(precision=3, suppress=True)

    # (i代4到Ti_i-1 的dh formular)
    t4_3=cg.get_ti2i_1(4)
    # returns the 3rd col
    p4_3_org=t4_3[:, 3]
    print('p4_3:', p4_3_org)
    t2_1= cg.get_ti2i_1(2)
    t3_2= cg.get_ti2i_1(3)

    p4_0_org= t2_1@t3_2@p4_3_org
    # !!!manually adjust +30, find a way to auto it.
    g1=p4_0_org[0]+30
    #print('p4_0:', p4_0_org)
    g2=p4_0_org[1]
    #print('g2:', g2)
    g3=p4_0_org[2]
    #print('g3:', g3)
    #q2, q3=symbols('q2, q3')
    #g1=trigsimp(g1)
    print('trigsimp_g1:', g1)
    print('trigsimp_g2:', trigsimp(g2))
    print('trigsimp_g3:', trigsimp(g3))
    #g3=trigsimp(g3)
    r = trigsimp((g1**2).expand()+(g2**2).expand()+(g3**2).expand())
    print('r:', r)
    #print(((np.sqrt(257**2+372**2))**2+188.6**2))

# getT4_0_org()
def pieper():
    #(alp3, a3, d4)=cg.dh_tbl[3, :]
    #p4_3=np.array([a3, -d4*sin(alp3), d4*round(cos(alp3)),1])
    #print('p4_3:', p4_3)

    '''
    [x,y,z,1]t=P4_0_org=t1_0@t2_1@t3_2@p4_3_org
    =
    '''
    t4_3=cg.get_ti2i_1(4)
    p4_3=t4_3[:, 3]
    print('p4_3:', p4_3)
    t1_0=cg.get_ti2i_1(1)
    t2_1=cg.get_ti2i_1(2)
    t3_2=cg.get_ti2i_1(3)
    p4_0_org  = t2_1@t3_2@p4_3
    #f is a func of theta3
    f=simplify(t3_2@p4_3)
    f1=f[0]
    f2=f[1]
    f3=f[2]
    # g is a func of theta2 and theta3
    g=t2_1@f
    g1=trigsimp(g[0])
    g2=trigsimp(g[1])
    g3=trigsimp(g[2])
    p4_0_org= t2_1@t3_2@p4_3_org
    print('p4_0:', p4_0_org)
    g1=p4_0_org[0]
    g3=p4_0_org[2]
    g1=trigsimp(g1)
    g1=trigsimp(g3)
    print('g1:', g1)
    print('g2:', g2)
    print('g3:', g3)
    #p4_0=[x,y,z,1]=t1_0@g
    # r=x**2+y**2+z**2=g1**2+g2**2+g3**2
    # r is func of only theta2 & 3
    # z = g3 (z is func of theta 3)
    # r=simplify(g1**2+g2**2+g3**2)
    r = trigsimp((g1**2).expand()+(g3**2).expand())
    print('r:', r)
    k1=f1
    k2=-f2
    k3=f1**2+f2**2+f3**2+a1**2+d2**2+2*d2*f3
    k4=f3*cos(alp1)+d2*cos(alp1)
    t=0
    u=tan(t/2)
    c=1-u**2/1+u**2
    s=2*u/1+u
    #(r-k3)**2/4*a1**2 + (z-k4)**2/sin(alp1)**2=k1**2+k2**2
pieper()
