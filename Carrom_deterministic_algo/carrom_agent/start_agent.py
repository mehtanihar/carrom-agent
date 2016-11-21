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
    
    #print(X1)
    #print(Y1)
    #print(x1)
    #print(y1)
    #print(alpha)
   
    a1=X1-x1
    b1=Y1-y1
    a=1
    b=2*(a1*np.cos(np.deg2rad(alpha))+b1*np.sin(np.deg2rad(alpha)))
    c=pow(a1,2)+pow(b1,2)-pow(R+r1,2)
   
    #print(a)
    #print(b)
    #print(c)
    r=(-b+np.sqrt(pow(b,2)-4*a*c))/2
    x2=r*np.cos(np.deg2rad(alpha))+x1
    y2=r*np.sin(np.deg2rad(alpha))+y1
    tan=(y2-y1)/(x2-x1)
    phi=pcangle-np.deg2rad(np.arctan(tan))
    theta=alpha-np.deg2rad(np.arctan(tan))
    
    u=(0.35*v*np.cos(np.deg2rad(phi))*(3.8))/np.cos(np.deg2rad(theta))
    #print(r)
    return (u-17.149)/(378.5-17.149)/2.0



def cut_force(X1,x1,Y1,y1,alpha,R,r1,pcangle,v):
    #print(X1)
    #rint(Y1)
    ##print(x1)
    #print(y1)
    alpha=180+alpha
    #print(alpha)

    a1=X1-x1
    b1=Y1-y1
    a=1
    b=2*(a1*np.cos(np.deg2rad(alpha))+b1*np.sin(np.deg2rad(alpha)))
    c=pow(a1,2)+pow(b1,2)-pow(R+r1,2)
   
    #print(a)
    #print(b)
    #print(c)  
    r=(-b+np.sqrt(pow(b,2)-4*a*c))/2
    #print(r)
    x2=r*np.cos(np.deg2rad(alpha))+x1
    y2=r*np.sin(np.deg2rad(alpha))+y1
    tan=(y2-y1)/(x2-x1)
    phi=pcangle-np.deg2rad(np.arctan(tan))
    theta=180.0-alpha-np.deg2rad(np.arctan(tan))
   
    u=(0.35*v*np.cos(np.deg2rad(phi))*(3.8))/np.cos(np.deg2rad(theta))
    #print(r)
    return (u-17.149)/(378.5-17.149)/2.0


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

def get_action_double_left_two_player(x,y):
	tan=(x-44.1)/((y-44.1)/0.35+(800.0*(73/75.0)-y)*(1+(1)))
	angle=np.rad2deg(np.arctan(tan))
	angle=90+angle
	m=-1/tan
	c=y-m*x
	l=(m,c)
	x=get(l)
	pos=(x-170.0)/460.0
	u=0.3
	m1=1/tan
	c1=44.1-m1*44.1
	l1=(m1,c1)
	if(pos<0 or pos>1):
		return -1
	return (pos,angle,u,l,l1)

def get_action_double_right_two_player(x,y):
	tan=(755.9-x)/((800.0*(73/75.0)-44.1) +800.0*(73/75.0)-y)
	angle=np.rad2deg(np.arctan(tan))
	angle=90-angle
	m=1/tan
	c=y-m*x
	l=(m,c)
	x=get(l)
	pos=(x-170)/460.0
	u=0.3
	m1=-1/tan
	c1=44.1-m1*755.9
	l1=(m1,c1)
	if(pos<0 or pos>1):
		return -1
	return (pos,angle,u,l,l1)


def get_action_double_left(x,y):
	tan=(x-44.1)/((y-44.1)/0.35+(800.0*(73/75.0)-y)*(1+(1)))
	angle=np.rad2deg(np.arctan(tan))
	angle=90+angle
	m=-1/tan
	c=y-m*x
	l=(m,c)
	x=get(l)
	pos=(x-170.0)/460.0
	u=1.0
	m1=1/tan
	c1=44.1-m1*44.1
	l1=(m1,c1)
	if(pos<0 or pos>1):
		return -1
	return (pos,angle,u,l,l1)

def get_action_double_right(x,y):
	tan=(755.9-x)/((800.0*(73/75.0)-44.1) +800.0*(73/75.0)-y)
	angle=np.rad2deg(np.arctan(tan))
	angle=90-angle
	m=1/tan
	c=y-m*x
	l=(m,c)
	x=get(l)
	pos=(x-170)/460.0
	u=1.0
	m1=-1/tan
	c1=44.1-m1*755.9
	l1=(m1,c1)
	if(pos<0 or pos>1):
		return -1
	return (pos,angle,u,l,l1)

def cut(check,red,white,black):
	if(check==0):  
		if(red!=[]):
			i=0
			while(i<len(red) and check==0):
				tan_angle=(755.9-red[i][1])/(44.1-red[i][0])
				if(abs(tan_angle)>4.8 and red[i][1]>300):
					#print("try red leftmost")
					dis=np.sqrt(pow((red[i][0]-44.1),2)+pow(755.9-red[i][1],2))
					v_vel=np.sqrt(2*0.95*dis)
					#print("v_vel:")
					#print(v_vel)
					line_angle=(red[i][1]-140.0)/(red[i][0]-170.0)
					phi=abs((tan_angle-line_angle)/(1+tan_angle*line_angle))
					theta=np.rad2deg(np.arctan(phi*0.35))
					#print("theta:")
					#print(theta)

					angle=np.rad2deg(np.arctan(line_angle))+180+theta

					phi=np.rad2deg(np.arctan(phi))

					u_vel=np.sqrt(pow(v_vel*np.cos(np.rad2deg(phi))/0.35,2)+pow(v_vel*np.sin(np.rad2deg(phi)),2))/2.8
					#print("u_vel:")
					#print(u_vel)
					dis1=np.sqrt(pow((red[i][0]-170.0),2)+pow(140.0-red[i][1],2))
					u_vel=np.sqrt(u_vel*u_vel+2*0.95*dis1)
					alpha=np.rad2deg(np.arctan((red[i][1]-20.6-140.0)/(red[i][0]-170.0)))
					#print(np.arctan(1))
					#print(((white[i][1]-20.6-140.0))/(white[i][0]-170.0))
					#print(np.arctan(((white[i][1]-20.6-140.0))/(white[i][0]-170.0)))
					force=cut_force(red[i][0],170.0,red[i][1],140.0,alpha,20.6,15.01,phi,v_vel)
					#force=(u_vel-17.15)/(378.5-17.15)
					a=str(0.0)+','+str(180.0+alpha)+','+str(force)
					
					check=1
					return a

				tan_angle=(755.9-red[i][1])/(755.9-red[i][0])
				if(abs(tan_angle)>4.8 and red[i][1]>300 and check==0):
					#print("try red rightmost")
					dis=np.sqrt(pow((red[i][0]-755.9),2)+pow(755.9-red[i][1],2))
					v_vel=np.sqrt(2*0.95*dis)
					#print("v_vel:")
					#print(v_vel)
					line_angle=(red[i][1]-140.0)/(red[i][0]-630.0)
					phi=abs((tan_angle-line_angle)/(1+tan_angle*line_angle))
					theta=np.rad2deg(np.arctan(phi*0.35))
					angle=np.rad2deg(np.arctan(line_angle))-theta
					phi=np.rad2deg(np.arctan(phi))
					u_vel=np.sqrt(pow(v_vel*np.cos(np.rad2deg(phi))/0.35,2)+pow(v_vel*np.sin(np.rad2deg(phi)),2))/2.8
					#print("u_vel:")
					#print(u_vel)
					dis1=np.sqrt(pow((red[i][0]-630.0),2)+pow(140.0-red[i][1],2))
					u_vel=np.sqrt(u_vel*u_vel+2*0.95*dis1)

					alpha=np.rad2deg(np.arctan((red[i][1]-20.6-140.0)/(red[i][0]-630.0)))
					#print(((white[i][1]-20.6-140.0))/(white[i][0]-630.0))

					#print(np.arctan((white[i][1]-20.6-140.0))/(white[i][0]-630.0))
					force=cut_force2(red[i][0],630.0,red[i][1],140.0,alpha,20.6,15.01,phi,v_vel)

					#force=(u_vel-17.15)/(378.5-17.15)
					a=str(1.0)+','+str(alpha)+','+str(force)
					check=1
					return a 

				i=i+1

		if(white!=[]):
			i=0
			while(i<len(white) and check==0):
				tan_angle=(755.9-white[i][1])/(44.1-white[i][0])
				if(abs(tan_angle)>4.8 and white[i][1]>300):
					#print("try white leftmost")
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
					return a

				tan_angle=(755.9-white[i][1])/(755.9-white[i][0])
				if(abs(tan_angle)>4.8 and white[i][1]>300 and check==0):
					#print("try white rightmost")
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
					return a 

				i=i+1

		if(black!=[] and check==0):
			i=0
			while(i<len(black) and check==0):
				tan_angle=(755.9-black[i][1])/(44.1-black[i][0])
				if(abs(tan_angle)>4.8 and black[i][1]>300):
					#print("try black leftmost")
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
					return a

				tan_angle=(755.9-black[i][1])/(755.9-black[i][0])
				if(abs(tan_angle)>4.8 and black[i][1]>300 and check==0):
					#print("try black rightmost")
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
					return a
				i=i+1
	if(check==0):
		return -1














	
def parse_state_message(msg):
    s = msg.split(";REWARD")
    s[0] = s[0].replace("Vec2d", "")
    try:
        reward = float(s[1])
    except:
        reward = 0
    state = ast.literal_eval(s[0])
    return state, reward
def line(coin,pocket):
	m=(pocket[1]-coin[1])/(pocket[0]-coin[0])
	c=pocket[1]-m*pocket[0]
	return (m,c)

def get(l):
	return (140-l[1])/l[0]

def get_refl(l,Y_r):
	m=-1*l[0]
	y1=Y_r
	x1=(y1-l[1])/l[0]
	c1=y1-m*x1
	return (m,c1)
	
def get_xrefl(l,X_r):
	m=-1*l[0]
	x1=X_r
	y1=l[0]*X_r+l[1]
	c1=y1-m*x1
	return (m,c1)
def isfree(l,coin,coins):
	n=0
	for x in coins:
		if(x!=coin):
			dis=abs(x[1]-l[0]*x[0]-l[1])/(np.sqrt(1+pow(l[0],2)))
			if(dis<35.0 and (x[1]-140.0)*(coin[1]-140.0)>=0):
				n=n+1
	return n
def strikerfree(pos,state):
	coins=[]
	white=state["White_Locations"]
	red=state["Red_Location"]
	black=state["Black_Locations"]
	if(red!=[]):
		coins.append(red[0])
	for coin in white :
		coins.append(coin)
	for coin in black :
		coins.append(coin)
	for coin in coins:
		if(np.sqrt(pow(170+460*pos-coin[0],2)+pow(coin[1]-140,2))<36):
			return False
	return True
def agent_1player(state):
	check=0
	flag = 1
	# print state

	if(not state):
		return 0

	try:
	    state, reward = parse_state_message(state)  # Get the state and reward
	except:
	    pass
	

	coins=[]
	white=state["White_Locations"]
	red=state["Red_Location"]
	black=state["Black_Locations"]
	if(red!=[]):
		coins.append(red[0])
	for coin in white :
		coins.append(coin)
	for coin in black :
		coins.append(coin)
	if(red!=[] and len(coins)<=3):
		coins=[coins[0]]
	pockets= [(44.1, 44.1), (755.9, 44.1), (755.9, 755.9), (44.1, 755.9)]
	max_a=0
	n=0
	p=0
	for coin in coins:
		if(check!=1):
			for pocket in pockets:
				l=line(coin,pocket)
				if(pocket==pockets[3]):
						if(l[0]>-4.89 and l[0]<-1.05 and coin[1]>173):
							x=get(l)
							pos=(x-170.0)/460.0
							angle=180.0+np.rad2deg(np.arctan(l[0]))
							v=np.sqrt(1.9*np.sqrt(pow(x-pocket[0],2)+pow(140.0-pocket[1],2)))
							force=(v-17.149)/(378.5-17.149)
							force=max(0,force-0.005)
							a=str(pos)+','+str(angle)+','+str(force)
							k=isfree(l,coin,coins)
							if(k==0 and pos<=1 and pos>=0 and strikerfree(pos,state)):
								check=1
								print("3sure")
							 	break
							else:
								if(k>n and pos<=1 and pos>=0 and strikerfree(pos,state)):
									max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
									n=k
									p="3suremany"
						elif(l[0]>-1.05 and coin[1]>170):
							Y_r=(800.0/75.0)*73.0;
							l1=get_refl(l,Y_r)
							x=get(l1)
							pos=(x-170.0)/460.0
							angle=np.rad2deg(np.arctan(l1[0]))
							dt=(1600.0*(73/75.0)-x-44.1)/np.cos(np.deg2rad(angle))
							dt=abs(dt)
							v=np.sqrt(1.9*dt)
							force=(v-17.149)/(378.5-17.149)
							force=max(0,force-0.005)
							a=str(pos)+','+str(angle)+','+str(force)
							k=isfree(l,coin,coins)+isfree(l1,coin,coins)
							if(k==0 and pos<=1 and pos>=0 and strikerfree(pos,state)):
								check=1
								print("3ref")
								break
							else:
								if(k>n and pos<=1 and pos>=0 and strikerfree(pos,state)):
									max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
									n=k
									p="3refmany"
						elif(l[0]<-4.88 and coin[1]>170):
							X_r=(2/75.0)*800.0
							l1=get_xrefl(l,X_r)
							x=get(l1)
							if(x<=630 and x>=170):
								pos=(x-170.0)/460.0
								angle=np.rad2deg(np.arctan(l1[0]))
								force=0.3
								a=str(pos)+','+str(180+angle)+','+str(force)
								k=isfree(l,coin,coins)+isfree(l1,coin,coins)
								if(k==0  and strikerfree(pos,state) and 180+angle<225):
									check=1
									print("3ref")
									break
								else:
									if(k>n  and strikerfree(pos,state) and 180+angle<225):
										max_a=str(pos)+','+str(180+angle)+','+str(min(force+force*0.35,1))
										n=k
									p="3refmany"
							else:
								X_r=(73/75.0)*800.0
								l2=get_xrefl(l1,X_r)
								x=get(l2)
								if(x<=630 and x>=170):
									pos=(x-170.0)/460.0
									angle=180+np.rad2deg(np.arctan(l2[0]))
									force=1
									a=str(pos)+','+str(180+angle)+','+str(force)
									k=isfree(l,coin,coins)+isfree(l1,coin,coins)+isfree(l2,coin,coins)
									if(k==0 and strikerfree(pos,state)):
										check=1
										print("3ref")
										break
									else:
										if(k>n and strikerfree(pos,state)):
											max_a=str(pos)+','+str(180+angle)+','+str(min(force+force*0.35,1))
											n=k
											p="3refmany"
				if(pocket==pockets[2]):
				    if(l[0]>1.04 and l[0]<4.88 and coin[1]>173):
					    x=get(l)
					    pos=(x-170.0)/460.0
					    angle=np.rad2deg(np.arctan(l[0]))
					    v=np.sqrt(1.9*np.sqrt(pow(x-pocket[0],2)+pow(140.0-pocket[1],2)))
					    force=(v-17.149)/(378.5-17.149)
					    force=max(0,force-0.005)
					    a=str(pos)+','+str(angle)+','+str(force)
					    k=isfree(l,coin,coins)
					    if(k==0 and pos<=1 and pos>=0 and strikerfree(pos,state)):
						    check=1
						    print("2sure")
						    break
					    else:
						    if(k>n and pos<=1 and pos>=0 and strikerfree(pos,state)):
							    max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
							    n=k
							    p="2suremany"
				    elif(l[0]<1.04 and coin[1]>170):
					    Y_r=(800.0/75.0)*2.0;
					    l1=get_refl(l,Y_r)
					    x=get(l1)
					    pos=(x-170.0)/460.0
					    angle=180+np.rad2deg(np.arctan(l1[0]))
					    dt=(-2*800.0*(73.0/75.0)+coin[0]+755.9)/np.cos(np.deg2rad(angle))
					    dt=abs(dt)
					    v=np.sqrt(1.9*dt)
					    force=(v-17.149)/(378.5-17.149)
					    force=max(0,force-0.005)
					    a=str(pos)+','+str(angle)+','+str(force)
					    k=isfree(l,coin,coins)+isfree(l1,coin,coins)
					    if(k==0 and pos<=1 and pos>=0 and strikerfree(pos,state)):
						    check=1
						    #("2ref")
						    break
					    else:
						    if(k>n and pos<=1 and pos>=0 and strikerfree(pos,state)):
							    max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
							    n=k
							    p="2refmany"
				    elif(l[0]>4.88 and coin[1]>170):
				        X_r=(2/75.0)*800.0
				        l1=get_xrefl(l,X_r)
				        x=get(l1)
				        if(x<=630 and x>=170):
							pos=(x-170.0)/460.0
							angle=np.rad2deg(np.arctan(l1[0]))
							force=0.3
							a=str(pos)+','+str(angle)+','+str(force)
							k=isfree(l,coin,coins)+isfree(l1,coin,coins)
							if(k==0 and strikerfree(pos,state) and angle>-45):
							    check=1
							    print("2ref")
							    break
							else:
							    if(k>n and strikerfree(pos,state) and angle>-45):
							        max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
							        n=k
							        p="2refmany"
				        else:
				            X_r=(73/75.0)*800.0
				            l2=get_xrefl(l1,X_r)
				            x=get(l2)
				            if(x<=630 and x>=170):
								pos=(x-170.0)/460.0
								angle=np.rad2deg(np.arctan(l2[0]))
								force=1
								a=str(pos)+','+str(angle)+','+str(force)
								k=isfree(l,coin,coins)+isfree(l1,coin,coins)+isfree(l2,coin,coins)
								if(k==0 and strikerfree(pos,state)):
								    check=1
								    print("2ref")
								    break
								else:
								    if(k>n and strikerfree(pos,state)):
								        max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
								        n=k
								        p="2refmany"    
				if(pocket==pockets[0]):
				    if(l[0]>0.168 and l[0]<.762 and coin[1]<107):
					    x=get(l)
					    pos=(x-170.0)/460.0
					    angle=180+np.rad2deg(np.arctan(l[0]))
					    v=np.sqrt(1.9*np.sqrt(pow(x-pocket[0],2)+pow(140-pocket[1],2)))
					    force=(v-17.149)/(378.5-17.149)
					    force=max(0,force-0.005)
					    a=str(pos)+','+str(angle)+','+str(force)
					    k=isfree(l,coin,coins)
					    if(k==0 and pos<=1 and pos>=0 and strikerfree(pos,state)):
						    check=1
						    print("0sure")
						    break
					    else:
						    if(k>n and pos<=1 and pos>=0 and strikerfree(pos,state)):
							    max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
							    n=k
							    p="0suremany"
				    if(l[0]>0.762):
					    X_r=(73/75.0)*800.0
					    l1=get_xrefl(l,X_r)
					    x=get(l1)
					    pos=(x-170)/460
					    angle=180-np.rad2deg(np.arctan(l[0]))
					    dt=(2*800.0*(73/75.0)-140-44.1)/np.sin(np.deg2rad(angle))
					    dt=abs(dt)
					    v=np.sqrt(1.9*dt)
					    force=(v-17.149)/(378.5-17.149)
					    force=max(0,force-0.005)
					    a=str(pos)+','+str(angle)+','+str(force)
					    k=isfree(l,coin,coins)+isfree(l1,coin,coins)
					    if(k==0 and pos<=1 and pos>=0 and strikerfree(pos,state)):
						    check=1
						    print("0ref")
						    break
					    else:
						    if(k>n and pos<=1 and pos>=0 and strikerfree(pos,state)):
							    max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
							    n=k
							    p="0refmany"
				if(pocket==pockets[1]):
				    if(l[0]>-0.762 and l[0]<-0.163 and coin[1]<107):
					    x=get(l)
					    pos=(x-170.0)/460.0
					    angle=np.rad2deg(np.arctan(l[0]))
					    v=np.sqrt(1.9*(np.sqrt(pow(x-pocket[0],2)+pow(140-pocket[1],2))))
					    force=(v-17.149)/(378.5-17.149)
					    force=max(0,force-0.005)
					    a=str(pos)+','+str(angle)+','+str(force)
					    k=isfree(l,coin,coins)
					    if(k==0 and pos<=1 and pos>=0 and strikerfree(pos,state)):
						    check=1
						    print("1sure")
						    break
					    else:
						    if(k>n and pos<=1 and pos>=0 and strikerfree(pos,state)):
							    max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
							    n=k
							    p="1suremany"
				    elif(l[0]<-0.762):
					    X_r=(73/75.0)*800.0
					    l1=get_xrefl(l,X_r)
					    x=get(l1)
					    pos=(x-170)/460
					    angle=np.rad2deg(np.arctan(l[0]))
					    dt=(2*800.0*(73/75.0)-140-44.1)/np.sin(np.deg2rad(angle))
					    dt=abs(dt)
					    v=np.sqrt(1.9*dt)
					    force=(v-17.149)/(378.5-17.149)
					    force=max(0,force-0.005)
					    a=str(pos)+','+str(angle)+','+str(force)
					    k=isfree(l,coin,coins)+isfree(l1,coin,coins)
					    if(k==0 and pos<=1 and pos>=0 and strikerfree(pos,state)):
						    check=1
						    print("1ref")
						    break
					    else:
						    if(k>n and pos<=1 and pos>=0 and strikerfree(pos,state)):
							    max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
							    n=k
							    p="1refmany"
		else:
			break
	
	'''
	if(check==0):
		a=cut(check,red,white,black)
		print(a)
		check=0
		if(a!=-1):
			check=1
	'''
	
	for coin in coins:				

		if(check==0):
			act=get_action_double_left(coin[0],coin[1])
			if(act!=-1 and coin[1]>170):
				k=isfree(act[3],coin,coins)+isfree(act[4],coin,coins)
				if(k==0 and strikerfree(act[0],state)):
				    a=str(act[0])+','+str(act[1])+','+str(act[2])
				    check=1
				    print("0double ",coin)
				    break
				else:
					if(k>n and strikerfree(act[0],state)):
					    max_a=str(act[0])+','+str(act[1])+','+str(min(act[2]+act[2]*0.35,1))
					    n=k
					    p="0doublemany "+str(coin)
		if(check==0):
			act=get_action_double_right(coin[0],coin[1])
			if(act!=-1 and coin[1]>170):
				k=isfree(act[3],coin,coins)+isfree(act[4],coin,coins)
				if(k==0 and strikerfree(act[0],state)):
				    a=str(act[0])+','+str(act[1])+','+str(act[2])
				    check=1
				    print("1double ",coin)
				    break
				else:
					if(k>n and strikerfree(act[0],state)):
						max_a=str(act[0])+','+str(act[1])+','+str(min(act[2]+act[2]*0.35,1))
						n=k
						p="1doublemany "+str(coin)

	

	if(check==0):
		if(max_a!=0):
			a = max_a
			check=1
			print p
		else:
			for coin in coins:	
				x=170
				if(coin[1]>140):
					while(not strikerfree((x-170.0)/460.0,state)):
						x=x+30
					l=line(coin,(x,140))
					angle=np.rad2deg(np.arctan(l[0]))
					if(l[0]<0):
						angle=180+angle
					a=str((x-170.0)/460.0)+','+str(angle)+','+str(1)
					check=1
					break
				else:
					angle=-90
					x=140
					while(angle>225 or angle<-45):
						x=x+30
						l=line(coin,(x,140))
						angle=np.rad2deg(np.arctan(l[0]))
						if(l[0]>0):
							angle=180+angle	
					a=str((x-170.0)/460.0)+','+str(angle)+','+str(1)
					check=1
					break
		if(check==0):
			a=str(random.random())+','+str(random.randrange(-45,225))+','+str(random.random())
	try:
		s.send(a)
	except Exception as e:
		print "Error in sending:",  a, " : ", e
		print "Closing connection"
		flag = 0

	return flag


def agent_2player(state, color):
	check=0
	flag = 1
	if(not state):
		return 0

	try:
	    state, reward = parse_state_message(state)  # Get the state and reward
	except:
	    pass
	

	coins=[]
	white=state["White_Locations"]
	red=state["Red_Location"]
	black=state["Black_Locations"]


	if(red!=[]):
		coins.append(red[0])
	
	if(color=="White"):
		for coin in white :
			coins.append(coin)
	
	if(color=="Black"):
		for coin in black :
			coins.append(coin)
	
	if(red!=[] and len(coins)<=3):
		coins=[coins[0]]
	
	pockets= [(44.1, 44.1), (755.9, 44.1), (755.9, 755.9), (44.1, 755.9)]
	max_a=0
	n=0
	p=0
	for coin in coins:
		if(check!=1):
			for pocket in pockets:
				l=line(coin,pocket)
				if(pocket==pockets[3]):
						if(l[0]>-4.89 and l[0]<-1.05 and coin[1]>173):
							x=get(l)
							pos=(x-170.0)/460.0
							angle=180.0+np.rad2deg(np.arctan(l[0]))
							v=np.sqrt(1.9*np.sqrt(pow(x-pocket[0],2)+pow(140.0-pocket[1],2)))
							force=(v-17.149)/(378.5-17.149)
							force=max(0,force-0.005)
							a=str(pos)+','+str(angle)+','+str(force)
							k=isfree(l,coin,coins)
							if(k==0 and pos<=1 and pos>=0 and strikerfree(pos,state)):
								check=1
								#print("3sure")
							 	break
							else:
								if(k>n and pos<=1 and pos>=0 and strikerfree(pos,state)):
									max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
									n=k
									p="3suremany"
						elif(l[0]>-1.05 and coin[1]>170):
							Y_r=(800.0/75.0)*73.0;
							l1=get_refl(l,Y_r)
							x=get(l1)
							pos=(x-170.0)/460.0
							angle=np.rad2deg(np.arctan(l1[0]))
							dt=(1600.0*(73/75.0)-x-44.1)/np.cos(np.deg2rad(angle))
							dt=abs(dt)
							v=np.sqrt(1.9*dt)
							force=(v-17.149)/(378.5-17.149)
							force=max(0,force-0.005)
							a=str(pos)+','+str(angle)+','+str(force)
							k=isfree(l,coin,coins)+isfree(l1,coin,coins)
							if(k==0 and pos<=1 and pos>=0 and strikerfree(pos,state)):
								check=1
								#print("3ref")
								break
							else:
								if(k>n and pos<=1 and pos>=0 and strikerfree(pos,state)):
									max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
									n=k
									p="3refmany"
						elif(l[0]<-4.88 and coin[1]>170):
							X_r=(2/75.0)*800.0
							l1=get_xrefl(l,X_r)
							x=get(l1)
							if(x<=630 and x>=170):
								pos=(x-170.0)/460.0
								angle=np.rad2deg(np.arctan(l1[0]))
								force=0.3
								a=str(pos)+','+str(180+angle)+','+str(force)
								k=isfree(l,coin,coins)+isfree(l1,coin,coins)
								if(k==0  and strikerfree(pos,state) and 180+angle<225):
									check=1
									#print("3ref")
									break
								else:
									if(k>n  and strikerfree(pos,state) and 180+angle<225):
										max_a=str(pos)+','+str(180+angle)+','+str(min(force+force*0.35,1))
										n=k
									p="3refmany"
							else:
								X_r=(73/75.0)*800.0
								l2=get_xrefl(l1,X_r)
								x=get(l2)
								if(x<=630 and x>=170):
									pos=(x-170.0)/460.0
									angle=180+np.rad2deg(np.arctan(l2[0]))
									force=1
									a=str(pos)+','+str(180+angle)+','+str(force)
									k=isfree(l,coin,coins)+isfree(l1,coin,coins)+isfree(l2,coin,coins)
									if(k==0 and strikerfree(pos,state)):
										check=1
										#print("3ref")
										break
									else:
										if(k>n and strikerfree(pos,state)):
											max_a=str(pos)+','+str(180+angle)+','+str(min(force+force*0.35,1))
											n=k
											p="3refmany"
				if(pocket==pockets[2]):
				    if(l[0]>1.04 and l[0]<4.88 and coin[1]>173):
					    x=get(l)
					    pos=(x-170.0)/460.0
					    angle=np.rad2deg(np.arctan(l[0]))
					    v=np.sqrt(1.9*np.sqrt(pow(x-pocket[0],2)+pow(140.0-pocket[1],2)))
					    force=(v-17.149)/(378.5-17.149)
					    force=max(0,force-0.005)
					    a=str(pos)+','+str(angle)+','+str(force)
					    k=isfree(l,coin,coins)
					    if(k==0 and pos<=1 and pos>=0 and strikerfree(pos,state)):
						    check=1
						    #print("2sure")
						    break
					    else:
						    if(k>n and pos<=1 and pos>=0 and strikerfree(pos,state)):
							    max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
							    n=k
							    p="2suremany"
				    elif(l[0]<1.04 and coin[1]>170):
					    Y_r=(800.0/75.0)*2.0;
					    l1=get_refl(l,Y_r)
					    x=get(l1)
					    pos=(x-170.0)/460.0
					    angle=180+np.rad2deg(np.arctan(l1[0]))
					    dt=(-2*800.0*(73.0/75.0)+coin[0]+755.9)/np.cos(np.deg2rad(angle))
					    dt=abs(dt)
					    v=np.sqrt(1.9*dt)
					    force=(v-17.149)/(378.5-17.149)
					    force=max(0,force-0.005)
					    a=str(pos)+','+str(angle)+','+str(force)
					    k=isfree(l,coin,coins)+isfree(l1,coin,coins)
					    if(k==0 and pos<=1 and pos>=0 and strikerfree(pos,state)):
						    check=1
						    #("2ref")
						    break
					    else:
						    if(k>n and pos<=1 and pos>=0 and strikerfree(pos,state)):
							    max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
							    n=k
							    p="2refmany"
				    elif(l[0]>4.88 and coin[1]>170):
				        X_r=(2/75.0)*800.0
				        l1=get_xrefl(l,X_r)
				        x=get(l1)
				        if(x<=630 and x>=170):
							pos=(x-170.0)/460.0
							angle=np.rad2deg(np.arctan(l1[0]))
							force=0.3
							a=str(pos)+','+str(angle)+','+str(force)
							k=isfree(l,coin,coins)+isfree(l1,coin,coins)
							if(k==0 and strikerfree(pos,state) and angle>-45):
							    check=1
							    #print("2ref")
							    break
							else:
							    if(k>n and strikerfree(pos,state) and angle>-45):
							        max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
							        n=k
							        p="2refmany"
				        else:
				            X_r=(73/75.0)*800.0
				            l2=get_xrefl(l1,X_r)
				            x=get(l2)
				            if(x<=630 and x>=170):
								pos=(x-170.0)/460.0
								angle=np.rad2deg(np.arctan(l2[0]))
								force=1
								a=str(pos)+','+str(angle)+','+str(force)
								k=isfree(l,coin,coins)+isfree(l1,coin,coins)+isfree(l2,coin,coins)
								if(k==0 and strikerfree(pos,state)):
								    check=1
								    #print("2ref")
								    break
								else:
								    if(k>n and strikerfree(pos,state)):
								        max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
								        n=k
								        p="2refmany"    
				if(pocket==pockets[0]):
				    if(l[0]>0.168 and l[0]<.762 and coin[1]<107):
					    x=get(l)
					    pos=(x-170.0)/460.0
					    angle=180+np.rad2deg(np.arctan(l[0]))
					    v=np.sqrt(1.9*np.sqrt(pow(x-pocket[0],2)+pow(140-pocket[1],2)))
					    force=(v-17.149)/(378.5-17.149)
					    force=max(0,force-0.005)
					    a=str(pos)+','+str(angle)+','+str(force)
					    k=isfree(l,coin,coins)
					    if(k==0 and pos<=1 and pos>=0 and strikerfree(pos,state)):
						    check=1
						    #print("0sure")
						    break
					    else:
						    if(k>n and pos<=1 and pos>=0 and strikerfree(pos,state)):
							    max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
							    n=k
							    p="0suremany"
				    if(l[0]>0.762):
					    X_r=(73/75.0)*800.0
					    l1=get_xrefl(l,X_r)
					    x=get(l1)
					    pos=(x-170)/460
					    angle=180-np.rad2deg(np.arctan(l[0]))
					    dt=(2*800.0*(73/75.0)-140-44.1)/np.sin(np.deg2rad(angle))
					    dt=abs(dt)
					    v=np.sqrt(1.9*dt)
					    force=(v-17.149)/(378.5-17.149)
					    force=max(0,force-0.005)
					    a=str(pos)+','+str(angle)+','+str(force)
					    k=isfree(l,coin,coins)+isfree(l1,coin,coins)
					    if(k==0 and pos<=1 and pos>=0 and strikerfree(pos,state)):
						    check=1
						    #print("0ref")
						    break
					    else:
						    if(k>n and pos<=1 and pos>=0 and strikerfree(pos,state)):
							    max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
							    n=k
							    p="0refmany"
				if(pocket==pockets[1]):
				    if(l[0]>-0.762 and l[0]<-0.163 and coin[1]<107):
					    x=get(l)
					    pos=(x-170.0)/460.0
					    angle=np.rad2deg(np.arctan(l[0]))
					    v=np.sqrt(1.9*(np.sqrt(pow(x-pocket[0],2)+pow(140-pocket[1],2))))
					    force=(v-17.149)/(378.5-17.149)
					    force=max(0,force-0.005)
					    a=str(pos)+','+str(angle)+','+str(force)
					    k=isfree(l,coin,coins)
					    if(k==0 and pos<=1 and pos>=0 and strikerfree(pos,state)):
						    check=1
						    #print("1sure")
						    break
					    else:
						    if(k>n and pos<=1 and pos>=0 and strikerfree(pos,state)):
							    max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
							    n=k
							    p="1suremany"
				    elif(l[0]<-0.762):
					    X_r=(73/75.0)*800.0
					    l1=get_xrefl(l,X_r)
					    x=get(l1)
					    pos=(x-170)/460
					    angle=np.rad2deg(np.arctan(l[0]))
					    dt=(2*800.0*(73/75.0)-140-44.1)/np.sin(np.deg2rad(angle))
					    dt=abs(dt)
					    v=np.sqrt(1.9*dt)
					    force=(v-17.149)/(378.5-17.149)
					    force=max(0,force-0.005)
					    a=str(pos)+','+str(angle)+','+str(force)
					    k=isfree(l,coin,coins)+isfree(l1,coin,coins)
					    if(k==0 and pos<=1 and pos>=0 and strikerfree(pos,state)):
						    check=1
						   # print("1ref")
						    break
					    else:
						    if(k>n and pos<=1 and pos>=0 and strikerfree(pos,state)):
							    max_a=str(pos)+','+str(angle)+','+str(min(force+force*0.35,1))
							    n=k
							    p="1refmany"
		else:
			break
	
	'''
	if(check==0):
		a=cut(check,red,white,black)
		print(a)
		check=0
		if(a!=-1):
			check=1
	'''
	
	for coin in coins:				

		if(check==0):
			act=get_action_double_left_two_player(coin[0],coin[1])
			if(act!=-1 and coin[1]>170):
				k=isfree(act[3],coin,coins)+isfree(act[4],coin,coins)
				if(k==0 and strikerfree(act[0],state)):
				    a=str(act[0])+','+str(act[1])+','+str(act[2])
				    check=1
				   # print("0double ",coin)
				    break
				else:
					if(k>n and strikerfree(act[0],state)):
					    max_a=str(act[0])+','+str(act[1])+','+str(min(act[2]+act[2]*0.35,1))
					    n=k
					    p="0doublemany "+str(coin)
		if(check==0):
			act=get_action_double_right_two_player(coin[0],coin[1])
			if(act!=-1 and coin[1]>170):
				k=isfree(act[3],coin,coins)+isfree(act[4],coin,coins)
				if(k==0 and strikerfree(act[0],state)):
				    a=str(act[0])+','+str(act[1])+','+str(act[2])
				    check=1
				    #print("1double ",coin)
				    break
				else:
					if(k>n and strikerfree(act[0],state)):
						max_a=str(act[0])+','+str(act[1])+','+str(min(act[2]+act[2]*0.35,1))
						n=k
						p="1doublemany "+str(coin)

	

	if(check==0):
		if(max_a!=0):
			a = max_a
			check=1
			#print p
		else:
			for coin in coins:	
				x=170
				if(coin[1]>140):
					while(not strikerfree((x-170.0)/460.0,state)):
						x=x+30
					l=line(coin,(x,140))
					angle=np.rad2deg(np.arctan(l[0]))
					if(l[0]<0):
						angle=180+angle
					a=str((x-170.0)/460.0)+','+str(angle)+','+str(1)
					check=1
					break
				else:
					angle=-90
					x=140
					while(angle>225 or angle<-45):
						x=x+30
						l=line(coin,(x,140))
						angle=np.rad2deg(np.arctan(l[0]))
						if(l[0]>0):
							angle=180+angle	
					a=str((x-170.0)/460.0)+','+str(angle)+','+str(1)
					check=1
					break
	if(check==0):
		a=str(random.random())+','+str(random.randrange(-45,225))+','+str(random.random())


   

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
