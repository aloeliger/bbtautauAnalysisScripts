#configuration designed to serve as analyzer/nano-ifier for the boosted tau 
#analysis
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run2_2016_cff import Run2_2016

process = cms.Process('NANO',Run2_2016)

process.load('FWCore.MessageService.MessageLogger_cfi')
# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.source = cms.Source('PoolSource',
                            fileNames = cms.untracked.vstring('/store/mc/RunIISummer20UL16MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v13-v2/260000/003F1A76-9CDA-7644-A34E-923C4B1C0E5E.root')
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('--filein=/store/mc/RunIISummer20UL16MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v13-v2/260000/003F1A76-9CDA-7644-A34E-923C4B1C0E5E.root nevts:-1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)


process.NANOAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODSIM'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:/data/aloeliger/test.root'),
    outputCommands = process.NANOAODSIMEventContent.outputCommands,
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('nanoAOD_step')
    ),
)

# Additional output definition
from bbtautauAnalysisScripts.boostedTauRecoFilter.boostedTauRecoFilter_cfi import boostedTauRecoFilter

process.theBoostedTauFilter = boostedTauRecoFilter

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mcRun2_asymptotic_v13', '')

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.theBoostedTauFilter + process.nanoSequenceMC)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOAODSIMoutput_step)

from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeMC 
process = nanoAOD_customizeMC(process)

from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)

