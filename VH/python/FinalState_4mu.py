# VH/FinalState_4mu.py
import glob
import itertools
import argparse
from collections import OrderedDict
import ROOT
from AnalysisBase import main as analysisBaseMain
from AnalysisToolLight.AnalysisToolLight.AnalysisBase import AnalysisBase

## ___________________________________________________________
class CutFlow(object):
    '''
    The CutFlow object keeps track of the cutflow and helps fill
    the efficiencies histogram at the end of the job.
    '''
    def __init__(self, *args):
        self.counters = OrderedDict()
        for arg in args: # initialise all counters to 0
            self.counters[arg] = 0
    def proliferate(self, arg): # increases counter "arg" by 1
        self.counters[arg] += 1.
    def numBins(self): # returns number of counters
        return len(self.counters)
    def count(self, counter): # returns the current value of the counter "arg"
        return self.counters[counter]
    def getNames(self): # returns ordered dict of counters
        return self.counters.keys()


## ___________________________________________________________
class VH4Mu(AnalysisBase):
    def __init__(self, **kwargs):
        filenames = []
        inputFileList = kwargs.pop(inputFileList, [])
        with open('inputFileList','r') as f:
            for line in f.readlines():
                self.filenames += glob.glob(line.strip())
        super(VH4Mu, self).__init__(filenames = filenames, **kwargs)
        #############################
        # Initialise event counters #
        #############################
        self.cutflow = CutFlow(
            'nEv_Skim',
            'nEv_PV',
        )

        #############################
        # Book histograms ###########
        #############################
        self.histograms['hLeadMuPt']    = ROOT.TH1F('hLeadMuPt', 'hLeadMuPt', 200, 0, 200)
        self.histograms['hSubLeadMuPt'] = ROOT.TH1F('hSubLeadMuPt', 'hSubLeadMuPt', 200, 0, 200)
        self.histograms['hDiMuPt']      = ROOT.TH1F('hDiMuPt', 'hDiMuPt', 200, 0, 200)
        self.histograms['hDiMuInvMass'] = ROOT.TH1F('hDiMuInvMass', 'hDiMuInvMass', 200, 0, 200)

        self.histograms['hEfficiencies'] = ROOT.TH1F('hEfficiencies', 'hEfficiencies', self.cutflow.numBins(), 0, self.cutflow.numBins())

    ## _______________________________________________________
    def perEventAction(self):
        '''
        This is the core of the analysis loop. Selection is done here.
        '''
        #############################
        # Define cuts ###############
        #############################
        cMuPt = 20.
        cMuEta = 2.4
        cDiMuPt = 50.

        self.cutflow.proliferate('nEv_Skim')

        #############################
        # MUONS #####################
        #############################
        # loop over muons and save the good ones
        self.goodMuons = []
        for muon in self.muons:

            # muon cuts
            if not muon.Pt() > cMuPt: continue
            if not muon.Eta() > cMuEta: continue

            # if we get to this point, push muon into goodMuons
            self.goodMuons += [muon]



        #############################
        # DIMUON PAIRS ##############
        #############################
        # loop over all possible pairs of muons
        self.dimuon = () 
        maxDiMuPt = 0
        if len(self.goodMuons) >= 2:
            for pair in itertools.combinations(self.goodMuons,2):
                diMuP4 = pair[0].P4() + pair[1].P4()
                if diMuP4.Pt() > min(maxDiMuPt, cDiMuPt):
                    maxDiMuPt = diMuP4.Pt()
                    #self.dimuon = pair if pair[0].Pt() > pair[1].Pt() else (pair[1], pair[0])
                    if pair[0].Pt() > pair[1].Pt(): self.dimuon = pair
                    else: self.dimuon = (pair[1], pair[0])

        # fill histograms
        self.fill()


    ## _______________________________________________________
    def fill(self):
        '''
        At the end of the analyze loop, fill the histograms. Called once per event.
        '''
        weight = 1.
        # leading muon
        mu0 = self.dimuon[0]

        self.histograms['hLeadMuPt'].Fill(mu0.Pt(), weight)

        # subleading muon
        mu1 = self.dimuon[1]
        self.histograms['hSubLeadMuPt'].Fill(mu1.Pt(), weight)

        # diumuon
        diMuP4 = mu0.P4() + mu1.P4()
        self.fillVar('hDiMuPt', diMuP4.Pt(), weight)
        self.fillVar('hDiMuInvMass', diMuP4.M(), weight)
        


    ## _______________________________________________________
    def endJob(self):
        '''
        At the end of the job, fill efficiencies histogram.
        '''
        for i, name in enumerate(self.cutflow.getNames()):
            # 0 is the underflow bin in root: first bin to fill is bin 1
            self.histograms['hEfficiencies'].SetBinContent(i+1, self.cutflow.count(name))
            self.histograms['hEfficiencies'].GetXaxis().SetBinLabel(i+1, name)

## ___________________________________________________________
if __name__ == "__main__":
    status = main()
    sys.exit(status)

# actually execute the analysis
def main(argv=None):
    args = analysisBaseMain(argv)
    VH4Mu(inputFileList = args.inputFileList).analyze()
