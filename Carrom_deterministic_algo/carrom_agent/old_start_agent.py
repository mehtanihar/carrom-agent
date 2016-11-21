# A Sample Carrom Agent to get you started. The logic for parsing a state
# is built in

from thread import *
import time
import socket
import sys
import argparse
import random
import ast
import math
import numpy as np


def cut_force2(X1,x1,Y1,y1,alpha,R,r1,pcangle,v):
    
    print(X1)
    print(Y1)
    print(x1)
    print(y1)
    print(alpha)
   
    a1=X1-x1
    b1=Y1-y1
    a=1
    b=2*(a1*np.cos(np.deg2rad(alpha))+b1*np.sin(np.deg2rad(alpha)))
    c=pow(a1,2)+pow(b1,2)-pow(R+r1,2)
   
    print(a)
    print(b)
    print(c)
    r=(-b+np.sqrt(pow(b,2)-4*a*c))/2
    x2=r*np.cos(np.deg2rad(alpha))+x1
    y2=r*np.sin(np.deg2rad(alpha))+y1
    tan=(y2-y1)/(x2-x1)
    phi=pcangle-np.deg2rad(np.arctan(tan))
    theta=alpha-np.deg2rad(np.arctan(tan))
    
    u=(0.35*v*np.cos(np.deg2rad(phi))*(3.8))/np.cos(np.deg2rad(theta))
    print(r)
    return (u-17.149)/(378.5-17.149)



def cut_force(X1,x1,Y1,y1,alpha,R,r1,pcangle,v):
    print(X1)
    print(Y1)
    print(x1)
    print(y1)
    alpha=180+alpha
    print(alpha)

    a1=X1-x1
    b1=Y1-y1
    a=1
    b=2*(a1*np.cos(np.deg2rad(alpha))+b1*np.sin(np.deg2rad(alpha)))
    c=pow(a1,2)+pow(b1,2)-pow(R+r1,2)
   
    print(a)
    print(b)
    print(c)  
    r=(-b+np.sqrt(pow(b,2)-4*a*c))/2
    print(r)
    x2=r*np.cos(np.deg2rad(alpha))+x1
    y2=r*np.sin(np.deg2rad(alpha))+y1
    tan=(y2-y1)/(x2-x1)
    phi=pcangle-np.deg2rad(np.arctan(tan))
    theta=180.0-alpha-np.deg2rad(np.arctan(tan))
   
    u=(0.35*v*np.cos(np.deg2rad(phi))*(3.8))/np.cos(np.deg2rad(theta))
    #print(r)
    return (u-17.149)/(378.5-17.149)


def force_from_pos(x,y):
    
    return (np.sqrt(1.9*np.sqrt(x*x+y*y))-np.sqrt(1.9*154.79))/(378.5-np.sqrt(1.9*154.79))
# Parse arguments
 #44.1 755.9 striker at 170-630, 14
 #554.790425693, 140.0) 554.79-170=154.79
#17.149=u_min

parser = argparse.ArgumentParser()

parser.add_argument('-np', '--num-players', dest="num_players", type=int,
                    default=1,
                    help='1 Player or 2 Player')
parser.add_argument('-p', '--port', dest="port", type=int,
                    default=12121,
                    help='port')
parser.add_argument('-rs', '--random-seed', dest="rng", type=int,
                    default=0,
                    help='Random Seed')
parser.add_argument('-c', '--color', dest="color", type=str,
                    default="Black",
                    help='Legal color to pocket')
args = parser.parse_args()


host = '127.0.0.1'
port = args.port
num_players = args.num_players
random.seed(args.rng)  # Important
color = args.color

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((host, port))


# Given a message from the server, parses it and returns state and action


def parse_state_message(msg):
    s = msg.split(";REWARD")
    s[0] = s[0].replace("Vec2d", "")
    try:
        reward = float(s[1])
    except:
        reward = 0
    state = ast.literal_eval(s[0])
    return state, reward
queen=0


def agent_1player(state):
    global queen
    flag = 1
    # print state
    try:
        state, reward = parse_state_message(state)  # Get the state and reward
    except:
        pass


    check=0
   
    cover=0
    white=state["White_Locations"]
    red=state["Red_Location"]
    black=state["Black_Locations"]
    if(queen==0 and red==[]):
        queen=1
    elif(queen==1 and red==[]):
        queen=2
    elif(queen==1 and red!=[]):
        queen=0
    tried=0

    if(red!=[] and red[0][1]>170):
        #print("try queen")
        tan_angle=(755.9-red[0][1])/(red[0][0]-44.1)
       
        if(tan_angle<4.8 and tan_angle>1):
            print("try queen")
            print("tan_angle")
            print(tan_angle)
            angle=np.rad2deg(np.arctan(tan_angle))
            pos=(615.9/tan_angle+44.1-170.0)/(630.0-170.0)
            if(pos>1):
                pos=1
            x=pos*(630.0-170.0)
            y=755.9-140.0

            force=force_from_pos(x,y)
            #force=np.sqrt(x*x+y*y)/(3.5*2000)
            a=str(pos)+','+str(180-angle)+','+str(force)
            check=1
            tried=1
        


    elif(red==[] and queen==1):
        tan_angle=(755.9-white[0][1])/(white[0][0]-44.1)
        if(tan_angle<4.8 and tan_angle >1):
            print("try cover")
            print("tan_angle")
            print(tan_angle)
            angle=np.rad2deg(np.arctan(tan_angle))
            pos=(615.9/tan_angle+44.1-170.0)/(630.0-170.0)
            if(pos>1):
                pos=1
            x=pos*(630.0-170.0)
            y=755.9-140.0
            force=force_from_pos(x,y)
            #force=np.sqrt(x*x+y*y)/(3.5*2000)
            a=str(pos)+','+str(180-angle)+','+str(force)
            check=1
            tried=1


    if(white!=[] and tried==0):
        i=0
        while(i<len(white) and check==0):
            print(i)

            tan_angle=(755.9-white[i][1])/(white[i][0]-44.1)
            if(tan_angle<4.8 and tan_angle >=1.0 and white[i][1]>170.0):
                print("try white left")
                print("tan_angle")
                print(tan_angle)
                angle=np.rad2deg(np.arctan(tan_angle))
                pos=(615.9/tan_angle+44.1-170.0)/(630.0-170.0)
                if(pos>1):
                    pos=1
                x=615.9/tan_angle
                y=755.9-140.0
                scale_x=(white[i][0]-x-44.1)
                scale_y=white[i][1]-140.0
                force=force_from_pos(x,y)
                #force=np.sqrt(x*x+y*y)/(3.5*2000)
                #force=min(np.sqrt(x*x+y*y)/(3.5*2000)/np.sqrt(scale_x*scale_x+scale_y*scale_y)*400,0.09)
                a=str(pos)+','+str(180-angle)+','+str(force)
                check=1
            
            tan_angle=(755.9-white[i][1])/(755.9-white[i][0])
            if(tan_angle<4.8 and tan_angle >=1.0 and white[i][1]>170.0 and check==0):
                print("try white right")
                print("tan_angle")
                print(tan_angle)
                angle=np.rad2deg(np.arctan(tan_angle))
                pos=1.0-((615.9/tan_angle-125.9)/(630.0-170.0))
                if(pos>1):
                    pos=1
                if(pos<0):
                    pos=0
                x=615.9/tan_angle
                y=755.9-140.0
                scale_x=((755.9-x)-white[i][0])
                scale_y=white[i][1]-170.0
                force=force_from_pos(x,y)
                #force=np.sqrt(x*x+y*y)/(3.5*2000)
                #force=min(np.sqrt(x*x+y*y)/(3.5*2000)/np.sqrt(scale_x*scale_x+scale_y*scale_y)*400,0.09)
                a=str(pos)+','+str(angle)+','+str(force)
                check=1
                
            i=i+1
            
    if(black!=[] and tried==0 and check==0):
        i=0
        while(i<len(black) and check==0):
            tan_angle=(755.9-black[i][1])/(black[i][0]-44.1)
            if(tan_angle<4.8 and tan_angle >1 and black[i][1]>170.0):
                print("try black left")
                print("tan_angle")
                print(tan_angle)
                angle=np.rad2deg(np.arctan(tan_angle))
                pos=(615.9/tan_angle+44.1-170.0)/(630.0-170.0)
                if(pos>1):
                    pos=1
                x=615.9/tan_angle
                y=755.9-140.0
                scale_x=(black[i][0]-x-44.1)
                scale_y=black[i][1]-170.0
                force=force_from_pos(x,y)
                #force=np.sqrt(x*x+y*y)/(3.5*2000)
                #force=min(np.sqrt(x*x+y*y)/(3.5*2000)/np.sqrt(scale_x*scale_x+scale_y*scale_y)*400,0.09)
                a=str(pos)+','+str(180.5-angle)+','+str(force)
                check=1

            tan_angle=(755.9-black[i][1])/(755.9-black[i][0])
            if(tan_angle<4.8 and tan_angle >=1.0 and black[i][1]>170.0 and check==0):
                print("try black right")
                print("tan_angle")
                print(tan_angle)
                angle=np.rad2deg(np.arctan(tan_angle))
                pos=1.0-((615.9/tan_angle-125.9)/(630.0-170.0))
                if(pos>1):
                    pos=1
                if(pos<0):
                    pos=0
                x=615.9/tan_angle
                y=755.9-140.0
                scale_x=((755.9-x)-black[i][0])
                scale_y=black[i][1]-170.0
                force=force_from_pos(x,y)
                #force=np.sqrt(x*x+y*y)/(3.5*2000)
                #force=min(np.sqrt(x*x+y*y)/(3.5*2000)/np.sqrt(scale_x*scale_x+scale_y*scale_y)*400,0.09)
                a=str(pos)+','+str(angle)+','+str(force)
                check=1 
            i=i+1   
    if(check==0):
       
        if(white!=[]):
            i=0
            while(i<len(white) and check==0):
                tan_angle=(755.9-white[i][1])/(44.1-white[i][0])
                if(abs(tan_angle)>4.8 and white[i][1]>300):
                    print("try white leftmost")
                    dis=np.sqrt(pow((white[i][0]-44.1),2)+pow(755.9-white[i][1],2))
                    v_vel=np.sqrt(2*0.95*dis)
                    #print("v_vel:")
                    #print(v_vel)
                    line_angle=(white[i][1]-140.0)/(white[i][0]-170.0)
                    phi=abs((tan_angle-line_angle)/(1+tan_angle*line_angle))
                    theta=np.rad2deg(np.arctan(phi*0.35))
                    #print("theta:")
                    #print(theta)

                    angle=np.rad2deg(np.arctan(line_angle))+180+theta
                    
                    phi=np.rad2deg(np.arctan(phi))

                    u_vel=np.sqrt(pow(v_vel*np.cos(np.rad2deg(phi))/0.35,2)+pow(v_vel*np.sin(np.rad2deg(phi)),2))/2.8
                    #print("u_vel:")
                    #print(u_vel)
                    dis1=np.sqrt(pow((white[i][0]-170.0),2)+pow(140.0-white[i][1],2))
                    u_vel=np.sqrt(u_vel*u_vel+2*0.95*dis1)
                    alpha=np.rad2deg(np.arctan((white[i][1]-20.6-140.0)/(white[i][0]-170.0)))
                    #print(np.arctan(1))
                    #print(((white[i][1]-20.6-140.0))/(white[i][0]-170.0))
                    #print(np.arctan(((white[i][1]-20.6-140.0))/(white[i][0]-170.0)))
                    force=cut_force(white[i][0],170.0,white[i][1],140.0,alpha,20.6,15.01,phi,v_vel)
                    #force=(u_vel-17.15)/(378.5-17.15)
                    a=str(0.0)+','+str(180.0+alpha)+','+str(force)
                    check=1

                tan_angle=(755.9-white[i][1])/(755.9-white[i][0])
                if(abs(tan_angle)>4.8 and white[i][1]>300 and check==0):
                    print("try white rightmost")
                    dis=np.sqrt(pow((white[i][0]-755.9),2)+pow(755.9-white[i][1],2))
                    v_vel=np.sqrt(2*0.95*dis)
                    #print("v_vel:")
                    #print(v_vel)
                    line_angle=(white[i][1]-140.0)/(white[i][0]-630.0)
                    phi=abs((tan_angle-line_angle)/(1+tan_angle*line_angle))
                    theta=np.rad2deg(np.arctan(phi*0.35))
                    angle=np.rad2deg(np.arctan(line_angle))-theta
                    phi=np.rad2deg(np.arctan(phi))
                    u_vel=np.sqrt(pow(v_vel*np.cos(np.rad2deg(phi))/0.35,2)+pow(v_vel*np.sin(np.rad2deg(phi)),2))/2.8
                    #print("u_vel:")
                    #print(u_vel)
                    dis1=np.sqrt(pow((white[i][0]-630.0),2)+pow(140.0-white[i][1],2))
                    u_vel=np.sqrt(u_vel*u_vel+2*0.95*dis1)
                  
                    alpha=np.rad2deg(np.arctan((white[i][1]-20.6-140.0)/(white[i][0]-630.0)))
                    #print(((white[i][1]-20.6-140.0))/(white[i][0]-630.0))
                    
                    #print(np.arctan((white[i][1]-20.6-140.0))/(white[i][0]-630.0))
                    force=cut_force2(white[i][0],630.0,white[i][1],140.0,alpha,20.6,15.01,phi,v_vel)
                   
                    #force=(u_vel-17.15)/(378.5-17.15)
                    a=str(1.0)+','+str(alpha)+','+str(force)
                    check=1
                i=i+1
        if(black!=[]):
            i=0
            while(i<len(black) and check==0):
                tan_angle=(755.9-black[i][1])/(44.1-black[i][0])
                if(abs(tan_angle)>4.8 and black[i][1]>300):
                    print("try black leftmost")
                    dis=np.sqrt(pow((black[i][0]-44.1),2)+pow(755.9-black[i][1],2))
                    v_vel=np.sqrt(2*0.95*dis)
                    #print("v_vel:")
                    #print(v_vel)
                    line_angle=(black[i][1]-140.0)/(black[i][0]-170.0)
                    phi=abs((tan_angle-line_angle)/(1+tan_angle*line_angle))
                    theta=np.rad2deg(np.arctan(phi*0.35))
                    #print("theta:")
                    #print(theta)

                    angle=np.rad2deg(np.arctan(line_angle))+180+theta
                    
                    phi=np.rad2deg(np.arctan(phi))

                    u_vel=np.sqrt(pow(v_vel*np.cos(np.rad2deg(phi))/0.35,2)+pow(v_vel*np.sin(np.rad2deg(phi)),2))/2.8
                    #print("u_vel:")
                    #print(u_vel)
                    dis1=np.sqrt(pow((black[i][0]-170.0),2)+pow(140.0-black[i][1],2))
                    u_vel=np.sqrt(u_vel*u_vel+2*0.95*dis1)
                    alpha=np.rad2deg(np.arctan((black[i][1]-20.6-140.0)/(black[i][0]-170.0)))
                    #print(np.arctan(1))
                    #print(((white[i][1]-20.6-140.0))/(white[i][0]-170.0))
                    #print(np.arctan(((white[i][1]-20.6-140.0))/(white[i][0]-170.0)))
                    force=cut_force(black[i][0],170.0,black[i][1],140.0,alpha,20.6,15.01,phi,v_vel)
                    #force=(u_vel-17.15)/(378.5-17.15)
                    a=str(0.0)+','+str(180.0+alpha)+','+str(force)
                    check=1

                tan_angle=(755.9-black[i][1])/(755.9-black[i][0])
                if(abs(tan_angle)>4.8 and black[i][1]>300 and check==0):
                    print("try black rightmost")
                    dis=np.sqrt(pow((black[i][0]-755.9),2)+pow(755.9-black[i][1],2))
                    v_vel=np.sqrt(2*0.95*dis)
                    #print("v_vel:")
                    #print(v_vel)
                    line_angle=(black[i][1]-140.0)/(black[i][0]-630.0)
                    phi=abs((tan_angle-line_angle)/(1+tan_angle*line_angle))
                    theta=np.rad2deg(np.arctan(phi*0.35))
                    angle=np.rad2deg(np.arctan(line_angle))-theta
                    phi=np.rad2deg(np.arctan(phi))
                    u_vel=np.sqrt(pow(v_vel*np.cos(np.rad2deg(phi))/0.35,2)+pow(v_vel*np.sin(np.rad2deg(phi)),2))/2.8
                    #print("u_vel:")
                    #print(u_vel)
                    dis1=np.sqrt(pow((black[i][0]-630.0),2)+pow(140.0-black[i][1],2))
                    u_vel=np.sqrt(u_vel*u_vel+2*0.95*dis1)
                  
                    alpha=np.rad2deg(np.arctan((black[i][1]-20.6-140.0)/(black[i][0]-630.0)))
                    #print(((white[i][1]-20.6-140.0))/(white[i][0]-630.0))
                    
                    #print(np.arctan((white[i][1]-20.6-140.0))/(white[i][0]-630.0))
                    force=cut_force2(black[i][0],630.0,black[i][1],140.0,alpha,20.6,15.01,phi,v_vel)
                   
                    #force=(u_vel-17.15)/(378.5-17.15)
                    a=str(1.0)+','+str(alpha)+','+str(force)
                    check=1
                i=i+1

            
        '''
        
        for i in range(0,len(black)):
            sum_x=sum_x+black[i][0]
            sum_y=sum_y+black[i][1]
        sum_x=sum_x/(len(white)+len(black)) 
        sum_y=sum_y/(len(white)+len(black)) 
        if(sum_y>600 or sum_y<145):
            a = str(0.5) + ',' + \
                str(90+random.randrange(-50, 50)) + ',' + str(1.0)

        if(sum_x<100 and sum_y<500):
             a = str(0.5) + ',' + \
                str(160+random.randrange(-50, 50)) + ',' + str(1.0)
        elif(sum_x>600 and sum_y<500):
            a = str(0.5) + ',' + \
                str(20+random.randrange(-50, 50)) + ',' + str(1.0)
        else:
            if(white!=[]):
                tan_angle=(145-white[0][1])/((630.0+170.0)/2-white[0][0])
                angle=np.rad2deg(np.arctan(tan_angle))
                #force=min(np.sqrt(x*x+y*y)/(3.5*2000)/np.sqrt(scale_x*scale_x+scale_y*scale_y)*400,0.09)
                a=str(0.5)+','+str(angle)+','+str(0.75)
                check=1
            if(black!=[] and check==0):
                tan_angle=(145-black[0][1])/((630.0+170.0)/2-black[0][0])
                angle=np.rad2deg(np.arctan(tan_angle))
                #force=min(np.sqrt(x*x+y*y)/(3.5*2000)/np.sqrt(scale_x*scale_x+scale_y*scale_y)*400,0.09)
                a=str(0.5)+','+str(angle)+','+str(0.75)
                check=1
        '''

            
    
    if(check==0):
        a = str(0.5) + ',' + str(90.0+random.randrange(-20,20)) + ',' + str(1.0)

    try:
        s.send(a)
    except Exception as e:
        print "Error in sending:",  a, " : ", e
        print "Closing connection"
        flag = 0

    return flag


def agent_2player(state, color):

    flag = 1

   
    a = str(random.random()) + ',' + \
        str(random.randrange(-45, 225)) + ',' + str(random.random())

    try:
        s.send(a)
    except Exception as e:
        print "Error in sending:",  a, " : ", e
        print "Closing connection"
        flag = 0

    return flag


while 1:
    state = s.recv(1024)  # Receive state from server
    if num_players == 1:
        if agent_1player(state) == 0:
            break
    elif num_players == 2:
        if agent_2player(state, color) == 0:
            break
s.close()
