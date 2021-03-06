# python/xsec.py

pb = 1. # picobarns

xsecs = {
    # data
    'DoubleMuon'                                                       : 1.,
    'SingleMuon'                                                       : 1.,

    # the values for signal below (except WPlus/WMinus) are based on the Yellow Report, not GenXSecAnalyzer
    # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt13TeV
    # signal
    'GluGlu_HToMuMu_M125_13TeV_powheg_pythia8'                         :     48.58   * 0.0002176 * pb, # ggf H * H-> 2mu
    'VBF_HToMuMu_M125_13TeV_powheg_pythia8'                            :      3.782  * 0.0002176 * pb,
    'WPlusH_HToMuMu_M125_13TeV_powheg_pythia8'                         :      0.851  * 0.0002176 * pb,
    'WMinusH_HToMuMu_M125_13TeV_powheg_pythia8'                        :      0.5331 * 0.0002176 * pb,
    'ZH_HToMuMu_M125_13TeV_powheg_pythia8'                             :      0.8839 * 0.0002176 * pb, 



    # Drell-yan (choose one)
    #'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'          :   6025.2      * pb,
    'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'          :   5765.       * pb, # Andrew B.
    'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'           :   4895.       * pb * 1.216, # 1.216 LO -> NNLO

    # t-tbar (choose one)
    'TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                    :    502.2      * pb,
    'TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'                   :    831.76     * pb,
    'TTJets_Dilept_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8'          :     85.656    * pb,
    'TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8'                 :    815.96     * pb,

    # tt associated production w/boson (inclusive)
    'ttZJets_13TeV_madgraphMLM'                                        :      0.259    * pb,
    'ttWJets_13TeV_madgraphMLM'                                        :      0.243    * pb,
    'TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8'     :      0.2043   * pb,
    'ttH_M125_13TeV_powheg_pythia8'                                    :      0.5085   * pb,

    # single top 
    'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1' :   35.85     * pb,
    'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1'  :      35.85     * pb,
    'tZq_ll_4f_13TeV-amcatnlo-pythia8_TuneCUETP8M1'                    :      0.0758   * pb,
    'tZq_ll_4f_13TeV-amcatnlo-pythia8'                                 :      0.0758   * pb,

    # W (choose one)
    'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'               :  61526.7      * pb,
    'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'                :  61526.7      * pb,

    # ZH, possible 2l from Z
    'ZH_HToBB_ZToLL_M125_13TeV_amcatnloFXFX_madspin_pythia8'           :      0.8696   * 0.5824 * (0.033658*3) * pb, # ZH * H->bb * Z->ll
    'ZH_HToBB_ZToNuNu_M125_13TeV_amcatnloFXFX_madspin_pythia8'         :      0.8696   * 0.5824 * 0.2          * pb, # ZH * H->bb * Z->inv
    'ZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8'                         :      0.8696   * 0.5824 * 0.6991       * pb, # ZH * H->bb * Z->had
    'ZH_HToGG_ZToAll_M125_13TeV_powheg_pythia8'                        :      0.8696   * 0.00227               * pb, # ZH * H->gamgam
    'ZH_HToZG_ZToAll_M-125_13TeV_powheg_pythia8'                       :      0.8696   * 0.001533              * pb, # ZH * H->Zgam
    'ZHToTauTau_M125_13TeV_powheg_pythia8'                             :      0.8696   * 0.006272              * pb, # ZH * H->tautau
    'ZH_HToZZ_4LFilter_M125_13TeV_powheg2-minlo-HZJ_JHUgenV6_pythia8'  :      0.147    * pb, # MCM , 0.8696 * 0.02619 * (0.033658*3)^2 # ZH * H->ZZ * Z->ll^2 
    'ZH_HToBB_ZToLL_M125_13TeV_powheg_herwigpp'                        :      0.07495  * pb,

    # WW
    #'WWTo2L2Nu_13TeV-powheg'                                           :     10.481    * pb,
    'WWTo2L2Nu_13TeV-powheg'                                           :     12.46     * pb, # Andrew B.
    'GluGluWWTo2L2Nu_MCFM_13TeV'                                       :      0.39     * pb,

    # WZ
    'WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8'                      :      5.60     * pb,
    'WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8'                       :      4.42965  * pb,
    'WZTo3LNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'                 :      4.712    * pb,

    # ZZ
    # extra factors:
    #     1.16 brings pp->ZZ from NLO to NNLO (http://arxiv.org/abs/1405.2219)
    #     1.67 brings gg->ZZ from LO to NLO (http://arxiv.org/abs/1509.06734)
    #         (since it is gg it is already kind of NLO though so it is more like "nlo" to "nnlo")
    'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8'                      :      3.22     * pb,
    'ZZTo2L2Nu_13TeV_powheg_pythia8'                                   :      0.564    * pb,
    'ZZTo4L_13TeV_powheg_pythia8'                                      :      1.256    * 1.16 * pb,
    #'ZZTo4L_13TeV-amcatnloFXFX-pythia8'                                :      1.211    * 1.16 * pb,
    'ZZTo4L_13TeV-amcatnloFXFX-pythia8'                                :      1.212    * pb, # Guess who
    # ggZZ (76X)
    'GluGluToZZTo2e2mu_BackgroundOnly_13TeV_MCFM'                      :      0.003194 * 1.67 * pb,
    'GluGluToZZTo2e2tau_BackgroundOnly_13TeV_MCFM'                     :      0.003194 * 1.67 * pb,
    'GluGluToZZTo2mu2tau_BackgroundOnly_13TeV_MCFM'                    :      0.003194 * 1.67 * pb,
    'GluGluToZZTo4e_BackgroundOnly_13TeV_MCFM'                         :      0.001586 * 1.67 * pb,
    'GluGluToZZTo4mu_BackgroundOnly_13TeV_MCFM'                        :      0.001586 * 1.67 * pb,
    'GluGluToZZTo4tau_BackgroundOnly_13TeV_MCFM'                       :      0.001586 * 1.67 * pb,
    # ggZZ (80X)
    'GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8'                  :      0.003194 * 1.67 * pb,
    'GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8'                 :      0.003194 * 1.67 * pb,
    'GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8'                :      0.003194 * 1.67 * pb,
    'GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8'                     :      0.001586 * 1.67 * pb,
    'GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8'                    :      0.001586 * 1.67 * pb,
    'GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8'                   :      0.001586 * 1.67 * pb,

    # triboson
    'WWW_TuneCUETP8M1_13TeV-amcatnlo-pythia8'                          :      0.1651   * pb,
    'WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8'                       :      0.2086   * pb,
    'WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8'                          :      0.1651   * pb,
    'WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8'                          :      0.05565  * pb,
    'ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8'                          :      0.01398  * pb,

    # don't use:
    'TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8'             :      0.2529   * pb,
    'TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8'          :      3.697    * pb,
    'ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'                  :    117.864    * pb,    
    'WWG_TuneCUETP8M1_13TeV-amcatnlo-pythia8'                          :      0.2147   * pb,
    'WZG_TuneCUETP8M1_13TeV-amcatnlo-pythia8'                          :      0.04123  * pb,
    'TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'             :     57.35     * pb,
}

