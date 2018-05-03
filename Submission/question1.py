import numpy as np
from math import sin, radians
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

side = 179  # using grid of 179x179 in the space of distance to wall vs theta

x, y = np.meshgrid(range(side),([_/10 for _ in range(side)]))

world = np.empty((side,side))  #2d matrix representing the state space

uniform = 1/float(side*side)  # normalization value to initalize with

world[:,:] = uniform # assigning uniform distribution

hit = 0.75
miss = 0.25

ranges = open('Given/ranges1.dat', 'r')
ranges = ranges.read()
ranges =  ranges.split('\r\n')
ranges = [float(i) for i in ranges[2:]]


def beam_observe():
	global world, ranges
	hypt = ranges.pop(0)
	for theta in range(side):
		for y in range(side):
			if abs(((y+1)/sin(radians(theta+1)))-hypt) <= 0.01:  # estimating distance using affine rotation logic
				world[theta,y] *= float(hit)
			else:
				world[theta,y] *= float(miss)
	norm = sum(sum(world))
	world[:,:] /= float(norm)
	max_val = np.amax(world)
	for theta in range(side):
		for y in range(side):
			if world[theta,y] == max_val:
				print ("theta: ",theta,"distance to wall: ",y)
	


def motion():
	global world
	world = np.roll(world, 23, axis=0) #rotate by approx 23 degrees every 0.2s


def main():
	loopcount = 0

	while(ranges):
		loopcount += 1
		print "timestep ",loopcount
		beam_observe()
		motion()
	ax.plot_wireframe(x,y,world)
	plt.show()

if __name__ == '__main__':
	main()
