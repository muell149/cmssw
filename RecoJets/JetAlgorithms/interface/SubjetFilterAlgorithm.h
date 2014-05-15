#ifndef RECOJETS_JETALGORITHMS_SUBJETFILTERALGORITHM_H
#define RECOJETS_JETALGORITHMS_SUBJETFILTERALGORITHM_H 1


/*
  Implementation of the subjet/filter jet reconstruction algorithm
  which is described in: http://arXiv.org/abs/0802.2470
  
  CMSSW implementation by David Lopes-Pegna           <david.lopes-pegna@cern.ch>
                      and Philipp Schieferdecker <philipp.schieferdecker@cern.ch>

  see: https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideSubjetFilterJetProducer

*/


#include <vector>

#include "RecoJets/JetAlgorithms/interface/CompoundPseudoJet.h"
#include "FWCore/Framework/interface/Event.h"

#include <fastjet/JetDefinition.hh>
#include <fastjet/AreaDefinition.hh>
#include <fastjet/PseudoJet.hh>




class SubjetFilterAlgorithm
{
  //
  // construction / destruction
  //
public:
  SubjetFilterAlgorithm(const std::string& moduleLabel,
			double rParam,			  unsigned nFatMax,
			const std::string& FilterjetAlgorithm,
			double   rFilt,        double jetPtMin,
			double   massDropCut,  double asymmCut,
			bool     asymmCutLater,bool   doAreaFastjet,
			bool   verbose);
  virtual ~SubjetFilterAlgorithm();
  
  
  //
  // member functions
  //
public:
  void run(const std::vector<fastjet::PseudoJet> & inputs, 
	   std::vector<CompoundPseudoJet> & fatJets,
		boost::shared_ptr<fastjet::ClusterSequence> & fjClusterSeq,
	   const edm::EventSetup & iSetup);
  
  std::string summary() const;
  
  
  //
  // member data
  //
private:
  std::string              moduleLabel_;
  double                   rParam_;
  unsigned                 nFatMax_;
  std::string              FilterjetAlgorithm_;
  double                   rFilt_;
  double                   jetPtMin_;
  double                   massDropCut_;
  double                   asymmCut2_;
  bool                     asymmCutLater_;
  bool                     doAreaFastjet_;
  bool                     verbose_;
  
  unsigned                 nevents_;
  unsigned                 ntotal_;
  unsigned                 nfound_;
  
  fastjet::JetDefinition*  fjJetDef_;
  fastjet::JetDefinition*  fjFilterJetDef_;
  fastjet::AreaDefinition* fjAreaDef_;

};


#endif
