import os
import sys
import glob

import ROOT

# constants
## ___________________________________________________________
Z_MASS = 91.1876 # GeV




# misc functions

## ___________________________________________________________
def DeltaPhi(c0, c1):
    result = c0.Phi() - c1.Phi()
    while result>ROOT.TMath.Pi():
        result -= 2*ROOT.TMath.Pi()
    while result <= -ROOT.TMath.Pi():
        result += 2*ROOT.TMath.Pi()
    return result

## ___________________________________________________________
def DeltaR(c0, c1):
    deta = c0.Eta() - c1.Eta()
    dphi = DeltaPhi(c0, c1)
    return ROOT.TMath.Sqrt(deta**2+dphi**2)



# eventlist must be a textfile with events listed as follows:
# run:lumi:event number
# eg. 1:239472:60085100
## ___________________________________________________________
def EventIsOnList(run, lumi, event, evtlist):
    with open(evtlist,'r') as f:
        for line in f.readlines():
            info = line.strip().split(':')
            if (run == long(float(info[0])) and lumi == long(float(info[1])) and event == long(float(info[2]))):
                return True

    return False



