
import sys, numpy as np, os, random


class Evolver(object) :
	def __init__(self, population, parents, mrate, controls, figures):
		# population size
		self.population = population
		# number of parents in every generation
		self.parents = parents
		# mutation rate
		self.mrate = mrate
		# tournament pool
		self.tourn = parents / 2
		# array of control variable ranges
		self.controls = controls
		# defining rest of params
		# dimention of a creature
		self.dim = [figures, len(controls)]
		# current population pool - randoms
		self.startPool()
		# previous population pool
		self.prevpool = np.array([np.zeros((self.dim[0], self.dim[1])) for i in range(population)]) 
		# current population fitness
		self.curfit = np.zeros((1, self.population))
		# previous population fitness
		self.prevfit = np.zeros((1, self.population))
		# list of the fittest
		self.fittest = []
		
	def startPool(self):
		self.curpool = []
		for i in range(self.population):
			dude = np.random.choice(np.arange(self.controls[0][0],self.controls[0][1]),size=(self.dim[0],self.dim[1]),replace=False)
			for col in range(1,dude.shape[1]):
				dude[:,col] = np.random.choice(np.arange(self.controls[col][0],self.controls[col][1]),size=(self.dim[0]),replace=False)
			self.curpool.append(dude)
		self.curpool = np.array(self.curpool)
			
	def evolve(self, fitfunc):
		# fitfunc takes vector and returns its fitness
		self.prevpool = np.copy(self.curpool)
		self.prevfit = np.copy(self.curfit)
		# dummy next population array
		self.curpool = np.array([np.zeros((self.dim[0], self.dim[1])) for i in range(self.population)])
		# dummy winners array - to use as parents
		self.winners = np.array([np.zeros((self.dim[0], self.dim[1])) for i in range(self.parents)])
		# Each element of curfit is an array consisting of the index of the 
		# creature in prevpool and its fitness, e.g. [0, 2.54] means that the 0th 
		# element in prevpool (first individual) has a fintess of 2.54
		self.curfit = np.array([np.array([x, fitfunc(self.prevpool[x])]) for x in range(self.population)])
		# select winners based on a tournament system
		for n in range(len(self.winners)):
			# select random solutions - indexes of fitVec
			# tournament size is half
			selected = np.random.choice(range(len(self.curfit)), self.tourn, replace=False)
			# find min from those selected - index in selected
			wnr = np.argmin(self.curfit[selected,1])
			# store the winner
			self.winners[n] = self.prevpool[int(self.curfit[selected[wnr]][0])]
		# store winners and add children
		# will be using a mask array where each element is a number of creature in winners 
		# for example [[1,1,1],[2,2,2],[3,3,3]] corresponds to 3 elements in winners
		# each element is a index of creature, its position - row index
		# once children are created will transform into population
		# 1. create mask array
		self.mask = np.array([ [x for i in range(self.dim[0])] for x in range(self.parents) ])
		# 2. pad mask array to create children
		self.mask = np.pad(self.mask, ((0,(self.population - self.parents)),(0,0)), mode='symmetric')
		# 3. reshuffle children genes
		self.mask[self.parents:] = shuffle2d(self.mask[self.parents:])
		# 4. rebuild population
		for i, dude in enumerate(self.mask):
			self.curpool[i] = np.array([ self.winners[dude[x]][x] for x in range(len(dude))])
		# 5. introduce mutation
		# [1] matrix with some deviations multiplied with nextPop
		for i, dude in enumerate(self.curpool):
			mutants = np.matrix([np.float(np.random.normal(1,0.3,1)) if random.random() < self.mrate else 1 for x in range(dude.size)]).reshape(dude.shape)
			self.curpool[i] = np.multiply(dude, mutants)
		# find the fittest and save
		fittestInd = np.argmin(self.curfit[:,-1])
		self.fittest.append(self.prevpool[fittestInd])
		


def shuffle2d(arr):
	oned = arr.flatten()
	np.random.shuffle(oned)
	twod = np.reshape(oned, arr.shape)
	return twod

controls = [[0,500],[0,500],[0,500],[0,500],[0,255],[0,255],[0,255]]
population = 10
parents = 4
mrate = 0.1
figures = 3

st = (controls[0][1] - controls[0][0]) / population
p = np.random.choice(np.arange(controls[0][0],controls[0][1]), size=(population,len(controls)), replace=False)

ev = Evolver(population, parents, mrate, controls, figures)
print(ev.curpool)
print(ev.prevpool)

def func(x):
	return x[0][0]

ev.evolve(func)
print(ev.curfit)
print(ev.winners)
print(ev.mask)
print(ev.curpool)
print(ev.fittest)
