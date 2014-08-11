import FWCore.ParameterSet.Config as cms

from CommonTools.ParticleFlow.ParticleSelectors.pfMuonsFromVertex_cfi import *
from CommonTools.ParticleFlow.ParticleSelectors.pfSelectedMuons_cfi import *
from CommonTools.ParticleFlow.Isolation.pfMuonIsolation_cff import *
from CommonTools.ParticleFlow.Isolation.pfIsolatedMuons_cfi import *

pfMuonsFromVertexForFatJets = pfMuonsFromVertex.clone()
pfMuonsFromVertexForFatJets.d0Cut = 0.2
pfMuonsFromVertexForFatJets.dzCut = 0.5

pfSelectedMuonsForFatJets = pfSelectedMuons.clone()
pfSelectedMuonsForFatJets.src = cms.InputTag("pfMuonsFromVertexForFatJets")
pfSelectedMuonsForFatJets.cut = 'pt > 20. && abs(eta) < 2.5'

muPFIsoDepositChargedForFatJets = muPFIsoDepositCharged.clone(src=cms.InputTag("pfSelectedMuonsForFatJets"))
muPFIsoDepositChargedAllForFatJets = muPFIsoDepositCharged.clone(src=cms.InputTag("pfSelectedMuonsForFatJets"))
muPFIsoDepositGammaForFatJets = muPFIsoDepositCharged.clone(src=cms.InputTag("pfSelectedMuonsForFatJets"))
muPFIsoDepositNeutralForFatJets = muPFIsoDepositCharged.clone(src=cms.InputTag("pfSelectedMuonsForFatJets"))
muPFIsoDepositPUForFatJets = muPFIsoDepositPU.clone(src=cms.InputTag("pfSelectedMuonsForFatJets"))
muPFIsoDepositSequenceForFatJets = cms.Sequence(muPFIsoDepositChargedForFatJets+muPFIsoDepositChargedAllForFatJets+muPFIsoDepositGammaForFatJets+muPFIsoDepositNeutralForFatJets+muPFIsoDepositPUForFatJets)

muPFIsoValuePU03ForFatJets = muPFIsoValuePU03.clone()
muPFIsoValuePU03ForFatJets.deposits[0].src = cms.InputTag("muPFIsoDepositPUForFatJets")
muPFIsoValueCharged03ForFatJets = muPFIsoValueCharged03.clone()
muPFIsoValueCharged03ForFatJets.deposits[0].src = cms.InputTag("muPFIsoDepositChargedForFatJets")
muPFIsoValueChargedAll03ForFatJets = muPFIsoValueChargedAll03.clone()
muPFIsoValueChargedAll03ForFatJets.deposits[0].src = cms.InputTag("muPFIsoDepositChargedAllForFatJets")
muPFIsoValueNeutral03ForFatJets = muPFIsoValueNeutral03.clone()
muPFIsoValueNeutral03ForFatJets.deposits[0].src = cms.InputTag("muPFIsoDepositNeutralForFatJets")
muPFIsoValueGamma03ForFatJets = muPFIsoValueGamma03.clone()
muPFIsoValueGamma03ForFatJets.deposits[0].src = cms.InputTag("muPFIsoDepositGammaForFatJets")
muPFIsoValueSequenceForFatJets = cms.Sequence(muPFIsoValuePU03ForFatJets+muPFIsoValueCharged03ForFatJets+muPFIsoValueChargedAll03ForFatJets+muPFIsoValueNeutral03ForFatJets+muPFIsoValueGamma03ForFatJets)

pfMuonIsolationSequenceForFatJets = cms.Sequence(muPFIsoDepositSequenceForFatJets*muPFIsoValueSequenceForFatJets)

pfIsolatedMuonsForFatJets = pfIsolatedMuons.clone()
pfIsolatedMuonsForFatJets.src = cms.InputTag("pfSelectedMuonsForFatJets")
pfIsolatedMuonsForFatJets.isolationCut = cms.double(0.15)
pfIsolatedMuonsForFatJets.deltaBetaIsolationValueMap = cms.InputTag("muPFIsoValuePU03ForFatJets", "", "")
pfIsolatedMuonsForFatJets.isolationValueMapsCharged = cms.VInputTag(cms.InputTag("muPFIsoValueCharged03ForFatJets"))
pfIsolatedMuonsForFatJets.isolationValueMapsNeutral = cms.VInputTag(cms.InputTag("muPFIsoValueNeutral03ForFatJets"), cms.InputTag("muPFIsoValueGamma03ForFatJets"))

pfMuonForFatJetsSequence = cms.Sequence(
    pfMuonsFromVertexForFatJets +
    pfSelectedMuonsForFatJets +
    pfMuonIsolationSequenceForFatJets + 
    pfIsolatedMuonsForFatJets
    )




