1. Detox policies

1.1 Generalities
The policy configuration fully defines the behavior of Detox. The file contains four classes of statements:

 . Target site definition
   Specifies which sites are considered for deletion, defined through site names and properties.

 . Deletion trigger definition
   Specifies two conditions: When deletions are triggered on target sites, and when deletions are no longer needed.

 . Replica protection / deletion policies
   Each dataset replica (parts subscribed to AnalysisOps) is passed through these policy lines.
   The first line with a matching condition determines the fate of the replica:
    If a Protect line matches, the replica is protected.
    If a Delete line matches, the replica is considered as a deletion candidate.
   If the site needs deletion, replicas in the deletion candidate list are deleted in the specified order.

 . Deletion order
   Order of deletion matters unless we are running a greedy deletion (Until never). Deletion candidates are sorted
   by the order specified in this line and deleted from the first in the list.

1.2 Variables in policy expressions
 <General>
 . always: evaluates to True
 . never: evaluates to False
 <Dataset>
 . dataset.name
 . dataset.status
 . dataset.on_tape: Status of tape replica. NONE = copy request is not made, FULL = fully copied to tape, PARTIAL = request is made but is not fulfilled.
 . dataset.last_update: Timestamp of last update (e.g. last block created) of the dataset.
 . dataset.num_full_disk_copy
 . dataset.usage_rank: sum_{site}[(# days since last access or update to the replica) - (replica size in TB)] / (# sites)
 <Site>
 . site.name
 . site.status: Status given by Site Status Board (http://dashb-ssb.cern.ch/dashboard/request.py). Values are READY, WAITROOM, MORGUE, UNKNOWN
 . site.active: Status defined by the DDM team. Values are IGNORE, AVAILABLE, NOCOPY (accepts deletions but not copies)
 . site.occupancy: Storage occupancy with respect to quota of the current partition.
 . site.quota: Quota assigned for the current partition.
 <Dataset replica>
 . replica.incomplete: Not all of scheduled block transfers are done.
 . replica.last_block_created: Timestamp of the last block transfer completion.
 . replica.num_access: Number of CRAB accesses recorded in popdb for the last 2 years.
 . replica.has_locked_block

Note to developers: New expressions can be added in lib/detox/variables.py

1.3 Exceptions requested by various gruops
Various groups can request specific protection rules and special deletion lists. These are typically based on dataset names. Following exceptions are currently implemented:

 - AnalysisOps & DataOps
  . Requested by ??? on ???; validity ???
    Protect dataset.name == /HLTPhysics/CMSSW_7_4_14-2015_10_20_newconditions0_74X_dataRun2_HLTValidation_Candidate_2015_10_12_10_41_09-v1/RECO
    Protect dataset.name == /HLTPhysics/CMSSW_7_4_14-2015_10_20_reference_74X_dataRun2_HLT_v2-v1/RECO
 
  . Requested by TSG? on ???; validity ???
    Protect dataset.name == /ZeroBias*/Run2015A-PromptReco-v1/RECO
    Protect dataset.name == /ZeroBias*/Run2015A-27Jan2016-v1/RECO
 
  . Requested by TOTEM? on ???; validity ???
    Protect dataset.name == /*TOTEM*/*Run2015D*/RECO

 - DataOps
  . Requested by ??? on ???; validity ???
    Protect dataset.name == /*/*-PromptReco-*/*
    Protect dataset.name == /*/*/RECO
    Protect dataset.name == /*/*/RAWAODSIM

  . Requested by Production team on Aug 9 2016; validity 1-2 weeks
    Protect dataset.name == /*/*RunIISummer16DR80*/*
