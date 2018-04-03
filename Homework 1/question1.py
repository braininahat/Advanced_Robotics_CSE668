import numpy as np
from math import sin, radians
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

side = 179

x, y = np.meshgrid(range(side),([_/10 for _ in range(side)]))

world = np.empty((side,side))

uniform = 1/float(side*side)

world[:,:] = uniform

hit = 0.75
miss = 0.25

ranges = open('Given/ranges1.dat', 'r')
ranges = ranges.read()
ranges =  ranges.split('\r\n')
ranges = [float(i) for i in ranges[2:]]


def sense():
	global world, ranges
	hypt = ranges.pop(0)
	for theta in range(side):
		for y in range(side):
			if abs(((y+1)/sin(radians(theta+1)))-hypt) <= 0.2:
				world[theta,y] *= float(hit)
			else:
				world[theta,y] *= float(miss)
	norm = sum(sum(world))
	world[:,:] /= float(norm)


def move():
	global world
	world = np.roll(world, 23, axis=0) #rotate by 23 degrees every 0.2s


def main():
	while(ranges):
		sense()
		move()
	ax.plot_wireframe(x,y,world)
	plt.show()

if __name__ == '__main__':
	main()
