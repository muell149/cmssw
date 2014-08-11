import FWCore.ParameterSet.Config as cms

from CommonTools.ParticleFlow.ParticleSelectors.pfAllElectrons_cfi  import *
from CommonTools.ParticleFlow.ParticleSelectors.pfElectronsFromVertex_cfi import *
from CommonTools.ParticleFlow.ParticleSelectors.pfSelectedElectrons_cfi import *
from CommonTools.ParticleFlow.Isolation.pfElectronIsolation_cff import *
from CommonTools.ParticleFlow.Isolation.pfIsolatedElectrons_cfi import *

pfAllElectronsForFatJets = pfAllElectrons.clone()
pfAllElectronsForFatJets.src = cms.InputTag("pfNoMuonForFatJets")

pfElectronsFromVertexForFatJets = pfElectronsFromVertex.clone()
pfElectronsFromVertexForFatJets.src = cms.InputTag("pfAllElectronsForFatJets")
pfElectronsFromVertexForFatJets.d0Cut = 0.2
pfElectronsFromVertexForFatJets.dzCut = 0.5

pfSelectedElectronsForFatJets = pfSelectedElectrons.clone()
pfSelectedElectronsForFatJets.src = cms.InputTag("pfElectronsFromVertexForFatJets")
pfSelectedElectronsForFatJets.cut = 'abs(eta)<2.5 && pt>20'

elPFIsoDepositChargedForFatJets = elPFIsoDepositCharged.clone(src=cms.InputTag("pfSelectedElectronsForFatJets"))
elPFIsoDepositChargedAllForFatJets = elPFIsoDepositCharged.clone(src=cms.InputTag("pfSelectedElectronsForFatJets"))
elPFIsoDepositGammaForFatJets = elPFIsoDepositCharged.clone(src=cms.InputTag("pfSelectedElectronsForFatJets"))
elPFIsoDepositNeutralForFatJets = elPFIsoDepositCharged.clone(src=cms.InputTag("pfSelectedElectronsForFatJets"))
elPFIsoDepositPUForFatJets = elPFIsoDepositPU.clone(src=cms.InputTag("pfSelectedElectronsForFatJets"))
elPFIsoDepositSequenceForFatJets = cms.Sequence(elPFIsoDepositChargedForFatJets+elPFIsoDepositChargedAllForFatJets+elPFIsoDepositGammaForFatJets+elPFIsoDepositNeutralForFatJets+elPFIsoDepositPUForFatJets)

elPFIsoValuePU03PFIdForFatJets=elPFIsoValuePU03PFId.clone()
elPFIsoValuePU03PFIdForFatJets.deposits[0].src = cms.InputTag("elPFIsoDepositPUForFatJets")
elPFIsoValueCharged03PFIdForFatJets=elPFIsoValueCharged03PFId.clone()
elPFIsoValueCharged03PFIdForFatJets.deposits[0].src = cms.InputTag("elPFIsoDepositChargedForFatJets")
elPFIsoValueChargedAll03PFIdForFatJets=elPFIsoValueChargedAll03PFId.clone()
elPFIsoValueChargedAll03PFIdForFatJets.deposits[0].src = cms.InputTag("elPFIsoDepositChargedAllForFatJets")
elPFIsoValueNeutral03PFIdForFatJets=elPFIsoValueNeutral03PFId.clone()
elPFIsoValueNeutral03PFIdForFatJets.deposits[0].src = cms.InputTag("elPFIsoDepositNeutralForFatJets")
elPFIsoValueGamma03PFIdForFatJets=elPFIsoValueGamma03PFId.clone()
elPFIsoValueGamma03PFIdForFatJets.deposits[0].src = cms.InputTag("elPFIsoDepositGammaForFatJets")
elPFIsoValueSequenceForFatJets = cms.Sequence(elPFIsoValuePU03PFIdForFatJets*elPFIsoValueCharged03PFIdForFatJets*elPFIsoValueChargedAll03PFIdForFatJets*elPFIsoValueNeutral03PFIdForFatJets*elPFIsoValueGamma03PFIdForFatJets)

pfElectronIsolationSequenceForFatJets = cms.Sequence(elPFIsoDepositSequenceForFatJets*elPFIsoValueSequenceForFatJets)

pfIsolatedElectronsForFatJets = pfIsolatedElectrons.clone()
pfIsolatedElectronsForFatJets.src = cms.InputTag("pfSelectedElectronsForFatJets")
pfIsolatedElectronsForFatJets.isolationCut = cms.double(0.15)
pfIsolatedElectronsForFatJets.deltaBetaIsolationValueMap = cms.InputTag("elPFIsoValuePU03PFIdForFatJets")
pfIsolatedElectronsForFatJets.isolationValueMapsCharged = cms.VInputTag(cms.InputTag("elPFIsoValueCharged03PFIdForFatJets"))
pfIsolatedElectronsForFatJets.isolationValueMapsNeutral = cms.VInputTag(cms.InputTag("elPFIsoValueNeutral03PFIdForFatJets"), cms.InputTag("elPFIsoValueGamma03PFIdForFatJets"))

pfElectronForFatJetsSequence = cms.Sequence(
    pfAllElectronsForFatJets +
    pfElectronsFromVertexForFatJets +
    pfSelectedElectronsForFatJets +
    pfElectronIsolationSequenceForFatJets +
    pfIsolatedElectronsForFatJets
    )




