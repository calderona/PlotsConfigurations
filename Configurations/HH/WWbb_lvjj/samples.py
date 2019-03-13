import os
import subprocess
import string
from LatinoAnalysis.Tools.commonTools import *

##############################################
###### Tree Directory according to site ######
##############################################

directory_MC = '/gwteraz/users/amassiro/latino/lepSel__MCWeights__bSFLpTEffMulti__cleanTauMC'
#directory_data = '/gwteras/cms/store/group/OneLepton/Apr2017_Run2016B_RemAOD/lepSel__EpTCorr__TrigMakerData__cleanTauData__hadd/'
treeBaseDir = '/gwteras/cms/store/group/OneLepton/'

#############################################
########### Definition of weights ###########
#############################################

XSWeight = 'event.baseW*event.GEN_weight_SM/abs(event.GEN_weight_SM)'

SFweight1l = 'event.puW*event.effTrigW*event.std_vector_lepton_recoW[0]*event.electron_etaW_1l*event.electron_ptW_1l'

METFilter_Common = '(event.std_vector_trigger_special[0]*\
                     event.std_vector_trigger_special[1]*\
                     event.std_vector_trigger_special[2]*\
                     event.std_vector_trigger_special[3]*\
                     event.std_vector_trigger_special[5] )'

METFilter_MCver  =  '(event.std_vector_trigger_special[8]==-2.)'
METFilter_MCOld  =  '(event.std_vector_trigger_special[6]*event.std_vector_trigger_special[7])'
METFilter_MCNew  =  '(event.std_vector_trigger_special[8]*event.std_vector_trigger_special[9])'
METFilter_MC     =  METFilter_Common + '*' + '(('+METFilter_MCver+'*'+METFilter_MCOld+') or ((not '+METFilter_MCver+')*'+METFilter_MCNew+'))' 

METFilter_DATA   =  METFilter_Common + '*' + '(event.std_vector_trigger_special[4]*\
                                              event.std_vector_trigger_special[8]*\
                                              event.std_vector_trigger_special[9])'




# samples

#samples = {}

samples['HH'] = {	'name' : getSampleFiles(directory_MC, 'HHWWbblvjj_nevents5k', True),
			'weight' : XSWeight + '*' + SFweight1l + '*' + METFilter_MC,
		}

samples['Wjets'] = { 	'name' :   getSampleFiles(directory_MC, 'WJetsToLNu_HT100_200', True)\
				+ getSampleFiles(directory_MC, 'WJetsToLNu_HT200_400', True)\
				+ getSampleFiles(directory_MC, 'WJetsToLNu_HT400_600', True)\
				+ getSampleFiles(directory_MC, 'WJetsToLNu_HT600_800', True)\
				+ getSampleFiles(directory_MC, 'WJetsToLNu_HT800_1200_ext1', True)\
				+ getSampleFiles(directory_MC, 'WJetsToLNu_HT1200_2500', True)\
				+ getSampleFiles(directory_MC, 'WJetsToLNu_HT2500_inf', True),
				'weight': XSWeight + '*' + SFweight1l + '*' + METFilter_MC ,
				'FilesPerJob' : 3,
		   }



#samples['TT']  = {    'name'   : getSampleFiles(directory_MC, 'TTToSemiLepton', True) ,
#                      'weight' :   XSWeight + '*' + SFweight1l + '*' + METFilter_MC ,
#		      'FilesPerJob' : 3,
#		 }

#others minor backgrounds all inside Others
#samples['Others']  = {    'name'   : getSampleFiles(directory_MC, 'TTWJetsToLNu', True) \
#                                +       getSampleFiles(directory_MC, 'WZTo1L1Nu2Q', True) \
#                                +       getSampleFiles(directory_MC, 'WZTo1L3Nu', True) \
#                                +       getSampleFiles(directory_MC, 'WWW', True) \
#                                +       getSampleFiles(directory_MC, 'WWZ', True) \
#                                +       getSampleFiles(directory_MC, 'DYJetsToLL_M-10to50-LO', True) \
#                                +       getSampleFiles(directory_MC, 'WWTo2L2Nu', True) \
#                                +       getSampleFiles(directory_MC, 'WZTo2L2Q', True) \
#                                +       getSampleFiles(directory_MC, 'ZZTo2L2Q', True) ,
#                                'weight' :    XSWeight + '*' + SFweight1l + '*' + METFilter_MC ,
#                        'FilesPerJob' : 3,
#                         }

#other minor backgrounds in separated samples
#samples['TTW']  = {    'name'   : getSampleFiles(directory, 'TTWJetsToLNu') ,
#                                                'weight' :   '1.' ,
#	                 }


#samples['WZTo1L1Nu2Q']  = {    'name'   : getSampleFiles(directory, 'WZTo1L1Nu2Q') ,
#                                                'weight' :   '1.' ,
#                 }



#samples['WZTo1L3Nu']  = {    'name'   : ['latino_WZTo1L3Nu__part0.root',
#					'latino_WZTo1L3Nu__part1.root'] ,
#                                                'weight' :   '1.' ,
#                 }



#samples['WWW']  = {    'name'   : ['latino_WWW__part0.root'] ,
#                                                'weight' :   '1.' ,
#                 }

#samples['WWZ']  = {    'name'   : ['latino_WWZ__part0.root'] ,
#                                                'weight' :   '1.' ,
#                 }

#samples['DY']  = {    'name'   : getSampleFiles(directory, 'DYJetsToLL_M-10to50-LO'),
#			'weight' :   '1.' ,
#			'FilesPerJob' : 3,
#                  }

#samples['WWTo2L2Nu']  = {    'name'   : getSampleFiles(directory, 'WWTo2L2Nu') ,
#                                'weight' :   '1.' ,
#				'FilesPerJob' : 3,
#                         }

#samples['WZTo2L2Q']  = {    'name'   : getSampleFiles(directory, 'WZTo2L2Q') ,
#                                'weight' :   '1.' ,
#				'FilesPerJob' : 3,
#                  }

#samples['ZZTo2L2Q']  = {    'name'   : getSampleFiles(directory, 'ZZTo2L2Q') ,
#                                'weight' :   '1.' ,
#				'FilesPerJob' : 3,
#                  }




###########################################
################## DATA ###################
###########################################

DataRun = [ 
            ['B','Run2016B-03Feb2017_ver2-v2'] , 
            ['C','Run2016C-03Feb2017-v1'] , 
            ['D','Run2016D-03Feb2017-v1'] , 
            ['E','Run2016E-03Feb2017-v1'] ,
            ['F','Run2016F-03Feb2017-v1'] , 
            ['G','Run2016G-03Feb2017-v1'] , 
            ['H','Run2016H-03Feb2017_ver2-v1'] ,
	    ['H','Run2016H-03Feb2017_ver3-v1'] ,
          ] 

DataSets = ['SingleMuon','SingleElectron']

DataTrig = {
            'SingleMuon'     : 'trig_SnglMu' ,
            'SingleElectron' : '!trig_SnglMu && trig_SnglEle' ,
	   }

samples['DATA']  = {    'name'   : [],
				   'weight' : METFilter_DATA,
				   'weights' : [],
				   'isData': ['all'],
                      		   'FilesPerJob' : 2,
		   }		

for Run in DataRun :
	directory = treeBaseDir+'Apr2017_Run2016'+Run[0]+'_RemAOD/lepSel__EpTCorr__TrigMakerData__cleanTauData__hadd/'
	for DataSet in DataSets :
 		FileTarget = getSampleFiles(directory,DataSet+'_'+Run[1],True)
		for iFile in FileTarget:
			samples['DATA']['name'].append(iFile)
			samples['DATA']['weights'].append(DataTrig[DataSet]) 
