#!/usr/bin/env python
import os, sys
import time
import math
import subprocess
from AnalysisToolLight.AnalysisTool.tools.batch_helper import createSubmissionScript, splitInputFile
from AnalysisToolLight.AnalysisTool.batch.datasets import *


# Analysis to run #######################
ANALYSIS = '2Mu'
#version = '76X'
version = '80X'

## Datasets ##############################
#datasets76X = {
#    'SingleMuon2015C' : { 'njobs' : 1 },
#    'SingleMuon2015D' : { 'njobs' : 12 },
#    'DYJetsToLL'  : { 'njobs' : 6 },
#    'TTJets'      : { 'njobs' : 2 },
#    'TTZToLLNuNu' : { 'njobs' : 1 },
#    'WWTo2L2Nu'   : { 'njobs' : 2 },
#    'WZTo2L2q'    : { 'njobs' : 8 },
#    'WZTo3LNu'    : { 'njobs' : 1 },
#    'ZZTo2L2Nu'   : { 'njobs' : 2 },
#    'ZZTo2L2q'    : { 'njobs' : 4 },
#    'ZZTo4L'      : { 'njobs' : 2 },
#}
#
#datasets80X = {
#    'SingleMuon2015C' : { 'njobs' : 1 },
#    'SingleMuon2015D' : { 'njobs' : 12 },
#    'DYJetsToLL'  : { 'njobs' : 6 },
#    'TTJets'      : { 'njobs' : 2 },
#    'TTZToLLNuNu' : { 'njobs' : 1 },
#    'WWTo2L2Nu'   : { 'njobs' : 2 },
#    'WZTo2L2q'    : { 'njobs' : 8 },
#    'WZTo3LNu'    : { 'njobs' : 1 },
#    'ZZTo2L2Nu'   : { 'njobs' : 2 },
#    'ZZTo2L2q'    : { 'njobs' : 4 },
#    'ZZTo4L'      : { 'njobs' : 2 },
#}


# Options ###############################
BASEDIR='{0}/src/AnalysisToolLight'.format(os.environ['CMSSW_BASE'])
RESULTSDIR='{0}/2Mu/batch/results{1}'.format(BASEDIR, version)

## ___________________________________________________________
def main():
    tmpdir = 'tmp{0}'.format(version)
    # clear tmp directory and start over
    if os.path.exists(tmpdir): 
        os.system('rm {0}/*'.format(tmpdir))
    else:
        os.system('mkdir {0}/'.format(tmpdir))
    os.chdir(tmpdir)
    # build options map
    options = {
        'ANALYSIS' : ANALYSIS,
        'BASEDIR' : BASEDIR,
        'RESULTSDIR' : RESULTSDIR,
        #'datasets' : datasets,
    }
    
    if '76X' in version: options['datasets'] = datasets76X
    elif '80X' in version: options['datasets'] = datasets80X

    # loop over datasets and make input files lists, sub scripts
    for dset in datasets:
        print '{0}:'.format(dset)

        # calculate number of jobs to run
        print '    calculating number of jobs and creating inputs'
        #datasets[dset]['inputlist'] = '{0}/AnalysisTool/data/inputfiles_{1}.txt'.format(BASEDIR, dset)
        datasets[dset]['inputlist'] = '{0}/AnalysisTool/data/{2}/inputfiles_{1}.txt'.format(BASEDIR, dset, version)
        datasets[dset]['output']    = '{0}/ana_{1}_{2}.root'.format(RESULTSDIR, ANALYSIS, dset)
        datasets[dset]['logfile']   = '{0}/log_{1}_{2}.log'.format(RESULTSDIR, ANALYSIS, dset)

        # create input file lists
        with open(datasets[dset]['inputlist'], 'r') as f:
            for i, line in enumerate(f):
                pass
        i+=1
        njobs = datasets[dset]['njobs']
        nlinesperjob = int(math.ceil(float(i)/njobs))
        nlineslastjob = i - (njobs-1)*nlinesperjob

        # print a warning if the last job is <15% the size of the others
        if (float(nlineslastjob)/float(nlinesperjob)) < 0.15:
            print 'Warning: last job is disproportionately small (NJOBS: {0}, NLINES/JOB: {1}, NLINES/LASTJOB: {2}'.format(njobs, nlinesperjob, nlineslastjob)
        splitInputFile(datasets[dset]['inputlist'], njobs, nlinesperjob)
    
        print '    creating {0} submission script{1}'.format(njobs, '' if njobs==1 else 's')

        # create submission scripts
        for n in xrange(0, njobs):
            createSubmissionScript(dset, n, njobs, **options)
    
    os.chdir('../')
    
    # submit jobs
    print '\nSubmitting jobs...'
    for dset in datasets:
        njobs = datasets[dset]['njobs']
        for n in xrange(0, njobs):
            scriptname = '{4}/job_{0}_{1}_{2}of{3}.sh'.format(dset, ANALYSIS, n+1, njobs, tmpdir)
            jobname = '{0}{2}{1}'.format(dset, '' if njobs==1 else '_{0}'.format(n+1), version[:-1])
            print 'bsub -q 8nh -J {0} < {1}'.format(jobname, scriptname)
            os.system('bsub -q 8nh -J {0} < {1}'.format(jobname, scriptname))
            print
            time.sleep(1)




if __name__ == "__main__":
    main()
