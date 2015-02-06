///
/// \class l1t::Stage1Layer2EtSumAlgorithmImpHW
///
/// Description: first iteration of stage 1 jet sums algo

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "L1Trigger/L1TCalorimeter/interface/Stage1Layer2EtSumAlgorithmImp.h"
#include "L1Trigger/L1TCalorimeter/interface/PUSubtractionMethods.h"
#include "L1Trigger/L1TCalorimeter/interface/legacyGtHelper.h"
#include "DataFormats/L1Trigger/interface/EtSum.h"
#include "DataFormats/L1CaloTrigger/interface/L1CaloRegionDetId.h"
#include "L1Trigger/L1TCalorimeter/interface/JetFinderMethods.h"
#include "L1Trigger/L1TCalorimeter/interface/JetCalibrationMethods.h"
#include "L1Trigger/L1TCalorimeter/interface/HardwareSortingMethods.h"

l1t::Stage1Layer2EtSumAlgorithmImpHW::Stage1Layer2EtSumAlgorithmImpHW(CaloParamsStage1* params) : params_(params)
{
  //now do what ever initialization is needed
  for(unsigned int i = 0; i < L1CaloRegionDetId::N_PHI; i++) {
    sinPhi.push_back(sin(2. * 3.1415927 * i * 1.0 / L1CaloRegionDetId::N_PHI));
    cosPhi.push_back(cos(2. * 3.1415927 * i * 1.0 / L1CaloRegionDetId::N_PHI));
  }
}


l1t::Stage1Layer2EtSumAlgorithmImpHW::~Stage1Layer2EtSumAlgorithmImpHW() {


}


//double l1t::Stage1Layer2EtSumAlgorithmImpHW::regionPhysicalEt(const l1t::CaloRegion& cand) const {
//  return jetLsb*cand.hwPt();
//}

void l1t::Stage1Layer2EtSumAlgorithmImpHW::processEvent(const std::vector<l1t::CaloRegion> & regions,
							const std::vector<l1t::CaloEmCand> & EMCands,
							      std::vector<l1t::EtSum> * etsums) {

  unsigned int sumET = 0;
  double sumEx = 0;
  double sumEy = 0;
  unsigned int sumHT = 0;
  double sumHx = 0;
  double sumHy = 0;

  std::vector<l1t::CaloRegion> *subRegions = new std::vector<l1t::CaloRegion>();


  //Region Correction will return uncorrected subregions if
  //regionPUSType is set to None in the config
  double jetLsb=params_->jetLsb();

  int etSumEtaMinEt = params_->etSumEtaMin(0);
  int etSumEtaMaxEt = params_->etSumEtaMax(0);
  //double etSumEtThresholdEt = params_->etSumEtThreshold(0);
  int etSumEtThresholdEt = (int) (params_->etSumEtThreshold(0) / jetLsb);

  int etSumEtaMinHt = params_->etSumEtaMin(1);
  int etSumEtaMaxHt = params_->etSumEtaMax(1);
  //double etSumEtThresholdHt = params_->etSumEtThreshold(1);
  int etSumEtThresholdHt = (int) (params_->etSumEtThreshold(1) / jetLsb);

  std::string regionPUSType = params_->regionPUSType();
  std::vector<double> regionPUSParams = params_->regionPUSParams();
  RegionCorrection(regions, subRegions, regionPUSParams, regionPUSType);

  for(std::vector<CaloRegion>::const_iterator region = subRegions->begin(); region != subRegions->end(); region++) {
    if (region->hwEta() < etSumEtaMinEt || region->hwEta() > etSumEtaMaxEt) {
      continue;
    }

    //double regionET= regionPhysicalEt(*region);
    int regionET = region->hwPt();

    if(regionET >= etSumEtThresholdEt){
      sumET += regionET;
      sumEx += (((double) regionET) * cosPhi[region->hwPhi()]);
      sumEy += (((double) regionET) * sinPhi[region->hwPhi()]);
    }
  }

  for(std::vector<CaloRegion>::const_iterator region = subRegions->begin(); region != subRegions->end(); region++) {
    if (region->hwEta() < etSumEtaMinHt || region->hwEta() > etSumEtaMaxHt) {
      continue;
    }

    //double regionET= regionPhysicalEt(*region);
    int regionET = region->hwPt();

    if(regionET >= etSumEtThresholdHt) {
      sumHT += regionET;
      sumHx += (((double) regionET) * cosPhi[region->hwPhi()]);
      sumHy += (((double) regionET) * sinPhi[region->hwPhi()]);
    }
  }

  unsigned int MET = ((unsigned int) sqrt(sumEx * sumEx + sumEy * sumEy));
  unsigned int MHT = ((unsigned int) sqrt(sumHx * sumHx + sumHy * sumHy));

  double physicalPhi = atan2(sumEy, sumEx) + 3.1415927;
  // Global Trigger expects MET phi to be 0-71 (e.g. tower granularity)
  // Although we calculated it with regions, there is some benefit to interpolation.
  unsigned int iPhiET = 4*L1CaloRegionDetId::N_PHI * physicalPhi / (2 * 3.1415927);

  double physicalPhiHT = atan2(sumHy, sumHx) + 3.1415927;
  unsigned int iPhiHT = L1CaloRegionDetId::N_PHI * (physicalPhiHT) / (2 * 3.1415927);

  const ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > etLorentz(0,0,0,0);

  int METqual = 0;
  int MHTqual = 0;
  int ETTqual = 0;
  int HTTqual = 0;
  if(MET >= 0xfff)
    METqual = 1;
  if(MHT >= 0xfff)
    MHTqual = 1;
  if(sumET >= 0xfff) //hardcoded 12 bit maximum
    ETTqual = 1;
  if(sumHT >= 0xfff)
    HTTqual = 1;

  // scale MHT by sumHT
  //double mtmp = ((double) MHT / (double) sumHT);
  //int rank=params_->HtMissScale().rank(mtmp);

  //MHT=rank;
  //iPhiHT=dijet_phi;

  l1t::EtSum etMiss(*&etLorentz,EtSum::EtSumType::kMissingEt,MET&0xfff,0,iPhiET,METqual);
  l1t::EtSum htMiss(*&etLorentz,EtSum::EtSumType::kMissingHt,MHT&0xfff,0,iPhiHT,MHTqual);
  l1t::EtSum etTot (*&etLorentz,EtSum::EtSumType::kTotalEt,sumET&0xfff,0,0,ETTqual);
  l1t::EtSum htTot (*&etLorentz,EtSum::EtSumType::kTotalHt,sumHT&0xfff,0,0,HTTqual);

  std::vector<l1t::EtSum> *preGtEtSums = new std::vector<l1t::EtSum>();

  preGtEtSums->push_back(etMiss);
  preGtEtSums->push_back(htMiss);
  preGtEtSums->push_back(etTot);
  preGtEtSums->push_back(htTot);

  EtSumToGtScales(params_, preGtEtSums, etsums);

  delete subRegions;
  // delete unCorrJets;
  // delete unSortedJets;
  // delete SortedJets;
  delete preGtEtSums;

  const bool verbose = true;
  if(verbose)
  {
    for(std::vector<l1t::EtSum>::const_iterator itetsum = etsums->begin();
	itetsum != etsums->end(); ++itetsum){
      if(EtSum::EtSumType::kMissingEt == itetsum->getType())
      {
      	cout << "Missing Et" << endl;
      	cout << bitset<7>(itetsum->hwPhi()).to_string() << bitset<1>(itetsum->hwQual()).to_string() << bitset<12>(itetsum->hwPt()).to_string() << endl;
      }
      if(EtSum::EtSumType::kMissingHt == itetsum->getType())
      {
      	cout << "Missing Ht" << endl;
      	cout << bitset<1>(itetsum->hwQual()).to_string() << bitset<7>(itetsum->hwPt()).to_string() << bitset<5>(itetsum->hwPhi()).to_string() << endl;
      }
      if(EtSum::EtSumType::kTotalEt == itetsum->getType())
      {
	cout << "Total Et" << endl;
	cout << bitset<1>(itetsum->hwQual()).to_string() << bitset<12>(itetsum->hwPt()).to_string() << endl;
      }
      if(EtSum::EtSumType::kTotalHt == itetsum->getType())
      {
	cout << "Total Ht" << endl;
	cout << bitset<1>(itetsum->hwQual()).to_string() << bitset<12>(itetsum->hwPt()).to_string() << endl;
      }
    }
  }
}

