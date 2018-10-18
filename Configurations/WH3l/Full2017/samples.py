import os
from LatinoAnalysis.Tools.commonTools import *

def getSampleFilesNano(inputDir,Sample,absPath=False,rootFilePrefix='nanoLatino_',FromPostProc=False):
    return [ s.lstrip('#') for s in getSampleFiles(inputDir, Sample, absPath, rootFilePrefix, FromPostProc) ]


def addSampleWeightNano(sampleDic,key,Sample,Weight):
    # Modified from LatinoAnalysis/Tools/python/commonTools.py
    if not 'weights' in sampleDic[key] :
      sampleDic[key]['weights'] = []
    if len(sampleDic[key]['weights']) == 0 :
      for iEntry in range(len(sampleDic[key]['name'])) : sampleDic[key]['weights'].append('(1.)')

    ### Now add the actual weight
    for iEntry in range(len(sampleDic[key]['name'])):
      name = sampleDic[key]['name'][iEntry].replace('nanoLatino_','').replace('.root','').split('__part')[0]
      if '/' in name : name = os.path.basename(name)
      if name == Sample:
        sampleDic[key]['weights'][iEntry] += '*(' + Weight + ')'

# samples={}

################################################
################# SKIMS ########################
################################################

skim='__vh3lSel'

if skim =='__vh3lSel' :
    skimFake='__vh3lFakeSel'
else:
    skimFake=skim

##############################################
###### Tree Directory according to site ######
##############################################

treeBaseDir = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/"

directoryMC     = os.path.join(treeBaseDir,"Fall2017_nAOD_v1_Full2017/MCl1loose2017__MCformulas__MCWeights2017")
directoryDATA   = os.path.join(treeBaseDir,"Run2017_nAOD_v1_Full2017/DATAl1loose2017__l2loose__hadd")
directoryFAKE   = os.path.join(treeBaseDir,"Run2017_nAOD_v1_Full2017/DATAl1loose2017__l2loose__hadd")


################################################
############ basic mc weights ##################
################################################

replaceNLep = lambda s, nLep : s.format(nLep)

XSWeight    = 'XSWeight'
SFweight    = replaceNLep('SFweight{0}l',3)

GenLepMatch   = 'GenLepMatch{0}l'
GenLepMatch2l = replaceNLep(GenLepMatch,2)
GenLepMatch3l = replaceNLep(GenLepMatch,3)

################################################
################# POG  WP ######################
################################################

#... b jet

bSF="bPogSF_deepCSVBT"
bVeto="bveto_deepCSVBT"

#... lepton:

eleWP='mvaFall17Iso_WP90'
muWP='cut_Tight'
LepWPCut        = 'LepCut3l__ele_'+eleWP+'__mu_'+muWP+'_HWWW'
LepWPweight     = 'LepSF3l__ele_'+eleWP+'__mu_'+muWP+'_HWWW'

#... And the fakeW
fakeW = 'fakeW_ele_'+eleWP+'_mu_'+muWP+'_3l'

SFweight += '*'+LepWPweight+'*'+LepWPCut

################################################
############   MET  FILTERS  ###################
################################################

METFilter_MC   = 'METFilter_MC'
METFilter_DATA = 'METFilter_DATA'

################################################
############ DATA DECLARATION ##################
################################################

DataRun = [
            ['B','Run2017B-31Mar2018-v1'] ,
            ['C','Run2017C-31Mar2018-v1'] ,
            ['D','Run2017D-31Mar2018-v1'] ,
            ['E','Run2017E-31Mar2018-v1'] ,
            ['F','Run2017F-31Mar2018-v1'] ,
          ]

DataSets = ['MuonEG','DoubleMuon','SingleMuon','DoubleEG','SingleElectron']


DataTrig = {
            'MuonEG'         : ' trig_EleMu' ,
            'DoubleMuon'     : '!trig_EleMu &&  trig_DbleMu' ,
            'SingleMuon'     : '!trig_EleMu && !trig_DbleMu &&  trig_SnglMu' ,
            'DoubleEG'       : '!trig_EleMu && !trig_DbleMu && !trig_SnglMu &&  trig_DbleEle' ,
            'SingleElectron' : '!trig_EleMu && !trig_DbleMu && !trig_SnglMu && !trig_DbleEle &&  trig_SnglEle' ,
           }

samples['DATA']  = {   'name': [] ,
                       'weight' : 'veto_EMTFBug'+'*'+METFilter_DATA+'*'+LepWPCut,
                       'weights' : [],
                       'isData': ['all'],
                       'FilesPerJob' : 5 ,
                   }

samples['Fake']  = {   'name': [] ,
                       'weight' : fakeW+'*'+'veto_EMTFBug'+'*'+METFilter_DATA,
                       'weights' : [],
                       'isData': ['all'],
                       'FilesPerJob' : 5 ,
                   }

for Run in DataRun :
    directoryDATARun = directoryDATA.format(Run[0])
    directoryFAKERun = directoryFAKE.format(Run[0])
    for DataSet in DataSets :
        FileTargetDATA = getSampleFilesNano(directoryDATARun,DataSet+'_'+Run[1],True)
        FileTargetFAKE = getSampleFilesNano(directoryFAKERun,DataSet+'_'+Run[1],True)
        for iFile in FileTargetDATA:
            samples['DATA']['name']   .append(iFile)
            samples['DATA']['weights'].append(DataTrig[DataSet])
            addSampleWeightNano(samples,'DATA',DataSet+'_'+Run[1],DataTrig[DataSet])
        for iFile in FileTargetFAKE:
            samples['Fake']['name']   .append(iFile)
            samples['Fake']['weights'].append(DataTrig[DataSet])
            addSampleWeightNano(samples,'Fake',DataSet+'_'+Run[1],DataTrig[DataSet])

###########################################
#############  BACKGROUNDS  ###############
###########################################

samples['WW'] = {
    'name'   : getSampleFilesNano(directoryMC,'WWTo2L2Nu'),
    'weight' : XSWeight+'*'+SFweight+'*'+GenLepMatch2l+'*'+METFilter_MC + '*nllW' ,
    'suppressNegativeNuisances' :['all'],
}

samples['ZZ'] = {
    'name': getSampleFilesNano(directoryMC,'ZZTo4L'),
    'weight' : XSWeight+'*'+SFweight+'*'+GenLepMatch3l+'*'+METFilter_MC ,
    'suppressNegativeNuisances' :['all'],
}

# samples['ggZZ_em'] = {
#     'name': getSampleFilesNano(directoryMC,'ggZZ2e2m'),
#     'weight' : XSWeight+'*'+SFweight+'*'+GenLepMatch3l+'*'+METFilter_MC ,
#     'suppressNegativeNuisances' :['all'],
# }

# samples['ggZZ_ee'] = {
#     'name': getSampleFilesNano(directoryMC,'ggZZ4e'),
#     'weight' : XSWeight+'*'+SFweight+'*'+GenLepMatch3l+'*'+METFilter_MC ,
#     'suppressNegativeNuisances' :['all'],
# }

# samples['ggZZ_mm'] = {
#     'name': getSampleFilesNano(directoryMC,'ggZZ4m'),
#     'weight' : XSWeight+'*'+SFweight+'*'+GenLepMatch3l+'*'+METFilter_MC ,
#     'suppressNegativeNuisances' :['all'],
# }

wzSF = '1.108'
samples['WZ'] = {
    'name': getSampleFilesNano(directoryMC,'WZTo3LNu'),
    'weight' : XSWeight+'*'+SFweight+'*'+GenLepMatch3l+'*'+METFilter_MC+'*'+wzSF,
    'suppressNegativeNuisances' :['all'],
}

samples['VVV'] = {
    'name': getSampleFilesNano(directoryMC,'WWW')
           +getSampleFilesNano(directoryMC,'WWZ')
           +getSampleFilesNano(directoryMC,'WZZ')
           +getSampleFilesNano(directoryMC,'ZZZ'),
    'weight' : XSWeight+'*'+SFweight+'*'+GenLepMatch3l+'*'+METFilter_MC,
    'suppressNegativeNuisances' :['all'],
}

# Not seen in nanoLatino
# samples['Vg'] = {
#     'name': getSampleFilesNano(directoryMC,'WgStarLNuEE')
#            +getSampleFilesNano(directoryMC,'WgStarLNuMuMu')
#            +getSampleFilesNano(directoryMC,'Zg'),
#     'weight' : XSWeight+'*'+SFweight+'*'+GenLepMatch3l+'*'+METFilter_MC ,
#     'suppressNegativeNuisances' :['all'],
# }

####################################
############# Signal ###############
####################################

# Not ready in nanoLatino
# samples['WH_htt']  = {
#     'name': getSampleFilesNano(directoryMC,'HWminusJ_HToTauTau_M125')
#            +getSampleFilesNano(directoryMC,'HWplusJ_HToTauTau_M125')
#            +getSampleFilesNano(directoryMC,'HZJ_HToTauTau_M125'),
#     'weight' : XSWeight+'*'+SFweight+'*'+GenLepMatch3l+'*'+METFilter_MC,
#     'suppressNegativeNuisances' :['all'],
# }

# samples['ZH_hww']  = {
#     'name': getSampleFilesNano(directoryMC,'ggZH_HToWW_M125')
#            +getSampleFilesNano(directoryMC,'HZJ_HToWW_M125'),
#     'weight' : XSWeight+'*'+SFweight+'*'+GenLepMatch3l+'*'+METFilter_MC,
#     'suppressNegativeNuisances' :['all'],
# }

# samples['WH_hww']  = {
#     'name': getSampleFilesNano(directoryMC,'HWminusJ_HToWW_M125')
#            +getSampleFilesNano(directoryMC,'HWplusJ_HToWW_M125'),
#     'weight' : XSWeight+'*'+SFweight+'*'+GenLepMatch3l+'*'+METFilter_MC,
#     'suppressNegativeNuisances' :['all'],
# }

