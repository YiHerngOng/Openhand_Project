#!/usr/bin/env python

#######################################################################################
#Written by Yi Herng Ong
#ME 599 Project Python Script 2
#Purpose: Conduct Data Analysis using joint position data that collected from Optitrack Motion Capture
#Goal: Calculate and plot Joint Angle Data for each finger joint (proximal and distal joint) & Three Grasp Positions (Grasp Setup, Pre Grasp, Final Grasp)
#Please use each of these below in command line for data analysis 
#Normal Grasp -> python grasp_analysis.py cy_grasp_data.csv 
#Palm Grasp -> python grasp_analysis.py cy_palm_data.csv
#Pinch Grasp -> python grasp_analysis.py cy_pinch_data.csv

#######################################################################################
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt,pi

#Open csv and read joint position data into numpy list
def open_csv_to_list(filename):
    words = []
    try:
	    with open(filename, 'rb') as csvfile:
	     	reader = csv.reader(csvfile)
	        for line in reader:
	        	words.append(line)
    except:
        sys.exit(str(filename)+ " "+ "does not exist")

    words_np = np.array(words)
    return words_np

#Check whether command line argument is less than 1
def check_argument():
    usr_argv = sys.argv[1]
    if len(usr_argv) < 1:
        sys.exit("No csv file detected") #system exit if argument less than 1
    return usr_argv

#Initiate a class for a finger
class finger():
	def __init__(self,pos):
		self.distal_x = []
		self.distal_z = []
		self.proximal_x = []
		self.proximal_z = []
		self.pos = pos
		self.currpos_x = []
		self.currpos_z = []
		self.prox_length = 0
		self.distal_length = 0
		self.prox_joint_angles = []
		self.dist_joint_angles = []

	#Store proximal joint positions based on x and z direction
	def proximal_pos(self):
		for i in xrange(len(self.pos)):
			self.proximal_x.append(float(self.pos[i,0]))
			self.proximal_z.append(float(self.pos[i,1]))			

		return None

	#Store distal joint positions based on x and z direction
	def distal_pos(self):
		for i in xrange(len(self.pos)):
			self.distal_x.append(float(self.pos[i,2]))
			self.distal_z.append(float(self.pos[i,3]))			
		return None

	#Store finger positions based on x and z direction
	def finger_pos(self):
		px = []
		pz = []
		for i in xrange(len(self.pos)):
			px = [float(self.pos[i,0]), float(self.pos[i,2])]
			pz = [float(self.pos[i,1]), float(self.pos[i,3])]
			self.currpos_x.append(px)
			self.currpos_z.append(pz)
		return None

	#Calculate and plot joint angle of proximal and distal joint at each finger position
	def joint_angle_calculation(self,finger_no):
		#Joint angle calculation for finger 1 (left finger on the plot)
		if finger_no == 1:
			#Finger 1 origin position in x and z direction
			oX = 0.024
			oZ = 0.06
			for i in xrange(len(self.currpos_x)):
				self.prox_length = sqrt((self.currpos_x[i][0] - oX)**2 + (self.currpos_z[i][0] - oZ)**2)
				self.distal_length = sqrt((self.currpos_x[i][1] - self.currpos_x[i][0])**2 + (self.currpos_z[i][1] - self.currpos_z[i][0])**2)
				self.prox_joint_angles.append(np.arccos(abs(self.currpos_x[i][0]- oX) / self.prox_length))
				self.dist_joint_angles.append(np.arccos(abs(self.currpos_x[i][1] - self.currpos_x[i][0]) / self.distal_length))

		#Joint angle calculation for finger 2 (right finger on the plot)
		elif finger_no == 2:
			#Finger 2 origin position in x and z direction
			oX = 0.05
			oZ = 0.06
			for i in xrange(len(self.currpos_x)):
				self.prox_length = sqrt((self.currpos_x[i][0] - oX)**2 + (self.currpos_z[i][0] - oZ)**2)
				self.distal_length = sqrt((self.currpos_x[i][1] - self.currpos_x[i][0])**2 + (self.currpos_z[i][1] - self.currpos_z[i][0])**2)
				self.prox_joint_angles.append(np.arccos((self.currpos_x[i][0]- oX) / self.prox_length))
				self.dist_joint_angles.append(np.arccos((self.currpos_x[i][1] - self.currpos_x[i][0]) / self.distal_length))

		#Plot joint angles
		t = np.arange(len(self.currpos_x))
		plt.plot(t,self.prox_joint_angles)
		plt.title('Finger {0} Proximal Joint Angles'.format(finger_no))
		plt.xlabel('Time Step')
		plt.ylabel('Joint Angles (Radian)')
		plt.show()
		plt.plot(t,self.dist_joint_angles)
		plt.title('Finger {0} Distal Joint Angles'.format(finger_no))
		plt.xlabel('Time Step')
		plt.ylabel('Joint Angles (Radian)')		
		plt.show()
		return None

#Plot grasp position by using calculated joint angles of proximal and distal joint of each finger
def plot_grasp_using_joint_angles(f1_prox_joint_angle, f1_dist_joint_angle, f2_prox_joint_angle, f2_dist_joint_angle, status_of_grasp):
	f1x = [-1, -1+1*np.cos(pi - f1_prox_joint_angle), -1+1*np.cos(pi - f1_prox_joint_angle)+1*np.cos(pi-f1_dist_joint_angle)]
	f1z = [0, 1*np.sin(pi - f1_prox_joint_angle), 1*np.sin(pi-f1_prox_joint_angle)+1*np.sin(pi-f1_dist_joint_angle)]
	f2x = [1, 1+1*np.cos(f2_prox_joint_angle), 1+1*np.cos(f2_prox_joint_angle)+1*np.cos(f2_dist_joint_angle)]
	f2z = [0, 1*np.sin(f2_prox_joint_angle), 1*np.sin(f2_prox_joint_angle)+1*np.sin(f2_dist_joint_angle)]

	plt.plot([-1,1],[0,0], 'b--', f1x, f1z, 'r', f2x, f2z, 'k')
	plt.title('Status of grasp: {0}'.format(status_of_grasp))
	plt.ylim(-1, 2)
	plt.xlim(-2.5, 3)
	plt.legend(['Hand Base', 'Finger 1', 'Finger 2'])
	plt.xlabel('X-axis')
	plt.ylabel('Z-axis')			
	plt.show()
	return None			

#Plot proximal and distal joint trajectory of each finger 
def plot_traj_(f1_prox_x, f1_prox_z, f1_dist_x, f1_dist_z, f2_prox_x, f2_prox_z, f2_dist_x, f2_dist_z):
	plt.plot(f1_prox_x, f1_prox_z, f1_dist_x, f1_dist_z, f2_prox_x, f2_prox_z, f2_dist_x, f2_dist_z)
	plt.title('Finger Joint Trajectory')
	plt.legend(['finger 1 proximal joint', 'finger 1 distal joint', 'finger 2 proximal joint', 'finger 2 distal joint'])
	plt.xlabel('X-axis')
	plt.ylabel('Z-axis')
	plt.show()
	return None


if __name__ == '__main__':
	#Read and take argument from command line
	filename = check_argument()

	#Open and Read csv file of joint position data
	all_pos = open_csv_to_list(filename)

	#Store first four column of joint position for finger 1, the last four column for finger 2
	f1_pos = []
	f2_pos = []
	for i in xrange(len(all_pos)):
		f1_pos.append(all_pos[i,0:4])
		f2_pos.append(all_pos[i,4:])
	f1_pos_np = np.array(f1_pos)
	f2_pos_np = np.array(f2_pos)

	#Create finger class for finger 1 and 2
	f1 = finger(f1_pos_np)
	f2 = finger(f2_pos_np)

	#Seperate proximal and distal joint position of finger 1
	f1.proximal_pos()
	f1.distal_pos()
	#Seperate proximal and distal joint position of finger 2
	f2.proximal_pos()
	f2.distal_pos()

	#Plot proximal and distal joint trajectory of finger 1 and 2 
	plot_traj_(f1.proximal_x,f1.proximal_z,f1.distal_x,f1.distal_z,f2.proximal_x, f2.proximal_z, f2.distal_x, f2.distal_z)

	#Store finger position of finger 1 and 2
	f1.finger_pos()
	f2.finger_pos()

	#Calculate joint angles for each finger
	f1.joint_angle_calculation(1)
	f2.joint_angle_calculation(2)

	#Plot three grasp position with joint position data
	#Finger 1 (Grasp Steup, Pre-Grasp, Final Grasp)
	f1x = [0.024, f1.currpos_x[0][0], f1.currpos_x[0][1]]
	f1z = [0.06, f1.currpos_z[0][0], f1.currpos_z[0][1]]
	f11x = [0.024, f1.currpos_x[len(f1.currpos_x)/2][0], f1.currpos_x[len(f1.currpos_x)/2][1]]
	f11z = [0.06, f1.currpos_z[len(f1.currpos_z)/2][0], f1.currpos_z[len(f1.currpos_z)/2][1]]
	f111x = [0.024, f1.currpos_x[-1][0], f1.currpos_x[-1][1]]
	f111z = [0.06, f1.currpos_z[-1][0], f1.currpos_z[-1][1]]

	#Finger 2 (Grasp Steup, Pre-Grasp, Final Grasp)
	f2x = [0.05, f2.currpos_x[0][0], f2.currpos_x[0][1]]
	f2z = [0.06, f2.currpos_z[0][0], f2.currpos_z[0][1]]
	f22x = [0.05, f2.currpos_x[len(f2.currpos_x)/2][0], f2.currpos_x[len(f2.currpos_x)/2][1]]
	f22z = [0.06, f2.currpos_z[len(f1.currpos_z)/2][0], f2.currpos_z[len(f2.currpos_z)/2][1]]
	f222x = [0.05, f2.currpos_x[-1][0], f2.currpos_x[-1][1]]
	f222z = [0.06, f2.currpos_z[-1][0], f2.currpos_z[-1][1]]

	plt.plot([0.024,0.05], [0.06,0.06],'b--',f1x,f1z,'r',f2x,f2z,'k',f11x,f11z,'r--',f22x,f22z,'k--.',f111x,f111z,'r-',f222x,f222z,'k-')
	plt.title('Grasp Position with raw finger data')
	plt.legend(['Hand Base', 'finger 1 setup', 'finger 2 setup', 'finger 1 pre grasp', 'finger 2 pre grasp', 'finger 1 final grasp', 'finger 2 final grasp'])
	plt.xlabel('X-axis')
	plt.ylabel('Z-axis')
	plt.show()

	#Plot three grasp position using joint angles of proximal and distal joint of finger 1 and 2
	#Grasp Setup
	plot_grasp_using_joint_angles(f1.prox_joint_angles[0], f1.dist_joint_angles[0], f2.prox_joint_angles[0], f2.dist_joint_angles[0], 'Grasp Setup')
	#Pre-grasp
	plot_grasp_using_joint_angles(f1.prox_joint_angles[len(f1.dist_joint_angles)/2], f1.dist_joint_angles[len(f1.dist_joint_angles)/2], f2.prox_joint_angles[len(f1.dist_joint_angles)/2], f2.dist_joint_angles[len(f1.dist_joint_angles)/2], 'Pre-Grasp')
	#Final grasp
	plot_grasp_using_joint_angles(f1.prox_joint_angles[-1], f1.dist_joint_angles[-1], f2.prox_joint_angles[-1], f2.dist_joint_angles[-1], 'Final Grasp (Grasping Object)')


