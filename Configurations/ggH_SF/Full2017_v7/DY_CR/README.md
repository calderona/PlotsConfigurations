# Systematic Uncertainties Extraction for Data-Driven Drell-Yan Estimation Method

Configuration for the extraction of the systematic uncertainties associated to the data-driven method used for Drell-Yan estimation in the same-flavor channel

### Submit shapesmulti in batch

    mkShapesMulti.py --pycfg=configuration.py --doBatch=1 --batchSplit=Samples,Files --batchQueue=testmatch

### Hadd files

    mkShapesMulti.py --pycfg=configuration.py --doHadd=1 --batchSplit=Samples,Files --doNotCleanup --nThreads=8

### Plot input distributions

    mkPlot.py --inputFile=rootFile/plots_ggH_SF_2017_v7_DYMVA_CR.root --fileFormats=png --onlyPlot=cratio --minLogCratio=1 --maxLogCratio=1000000


Remove meaningless plots:

    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_0j_*dnn_1j* 
    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_0j_*dnn_2j* 
    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_0j_*dnn_VH* 
    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_0j_*dnn_VBF* 

    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_1j_*dnn_0j* 
    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_1j_*dnn_2j* 
    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_1j_*dnn_VH* 
    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_1j_*dnn_VBF* 

    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_2j_*dnn_0j* 
    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_2j_*dnn_1j* 
    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_2j_*dnn_VH* 
    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_2j_*dnn_VBF* 

    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_VBF_*dnn_0j* 
    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_VBF_*dnn_1j* 
    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_VBF_*dnn_2j* 
    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_VBF_*dnn_VH* 

    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_VH_*dnn_0j* 
    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_VH_*dnn_1j* 
    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_VH_*dnn_2j* 
    rm plots_ggH_SF_2017_v7_DY_CR/*cratio*_VH_*dnn_VBF* 


To get a reasonable correction we subtract from data all processes except Drell-Yan. The output is then divided by the DY MC histogram, and a linear fit is performed.

    mkDYCorr.py --input_file=rootFile/plots_ggH_SF_2017_v7_DYMVA_CR.root --cut=0j_ee_in --variable=mth --fit_func=pol1
    mkDYCorr.py --input_file=rootFile/plots_ggH_SF_2017_v7_DYMVA_CR.root --cut=0j_mm_in --variable=mth --fit_func=pol1
    mkDYCorr.py --input_file=rootFile/plots_ggH_SF_2017_v7_DYMVA_CR.root --cut=1j_ee_in --variable=mth --fit_func=pol2
    mkDYCorr.py --input_file=rootFile/plots_ggH_SF_2017_v7_DYMVA_CR.root --cut=1j_mm_in --variable=mth --fit_func=pol2
    mkDYCorr.py --input_file=rootFile/plots_ggH_SF_2017_v7_DYMVA_CR.root --cut=2j_ee_in --variable=mth --fit_func=pol1
    mkDYCorr.py --input_file=rootFile/plots_ggH_SF_2017_v7_DYMVA_CR.root --cut=2j_mm_in --variable=mth --fit_func=pol1
