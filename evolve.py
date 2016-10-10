
import sys, numpy as np, os, random

# first argument is init file
# second argument is intermidiate file - must be empty or absent in the begining
# third argument is output file - will be overwritten

# check sys.argv and assign defaultsif empty

def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
# control variables
controls = [[0,WIDHT],[0,HEIGHT]]
params = {'POPN' : 40, 'PARENTS' : 15, 'MRATE' : 0.05, 'TOURN' : 0 }

# default tournament size is half 
if params['TOURN'] is 0: 
	params['TOURN'] = int(params['PARENTS']/2)
	
dim = len(controls)

# now read second param which is a intermidiate file
# if file is not there or empty -> first iteration
if not os.path.isfile(dumpFile) :#or os.stat("file").st_size == 0:
	# generate POPN - population
	# random values in every column based on given ranges
	
	nextPop = np.random.choice(np.arange(controls[0][0],controls[0][1],step=0.01),size=(params['POPN'],dim),replace=False)
	for col in range(1,nextPop.shape[1]):
		nextPop[:,col] = np.random.choice(np.arange(controls[col][0],controls[col][1],step=0.01),size=(params['POPN']),replace=False)
	
else :
	# reading file with current population and fitness
	curData = np.loadtxt(sys.argv[2])
	curPop = curData[:,:-1]
	# dummy next population array
	nextPop = np.zeros((params['POPN'],dim))
	# dummy winners array - to use as parents
	winners = np.zeros((params['PARENTS'],dim))	
	# Each element of fitVec is an array consisting of the index of the 
	# solution in curPop and its cost, e.g. [0, 2.54] means that the 0th 
	# element in curPop (first solution) has an error of 2.54
	fitVec = np.array([np.array([x, curData[x,-1]]) for x in range(params['POPN'])])
	# select winners based on a tournament system
	for n in range(len(winners)):
		# select 10 random solutions - indexes of fitVec
		# tournament size is half
		selected = np.random.choice(range(len(fitVec)), params['TOURN'], replace=False)
		# find min from those 10 - index in selected
		wnr = np.argmin(fitVec[selected,1])
		# store the winner
		winners[n] = curPop[int(fitVec[selected[wnr]][0])]
	# store parents in next population and generate children
	# step1. pad array symmetrically to fill the rest of new population
	nextPop = np.pad(winners, ((0,(params['POPN'] - len(winners))),(0,0)), mode='symmetric')
	# step2. shuffle new added winners to create children
	np.random.shuffle(nextPop[len(winners):])
	# introduce mutation
	# [1] matrix with some deviations multiplied with nextPop
	mutants = np.matrix([np.float(np.random.normal(1,0.3,1)) if random.random() < params['MRATE'] else 1 for x in range(nextPop.size)]).reshape(nextPop.shape)
	nextPop = np.multiply(nextPop, mutants)
	# find the fittest individual and store into output file
	fittestInd = np.argmin(curData[:,-1])
	fittest = [ "%.4f\t" % x for x in curData[fittestInd, :]]
	fittest[-1] += '\n'
	# check if output file exists or not
	if not os.path.isfile(outFile) :
		# make header
		header = ['CTRL'+ str(x) + '\t' for x in range(len(controls))]	
		header.append('OBJ\n')
		# write to file
		with open(outFile, "w") as f:			
			f.writelines(header)
			f.close()
	# write fittest to file
	with open(outFile, "a") as f:
		f.writelines(fittest)
		f.close()

# write new population to a file
np.savetxt(dumpFile, nextPop, delimiter='\t', fmt='%10.5f', newline="\n")
