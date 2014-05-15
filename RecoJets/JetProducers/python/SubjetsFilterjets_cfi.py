################################################################################
# see: https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideSubjetFilterJetProducer
################################################################################

import FWCore.ParameterSet.Config as cms

from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.GenJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *

CA12JetsCA3FilterjetsPF = cms.EDProducer(
    "SubjetFilterJetProducer",
    PFJetParameters,
    AnomalousCellParameters,
    jetAlgorithm 			= cms.string("CambridgeAachen"),
    filterjetAlgorithm	= cms.string("CambridgeAachen"),
    nFatMax      			= cms.uint32(0),
    rParam       			= cms.double(1.2),
    rFilt        			= cms.double(0.3),
    massDropCut  			= cms.double(0.67),
    asymmCut     			= cms.double(0.3),
    asymmCutLater			= cms.bool(True),
    nSubjettinessNmin	= cms.int32(1),
    nSubjettinessNmax	= cms.int32(4), 
    )
CA12JetsCA3FilterjetsPF.jetPtMin		= cms.double(100.)
CA12JetsCA3FilterjetsPF.doAreaFastjet= cms.bool(True)

CA12JetsCA3FilterjetsGen = cms.EDProducer(
    "SubjetFilterJetProducer",
    GenJetParameters,
    AnomalousCellParameters,
    jetAlgorithm 			= cms.string("CambridgeAachen"),
	 filterjetAlgorithm 	= cms.string("CambridgeAachen"),
    nFatMax      			= cms.uint32(0),
    rParam       			= cms.double(1.2),
    rFilt        			= cms.double(0.3),
    massDropCut  			= cms.double(0.67),
    asymmCut     			= cms.double(0.3),
    asymmCutLater			= cms.bool(True),
	 nSubjettinessNmin	= cms.int32(1),
	 nSubjettinessNmax	= cms.int32(4)
    )
CA12JetsCA3FilterjetsGen.jetPtMin		= cms.double(100.)
CA12JetsCA3FilterjetsGen.doAreaFastjet= cms.bool(True)

filtjet_pf_seq = cms.Sequence(CA12JetsCA3FilterjetsPF)
filtjet_gen_seq = cms.Sequence(CA12JetsCA3FilterjetsGen)
