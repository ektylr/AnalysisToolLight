# AnalysisToolLight/AnalysisTool/python/ScaleFactors.py
'''
ScaleFactor class base
'''
import argparse
import logging

import ROOT
from collections import OrderedDict, namedtuple

## ___________________________________________________________
class ScaleFactor(object):
    '''
    Scale factor object
    '''
    # constructors/helpers
    def __init__(self, cmsswversion, datadir):
        self.cmsswversion = cmsswversion
        self.datadir = datadir


## ___________________________________________________________
class PileupWeights(ScaleFactor):
    # constructors/helpers
    def __init__(self, cmsswversion, datadir):
        super(PileupWeights, self).__init__(cmsswversion, datadir)

        self.pileupScale = []
        self.pileupScale_up = []
        self.pileupScale_down = []

        logging.info('  Looking for pileup file at {0}/pileup/pileup_{1}.root'.format(self.datadir, self.cmsswversion))
        # now we look for a file called pileup_76X.root or pileup_80X.root in datadir/pileup/
        try:
            pufile = ROOT.TFile('{0}/pileup/pileup_{1}.root'.format(self.datadir, self.cmsswversion))
            scalehist_ = pufile.Get('pileup_scale')

            # save scale factors in vectors where each index corresponds to the NumTruePileupInteractions
            # for each histogram, set (b)th entry in self.pileupScale to bin content of (b+1)th bin (0th bin is underflow)
            for b in range(scalehist_.GetNbinsX()):
                self.pileupScale.append(scalehist_.GetBinContent(b+1))
            scalehist_ = pufile.Get('pileup_scale_up')
            for b in range(scalehist_.GetNbinsX()):
                self.pileupScale_up.append(scalehist_.GetBinContent(b+1))
            scalehist_ = pufile.Get('pileup_scale_down')
            for b in range(scalehist_.GetNbinsX()):
                self.pileupScale_down.append(scalehist_.GetBinContent(b+1))

            pufile.Close()

        # AttributeError: 'TObject' object has no attribute 'GetNbinsX' - happens if we couldn't find the file
        except AttributeError:
            logging.info('    *******')
            logging.info('    WARNING: Pileup file probably doesn\'t exist or was made improperly.')
            logging.info('    Will not include pileup reweighting.')
            logging.info('    *******')

    # methods
    def getWeight(self, numtrueinteractions):
        return self.pileupScale[int(round(numtrueinteractions))] if len(self.pileupScale) > numtrueinteractions else 0.
    def getWeightUp(self, numtrueinteractions):
        return self.pileupScale_up[int(round(numtrueinteractions))] if len(self.pileupScale_up) > numtrueinteractions else 0.
    def getWeightDown(self, numtrueinteractions):
        return self.pileupScale_down[int(round(numtrueinteractions))] if len(self.pileupScale_down) > numtrueinteractions else 0.








## ___________________________________________________________
class HLTScaleFactors(ScaleFactor):
# https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffsRun2
    # constructors/helpers
    def __init__(self, cmsswversion, datadir, hltrigger):
        super(HLTScaleFactors, self).__init__(cmsswversion, datadir)

        # right now the only choice is single muon hlt
        if hltrigger=='IsoMu20_OR_IsoTkMu20':
            filename = 'singlemuontrigger'
        else:
            raise ValueError('Right now the only available HLT for scale factors is "IsoMu20_OR_IsoTkMu20".')

        logging.info('  Looking for scale factor file at {0}/scalefactors/{1}_{2}.root'.format(self.datadir, filename, self.cmsswversion))

        #try:
        # this is the file created by AnalysisTool/scripts/collectTriggerScaleFactors.py
        self.hltfile = ROOT.TFile('{0}/scalefactors/{1}_{2}.root'.format(self.datadir, filename, self.cmsswversion))

        # the histograms in the file are named effMC and effDA, with x axis: Pt, y axis: AbsEta
        self.effhistDA_ = self.hltfile.Get('effDA')
        self.effhistMC_ = self.hltfile.Get('effMC')

        self.maxpt = self.effhistDA_.GetXaxis().GetXmax()
        self.maxeta = self.effhistDA_.GetYaxis().GetXmax()

        print 'maxpt = {0} and maxeta = {1}'.format(self.maxpt, self.maxeta)

        #except :

        ## trigger scale factors
        #logging.info('Loading trigger scale factor info...')
        ##try:
        #self.hltweights = HLTScaleFactors(self.cmsswversion, self.datadir, self.pathForTriggerScaleFactors)
        ##except AttributeError as err:
        ##    logging.info('    AttributeError: '.format(err))
        ##    logging.info('    *******')
        ##    logging.info('    WARNING: self.pathForTriggerScaleFactors is not set.')
        ##    logging.info('    Will not include trigger scale factors.')
        ##    logging.info('    *******')


    # methods
    def getScale(self, muons):
        xda = 1.
        xmc = 1.
        for mu in muons:
            # make sure the muon is in range
            pt_ = min(self.maxpt, mu.Pt())
            eta_ = min(self.maxeta, mu.AbsEta())
            # find efficiencies for this muon
            effda = self.effhistDA_.GetBinContent( self.effhistDA_.GetXaxis().FindBin(pt_) , self.effhistDA_.GetYaxis().FindBin(eta_))
            print 'da: found eff of {0} in bin {1},{2} for mu with pt {3} and eta {4}'.format(effda, self.effhistDA_.GetXaxis().FindBin(pt_), self.effhistDA_.GetYaxis().FindBin(eta_), pt_, eta_)
            effmc = self.effhistMC_.GetBinContent( self.effhistMC_.GetXaxis().FindBin(pt_) , self.effhistMC_.GetYaxis().FindBin(eta_))
            print 'mc: found eff of {0} in bin {1},{2} for mu with pt {3} and eta {4}'.format(effmc, self.effhistMC_.GetXaxis().FindBin(pt_), self.effhistMC_.GetYaxis().FindBin(eta_), pt_, eta_)
            # update total efficiency
            xda *= (1. - effda)
            xmc *= (1. - effmc)
        # calculate scale factor and return it
        sf = (1. - xda) / (1. - xmc)
        return sf

    def __del__(self):
        self.hltfile.Close()

