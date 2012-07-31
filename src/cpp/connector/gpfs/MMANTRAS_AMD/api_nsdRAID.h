/* @(#)81  1.5.2.2  src/avs/fs/mmfs/ts/mmantras/api_nsdRAID.h, mmfs, avs_rhrz1 3/6/12 13:32:17 */

#ifndef _h_api_nsdRAID
#define _h_api_nsdRAID

/*
 * api_nsdRAID.h
 *
 * classes:
 *   gpfsRecoveryGroupSdrInfo
 *   gpfsRecoveryGroup
 *   gpfsRecoveryGroupDeclusteredArray
 *   gpfsDeclusteredArrayVdisk
 *   gpfsDeclusteredArrayPdisk
 *   gpfsNsdRAIDConfigParms
 *   gpfsDeclusteredArrayVdiskIoStats
 *
 * gpfsRecoveryGroupSdrInfo - portion of NSD RAID recovery group 
 *                   information stored in GPFS SDR file.
 *
 * gpfsRecoveryGroup - GPFS recovery group (RG) information
 *  -- gpfsRecoveryGroupDeclusteredArray - GPFS declustered array (DA)
 *             information in a Recovery Group
 *     --- gpfsDeclusteredArrayVdisk - virtual disk (vdisk) information 
 *             in recovery group RG declustered array DA  
 *     --- gpfsDeclusteredArrayPdisk - physical disk (pdisk) information 
 *             in recovery group RG declustered array DA
 * 
 * gpfsNsdRAIDConfigParms - an array of NSD RAID configuration parameters
 *  -- gpfsNsdRAIDConfigVar - an NSD RAID configuration parameter
 *
 * gpfsDeclusteredArrayVdiskIoStats
 *
 * Externals:
 *  int getNsdRAIDSdrInfo(gpfsRecoveryGroupSdrInfo *rgSdrTableP, 
 *                        int *nRgSdrAllocP);
 *  int getRecoveryGroupSummary(gpfsRecoveryGroup *rgP);
 *  int getRecoveryGroupDeclusteredArrays(gpfsRecoveryGroup *rgP);
 *  int getNsdRAIDParameters(gpfsNsdRAIDConfigParms *configTableP,
 *                           int *nAllocP);
 *  int gpfsRGDefined();
 */

#define RAID_NAME_MAX   63
#define RAID_NAME_LEN   RAID_NAME_MAX+1
#define MAX_DA          16 /* RG_MAX_DECLUSTERED_ARRAYS */

#define STR8_LEN         8
#define STR32_LEN        32
#define STR64_LEN        64
#define STR128_LEN       128
#define PDISK_STATE_LEN  160
#define STATE_STR_LEN    STR64_LEN
#define SERVER_LIST_LEN  STR128_LEN
#define PATH_LEN         STR64_LEN

#define PVID_MAX_CHARS   20 /* defined in GPFS */

/* number of Recovery Group defined in the cluster */
extern int nRGDefined;   /* -1 uninitialized, 0 no RG defined */


/* 
 * gpfsDeclusteredArrayPdisk - description of a pdisk
 */

class gpfsDeclusteredArrayPdisk
{
  char gpfsPdiskName[RAID_NAME_LEN];   /* Pdisk Name */
  UInt32 gpfsPdiskReplacementPriority;  /* replacementPriority 
                                          (daCalcReplacementPriorityLocked) */
  char gpfsPdiskDevicePath[PATH_LEN];  /* path */
  char gpfsPdiskState[PDISK_STATE_LEN];/* State, possible values see:
                                          PdiskState_t::toString()  */
  UInt64 gpfsPdiskFreeSpace;           /* free space bytes */
  char gpfsPdiskFru[STR32_LEN];        /* Field Replaceable Unit number */
  char gpfsPdiskLocation[STR32_LEN];   /* where the disk is physically located
                                          in the carrier */
  public:
  gpfsDeclusteredArrayPdisk();
  ~gpfsDeclusteredArrayPdisk();

  void init(); 
  void update(char *pDiskName, int prior, char *path,
              char *state, UInt64 freeSpace, char *fru, char *location);

  void print_gpfsDeclusteredArrayPdisk(int verbose = 0);
  
  char *getPdiskName() { return gpfsPdiskName; }
  UInt32 getPdiskReplacementPriority() 
                                  { return gpfsPdiskReplacementPriority; }
  char *getPdiskDevicePath() { return gpfsPdiskDevicePath; }
  char *getPdiskState(){ return gpfsPdiskState; }
  UInt64 getPdiskFreeSpace() { return gpfsPdiskFreeSpace; }
  char *getPdiskFru() { return gpfsPdiskFru; }
  char *getPdiskLocation() { return gpfsPdiskLocation; }
};


/*
 * gpfsDeclusteredArrayVdiskIoStats - vdisk IO stats
 */

class gpfsDeclusteredArrayVdiskIoStats
{
  friend class gpfsDeclusteredArrayVdisk;

  UInt64 gpfsVdiskIoStatRead;
  UInt64 gpfsVdiskIoStatShortWrite;
  UInt64 gpfsVdiskIoStatMediumWrite;
  UInt64 gpfsVdiskIoStatFTW;
  UInt64 gpfsVdiskIoStatPromotedFTW;
  UInt64 gpfsVdiskIoStatFlushedUpdateWrite;
  UInt64 gpfsVdiskIoStatFlushedPromotedFTW;
  UInt64 gpfsVdiskIoStatMigrate;
  UInt64 gpfsVdiskIoStatScrub;
  UInt64 gpfsVdiskIoStatLogWrite;

  public:
  gpfsDeclusteredArrayVdiskIoStats();
  ~gpfsDeclusteredArrayVdiskIoStats();

  void init();

  UInt64 getVdiskIoStatRead() { return  gpfsVdiskIoStatRead; }
  UInt64 getVdiskIoStatShortWrite() 
                             { return gpfsVdiskIoStatShortWrite; }
  UInt64 getVdiskIoStatMediumWrite() 
                             { return gpfsVdiskIoStatMediumWrite; }
  UInt64 getVdiskIoStatFTW() { return gpfsVdiskIoStatFTW; }
  UInt64 getVdiskIoStatPromotedFTW() 
                         { return gpfsVdiskIoStatPromotedFTW; }
  UInt64 getVdiskIoStatFlushedUpdateWrite() 
                         { return gpfsVdiskIoStatFlushedUpdateWrite; }
  UInt64 getVdiskIoStatFlushedPromotedFTW() 
                         { return gpfsVdiskIoStatFlushedPromotedFTW; }
  UInt64 getVdiskIoStatMigrate() { return gpfsVdiskIoStatMigrate; }
  UInt64 getVdiskIoStatScrub() { return gpfsVdiskIoStatScrub; }
  UInt64 getVdiskIoStatLogWrite() { return gpfsVdiskIoStatLogWrite; }
};


/* 
 * gpfsDeclusteredArrayVdisk - description of a vdisk
 */

class gpfsDeclusteredArrayVdisk
{
  friend class gpfsDeclusteredArrayVdiskIoStats;

  char gpfsVdiskName[RAID_NAME_LEN]; /* Vdisk name */
  char gpfsVdiskRaidCode[STR32_LEN]; /* RaidCode, see ErasureCodeNames[]
                                        "8WayStriping", 
                                        "2WayReplication", 
                                        "3WayReplication", 
                                        "4WayReplication", 
                                        "8+2p",
                                        "8+3p" */
  UInt32 gpfsVdiskBlockSizeInKiB;    /* BlockSizeInKiB */
  UInt64 gpfsVdiskSize;              /* VdiskSize in bytes */ 
  char gpfsVdiskState[STATE_STR_LEN];/* State, possible values: 
                                        "ok", "critical", "offline",
                                        "%d/%d-degraded" 
                                        (faultLevel, faultTolerance)*/
  char gpfsVdiskRemarks[STR32_LEN];  /* Vidsk remarks, possible values:
                                        "log", "" */

  gpfsDeclusteredArrayVdiskIoStats gpfsVdiskIoStats;

  public:
  gpfsDeclusteredArrayVdisk();
  ~gpfsDeclusteredArrayVdisk();

  void init();
  void update(char *vDiskName, char *vDiskRaidCode, int vDiskBlockSizeInKiB,
              UInt64 vDiskSize, char *vDiskState, char *vDiskRemarks);

  void print_gpfsDeclusteredArrayVdisk(int verbose = 0);

  char *getVdiskName() { return gpfsVdiskName; }
  char *getVdiskRaidCode() { return gpfsVdiskRaidCode; }
  UInt32 getVdiskBlockSizeInKiB() { return gpfsVdiskBlockSizeInKiB; }
  UInt64 getVdiskSize() { return gpfsVdiskSize; }
  char *getVdiskState() { return gpfsVdiskState; }
  char *getVdiskRemarks() { return gpfsVdiskRemarks; }
  gpfsDeclusteredArrayVdiskIoStats *getVdiskIoStatsP() 
                                     { return &gpfsVdiskIoStats; }
};


/* 
 *  gpfsRecoveryGroupDeclusteredArray  - description of a Declustered Array
 */

class gpfsRecoveryGroupDeclusteredArray
{
  friend class gpfsDeclusteredArrayPdisk;
  friend class gpfsDeclusteredArrayVdisk;

  char   gpfsDeclusteredArrayName[RAID_NAME_LEN]; /* declustered array name */
  char   gpfsDeclusteredArrayNeedsService[STR8_LEN]; /* needs services */
  UInt32 gpfsDeclusteredArrayVdisks;              /* number of vDisks */
  UInt32 gpfsDeclusteredArrayPdisks;              /* number of pDisks */
  UInt32 gpfsDeclusteredArraySpares;              /* Spares */
  UInt32 gpfsDeclusteredArrayReplaceThreshold;    /* replace threshold */
  UInt64 gpfsDeclusteredArrayFreeSpace;      
  UInt32 gpfsDeclusteredArrayScrubDuration;       /* scrub duration in days*/
  char   gpfsDeclusteredArrayBackgroundTask[STR32_LEN]; /* background task 
                                             see: IM_ServiceLevel_tToString() 
                                             "inactive"
                                             "rebuild-critical"
                                             "rebuild-1r"
                                             "rebuild-2r"
                                             "rebuild-3r"
                                             "rebuild-offline"
                                             "rebalance"
                                             "scrub1"
                                             "scrub2"
                                             "in-transition"
                                             "metadata"
                                             "error"
                                             "Unknown IM_ServiceLevel_t" */
  UInt32 gpfsDeclusteredArrayTaskPercentComplete;   /* task percent complete */
  char   gpfsDeclusteredArrayTaskPrioriy[STR32_LEN];/* task prioriy 
                                                       "high", "low" */

  gpfsDeclusteredArrayPdisk *daPdiskArrayP;/* pointer to 
                                              gpfsDeclusteredArrayPdisk Table */

  gpfsDeclusteredArrayVdisk *daVdiskArrayP;/* pointer to 
                                              gpfsDeclusteredArrayVdisk Table */

  public:

  gpfsRecoveryGroupDeclusteredArray();
  ~gpfsRecoveryGroupDeclusteredArray();

  void init();
  void update(char *daName, char *daNeedsService,
              int nDaVdisks, int nDaPdisks, int nDaSpares, 
              int replaceThr, UInt64 freeSpace, int scrubDuration,
              char *bgTaskType, int bgTaskPct, char *priority);

  void allocDiskArrays(int nPdisks, int nVdisks);
  void deallocDiskArrays();

  void print_gpfsDeclusterArray(int verbose = 0);

  gpfsDeclusteredArrayPdisk *getDeclusteredArrayPdiskP(int index);
  gpfsDeclusteredArrayVdisk *getDeclusteredArrayVdiskP(int index);

  char *getDeclusteredArrayName() 
                 { return gpfsDeclusteredArrayName; }
  char *getDeclusteredNeedsService() 
                 { return gpfsDeclusteredArrayNeedsService; }
  UInt32 getDeclusteredArrayVdisks () 
                 { return gpfsDeclusteredArrayVdisks; } 
  UInt32 getDeclusteredArrayPdisks() 
                 { return gpfsDeclusteredArrayPdisks; }
  UInt32 getDeclusteredArraySpares() 
                 { return gpfsDeclusteredArraySpares; }
  UInt32 getDeclusteredArrayReplaceThreshold() 
                 { return gpfsDeclusteredArrayReplaceThreshold;  }
  UInt64 getDeclusteredArrayFreeSpace() 
                 { return gpfsDeclusteredArrayFreeSpace; }
  UInt32 getDeclusteredArrayScrubDuration() 
                 { return gpfsDeclusteredArrayScrubDuration;  }
  char *getDeclusteredArrayBackgroundTask()
                 { return gpfsDeclusteredArrayBackgroundTask; }
  UInt32 getDeclusteredArrayTaskPercentComplete()
                 { return gpfsDeclusteredArrayTaskPercentComplete; }
  char *getDeclusteredArrayTaskPrioriy() 
                 { return gpfsDeclusteredArrayTaskPrioriy; }
};


/*  
 *  gpfsRecoveryGroup - description of a recovery group
 */

class gpfsRecoveryGroup
{
  friend class gpfsRecoveryGroupDeclusteredArray;

  char   gpfsRecoveryGroupName[RAID_NAME_LEN]; /* RecoveryGroup Name */
  char   gpfsRecoveryGroupActiveServer[STR64_LEN];  /* active server */
  char   gpfsRecoveryGroupServers[SERVER_LIST_LEN]; /* primary and backup 
                                                       servers */
  char   gpfsRecoveryGroupId[PVID_MAX_CHARS];
  UInt32 gpfsRecoveryGroupDeclusterArrays;     /* DA with vdisks */
  UInt32 gpfsRecoveryGroupVdisks;              /* vDdisks */
  UInt32 gpfsRecoveryGroupPdisks;              /* pDisks */
  gpfsRecoveryGroupDeclusteredArray gpfsDeclusteredArray[MAX_DA];

  public:

  gpfsRecoveryGroup();
  ~gpfsRecoveryGroup();

  void init();
  void updateRgSdrInfo(char *rgName, char *serverList, char *rgId);
  void updateRgSummary(int nDas, int nVdisks, int nPdisks);
  void updateRgServers(char *activeServerP, char *serversP); 
  void print_gpfsRecoveryGroup(char *banner);

  char *getRecoveryGroupName() { return gpfsRecoveryGroupName; };
  char *getRecoveryGroupActiveServer() 
                               { return gpfsRecoveryGroupActiveServer; }
  char *getRecoveryGroupServers() 
                               { return gpfsRecoveryGroupServers; }
  char *getRecoveryGroupId() 
                               { return gpfsRecoveryGroupId; }
  UInt32 getRecoveryGroupDeclusterArrays()
                               { return gpfsRecoveryGroupDeclusterArrays; }
  UInt32 getRecoveryGroupVdisks()
                               { return gpfsRecoveryGroupVdisks; }
  UInt32 getRecoveryGroupPdisks()
                               { return gpfsRecoveryGroupPdisks; }
  gpfsRecoveryGroupDeclusteredArray *getRecoveryGroupDeclusterArraysP() 
                               { return gpfsDeclusteredArray; };

  gpfsRecoveryGroupDeclusteredArray *getDeclusteredArrayP(int index);
};


/* 
 * gpfsRecoveryGroupSdrInfo - NSD RAID information from GPFS SDR
 */

class gpfsRecoveryGroupSdrInfo
{
  char   gpfsRecoveryGroupName[RAID_NAME_LEN];
  char   gpfsRecoveryGroupServerList[SERVER_LIST_LEN]; 
  char   gpfsRecoveryGroupId[PVID_MAX_CHARS];    /* PVID_MAX_CHARS = 20 */ 

  public:

  gpfsRecoveryGroupSdrInfo();
  ~gpfsRecoveryGroupSdrInfo();

  void init();
  void update(char *newName, char *newServerList, char *newId);
  void print_gpfsRecoveryGroupSdrInfo();

  char *getRecoveryGroupName() { return gpfsRecoveryGroupName; };
  char *getRecoveryGroupServerList() { return gpfsRecoveryGroupServerList; };
  char *getRecoveryGroupId() { return gpfsRecoveryGroupId; };
};


/*
 * gpfsNsdRAIDConfigParms - NSD RAID related config parameters/variables
 * gpfsNsdRAIDConfigVar - config variable (name and value string)
 */

class gpfsNsdRAIDConfigVar
{
  friend class gpfsNsdRAIDConfigParms;

  char configVarName[STR64_LEN];
  char configVarValueStr[STR64_LEN];

  public:
  gpfsNsdRAIDConfigVar();
  ~gpfsNsdRAIDConfigVar();
  void init();

  char *getNsdRaidConfigVar() { return configVarName; };
  char *getNsdRaidConfigValue() { return configVarValueStr; };
};

class gpfsNsdRAIDConfigParms
{
  UInt32 nParms;        /* num parameters defined */
  UInt32 nParmsAlloc;   /* maximum allocated array */
  gpfsNsdRAIDConfigVar *gpfsNsdRAIDConfigVarTableP;
  
  public:
  gpfsNsdRAIDConfigParms(int maxElem);
  ~gpfsNsdRAIDConfigParms();

  int init(int maxElem);
  
  UInt32 getNParms() { return nParms; };
  UInt32 getNParmsAlloc() { return nParmsAlloc; };
  void   setNParms(int nFound) { nParms = nFound; };
  void   setNParmsAlloc(int nAlloc) { nParmsAlloc = nAlloc; };
  int    findNsdRAIDConfigParmIndex(char *varName);
  void   updateNsdRAIDConfigParm(int index, char *varName, char *varValue);
  void   print_gpfsNsdRAIDConfigParms();
  gpfsNsdRAIDConfigVar *getConfigVarP(int index);
};


extern int getNsdRAIDSdrInfo(
              gpfsRecoveryGroupSdrInfo *rgSdrTableP, /* buffer */
              int *nRgSdrAllocP /* in: size of the buffer 
                                   out: num of RGs in this cluster */);
extern int getRecoveryGroupSummary(gpfsRecoveryGroup *rgP);
extern int getRecoveryGroupDeclusteredArrays(gpfsRecoveryGroup *rgP);
extern int getNsdRAIDParameters(gpfsNsdRAIDConfigParms *configTableP, 
                                int *nAllocP);

extern int gpfsRGDefined();

#endif /* _h_api_nsdRAID */
