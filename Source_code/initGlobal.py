# linh.homanh@hust.edu.vn - 2018
# thuan.bb.hust@gmail.com - 2018
numProcess = 2 # number of the script process would be run in each computer.
# = ['CRD02-PC'] #-- list of exist computers for running scripts.
#PCnames = ['DESKTOP-K6646BG']
PCnames = ['CRD-PC']
Re_trainning = False
Re_trainning_folder = 'C:/Opt_files/GP2019_03_21_11h44m55s/'		 # path to the folder need being retrained. 
start_gen_for_retraining = 12
save_paras = 'numbs_paras.txt'   # do not change this parameter
save_names = 'names_paras.txt'   # de not change this parameter 
# related to antenna.
debug = False   # this variable turn on to debug the program that related to GEOPANDAS library. 
class AnT:
	def __init__(self):
		self.c = 3e8					# save_on 1
		self.fC = 3.5e9 				# save_on 2 
		self.fStart = 3.3				# save_on 3
		self.fStop = 3.7				# save_on 4
		self.npoints = 200				# save_on 5
		self.Band_fitness = [3.4,3.6]	# save_on 6, 7
		self.Point_start_eval,self.Point_stop_eval = self.__getNum_point_for_evaluation() 		# save_on 8, 9
		self.Center_start_eval,self.Center_stop_eval = self.__getNum_center_point_evaluation()	# save_on 10, 11
		self.substrate_material = 'FR4_epoxy'													# save_on text_1
		self.hfssExePath   = 'C:/"Program Files (x86)"/Ansoft/HFSS13.0/hfss.exe'; # location of hfss executable (needs to be the
		#self.hfssExePath   = r'C:\"Program Files"\Ansoft\HFSS14.0\Win64\hfss.exe'; # location of hfss executable (needs to be the  
		self.resultsDir    = 'path2';   # location of results folders (containing final .hfss files)			# save_on text_2
		self.tmpDir        = 'path3';  # location of hfss temp files 								
		self.tmpTab 	   = 'path4'																
		self.overcome_desired = self.resultsDir + r'C:\Opt_files\overcome_desired'  # folder save any best found antenna structure with overcome of the
																	# fitness.
		self.Antenna_Name  	   = 'MPA'												# save_on  text_3
		self.maxTime = 15; # maximum allowed time (in minutes) for each computer to solve batch of files,
							# where the batch size is equal to the number ofs
							# processors on a computer
		self.hfss_save = False
	def __getNum_point_for_evaluation(self):
		# function gets two specified points for evaluation_band.
		# for automated finding these two points.
		step = (self.fStop - self.fStart)/(self.npoints-1)
		temp = self.fStart
		i = 0
		while (temp < self.Band_fitness[0]):
			temp = temp + step
			i = i + 1
		temp = self.fStart
		j = 0
		while (temp < self.Band_fitness[1]):
			temp = temp + step
			j = j + 1
		return i,j
	def __getNum_center_point_evaluation(self):
		# similarly with above function.
		step = (self.fStop - self.fStart)/(self.npoints-1)
		temp = self.fStart
		i = 0
		center = self.fC/1e9
		while (temp < (center-0.01)):
			temp = temp + step
			i = i + 1
		temp = self.fStart
		j = 0
		while (temp < (center+0.01)):
			temp = temp + step
			j = j + 1
		return i,j

# related substrate.
class Sub:
	def __init__(self):
		self.rangeOx = [11,14] # min/max range of width of patch antenna.				# save_on 12, 13
		self.rangeOy = [11,14] # min/max range of length of patch antenn.				# save_on 14, 15
		self.rangeOz = [0.7,1.2] # min/max range of 									# save_on 16, 17
		self.addition = 2 # 'mm' # increase the range of substrate.						# save_on 18
		self.decrease = 0 # 'mm' # number mm of substrate's both width and length will be decrease before create any pattern. 	# save_on 19

sub = Sub()
# L parameter.
min_basic_pattern = min(min(sub.rangeOx),min(sub.rangeOy))
minL_x = min_basic_pattern*0.12
maxL_x = min_basic_pattern*0.4
minL_y = min_basic_pattern*0.12
maxL_y = min_basic_pattern*0.4
# U parameter.
minU_x = min_basic_pattern/8.5
maxU_x = (min_basic_pattern*0.8)/4
minU_y = min_basic_pattern/4.5
maxU_y = min_basic_pattern/2
# related to 2D polygon.
class L:
	# L terminal.
	def __init__(self):
		self.rangex1 = [minL_x,maxL_x] #min/max range of x1.					# save_on 17, 18 + 3
		self.rangex2 = [minL_x,maxL_x]											# save_on 19, 20 + 3
		self.rangey1 = [minL_y,maxL_y]											# save_on 21, 22 + 3
		self.rangey2 = [minL_y,maxL_y]											# save_on 23, 24 + 3
class U:
	# U terminal.
	def __init__(self):
		self.rangex1 = [minU_x,maxU_x]											# save_on 25, 26 + 3
		self.rangex2 = [minU_x,maxU_x]											# save_on 27, 28 + 3
		self.rangex3 = [minU_x,maxU_x]											# save_on 29, 30 + 3
		self.rangey1 = [minU_y,maxU_y]											# save_on 31, 32 + 3
		self.rangey2 = [minU_y/2,minU_y]										# save_on 33, 34 + 3
		self.rangey3 = [minU_y,maxU_y]											# save_on 35, 36 + 3

class GP:
	def __init__(self):
		self.maxSub = 1 # maxdep of the the gensubstrate tree.
		self.maxPat = 1 
		self.maxBlue = 3														# save_on 40

		self.rate = 0 # is the rate of number grow type of ind in all popsize.
		self.proRed = 0.05 # the probability selects red node to apply GP operators. 
		self.prosubBlue = 0.75 # the probability selects subBlue node(like union node, Usubtree9 node,...)
		self.proBlue = 0.05 # the probability selects Blue node(Bluetree).
		self.proSubstrate = 0.05 # .............................
		self.proGensub = 0.05 # ...............................
		self.proGenpat = 1 - self.proRed - self.prosubBlue\
        - self.proBlue - self.proSubstrate - self.proGensub # Don't change, and make sure it's not negative.


		self.numpop = 10 # number of the individuals in a population.			# save_on 41
		self.numgen =  10 # number of generation in a GP process.
		self.reprorate = 0.2  # the rate of the best individuals that will be remained to the next generation. 
		self.crossrate = 0.4  # the probability selects the crossover operator.
		self.mutarate = 1 - self.reprorate - self.crossrate # the probability selects mutation operator.

		self.desired_fitness = -800 # parameter for evaluating wheather a antenna structure is good enough or not, and then if it's 
									# good enough. It will be saved in a specified result folder.
		self.overcome_fitness = -1200 # parameter for evaluating wheather a antenna structure is overcome the desired result. It's will be
									# saved in specified result folder.
class lowlevel:
	def __init__(self):
		self.lowoptimize = True
		self.number_iters = 5  
		# self.step_size = 0.01
		self.init_number = 5
		self.active_function = 'relu' # the activation function for neural network architecture.
		self.optimizer = 'adam'       # the method for optimize the neural network.
		self.number_direction = 4    # the number of direction search.
		self.anpha = 0.06		 	  # the step size for direct search method.
		self.shrink = 0.25 			  # parameter for shrink the step size anpha.
		self.number_search_step = 4   # the number of search step for direct search method.
		self.number_sample = 15		  # number of samples for creating the trainning data for neural network.
		self.tmpDir        = 'path6'  # location of temporary hfss and vbs files.
		self.tmpTab 	   = 'path7'  # location of temporary .tab files.

