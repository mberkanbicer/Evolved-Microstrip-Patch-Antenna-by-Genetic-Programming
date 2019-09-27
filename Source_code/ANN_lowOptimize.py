#thuan.bb.hust@gmail.com
import Helper as hp 
import initGlobal as init
import numpy as np
import os
from genscript import genscript
import copy 
import random
import matplotlib.pyplot as plt
import helpRunning as hrun 
lowinit = init.lowlevel()
ant = init.AnT()
class temppp:
	pass
def lowlevel_optimizer(ind,state,pop_num):
	# the inputs: - IND  individual
	# 			  - STATE
	#			  - POP_NUM the specified ID of current individual which be optimized in here.
	state.lowlevel = True
	global_name = lowinit.tmpDir + ant.Antenna_Name + '_gen_'
	global_tabname = lowinit.tmpTab + ant.Antenna_Name + '_gen_'
	print('running low-level optimizer for generation ',state.gen,'population ', pop_num)
	chromosome, subtree_chrom, IDlist = hp.getChrom(ind) # get chromosome from tree and other atributes.

	num = len(chromosome) # number of values will be optimized.

	# create randomly the trainning data for ANN.

	y = np.zeros(lowinit.number_sample+1)
	y[0] = ind.fitness  # save original chromosome fitness.
	return_loss = []
	return_loss.append(ind.ReturnLoss) # save original return loss variable.
	for i in range(lowinit.number_sample):
		return_loss.append([])

	X_training = np.zeros((lowinit.number_sample+1,num)) # X_train data

	for i in range(num): # save original chromosome.
		X_training[0,i] = chromosome[i]

	for i in range(1,lowinit.number_sample+1):
		for ii in range(num):
			X_training[i][ii] = round(random.uniform(-1,1),4)
	print(X_training)
	# generate all of the scripts.
	print('generating ',lowinit.number_sample, ' scripts in low lelvel optimizer in generation ',state.gen)
	# before run the next generation, all of the tab file need be deleted.
	filelist = [ f for f in os.listdir(lowinit.tmpDir) if f.endswith(".tab") ]
	for f in filelist:
		os.remove(os.path.join(lowinit.tmpDir, f))
	# be fore run the next gen, all of the hfss file in temp need be deleted.
	filelist = [ f for f in os.listdir(lowinit.tmpTab) if (f.endswith(".hfss") or f.endswith(".vbs") or f.endswith(".txt"))]
	for f in filelist: # delete all before files.
		os.remove(os.path.join(lowinit.tmpTab, f))
	########################################################
	############## insert chromosome.
	# create temporary population to save current new individual.
	#pop = []
	#for i in range(1,lowinit.number_sample + 1):
	#	tree = hp.insert_chrom(ind.tree,X_training[i,:],subtree_chrom, IDlist)
		



	for i in range(1,lowinit.number_sample + 1):
		tree = hp.insert_chrom(ind.tree,X_training[i,:],subtree_chrom, IDlist)
		#pop[i].tree.childs[1].valueofnode.plot()
		[Substrate,polygons,centroid] = hp.get_all_para_for_hfss(tree) # get necessary parameters for genscript function.
		name = global_name + str(state.gen) + '_pop_' + str(i) # name of directory would
																			# be used to save .vbs and .hfss file.
		tabname = global_tabname + str(state.gen) + '_pop_' + str(i) # name of directory
																			# would be used to save .tab file. 
		temppp.tree = tree
		temppp.nodelist = ind.nodelist
		temp,_,_ = hp.getChrom(temppp)
		print(X_training[i,:])
		print(".....")
		print(temp)
		for iiii in range(len(X_training[i,:])):
			if not (X_training[i,iiii] == temp[iiii]):
				raise 
		genscript(Substrate,polygons,centroid,name + '.vbs',tabname,name + '.hfss')
		del tree
		del Substrate
		del polygons
		del centroid

	#raise ValueError("Finished testing")
	#######
	#  running all of the scripts.
	nameDir = global_name + str(state.gen) + '_pop_'  # file name direction of the vbs file.
	hrun.RunPopScript(lowinit.number_sample,nameDir,1,len(init.PCnames),state)

	# getting the fitness of each 
	for i in range(1,lowinit.number_sample+1):
		spec_nameDir_tab = global_tabname + str(state.gen) + '_pop_' + str(i) + '.tab'
		[m,n] = hrun.assignFitness(spec_nameDir_tab,state.gen)
		print('i ',i, '___',m)
		[y[i],return_loss[i]] = [m,n]

	np.savetxt('C:\\Opt_files\\lowlevel\\y.txt',y,delimiter = ',')
	np.savetxt('C:\\Opt_files\\lowlevel\\X.txt',X_training,delimiter = ',')

	state.lowlevel = False


