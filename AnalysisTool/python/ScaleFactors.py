# AnalysisToolLight/AnalysisTool/python/ScaleFactors.py
'''
ScaleFactor class base
'''
import argparse
import logging
import os.path

import ROOT
from collections import OrderedDict, namedtuple

## _____________________________________________________________________________
class ScaleFactor(object):
    '''
    Scale factor object
    '''
    # constructors/helpers
    def __init__(self, cmsswversion, datadir):
        self.cmsswversion = cmsswversion
        self.datadir = datadir


## _____________________________________________________________________________
class PileupWeights(ScaleFactor):
    # constructors/helpers
    def __init__(self, cmsswversion, datadir, shift):
        super(PileupWeights, self).__init__(cmsswversion, datadir)
        self.error = False
        self.shift = shift
        self.pileup_scale = []
        self.pileup_scale_up = []
        self.pileup_scale_down = []
        filename = '{0}/pileup/pileup_{1}.root'.format(self.datadir,
            self.cmsswversion)

        logging.info('  Looking for pileup file at {0}'.format(filename))
        if not os.path.exists(filename):
            self.error = True
            logging.info('       *   ')
            logging.info('    *******')
            logging.info('    WARNING: Can\'t find Pileup file.')
            logging.info('    Will not include pileup reweighting.')
            logging.info('    *******')
            logging.info('       *   ')
        else:
            # now we look for a file called pileup_76X.root or pileup_80X.root
            #     in datadir/pileup/
            pufile = ROOT.TFile(filename)
            scalehist_ = pufile.Get('pileup_scale')

            # save scale factors in vectors where each index corresponds
            #     to the NumTruePileupInteractions 
            # for each histogram, set (b)th entry in self.pileup_scale
            #     to bin content of (b+1)th bin (0th bin is underflow)
            for b in range(scalehist_.GetNbinsX()):
                self.pileup_scale.append(scalehist_.GetBinContent(b+1))
            scalehist_ = pufile.Get('pileup_scale_Up')
            for b in range(scalehist_.GetNbinsX()):
                self.pileup_scale_up.append(scalehist_.GetBinContent(b+1))
            scalehist_ = pufile.Get('pileup_scale_Down')
            for b in range(scalehist_.GetNbinsX()):
                self.pileup_scale_down.append(scalehist_.GetBinContent(b+1))

            pufile.Close()


    # methods
    ## _________________________________________________________________________
    def get_weight(self, numtrueinteractions):
        if self.error: return 1.
        thisindex = int(round(numtrueinteractions))
        if self.shift == 'Down':
            return self.pileup_scale_down[thisindex] if len(self.pileup_scale_down) > thisindex else 0.
        elif self.shift == 'Up':
            return self.pileup_scale_up[thisindex]if len(self.pileup_scale_up) > thisindex else 0.
        else:
            return self.pileup_scale[thisindex] if len(self.pileup_scale) > thisindex else 0.


## _____________________________________________________________________________
class VariablePileupWeights(ScaleFactor):
    # constructors/helpers
    def __init__(self, cmsswversion, datadir, fname_tail, xsec_list):
        super(VariablePileupWeights, self).__init__(cmsswversion, datadir)
        self.error = False

        self.xsec_range = xsec_list

        self.pileup_scale_map = {}
        for xsec in self.xsec_range:
            self.pileup_scale_map[xsec] = []

        filename = '{0}/pileup/pileup_{1}_{2}.root'.format(self.datadir,
            cmsswversion, fname_tail)

        logging.info('  Looking for pileup file at {0}'.format(filename))
        if not os.path.exists(filename):
            self.error = True
            logging.info('       *   ')
            logging.info('    *******')
            logging.info('    WARNING: Can\'t find Pileup file.')
            logging.info('    *******')
            logging.info('       *   ')
        else:
            pufile = ROOT.TFile(filename)
            for xsec in self.xsec_range:
                scalehist_ = pufile.Get('pileup_scale_{0}'.format(xsec))
                for b in range(scalehist_.GetNbinsX()):
                    self.pileup_scale_map[xsec].append(
                        scalehist_.GetBinContent(b+1))
                    
            pufile.Close()

    # methods 
    ## _________________________________________________________________________
    def get_minbias_range(self):
        return self.xsec_range

    ## _________________________________________________________________________
    def get_weight_for_xsec(self, minbiasxsec, numtrueinteractions):
        if minbiasxsec not in self.xsec_range:
            raise ValueError('{0} is not an available min bias xsec'.format(
                minbiasxsec))
        if self.error: return 1.

        thisindex = int(round(numtrueinteractions))
        if len(self.pileup_scale_map[minbiasxsec]) > thisindex:
            return self.pileup_scale_map[minbiasxsec][thisindex]
        else:
            return 0.



## _____________________________________________________________________________
class HLTScaleFactors(ScaleFactor):
# https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffsRun2
    # constructors/helpers
    def __init__(self, cmsswversion, datadir, hltrigger, shift):
        super(HLTScaleFactors, self).__init__(cmsswversion, datadir)
        self.error = False
        self.shift = shift

        # right now the only choice is single muon hlt
        if hltrigger=='IsoMu24_OR_IsoTkMu24':
            filename = 'singlemuontrigger'
        else:
            raise ValueError('Right now the only available HLT for scale '
                'factors is "IsoMu24_OR_IsoTkMu24".')

        filename = '{0}/scalefactors/{1}_{2}.root'.format(self.datadir,
            filename, self.cmsswversion)

        logging.info('  Looking for trigger scale factor file '
            'at {0}'.format(filename))
        if not os.path.exists(filename):
            self.error = True
            logging.info('       *   ')
            logging.info('    *******')
            logging.info('    WARNING: Can\'t find HLT scale factors file.')
            logging.info('    Will not include trigger scale factors.')
            logging.info('    *******')
            logging.info('       *   ')
            return
        else:
            # this is the file created by
            #     AnalysisTool/scripts/collectTriggerScaleFactors.py
            self.hltfile = ROOT.TFile(filename)

        # the histograms in the file are named effMC and effDA,
        #     with x axis: Pt, y axis: AbsEta
        self.effhistDA_ = self.hltfile.Get('effDA')

        self.effhistMC_ = self.hltfile.Get('effMC')

        self.minpt = self.effhistDA_.GetXaxis().GetXmin() + 0.1
        self.maxpt = self.effhistDA_.GetXaxis().GetXmax() - 1.
        self.maxeta = self.effhistDA_.GetYaxis().GetXmax()


    # methods
    def get_scale(self, muons):
        if self.error: return 1.

        s = 1.
        if self.shift == 'Down': s = 0.995
        elif self.shift == 'Up': s = 1.005

        xda = 1.
        xmc = 1.
        for mu in muons:
            # make sure the muon is in range
            pt_  = min(self.maxpt, mu.pt())
            eta_ = min(self.maxeta, mu.abs_eta())
            # find efficiencies for this muon
            #if scheme=='BCDEF':
            #    effda = self.effhistDA_BCDEF_.GetBinContent(
            #        self.effhistDA_BCDEF_.GetXaxis().FindBin(pt_),
            #        self.effhistDA_BCDEF_.GetYaxis().FindBin(eta_))
            #    effmc = self.effhistMC_BCDEF_.GetBinContent(
            #        self.effhistMC_BCDEF_.GetXaxis().FindBin(pt_),
            #        self.effhistMC_BCDEF_.GetYaxis().FindBin(eta_))
            #elif scheme=='GH':
            #    effda = self.effhistDA_GH_.GetBinContent(
            #        self.effhistDA_GH_.GetXaxis().FindBin(pt_),
            #        self.effhistDA_GH_.GetYaxis().FindBin(eta_))
            #    effmc = self.effhistMC_GH_.GetBinContent(
            #        self.effhistMC_GH_.GetXaxis().FindBin(pt_),
            #        self.effhistMC_GH_.GetYaxis().FindBin(eta_))
            #else:
            effda = self.effhistDA_.GetBinContent(
                self.effhistDA_.GetXaxis().FindBin(pt_),
                self.effhistDA_.GetYaxis().FindBin(eta_))
            effmc = self.effhistMC_.GetBinContent(
                self.effhistMC_.GetXaxis().FindBin(pt_),
                self.effhistMC_.GetYaxis().FindBin(eta_))

            # update total efficiency
            xda *= (1. - effda*shift)
            xmc *= (1. - effmc*shift)

        # calculate scale factor and return it
        return (1.-xda)/(1.-xmc) if xmc!= 1. else 1.


    ## _________________________________________________________________________
    def __del__(self):
        #if self.hltfile: self.hltfile.Close()
        try:
            self.hltfile.Close()
        except AttributeError:
            pass


## _____________________________________________________________________________
class MuonScaleFactors(ScaleFactor):
# https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffsRun2
    # constructors/helpers
    def __init__(self, cmsswversion, datadir, shift):
        super(MuonScaleFactors, self).__init__(cmsswversion, datadir)
        self.error = False

        self.shift = shift

        self.muonideffs = {
            'looseID' : {},
            'mediumID' : {},
            'tightID' : {},
        }
        self.muonisoeffs = {
            'looseIso_looseID' : {},
            'looseIso_mediumID' : {},
            'looseIso_tightID' : {},
            'tightIso_mediumID' : {},
            'tightIso_tightID' : {},
        }

        filename = '{0}/scalefactors/muonidiso_{1}.root'.format(self.datadir,
            self.cmsswversion)

        logging.info('  Looking for muon scale factor file '
            'at {0}'.format(filename))
        if not os.path.exists(filename):
            self.error = True
            logging.info('       *   ')
            logging.info('    *******')
            logging.info('    WARNING: Can\'t find Muon scale factors file.')
            logging.info('    Will not include muon ID/Iso scale factors.')
            logging.info('    *******')
            logging.info('       *   ')
        else:
            # this is the file created by
            #     AnalysisTool/scripts/collectMuonScaleFactors.py
            self.mufile = ROOT.TFile(
                '{0}/scalefactors/muonidiso_{1}.root'.format(
                    self.datadir, self.cmsswversion))
            # the histograms in the file have x axis: Pt, y axis: AbsEta
            for cut in self.muonideffs:
                self.muonideffs[cut]['R'] = ROOT.TH2F(
                    self.mufile.Get(cut))
            for cut in self.muonisoeffs:
                self.muonisoeffs[cut]['R'] = ROOT.TH2F(
                    self.mufile.Get(cut))

            self.maxpt = self.muonideffs['tightID']['R'].GetXaxis().GetXmax()-1.
            self.minpt = self.muonideffs['tightID']['R'].GetXaxis().GetXmin()+0.01
            self.maxeta = self.muonideffs['tightID']['R'].GetYaxis().GetXmax()


    # methods
    ## _________________________________________________________________________
    def get_id_scale(self, muons, idcut):
        '''
        Returns the total scale factor for a list of muons
        for ID cuts.
        '''
        if self.error: return 1.

        s = 1.
        if self.shift == 'Down': s = 0.99
        elif self.shift == 'Up': s = 1.01

        if idcut in ['loose', 'medium', 'tight']:
            cut = '{0}ID'.format(idcut)
        else:
            raise ValueError('Muon get_id_scale: id '
                '"{0}" not recognised.'.format(idcut))

        sf = 1.
        for mu in muons:
            # make sure the muon is in range
            #pt_ = min(self.maxpt, mu.pt())
            pt_ = max( self.minpt, min(self.maxpt, mu.pt()) )
            eta_ = min(self.maxeta, mu.abs_eta())
            # find efficiencies for this muon
            musf = self.muonideffs[cut]['R'+scheme].GetBinContent(
                self.muonideffs[cut]['R'+scheme].GetXaxis().FindBin(pt_),
                self.muonideffs[cut]['R'+scheme].GetYaxis().FindBin(eta_) )
            #if not musf: 
            #    print 'found ID eff '
            #        '{0} for mu pt = {1}, eta = {2}'.format(musf, pt_, eta_)

            # update total efficiency
            sf *= (musf*s)

        return sf


    ## _________________________________________________________________________
    def get_iso_scale(self, muons, idcut, isotype, isocut):
        '''
        Returns the total scale factor for a list of muons
        for ID and isolation cuts. The efficiencies for these two cuts
        are already merged and located in a single TH2F.
        '''
        if self.error: return 1.

        s = 1.
        if self.shift == 'Down': s = 0.995
        elif self.shift == 'Up': s = 1.005

        if isotype!='PF_dB':
            print ('WARNING: Scale factors are only available for PF_dB iso. '
                'Using PF_dB scale factors.')
            isotype = 'PF_dB'

        # input validation
        if isocut=='loose':
            if idcut in ['loose', 'medium', 'tight']:
                cut = '{0}Iso_{1}ID'.format(isocut, idcut)
            else:
                raise ValueError('Muon get_iso_scale: ID "{0}" not recognised, \
                or you are trying to use an invalid ID+Iso pairing \
                ({0}+{1}.'.format(idcut, isocut))
        elif isocut=='tight':
            if idcut in ['medium', 'tight']:
                cut = '{0}Iso_{1}ID'.format(isocut, idcut)
            else:
                raise ValueError('Muon get_iso_scale: ID "{0}" not recognised, \
                or you are trying to use an invalid ID+Iso pairing \
                ({0}+{1}.'.format(idcut, isocut))
        else:
            raise ValueError('Muon get_iso_scale: Iso '
                '"{0}" not recognised.'.format(isocut))

        # find scale factor
        sf = 1.
        for mu in muons:
            # make sure the muon is in range
            #pt_ = min(self.maxpt, mu.pt())
            pt_ = max( self.minpt, min(self.maxpt, mu.pt()) )
            eta_ = min(self.maxeta, mu.abs_eta())
            # find efficiencies for this muon
            musf = self.muonisoeffs[cut]['R'].GetBinContent(
                self.muonisoeffs[cut]['R'].GetXaxis().FindBin(pt_),
                self.muonisoeffs[cut]['R'].GetYaxis().FindBin(eta_) )
            #if not musf: 
            #    print 'found Iso eff '
            #        '{0} for mu pt = {1}, eta = {2}'.format(musf, pt_, eta_)

            # update total efficiency
            sf *= (musf*s)

        return sf


    ## _________________________________________________________________________
    def __del__(self):
        try:
            self.mufile.Close()
        except AttributeError:
            pass

