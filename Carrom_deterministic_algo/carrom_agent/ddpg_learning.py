import numpy as np

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





#iterate through rows of X

def scalar_multiply(X,Y):
	#print(len(X))
	#print(len(X[0]))

	result=[[0 for j in range(len(X[0]))] for i in range(len(X))]
	
	for i in range(len(X)):
	   # iterate through columns of Y
	   for j in range(len(X[0])):
	   		result[i][j] = X[i][j] * Y

	#print(len(X))
	#print(len(X[0]))
	return result
def multiply(X,Y):
	
	
	result=[[0 for j in range(len(Y[0]))] for i in range(len(X))]
	#print(result)
	for i in range(len(X)):
	   # iterate through columns of Y
	   for j in range(len(Y[0])):
	       # iterate through rows of Y
	       for k in range(len(Y)):
	    
	        result[i][j]= result[i][j]+ (X[i][k] * Y[k][j])


	return result

def element_multiply(X,Y):
	result=[[0 for j in range(len(Y[0]))] for i in range(len(X))]
	
	for i in range(len(X)):
	   # iterate through columns of Y
	   for j in range(len(Y[0])):
	   		result[i][j] = X[i][j] * Y[i][j]

	return result

def element_subtract(X,Y):
	
	
	result=[[0 for j in range(len(Y[0]))] for i in range(len(X))]

	for i in range(len(X)):
	   # iterate through columns of Y
	   for j in range(len(Y[0])):
	   		result[i][j] = X[i][j] - Y[i][j]

	return result
def element_add(X,Y):
	result=[[0 for j in range(len(Y[0]))] for i in range(len(X))]
	
	for i in range(len(X)):
	   # iterate through columns of Y
	   for j in range(len(Y[0])):
	   		result[i][j] = X[i][j] + Y[i][j]

	return result
def get_action(curr_state,hidden_layers,theta):
	a=[]
	z=[]

	

		
	a.append(curr_state)

	for j in range(0,hidden_layers+1):
		#print(theta[j])
		#print(a[j])
		z.append(multiply(a[j],theta[j])) 
		a.append(np.tanh(z[j]))
	

	#print(a[hidden_layers_1+1])

	action=a[hidden_layers+1]
	

	return action


def get_value(state,action,hidden_layers,theta):
	
	curr_state=[[]]

	for i in range(0,38):
		curr_state[0].append(state[0][i])
	
	curr_state[0].append(action[0][0])
	curr_state[0].append(action[0][1])
	curr_state[0].append(action[0][2])
	
	a=[]
	a.append(curr_state)
	#print(current_state)

	for j in range(0,hidden_layers+1):
	    a.append(np.tanh(multiply(a[j],theta[j])))       
	    

	

	action=(a[hidden_layers+1][0][0])
	return action




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
def transpose(z):
	n=len(z)
	m=len(z[0])
	res=[]
	for i in range(0,m):
		r=[]
		for j in range(0,n):
			r.append(z[j][i])
		res.append(r)
	return res
def act(x):
	res=[]
	for i in range(0,len(x[0])):
		res.append(np.tanh(x[0][i]))
	return [res]
def getdiff(x):
	res=[]
	for i in range(0,len(x[0])):
		res.append(1-pow(x[0][i],2))
	return [res]
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


outputs_1=3
inputs_1=38
hidden_layers_1=1
hidden_units_1=[inputs_1,15,outputs_1]
alpha=0.001
outputs_2=1
inputs_2=41
hidden_layers_2=2
hidden_units_2=[inputs_2,15,15,outputs_2]

N=16


read_1 = open("theta_1.txt", "r")
read_2 = open("theta_2.txt", "r")
read_3 = open("theta_3.txt", "r")
read_4 = open("theta_4.txt", "r")

theta_1=[[],[]]
theta_2=[[],[],[]]
theta_3=[[],[]]
theta_4=[[],[],[]]


for i in range(0,38):
	theta_1[0].append([])
	for j in range(0,15):
		theta_1[0][i].append(float(read_1.readline()))


for i in range(0,15):
	theta_1[1].append([])
	for j in range(0,3):
		theta_1[1][i].append(float(read_1.readline()))


for i in range(0,41):
	theta_2[0].append([])
	for j in range(0,15):
		theta_2[0][i].append(float(read_2.readline()))
for i in range(0,15):
	theta_2[1].append([])
	for j in range(0,15):
		theta_2[1][i].append(float(read_2.readline()))
for i in range(0,15):
	theta_2[2].append([])
	for j in range(0,1):
		theta_2[2][i].append(float(read_2.readline()))


for i in range(0,38):
	theta_3[0].append([])
	for j in range(0,15):
		theta_3[0][i].append(float(read_3.readline()))
for i in range(0,15):
	theta_3[1].append([])
	for j in range(0,3):
		theta_3[1][i].append(float(read_3.readline()))


for i in range(0,41):
	theta_4[0].append([])
	for j in range(0,15):
		theta_4[0][i].append(float(read_4.readline()))
for i in range(0,15):
	theta_4[1].append([])
	for j in range(0,15):
		theta_4[1][i].append(float(read_4.readline()))
for i in range(0,15):
	theta_4[2].append([])
	for j in range(0,1):
		theta_4[2][i].append(float(read_4.readline()))


print(theta_1[0])
read_1.close()
read_2.close()
read_3.close()
read_4.close()

'''
theta_1=[]
theta_2=[]
theta_3=[]
theta_4=[]



for i in range(0,hidden_layers_1+1):
	theta_1.append([[random.random() for k in range(hidden_units_1[i+1])] for j in range(hidden_units_1[i])])


for i in range(0,hidden_layers_2+1):
	theta_2.append([[random.random() for k in range(hidden_units_2[i+1])] for j in range(hidden_units_2[i])])

for i in range(0,hidden_layers_1+1):
	theta_3.append([[random.random() for k in range(hidden_units_1[i+1])] for j in range(hidden_units_1[i])])


for i in range(0,hidden_layers_2+1):
	theta_4.append([[random.random() for k in range(hidden_units_2[i+1])] for j in range(hidden_units_2[i])])
'''





count=0
gamma=0.9
tau=0.001


def agent_1player(state):
	if(not state):
		return 0
	
	#print(theta_1)
	global outputs_1
	global inputs_1
	global hidden_layers_1
	global hidden_units_1
	global alpha
	global outputs_2
	global inputs_2
	global hidden_layers_2
	global hidden_units_2
	global tau
	global theta_1
	global theta_2
	global theta_3
	global theta_4
	global count
	global N
	global f
	global prev_state
	flag = 1
	# print state
	try:
	    state, reward = parse_state_message(state)  # Get the state and reward
	except:
	    pass


	check=0
	

	white=state["White_Locations"]
	black=state["Black_Locations"]
	red=state["Red_Location"]

	white_x=[] 
	white_y=[]
	
	for i in range(0,len(white)):
		white_x.append(white[i][0])
		white_y.append(white[i][1])
	white_x=sorted(white_x)
	white_y=sorted(white_y)
	print(white_y)

	black_x=[] 
	black_y=[]
	
	for i in range(0,len(black)):
		black_x.append(black[i][0])
		black_y.append(black[i][1])
	black_x=sorted(black_x)
	black_y=sorted(black_y)

	current_state=[[]]
	
	for i in range(0,len(red)):
		current_state[0].append((red[i][0]-400.0)/400.0)
		current_state[0].append((red[i][1]-400.0)/400.0)


	if(len(red)==0):
		current_state[0].append(1.0)
		current_state[0].append(1.0)

	for i in range(0,len(white)):
		current_state[0].append((white_x[i]-400.0)/400.0)
		current_state[0].append((white_y[i]-400.0)/400.0)

	if(len(white)<9):
		for i in range(0,9-len(white)):
			current_state[0].append(1.0)
			current_state[0].append(1.0)

	for i in range(0,len(black)):
		current_state[0].append((black_x[i]-400.0)/400.0)
		current_state[0].append((black_y[i]-400.0)/400.0)

	if(len(black)<9):
		for i in range(0,9-len(black)):
			current_state[0].append(1.0)
			current_state[0].append(1.0)

	#print(len(current_state[0]))
	
	state_check=0
	if(count>=1):
		
		f=open("episode.txt","a")		
		f.write(str(reward)+'\n')
		for i in range(0,38):
			f.write(str(current_state[0][i])+' ')
		f.write('\n')
		f.close()

		if(prev_state!=current_state):
			state_check=1
			
		


			#sample from R
			
			

			read=open("episode.txt",'r')
			num_lines = sum(1 for line in read)
			read.close()
			

		   	total_size=(num_lines)/4
		   	minibatch=[]
		   	if(total_size<=N):
		   		read=open("episode.txt",'r')
		   		for i in range(0,total_size):
		   			
		   				
		   			file_state_temp=read.readline()
		   			
		   			file_action=read.readline()
		   			file_reward=float(read.readline())
		   		
		   			file_next_state_temp=read.readline()
		   			file_state_temp = file_state_temp.split(" ")
		   			file_state=[]
		   			file_next_state=[]
		   			
		   			
		   			
		   			for j in range(0,38):
		   				file_state.append(float(file_state_temp[j]))
		   			

		   			file_next_state_temp= file_next_state_temp.split(" ")

		   			for j in range(0,38):
		   				file_next_state.append(float(file_next_state_temp[j]))

		   			file_action = file_action.split(" ")
		   			for j in range(0,3):
		   				file_action[j]=float(file_action[j])
		   			file_state=[file_state]
		   			file_action=[file_action]
		   			file_next_state=[file_next_state]
		   			
		   			transition=[]
		   			
		   			transition.append(file_state)
		   			transition.append(file_action)
		   			transition.append(file_reward)
		   			transition.append(file_next_state)
		   			minibatch.append(transition)
		   			
		   		read.close()
		   	else:
		   		
		   		arr1=random.sample(range(0,total_size),N)
		   		
		   	
		   		
		   		read=open("episode.txt",'r')
		   		file_whole=read.readlines()
		   		
		   		

	   			for i in range(0,N):
	   			
		   			file_state_temp=file_whole[arr1[i]*4]
		   			file_action=file_whole[arr1[i]*4+1]
		   			file_reward=float(file_whole[arr1[i]*4+2])
		   			file_next_state_temp=file_whole[arr1[i]*4+3]
		   			
		   			
		   			file_state_temp = file_state_temp.split(" ")
		   			file_state=[]
		   			file_next_state=[]
		   			for j in range(0,38):
		   				file_state.append(float(file_state_temp[j]))

		   			file_next_state_temp = file_next_state_temp.split(" ")
		   			for j in range(0,38):
		   				file_next_state.append(float(file_next_state_temp[j]))

		   			file_action = file_action.split(" ")
		   			for j in range(0,3):
		   				file_action[j]=float(file_action[j])
		   			
		   			file_state=[file_state]
			   		file_action=[file_action]
			   		file_next_state=[file_next_state]
		   			transition=[]
		   			transition.append(file_state)
		   			transition.append(file_action)
		   			transition.append(file_reward)
		   			transition.append(file_next_state)
		   			minibatch.append(transition)

		   			
		   
		    
			
			
			error_outputs=0
			for i in range(len(minibatch)):


				#compute action using s[i+1]*theta_3
				'''
				print("current state:")	
				print(minibatch[i][3])
				print("theta:")
				print(theta_3[0])
				print(multiply(current_state,theta_3[0]))
				'''

				new_action=get_action(minibatch[i][3],hidden_layers_1,theta_3)
				
				#compute Q using s[i+1] and a[i+1]
				q=get_value(minibatch[i][3],new_action,hidden_layers_2,theta_4)
				#ri+gamma*Q
				

				y=reward+gamma*q
				#si, ai = q 
				Q=get_value(minibatch[i][0],minibatch[i][1],hidden_layers_2,theta_2)
				
				error_outputs=error_outputs+(y-Q)
			

			error_outputs=error_outputs*2.0/len(minibatch)
			
			dJdO=[[error_outputs]]
		
			I=file_state
			I[0].append(file_action[0][0])
			I[0].append(file_action[0][1])
			I[0].append(file_action[0][2])
			
			o1=multiply(I,theta_2[0])
			o2=multiply(o1,theta_2[1])
			O=multiply(o2,theta_2[2])
			dJdt2=multiply(transpose(o2),dJdO) #15*1
			dJdo2=transpose(multiply(theta_2[2],dJdO)) #1*15
			dJdt1=multiply(transpose(o1),dJdo2)#15*15
			dJdo1=transpose(multiply(theta_2[1],transpose(dJdo2))) #1*15
			dJdt0=multiply(transpose(I),dJdo1)#41*15
			alp1=[alpha]*len(theta_2[0][0])#1*15
			alp1=[alp1]*len(theta_2[0])#41*15
			alp2=[alpha]*len(theta_2[1][0])#1*15
			alp2=[alp2]*len(theta_2[1])#15*15
			alp3=[alpha]*len(theta_2[2][0])#1*1
			alp3=[alp3]*len(theta_2[2])#15*1
		
			
		
			theta_2[0]=element_subtract(theta_2[0],element_multiply(alp1,dJdt0)) 
			theta_2[1]=element_subtract(theta_2[1],element_multiply(alp2,dJdt1))
			theta_2[2]=element_subtract(theta_2[2],element_multiply(alp3,dJdt2))
			dt1=[0]*len(theta_1[1][0])
			dt1=[dt1]*len(theta_1[1])#15*3
			
			dt0=[0]*len(theta_1[0][0])
			
			dt0=[dt0]*len(theta_1[0])#38*15
			
			for i in range(len(minibatch)):
				
				
			
				I[0].append(minibatch[i][1][0][0])
				I[0].append(minibatch[i][1][0][1])
				I[0].append(minibatch[i][1][0][2])
				
				o1=multiply(I,theta_2[0])
				o2=multiply(o1,theta_2[1])
				O=multiply(o2,theta_2[2])
				dJdt2=multiply(transpose(o2),dJdO) #15*1
				dJdo2=transpose(multiply(theta_2[2],dJdO)) #1*15
				dJdt1=multiply(transpose(o1),dJdo2)#15*15
				dJdo1=transpose(multiply(theta_2[1],transpose(dJdo2))) #1*15
				dJdt0=multiply(transpose(I),dJdo1)#41*15
				dJdI=transpose(multiply(theta_2[0],transpose(dJdo1)))#1-41
				
				dQda=dJdI[0][38]+dJdI[0][39]+dJdI[0][40]
				J=minibatch[i][0]#1*38
				
				net1=multiply(J,theta_1[0]) #1*15
				o1=act(net1)#1*15
				net0=multiply(o1,theta_1[1])#1*3
				O=act(net0)#1*3
				dOdnet0=getdiff(O)#1*3
				dOdt1=multiply(transpose(o1),dOdnet0)#15*3
				alp1=[dQda]*len(theta_1[1][0])
				alp1=[alp1]*len(theta_1[1])#15*3
				dt1=element_add(dt1,element_multiply(alp1,dOdt1))#15*3
				dOdo1=transpose(multiply(theta_1[1],transpose(dOdnet0)))#1*15
				dOdnet1=element_multiply(getdiff(o1),dOdo1)#1*15
				dOdt0=multiply(transpose(I),dOdnet1)#38*15
				alp1=[dQda]*len(theta_1[0][0])
				alp1=[alp1]*len(theta_1[0])
						
				dt0=element_add(dt0,element_multiply(alp1,dOdt0))#38*15
			alp1=[alpha/len(minibatch)]*len(theta_1[1][0])
			alp1=[alp1]*len(theta_1[1])	
			dt1=element_multiply(alp1,dt1)
			alp1=[alpha/len(minibatch)]*len(theta_1[0][0])
			alp1=[alp1]*len(theta_1[0])	
			dt0=element_multiply(alp1,dt0)
				
			theta_1[1]=element_subtract(theta_1[1],dt1)
			
			theta_1[0]=element_subtract(theta_1[0],dt0)
			
			theta_3[0]=element_add(scalar_multiply(theta_3[0],(1-tau)),scalar_multiply(theta_1[0],tau))
			theta_3[1]=element_add(scalar_multiply(theta_3[1],(1-tau)),scalar_multiply(theta_1[1],tau))
			theta_4[0]=element_add(scalar_multiply(theta_4[0],(1-tau)),scalar_multiply(theta_2[0],tau))
			theta_4[1]=element_add(scalar_multiply(theta_4[1],(1-tau)),scalar_multiply(theta_2[1],tau))
			theta_4[2]=element_add(scalar_multiply(theta_4[2],(1-tau)),scalar_multiply(theta_2[2],tau))
		
	

	if(state_check==1 or count==0):
		action_1=get_action(current_state,hidden_layers_1,theta_1)
		prev_state=current_state
		prev_action=action_1
		
		pos=(action_1[0][0]+1)/2
		angle=(action_1[0][1]*135+90)
		force=(action_1[0][2]+1)/2

		f=open("episode.txt","a")
		for i in range(0,38):

			f.write(str(current_state[0][i])+' ')

		f.write('\n'+ str(action_1[0][0]) + ' ' + str(action_1[0][1]) +' ' + str(action_1[0][2]) +'\n')
		f.close()
		#output current_state and action

		a=str(pos)+','+str(angle)+','+str(force)
		
		'''
		if(check==0):
		    a = str(0.5) + ',' + str(90.0+random.randrange(-20,20)) + ',' + str(1.0)
		'''

		try:
		    s.send(a)
		    count=count+1
		except Exception as e:
		    print "Error in sending:",  a, " : ", e
		    print "Closing connection"
		    flag = 0

	else:
		flag=0
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
			target_1 = open("theta_1.txt", "w")
			target_2 = open("theta_2.txt", "w")
			target_3 = open("theta_3.txt", "w")
			target_4 = open("theta_4.txt", "w")

			for i in range(0,len(theta_1[0])):
				for j in range(0,len(theta_1[0][0])):
					target_1.write(str(theta_1[0][i][j])+'\n')
			for i in range(0,len(theta_1[1])):
				for j in range(0,len(theta_1[1][0])):
					target_1.write(str(theta_1[1][i][j])+'\n')
			

			for i in range(0,len(theta_2[0])):
				for j in range(0,len(theta_2[0][0])):
					target_2.write(str(theta_2[0][i][j])+'\n')
			for i in range(0,len(theta_2[1])):
				for j in range(0,len(theta_2[1][0])):
					target_2.write(str(theta_2[1][i][j])+'\n')
			for i in range(0,len(theta_2[2])):
				for j in range(0,len(theta_2[2][0])):
					target_2.write(str(theta_2[2][i][j])+'\n')
			
			for i in range(0,len(theta_3[0])):
				for j in range(0,len(theta_3[0][0])):
					target_3.write(str(theta_3[0][i][j])+'\n')
			for i in range(0,len(theta_3[1])):
				for j in range(0,len(theta_3[1][0])):
					target_3.write(str(theta_3[1][i][j])+'\n')
		
			for i in range(0,len(theta_4[0])):
				for j in range(0,len(theta_4[0][0])):
					target_4.write(str(theta_4[0][i][j])+'\n')
			for i in range(0,len(theta_4[1])):
				for j in range(0,len(theta_4[1][0])):
					target_4.write(str(theta_4[1][i][j])+'\n')
			for i in range(0,len(theta_4[2])):
				for j in range(0,len(theta_4[2][0])):
					target_4.write(str(theta_4[2][i][j])+'\n')

			target_1.close()
			target_2.close()
			target_3.close()
			target_4.close()
			break
	elif num_players == 2:
	    if agent_2player(state, color) == 0:
	        break
s.close()





