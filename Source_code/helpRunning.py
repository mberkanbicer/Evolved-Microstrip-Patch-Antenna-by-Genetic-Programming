# linh.homanh@hust.edu.vn - 2018
# bachthuan03111997@gmail.com - 2018
import initGlobal as init 
import os
import time 
from pathlib import Path 
import numpy as np 
inAnT = init.AnT() # get the essential parameters of antenna from initglobal.py 
inGP = init.GP() # get the essential parameters of GP process from initGlobal.py file. note: this's global parameter.
lowinit = init.lowlevel()
def RunPopScript(poplength,dirName,runFrom,numComp,state):
	# state: save all of current variables in GP process.
	# poplength is the length of population
	# dirName is the vbs file name directory.
	# runFrom is the specified ID of indiviudal to start running scripts.
	# numComp is the number of computer gived to run scripts. 
	# note: inAnT is the global parameter that get from initGlobal.py file.
	#		it need be declared before this function.
	print('Start running all of the scripts.')
	poplength = poplength - 1 # need be minused 1 because the saved directory names start from 0. 
	i = runFrom
	parallel = numComp != 1
	if not parallel:
		while(i<=poplength):
			#if i > poplength:
			#	break
			# run a specified number of scripts.
			print('Run script ',i)
			theHFSS1 = 'start ' + inAnT.hfssExePath + ' /RunScriptAndExit ' + dirName + str(i) + '.vbs'
			print(theHFSS1)
			i = i + 1
			os.system(theHFSS1) # run specified script
			if (i <= poplength):
				print('Run script ',i)
				theHFSS2 = 'start ' + inAnT.hfssExePath + ' /RunScriptAndExit ' + dirName + str(i) + '.vbs'
				if not i == poplength:
					i = i + 1
				os.system(theHFSS2) # run specified script
			done = False    
			start_time = time.time()
			while not done:
				# check to see wheather all script is done.
				print('generation: ',state.gen,"/",inGP.numgen)
				if state.lowlevel:
					print("RUNNING LOWLEVEL ..... population ", state.population_num,"/",inGP.numpop)
					print("LOWLEVEL FITNESS: ",state.current_low_fitness)
					print("lowlevel_k: ", state.lowlevel_k ,"/",lowinit.number_search_step)
				done = check_Done(1,start_time)
				if state.gen > 1:
					print('current best fitness: ',state.best_hisFitness[-1])
					print('current fitness: ',state.curFitness)
	print('Done running all scripts.')
###################################################################################################################
def check_Done(i,start_time):
	#-- check to see if hfss is still running on this computer.
	#-- i is specified computer number need be ckecked.
	#-- start_time: is the start point of time to check wheather the scrpit running out of time?.
	# note: inAnT is the global parameter that get from initGlobal.py file.
	#		it need be declared before this function.
	done = False
	# name file to store task list info.
	#file = r'\\' + init.PCnames[0] + r'C:\HFSS_shared'+'/' + init.PCnames[i-1] +'_procs.txt'
	file = r'C:\HFSS_shared'+'/' + init.PCnames[i-1] +'_procs.txt'
	# file = \\DESKTOP-K6646BG\HFSS_shared\DESKTOP-K6646BG_procs.txt
	# check for running processes.
	theSys = r'pslist \\' + init.PCnames[i-1] + ' hfss > ' + file
	os.system(theSys)
	# pslist \\CRD02-PC chrom > C:\HFSS_shared/CRD02-PC_procs.txt
	non_blank_count = 0
	with open(file) as infp:
		for line in infp:
			if line.strip():
				non_blank_count += 1
	done = non_blank_count==2
	# check for time up
	if (not done):
		if (time.time() - float(start_time) > inAnT.maxTime*60) :
#     if (lineCount(file[i]) > 2) # kill open processes:
			print(r'timer has expired\killing open HFSS files on ' + init.PCnames[i-1])
			if (i == 1):
				os.system("Taskkill /IM hfss.exe /F");    
			done = 1
	return done
#####################################################################################################################3
def assignFitness(nameDir,gen):
	# evaluate the S11.
	# output: - the fitness.
	#		  - S11(fre,S11).
	# nameDir: .tab file source.
	# note: inAnT and inGP are the global parameter that get from initGlobal.py file.
	#		they need be declared before this function.
	file = Path(nameDir)
	if not file.is_file():
		return [100,None,False,False]
	else:
		Fre,S11 = np.genfromtxt(file,dtype = float,skip_header=1, unpack=True)
		Band = S11[inAnT.Point_start_eval:inAnT.Point_stop_eval]
		#count = 0
		fitness = 0
		for i in range(len(Band)):
			#if Band[i] < -10:
				#count = count + 1 # count the number of points that have S11 < -10
			fitness = fitness + Band[i]
		min_S11 = min(S11)
		so_best = S11[inAnT.Center_start_eval:inAnT.Center_stop_eval]
		exist1 = False
		exist2 = False
		if (min_S11 in so_best) and (min_S11 < -10):
			print('exist a best fitness')
			exist1 = True
			fitness = fitness - 300
			if fitness < inGP.overcome_fitness:
				exist2 = True
	return [fitness,[Fre,S11],exist1,exist2]