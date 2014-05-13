import FWCore.ParameterSet.Config as cms

from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.GenJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *

# HEP top jet producer parameters
# $Id

HEPTopJetsPF = cms.EDProducer(
    "HEPTopJetProducer",
    PFJetParameters,
    AnomalousCellParameters,
    jetAlgorithm 			= cms.string("CambridgeAachen"),
	 rParam       			= cms.double(1.5),
	 MassDropThreshold	= cms.double(0.8),
	 MaxSubjetMass 		= cms.double(30.),
	 UseSubjetMassCuts	= cms.bool(False),
	 centralEtaCut			= cms.double(2.5),
	 nSubjettinessNmin	= cms.int32(1),
	 nSubjettinessNmax	= cms.int32(4)
)
HEPTopJetsPF.jetPtMin		= cms.double(20.)
HEPTopJetsPF.doAreaFastjet = cms.bool(False)

HEPTopJetsGen = cms.EDProducer(
    "HEPTopJetProducer",
    GenJetParameters,
    AnomalousCellParameters,
    jetAlgorithm 			= cms.string("CambridgeAachen"),
	 rParam       			= cms.double(1.5),
	 MassDropThreshold	= cms.double(0.8),
	 MaxSubjetMass 		= cms.double(30.),
	 UseSubjetMassCuts	= cms.bool(False),
	 centralEtaCut			= cms.double(2.5),
	 nSubjettinessNmin	= cms.int32(1),
	 nSubjettinessNmax	= cms.int32(4)
)
HEPTopJetsGen.jetPtMin			= cms.double(20.)
HEPTopJetsGen.doAreaFastjet	= cms.bool(False)

heptopjet_seq = cms.Sequence(HEPTopJetsPF)
heptopjet_genseq = cms.Sequence(HEPTopJetsGen)
