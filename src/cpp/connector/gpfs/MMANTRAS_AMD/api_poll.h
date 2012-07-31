/* @(#)49       1.39.2.1  src/avs/fs/mmfs/ts/mmantras/api_poll.h, mmfs, avs_rhrz1 4/3/12 12:42:34 */

#ifndef _h_api_poll
#define _h_api_poll



#include <stdio.h>
#include <vector>
#include <pthread.h>
#include <sys/time.h>

/* MODS_START */
#include <string>
/* MODS_END */

#include <api_types.h>

/* String length */
#define NAME_STRING_LEN    128

/* Comma separated string length */
#define LIST_STRING_LEN    1024

/* DJ_MODS_START */
/* Buf length for Return messages from GPFS */
#define MMCMD_RET_MSG_BUF_LEN  400
/* Number of tokens in a GPFS cmd with small number of parameters */
#define MAX_NUM_TOKENS_SHORT_CMD 8

#define TIME_STAMP_CHARS   25

/* DJ_MODS_END */

/* Timer thread interval */
#define TIMER_INTERVAL     300

/* Management application protocol. It is for protocol-specific
   functionalities. */
typedef enum
{
  MGMT_SNMP = 0,
  MGMT_CIM = 1
} MgmtProtocol;

/* Enable logging */
#define ENABLE_MMANTRAS_LOG

/* Maximum log level */
#define MMANTRAS_LOG_MAX_LEVEL  3

/* Supported log levels */
enum MmantrasLogLevel
{
  INFO = 0,
  WARNING = 1,
  ERROR = 2,
  SEVERE = 3
};

#define LIBMMANTRAS_VERSION 3404  /* version of currently defined MMANTRAS 
                                     interface - must update the corresponding
                                     version number at daemon side */

extern int libmmantrasVersion();

/* Define maximum number of objects */
#define  MAX_NODE         1024
#define  MAX_FS           32
#define  MAX_DISK         1024
#define  MAX_POOL         256
#define  MAX_POLICY       32
#define  MAX_RULE         65536
#define  MAX_NSD_SERVER   32
#define  MAX_TASK         1024
#define  MAX_PCACHE_CMD_INFO 32  /* must be >= MAX_PACACHE_CMD */

#define CLUSTER_MANAGER   0x1
#define CLUSTER_STATUS    0x2
#define CLUSTER_STATE_ALL CLUSTER_MANAGER | CLUSTER_STATUS


/* Info structs
   The latest data from GPFS is stored in an internal copy of these structs.
   The caller has his own copy, which is updated to be consistent with the
   internal copy by calling the PollingHandler::update routines. */


/* Asynchronous command execution information */
class ExecutionTask
{
  friend class PollingHandler;

  char cmd[NAME_STRING_LEN];
  std::vector<char *>argItems;
  int (*callbackFn)(void *callbackData);
  void *callbackData;

public:

  ExecutionTask(MErrno *errP);

  ~ExecutionTask();

  ExecutionTask& operator=(ExecutionTask &t);

  void setCmd(const char *cmdP);
  void addArg(char *argP);

  void copyArgs(ExecutionTask *taskP);

  inline char* getCmd() { return cmd; }
  inline UInt32 getNumArgItems() { return argItems.size(); }
  inline char *getArg(int d) { return argItems.at(d); }
};

/* Asynchronous command execution result */
class ExecutionResult
{
  UInt16 percentComplete;

public:
  ExecutionResult(MErrno *errP);

  ~ExecutionResult();

  inline UInt16 getPercentComplete() { return percentComplete; }
};

/* Disk server information */
class DiskServerInfo
{
  friend class PollingHandler;

  char name[NAME_STRING_LEN];

public:
  DiskServerInfo(MErrno *errP);

  ~DiskServerInfo();

  DiskServerInfo& operator=(DiskServerInfo &d);

  inline char* getName() { return name; }
};

/* Disk information */
class DiskInfo
{
  friend class PollingHandler;

  Boolean_t found;

  /* Indicate whether it is free NSD or not. */
  Boolean_t free;

  char name[NAME_STRING_LEN];
  char nodeName[NAME_STRING_LEN];       // for easy association

  /* Use only when this NSD is free. */
  char poolName[NAME_STRING_LEN];

  char status[NAME_STRING_LEN];
  char availability[NAME_STRING_LEN];
  Int32 failureGroupId;

  char volumeId[NAME_STRING_LEN];

  char metadata[NAME_STRING_LEN];
  char data[NAME_STRING_LEN];
  char diskWait[NAME_STRING_LEN];
  UInt64 totalSpace;
  UInt64 fullBlockFreeSpace;
  UInt64 subBlockFreeSpace;

  double readTime;
  double writeTime;
  double longestReadTime;
  double longestWriteTime;
  double shortestReadTime;
  double shortestWriteTime;
  UInt64 readBytes;
  UInt64 writeBytes;
  UInt32 readOps;
  UInt32 writeOps;

  UInt32 nodePerfCount;    // number of nodes that had valid contribution to perf aggregate

  std::vector<DiskServerInfo *>serverItems;
  std::vector<DiskServerInfo *>backupServerItems;

  void copyServers(DiskInfo *diskP);
  int getServerIndex(char *nameP);
  void copyBackupServers(DiskInfo *diskP);
  int getBackupServerIndex(char *nameP);

public:
  DiskInfo(MErrno *errP);

  ~DiskInfo();

  DiskInfo& operator=(DiskInfo &d);
  void clearStats();

  inline Boolean_t isFree() { return free; }

  inline char* getName() { return name; }
  inline char *getNodeName() { return nodeName; }

  /* Disk stats from EE get fs command */
  inline char *getStatus() { return status; }
  inline char *getAvailability() { return availability; }
  inline Int32 getFailureGroupId() { return failureGroupId; }
  inline char *getVolumeId() { return volumeId; }
  inline char *getMetadata() { return metadata; }
  inline char *getData() { return data; }
  inline char *getDiskWait() { return diskWait; }
  inline UInt64 getTotalSpace() { return totalSpace; }
  inline UInt64 getFullBlockFreeSpace() { return fullBlockFreeSpace; }
  inline UInt64 getSubBlockFreeSpace() { return subBlockFreeSpace; }

  /* Disk performance statistics: see mmpmon ds for details */
  /* Note: getReadTime() and getWriteTime() return the total time of all
     operations; divide by the total ops to get average */
  inline double getReadTime() { return readTime; }    /* microseconds */
  inline double getWriteTime() { return writeTime; }
  inline double getLongestReadTime() { return longestReadTime; }
  inline double getLongestWriteTime() { return longestWriteTime; }
  inline double getShortestReadTime() { return shortestReadTime; }
  inline double getShortestWriteTime() { return shortestWriteTime; }
  inline UInt64 getReadBytes() { return readBytes; }
  inline UInt64 getWriteBytes() { return writeBytes; }
  inline UInt32 getReadOps() { return readOps; }
  inline UInt32 getWriteOps() { return writeOps; }
  inline UInt32 getNodePerfCount() { return nodePerfCount; }
  inline UInt32 getNumServerItems() { return serverItems.size(); }
  inline DiskServerInfo *getServer(int d) { return serverItems.at(d); }
  inline UInt32 getNumBackupServerItems() { return backupServerItems.size(); }
  inline DiskServerInfo *getBackupServer(int d) { return backupServerItems.at(d); }
  inline char *getPoolName() { return poolName; }
  void updateTotalSpace(UInt64 dSizeInKB) { totalSpace = dSizeInKB; }
  void updateDiskInfoStatus(char *dsStatus);
};

/* forward decl */
class FilesystemInfo;

/* Storage pool information */
class StoragePoolInfo
{
  friend class PollingHandler;

  char name[NAME_STRING_LEN];
  char status[NAME_STRING_LEN];
  UInt32 numDisks;
  UInt64 totalSpace;
  UInt64 freeSpace;

  UInt32 parentFS;    /* index of parent filesystem */
  Boolean_t found;

  /* Store the list of disk name - primary key */
  std::vector<DiskInfo *>diskItems;
  struct timeval diskRefreshTime;
  struct timeval diskPerfRefreshTime;

  void copyDisks(StoragePoolInfo *poolP);
  int getDiskInfoIndex(char *nameP);

public:
  StoragePoolInfo(MErrno *errP);
  ~StoragePoolInfo();
  StoragePoolInfo& operator=(StoragePoolInfo &sp);
  inline char *getName() { return name; }
  inline char *getStatus() { return status; }
  inline UInt64 getTotalSpace() { return totalSpace; }
  inline UInt64 getFreeSpace() { return freeSpace; }
  inline UInt32 getParent() { return parentFS; }
  inline UInt32 getNumDisks() { return numDisks; } // Use only when file system is mounted
  inline UInt32 getNumDiskItems() { return diskItems.size(); }
  inline DiskInfo *getDisk(int d) { return diskItems.at(d); }
  inline struct timeval getDiskRefreshTime() { return diskRefreshTime; }
  inline struct timeval getDiskPerfRefreshTime() { return diskPerfRefreshTime; }
};

/* Mounted node information */
class MountedNodeInfo
{
  friend class PollingHandler;

  char name[NAME_STRING_LEN];
  char ipAddr[NAME_STRING_LEN];

  Boolean_t found;

public:
  MountedNodeInfo(MErrno *errP);

  ~MountedNodeInfo();

  MountedNodeInfo& operator=(MountedNodeInfo &d);

  inline char* getName() { return name; }
  inline char* getIpAddr() { return ipAddr; }
};

/* File system policy rule information */
class RuleInfo
{
  friend class PollingHandler;

  char name[NAME_STRING_LEN];
  char desc[LIST_STRING_LEN];

public:
  RuleInfo(MErrno *errP);

  ~RuleInfo();

  RuleInfo& operator=(RuleInfo &d);

  inline char *getName() { return name; }
  inline char *getDesc() { return desc; }
};

/* File system policy information */
class PolicyInfo
{
  friend class PollingHandler;

  char name[NAME_STRING_LEN];
  char installUser[NAME_STRING_LEN];
  char installTime[NAME_STRING_LEN];

  std::vector<RuleInfo *>ruleItems;

  void copyRules(PolicyInfo *piP);
  int getRuleInfoIndex(char *nameP);

public:
  PolicyInfo(MErrno *errP);

  ~PolicyInfo();

  PolicyInfo& operator=(PolicyInfo &d);

  inline char *getName() { return name; }
  inline char *getInstallUser() { return installUser; }
  inline char *getInstallTime() { return installTime; }
  inline UInt32 getNumRules() { return ruleItems.size(); }
  inline RuleInfo *getRule(int r) { return ruleItems.at(r); }
};

/* File system performance */
class FilesystemPerf
{
  friend class PollingHandler;

  char fsName[NAME_STRING_LEN];
  char nodeName[NAME_STRING_LEN];
  char nodeIpAddr[NAME_STRING_LEN];

  UInt64 bytesRead;
  UInt64 bytesCache;
  UInt64 bytesWritten;
  UInt32 reads;
  UInt32 caches;
  UInt32 writes;
  UInt32 openCalls;
  UInt32 closeCalls;
  UInt32 readCalls;
  UInt32 writeCalls;
  UInt32 readdirCalls;
  UInt64 inodesWritten;
  UInt64 inodesRead;
  UInt64 inodesDeleted;
  UInt64 inodesCreated;
  UInt32 statCacheHit;
  UInt32 statCacheMiss;

  Boolean_t found;

public:
  FilesystemPerf(MErrno *errP);

  ~FilesystemPerf();

  FilesystemPerf& operator=(FilesystemPerf &fs);
  void clearStats();

  inline char *getFsName() { return fsName; }
  inline char *getNodeName() { return nodeName; }
  inline char *getNodeIpAddr() { return nodeIpAddr; }
  inline UInt64 getBytesRead() { return bytesRead; }
  inline UInt64 getBytesCache() { return bytesCache; }
  inline UInt64 getBytesWritten() { return bytesWritten; }
  inline UInt32 getReads() { return reads; }
  inline UInt32 getCaches() { return caches; }
  inline UInt32 getWrites() { return writes; }
  inline UInt32 getOpenCalls() { return openCalls; }
  inline UInt32 getCloseCalls() { return closeCalls; }
  inline UInt32 getReadCalls() { return readCalls; }
  inline UInt32 getWriteCalls() { return writeCalls; }
  inline UInt32 getReaddirCalls() { return readdirCalls; }
  inline UInt64 getInodesWritten() { return inodesWritten; }
  inline UInt64 getInodesRead() { return inodesRead; }
  inline UInt64 getInodesDeleted() { return inodesDeleted; }
  inline UInt64 getInodesCreated() { return inodesCreated; }
  inline UInt32 getStatCacheHit() { return statCacheHit; }
  inline UInt32 getStatCacheMiss() { return statCacheMiss; }
};

/* File system information */
class FilesystemInfo
{
  friend class PollingHandler;

  char name[NAME_STRING_LEN];

  /* Manager node name. */
  char manager[NAME_STRING_LEN];

  char status[NAME_STRING_LEN];
  char xstatus[NAME_STRING_LEN];

  UInt32 readDuration;
  UInt32 writeDuration;
  UInt32 numMgmt;
  UInt32 numMgrChange;
  UInt64 totalSpace;
  UInt64 numTotalInodes;
  UInt64 freeSpace;
  UInt64 numFreeInodes;
  UInt64 fullBlockFreeSpace;
  UInt64 subBlockFreeSpace;
  char threadWait[NAME_STRING_LEN];
  char diskWait[NAME_STRING_LEN];

  /* Configuration information. */
  UInt64 minFragmentSize;
  UInt64 inodeSize;
  UInt64 indirectBlockSize;
  UInt32 defaultMetadataReplicas;
  UInt32 maxMetadataReplicas;
  UInt32 defaultDataReplicas;
  UInt32 maxDataReplicas;
  char blockAllocationType[NAME_STRING_LEN];
  char fileLockingSemantics[NAME_STRING_LEN];
  char aclSemantics[NAME_STRING_LEN];
  UInt64 estimatedAverageFileSize;
  UInt64 numNodes;
  UInt64 blockSize;
  char quotaEnforced[NAME_STRING_LEN];
  char defaultQuotasEnabled[NAME_STRING_LEN];
  UInt64 maxNumInodes;
  char filesystemVersion[NAME_STRING_LEN];
  char supportForLargeLuns[NAME_STRING_LEN];
  char dmapiEnabled[NAME_STRING_LEN];
  char exactMtime[NAME_STRING_LEN];
  char suppressAtime[NAME_STRING_LEN];
  char automaticMountOption[NAME_STRING_LEN];
  char additionalMountOptions[NAME_STRING_LEN];
  char defaultMountPoint[NAME_STRING_LEN];

  UInt64 bytesRead;
  UInt64 bytesCache;
  UInt64 bytesWritten;

  UInt32 reads;
  UInt32 caches;
  UInt32 writes;

  UInt32 openCalls;
  UInt32 closeCalls;
  UInt32 readCalls;
  UInt32 writeCalls;
  UInt32 readdirCalls;

  UInt64 inodesWritten;
  UInt64 inodesRead;
  UInt64 inodesDeleted;
  UInt64 inodesCreated;

  UInt32 statCacheHit;
  UInt32 statCacheMiss;

  UInt32 nodePerfCount;

  /* Store the list of storage pools - primary key */
  std::vector<StoragePoolInfo *>poolItems;
  struct timeval          poolRefreshTime;    /* Last data refresh time */

  /* Store the list of mounted nodes */
  std::vector<MountedNodeInfo *>mountedNodeItems;

  /* Store the list of policies */
  std::vector<PolicyInfo *>policyItems;

  /* Store the list of per-node performance */
  std::vector<FilesystemPerf *>perfItems;

  /* Workspace indicating this item was found in the SDR file */
  Boolean_t found;

  /* MODS_START */
  bool updated;
  /* MODS_END */

  void copyPools(FilesystemInfo *fsP);
  int getStoragePoolInfoIndex(char *nameP);

  void copyMountedNodes(FilesystemInfo *fsP);
  int getMountedNodeIndex(char *ipAddrP);

  void copyPolicies(FilesystemInfo *fsP);
  int getPolicyInfoIndex(char *nameP);

  void copyPerNodePerfs(FilesystemInfo *fsP);
  int getPerNodePerfIndex(char *ipAddrP);

public:
  FilesystemInfo(MErrno *errP);

  ~FilesystemInfo();

  FilesystemInfo& operator=(FilesystemInfo &fs);
  void clearStats();

  /* Filesystem info from SDR and EE get fs */
  inline char *getName() { return name; }
  inline char *getManager() { return manager; }
  inline char *getStatus() { return status; }
  inline char *getXstatus() { return xstatus; }

  inline UInt32 getReadDuration() { return readDuration; }
  inline UInt32 getWriteDuration() { return writeDuration; }
  inline UInt32 getNumMgmt() { return numMgmt; }
  inline UInt32 getNumMgrChange() { return numMgrChange; }
  inline UInt64 getTotalSpace() { return totalSpace; }
  inline UInt64 getNumTotalInodes() { return numTotalInodes; }
  inline UInt64 getFreeSpace() { return freeSpace; }
  inline UInt64 getNumFreeInodes() { return numFreeInodes; }
  inline UInt64 getFullBlockFreeSpace() { return fullBlockFreeSpace; }
  inline UInt64 getSubBlockFreeSpace() { return subBlockFreeSpace; }

  /* Filesystem performance statistics from mmpmon gfis */
  inline char *getThreadWait() { return threadWait; }
  inline char *getDiskWait() { return diskWait; }

  inline UInt64 getMinFragmentSize() { return minFragmentSize; }
  inline UInt64 getInodeSize() { return inodeSize; }
  inline UInt64 getIndirectBlockSize() { return indirectBlockSize; }
  inline UInt64 getEstimatedAverageFileSize() { return estimatedAverageFileSize; }
  inline UInt64 getNumNodes() { return numNodes; }
  inline UInt64 getBlockSize() { return blockSize; }
  inline UInt64 getFSInodeLimit() { return maxNumInodes; }
  inline UInt32 getDefaultMetadataReplicas() { return defaultMetadataReplicas; }
  inline UInt32 getMaxMetadataReplicas() { return maxMetadataReplicas; }
  inline UInt32 getDefaultDataReplicas() { return defaultDataReplicas; }
  inline UInt32 getMaxDataReplicas() { return maxDataReplicas; }
  inline char *getBlockAllocationType() { return blockAllocationType; }
  inline char *getFileLockingSemantics() { return fileLockingSemantics; }
  inline char *getAclSemantics() { return aclSemantics; }
  inline char *getQuotaEnforced() { return quotaEnforced; }
  inline char *getDefaultQuotasEnabled() { return defaultQuotasEnabled; }
  inline char *getFilesystemVersion() { return filesystemVersion; }
  inline char *getSupportForLargeLuns() { return supportForLargeLuns; }
  inline char *getDmapiEnabled() { return dmapiEnabled; }
  inline char *getExactMtime() { return exactMtime; }
  inline char *getSuppressAtime() { return suppressAtime; }
  inline char *getAutomaticMountOption() { return automaticMountOption; }
  inline char *getAdditionalMountOptions() { return additionalMountOptions; }
  inline char *getDefaultMountPoint() { return defaultMountPoint; }

  inline UInt64 getBytesRead() { return bytesRead; }
  inline UInt64 getBytesCache() { return bytesCache; }
  inline UInt64 getBytesWritten() { return bytesWritten; }
  inline UInt32 getReads() { return reads; }
  inline UInt32 getCaches() { return caches; }
  inline UInt32 getWrites() { return writes; }
  inline UInt32 getOpenCalls() { return openCalls; }
  inline UInt32 getCloseCalls() { return closeCalls; }
  inline UInt32 getReadCalls() { return readCalls; }
  inline UInt32 getWriteCalls() { return writeCalls; }
  inline UInt32 getReaddirCalls() { return readdirCalls; }
  inline UInt64 getInodesWritten() { return inodesWritten; }
  inline UInt64 getInodesRead() { return inodesRead; }
  inline UInt64 getInodesDeleted() { return inodesDeleted; }
  inline UInt64 getInodesCreated() { return inodesCreated; }
  inline UInt32 getStatCacheHit() { return statCacheHit; }
  inline UInt32 getStatCacheMiss() { return statCacheMiss; }

  /* Storage pool information from EE get stgpools */
  inline UInt32 getNumStoragePools() { return poolItems.size(); }
  inline StoragePoolInfo *getStoragePool(int p) { return poolItems.at(p); }
  inline struct timeval getPoolRefreshTime() { return poolRefreshTime; }

  inline UInt32 getNodePerfCount() { return nodePerfCount; }

  inline UInt32 getNumMountedNodes() { return mountedNodeItems.size(); }
  inline MountedNodeInfo *getMountedNode(int n) { return mountedNodeItems.at(n); }

  inline UInt32 getNumPolicies() { return policyItems.size(); }
  inline PolicyInfo *getPolicy(int n) { return policyItems.at(n); }

  inline UInt32 getNumPerNodePerfs() { return perfItems.size(); }
  inline FilesystemPerf *getPerNodePerf(int n) { return perfItems.at(n); }
  
  /* MODS_START */
  inline bool wasUpdated() { return updated; }
  /* MODS_END */
    
};

/* Disk access information */
class DiskAccessInfo
{
  friend class PollingHandler;

  char diskName[NAME_STRING_LEN];
  Boolean_t local;
  char deviceName[NAME_STRING_LEN];
  char serverName[NAME_STRING_LEN];

public:
  DiskAccessInfo(MErrno *errP);

  ~DiskAccessInfo();

  DiskAccessInfo& operator=(DiskAccessInfo &d);

  inline char *getDiskName() { return diskName; }
  inline Boolean_t isLocal() { return local; }
  inline char *getDeviceName() { return deviceName; }
  inline char *getServerName() { return serverName; }
};

/* I/O statistics counted by context

   _response_ begin mmpmon iocs
   _mmpmon::iocs_ _n_ 192.168.105.101 _nn_ c6f2c5vp1 _rc_ 0 _t_ 1262967025 
     _tu_ 739667 _other_ 672560 18244 _mb_ 3427 580 _steal_ 5 8 
     _cleaner_ 0 910 _sync_ 22 487 _logwrap_ 0 16703 _revoke_ 0 0 
     _prefetch_ 9250 0
   _response_ end
*/

class IocStatsInfo
{
  friend class PollingHandler;

  UInt32 iocUnknown_r;
  UInt32 iocUnknown_w;
  UInt32 iocMBHandler_r;
  UInt32 iocMBHandler_w;
  UInt32 iocSteal_r;
  UInt32 iocSteal_w;
  UInt32 iocCleaner_r;
  UInt32 iocCleaner_w;
  UInt32 iocSync_r;
  UInt32 iocSync_w;
  UInt32 iocLogwrap_r;
  UInt32 iocLogwrap_w;
  UInt32 iocRevoke_r;
  UInt32 iocRevoke_w;
  UInt32 iocPrefetch_r;
  UInt32 iocPrefetch_w;

public:
  IocStatsInfo(MErrno *errP);
  ~IocStatsInfo();

  IocStatsInfo& operator=(IocStatsInfo &ioc);

  void clearStats();

  inline UInt32 getIocUnknown_r() { return iocUnknown_r; }
  inline UInt32 getIocUnknown_w() { return iocUnknown_w; }
  inline UInt32 getIocMBHandler_r() { return iocMBHandler_r; }
  inline UInt32 getIocMBHandler_w() { return iocMBHandler_w; }
  inline UInt32 getIocSteal_r() { return iocSteal_r; }
  inline UInt32 getIocSteal_w() { return iocSteal_w; }
  inline UInt32 getIocCleaner_r() { return iocCleaner_r; }
  inline UInt32 getIocCleaner_w() { return iocCleaner_w; }
  inline UInt32 getIocSync_r() { return iocSync_r; }
  inline UInt32 getIocSync_w() { return iocSync_w; }
  inline UInt32 getIocLogwrap_r() { return iocLogwrap_r; }
  inline UInt32 getIocLogwrap_w() { return iocLogwrap_w; }
  inline UInt32 getIocRevoke_r() { return iocRevoke_r; }
  inline UInt32 getIocRevoke_w() { return iocRevoke_w; }
  inline UInt32 getIocPrefetch_r() { return iocPrefetch_r; }
  inline UInt32 getIocPrefetch_w() { return iocPrefetch_w; }

};


/* vfs statistics 

 mmfsadm eventsExporter mmpmon vfss

_response_ begin mmpmon vfss
_mmpmon::vfss_ _n_ 192.168.105.101 _nn_ c6f2c5vp1 _rc_ 0 _t_ 1262970919 
  _tu_ 253243 _access_ 3106 0.037376 _close_ 218 0.033548 _create_ 0 0.000000 
  _fclear_ 0 0.000000 _fsync_ 0 0.000000 _fsync_range_ 0 0.000000 
  _ftrunc_ 0 0.000000 _getattr_ 13590 7.612393 _link_ 0 0.000000 
  _lockctl_ 0 0.000000 _lookup_ 30154 1.026978 _map_lloff_ 0 0.000000 
  _mkdir_ 0 0.000000 _mknod_ 0 0.000000 _open_ 218 0.127916 
  _read_ 380 0.081198 _write_ 0 0.000000 _mmapRead_ 0 0.000000 
  _mmapWrite_ 0 0.000000 _readdir_ 1131 0.459991 _readlink_ 0 0.000000 
  _readpage_ 0 0.000000 _remove_ 3104 45.060595 _rename_ 0 0.000000 
  _rmdir_ 0 0.000000 _setacl_ 0 0.000000 _setattr_ 0 0.000000 
  _symlink_ 0 0.000000 _unmap_ 0 0.000000 _writepage_ 0 0.000000 
  _tsfattr_ 0 0.000000 _tsfsattr_ 0 0.000000 _flock_ 0 0.000000 
  _setxattr_ 0 0.000000 _getxattr_ 0 0.000000 _listxattr_ 0 0.000000 
  _removexattr_ 0 0.000000 _encode_fh_ 0 0.000000 _decode_fh_ 0 0.000000 
  _get_dentry_ 0 0.000000 _get_parent_ 0 0.000000 _mount_ 1 13.515959 
  _statfs_ 0 0.000000 _sync_ 2796 5.254986 _vget_ 0 0.000000
_response_ end

*/

class VfsStatsInfo
{
  friend class PollingHandler;
  
  /* vfs calls */
  UInt32 accessCalls;
  UInt32 closeCalls;
  UInt32 createCalls;
  UInt32 fclearCalls;
  UInt32 fsyncCalls;
  UInt32 fsync_rangeCalls;
  UInt32 ftruncCalls;
  UInt32 getattrCalls;
  UInt32 linkCalls;
  UInt32 lockctlCalls;
  UInt32 lookupCalls;
  UInt32 map_lloffCalls;
  UInt32 mkdirCalls;
  UInt32 mknodCalls;
  UInt32 openCalls;
  UInt32 readCalls;
  UInt32 writeCalls;
  UInt32 mmapReadCalls;
  UInt32 mmapWriteCalls;
  UInt32 readdirCalls;
  UInt32 readlinkCalls;
  UInt32 readpageCalls;
  UInt32 removeCalls;
  UInt32 renameCalls;
  UInt32 rmdirCalls;
  UInt32 setaclCalls;
  UInt32 setattrCalls;
  UInt32 symlinkCalls;
  UInt32 unmapCalls;
  UInt32 writepageCalls;
  UInt32 tsfattrCalls;
  UInt32 tsfsattrCalls;
  UInt32 flockCalls;
  UInt32 setxattrCalls;
  UInt32 getxattrCalls;
  UInt32 listxattrCalls;
  UInt32 removexattrCalls;
  UInt32 encode_fhCalls;
  UInt32 decode_fhCalls;
  UInt32 get_dentryCalls;
  UInt32 get_parentCalls;
  UInt32 mountCalls;
  UInt32 statfsCalls;
  UInt32 syncCalls;
  UInt32 vgetCalls;

  /* total time spent on each call */
  float accessT;
  float closeT;
  float createT;
  float fclearT;
  float fsyncT;
  float fsync_rangeT;
  float ftruncT;
  float getattrT;
  float linkT;
  float lockctlT;
  float lookupT;
  float map_lloffT;
  float mkdirT;
  float mknodT;
  float openT;
  float readT;
  float writeT;
  float mmapReadT;
  float mmapWriteT;
  float readdirT;
  float readlinkT;
  float readpageT;
  float removeT;
  float renameT;
  float rmdirT;
  float setaclT;
  float setattrT;
  float symlinkT;
  float unmapT;
  float writepageT;
  float tsfattrT;
  float tsfsattrT;
  float flockT;
  float setxattrT;
  float getxattrT;
  float listxattrT;
  float removexattrT;
  float encode_fhT;
  float decode_fhT;
  float get_dentryT;
  float get_parentT;
  float mountT;
  float statfsT;
  float syncT;
  float vgetT;

public:
  VfsStatsInfo(MErrno *errP);
  ~VfsStatsInfo();

  VfsStatsInfo& operator=(VfsStatsInfo &v);
  
  void clearStats();

  inline UInt32 getAccessCalls() { return  accessCalls; }
  inline UInt32 getCloseCalls() { return  closeCalls; }
  inline UInt32 getCreateCalls() { return  createCalls; }
  inline UInt32 getFclearCalls() { return  fclearCalls; }
  inline UInt32 getFsyncCalls() { return  fsyncCalls; }
  inline UInt32 getFsync_rangeCalls() { return  fsync_rangeCalls; }
  inline UInt32 getFtruncCalls() { return  ftruncCalls; }
  inline UInt32 getGetattrCalls() { return getattrCalls; }
  inline UInt32 getLinkCalls() { return  linkCalls; }
  inline UInt32 getLockctlCalls() { return  lockctlCalls; }
  inline UInt32 getLookupCalls() { return  lookupCalls; }
  inline UInt32 getMap_lloffCalls() { return  map_lloffCalls; }
  inline UInt32 getMkdirCalls() { return  mkdirCalls; }
  inline UInt32 getMknodCalls() { return mknodCalls; }
  inline UInt32 getOpenCalls() { return  openCalls; }
  inline UInt32 getReadCalls() { return  readCalls; }
  inline UInt32 getWriteCalls() { return  writeCalls; }
  inline UInt32 getMmapReadCalls() { return  mmapReadCalls; }
  inline UInt32 getMmapWriteCalls() { return  mmapWriteCalls; }
  inline UInt32 getReaddirCalls() { return  readdirCalls; }
  inline UInt32 getReadlinkCalls() { return readlinkCalls; }
  inline UInt32 getReadpageCalls() { return  readpageCalls; }
  inline UInt32 getRemoveCalls() { return removeCalls; }
  inline UInt32 getRenameCalls() { return renameCalls ; }
  inline UInt32 getRmdirCalls() { return rmdirCalls; }
  inline UInt32 getSetaclCalls() { return setaclCalls; }
  inline UInt32 getSetattrCalls() { return  setattrCalls; }
  inline UInt32 getSymlinkCalls() { return  symlinkCalls; }
  inline UInt32 getUnmapCalls() { return  unmapCalls; }
  inline UInt32 getWritepageCalls() { return  writepageCalls; }
  inline UInt32 getTsfattrCalls() { return  tsfattrCalls; }
  inline UInt32 getTsfsattrCalls() { return  tsfsattrCalls; }
  inline UInt32 getFlockCalls() { return  flockCalls; }
  inline UInt32 getSetxattrCalls() { return  setxattrCalls; }
  inline UInt32 getGetxattrCalls() { return  getxattrCalls; }
  inline UInt32 getListxattrCalls() { return listxattrCalls ; }
  inline UInt32 getRemovexattrCalls() { return  removexattrCalls; }
  inline UInt32 getEncode_fhCalls() { return  encode_fhCalls; }
  inline UInt32 getDecode_fhCalls() { return  decode_fhCalls; }
  inline UInt32 getGet_dentryCalls() { return  get_dentryCalls; }
  inline UInt32 getGet_parentCalls() { return  get_parentCalls; }
  inline UInt32 getMountCalls() { return  mountCalls; }
  inline UInt32 getStatfsCalls() { return  statfsCalls; }
  inline UInt32 getSyncCalls() { return  syncCalls; }
  inline UInt32 getVgetCalls() { return  vgetCalls; }

  inline float getAccessTime() { return  accessT; }
  inline float getCloseTime() { return  closeT; }
  inline float getCreateTime() { return  createT; }
  inline float getFclearTime() { return  fclearT; }
  inline float getFsyncTime() { return  fsyncT; }
  inline float getFsync_rangeTime() { return  fsync_rangeT; }
  inline float getFtruncTime() { return  ftruncT; }
  inline float getGetattrTime() { return  getattrT; }
  inline float getLinkTime() { return  linkT; }
  inline float getLockctlTime() { return  lockctlT; }
  inline float getLookupTime() { return  lookupT; }
  inline float getMap_lloffTime() { return  map_lloffT; }
  inline float getMkdirTime() { return  mkdirT; }
  inline float getMknodTime() { return mknodT; }
  inline float getOpenTime() { return  openT; }
  inline float getReadTime() { return  readT; }
  inline float getWriteTime() { return  writeT; }
  inline float getMmapReadTime() { return  mmapReadT; }
  inline float getMmapWriteTime() { return  mmapWriteT; }
  inline float getReaddirTime() { return  readdirT; }
  inline float getReadlinkTime() { return readlinkT; }
  inline float getReadpageTime() { return  readpageT; }
  inline float getRemoveTime() { return removeT; }
  inline float getRenameTime() { return renameT ; }
  inline float getRmdirTime() { return rmdirT; }
  inline float getSetaclTime() { return setaclT; }
  inline float getSetattrTime() { return  setattrT; }
  inline float getSymlinkTime() { return  symlinkT; }
  inline float getUnmapTime() { return  unmapT; }
  inline float getWritepageTime() { return  writepageT; }
  inline float getTimesfattrT() { return  tsfattrT; }
  inline float getTimesfsattrT() { return  tsfsattrT; }
  inline float getFlockTime() { return  flockT; }
  inline float getSetxattrTime() { return  setxattrT; }
  inline float getGetxattrTime() { return  getxattrT; }
  inline float getListxattrTime() { return listxattrT ; }
  inline float getRemovexattrTime() { return  removexattrT; }
  inline float getEncode_fhTime() { return  encode_fhT; }
  inline float getDecode_fhTime() { return  decode_fhT; }
  inline float getGet_dentryTime() { return  get_dentryT; }
  inline float getGet_parentTime() { return  get_parentT; }
  inline float getMountTime() { return  mountT; }
  inline float getStatfsTime() { return  statfsT; }
  inline float getSyncTime() { return  syncT; }
  inline float getVgetTime() { return  vgetT; }
};

/* Per node thread utilization stats

  _response_ begin mmpmon threads
  _mmpmon::threads_ _n_ 192.168.105.101 _nn_ c6f2c5vp1 _rc_ 0 _t_ 1263415922 
     _tu_ 317953 _nthreads_ 127 _seq_ 60149 _noncritical_ 13 28 1473 
     _daemonstartup_ 14 16 33 _mbhandler_ 29 29 65 _rcvworker_ 10 11 266 
     _revokeworker_ 0 0 35 _rangerevoke_ 0 0 20 _reclockrevoke_ 0 0 10 
     _prefetch_ 1 1 72 _sgexception_ 0 3 16 _receiver_ 12 12 16 
     _pcache_ 0 0 0 _multithreadworker_ 0 0 974
  _response_ end
  
*/

class ThreadUtilInfo
{
  friend class PollingHandler;
  UInt32 nThreads;
  UInt32 seq; 

  /* Thread pool utilization (current/highest/maximum) */
  threadUtil_t noncritical;
  threadUtil_t daemonstartup;
  threadUtil_t mbhandler;
  threadUtil_t rcvworker;
  threadUtil_t revokeworker;
  threadUtil_t rangerevoke;
  threadUtil_t reclockrevoke;
  threadUtil_t prefetch;
  threadUtil_t sgexception;
  threadUtil_t receiver;
  threadUtil_t pcache;
  threadUtil_t multithreadworker;

public:
  ThreadUtilInfo(MErrno *errP);
  ~ThreadUtilInfo();

  ThreadUtilInfo& operator=(ThreadUtilInfo &th_u);

  void clearStats();

  inline UInt32 getNthreads() { return nThreads; }
  inline UInt32 getSeq() { return seq; }

  inline threadUtil_t getNoncritical() { return noncritical; }
  inline threadUtil_t getDaemonstartup() { return daemonstartup; }
  inline threadUtil_t getMbhandler() { return mbhandler; }
  inline threadUtil_t getRcvworker() { return rcvworker; }
  inline threadUtil_t getRevokeworker() { return revokeworker; }
  inline threadUtil_t getRrangerevoke() { return rangerevoke; }
  inline threadUtil_t getReclockrevoke() { return reclockrevoke; }
  inline threadUtil_t getPrefetch() { return prefetch; }
  inline threadUtil_t getSgexception() { return sgexception; }
  inline threadUtil_t getReceiver() { return receiver; }
  inline threadUtil_t getPcache() { return pcache; }
  inline threadUtil_t getMultithreadworker() { return multithreadworker; }

};

/* Cache hit miss statistics

   _response_ begin mmpmon chms
   _mmpmon::chms_ _n_ 192.168.105.101 _nn_ c6f2c5vp1 _rc_ 0 _t_ 1263846820 
                 _tu_ 373341 _dch_ 0 _dcm_ 0 _sch_ 43027 _scm_ 34
   _response_ end

*/

class CacheStatsInfo
{
  friend class PollingHandler;

  UInt32 dataCacheHit;   /* _dch_ */
  UInt32 dataCacheMiss;  /* _dcm_ */
  UInt32 statCacheHit;   /* _sch_ */
  UInt32 statCacheMiss;  /* _scm_ */

public:
  CacheStatsInfo(MErrno *errP);
  ~CacheStatsInfo();

  CacheStatsInfo& operator=(CacheStatsInfo &c);

  void clearStats();

  inline UInt32 getDataCacheHit() { return dataCacheHit; }
  inline UInt32 getDataCacheMiss() { return dataCacheMiss; }
  inline UInt32 getStatCacheHit() { return statCacheHit; }
  inline UInt32 getStatCacheMiss() { return statCacheMiss; }
};

/* 
 * PANACHE statistics
   _response_ begin mmpmon pncs
   _mmpmon::pncs_ _n_ 192.168.115.156 _nn_ hs21n20 _rc_ 0 _t_ 1263954355 
     _tu_ 209718 _br_ 0 _bw_ 0 _ws_ 0 _wl_ 0 _wa_ 0 _ne_ 0 _nf_ 0 _ns_ 0 _nr_ 0
     _ncmd_ 20 _q_ 0 _i_ 0 _c_ 0 _e_ 0 _f_ 0 _n_ 0 
               _q_ 0 _i_ 0 _c_ 0 _e_ 0 _f_ 0 _n_ 0 
               _q_ 0 _i_ 0 _c_ 0 _e_ 0 _f_ 0 _n_ 0
              ... 
               _q_ 0 _i_ 0 _c_ 0 _e_ 0 _f_ 0 _n_ 0 
               _q_ 0 _i_ 0 _c_ 0 _e_ 0 _f_ 0 _n_ 0
   _response_ end
 *
 */

class PCacheStatsInfo
{
  friend class PollingHandler;

  UInt64 bytesRead;
  UInt64 bytesWritten;
  UInt32 numExpire;   /* msgs exec due to timer */
  UInt32 numForce;    /* msgs exec due to Q limit, etc */
  UInt32 numSync;     /* msgs exec due to sync cmd */
  UInt32 numRevoke;   /* msgs exec due to revoke */
  UInt32 numExecuted; /* total msgs exec */
  UInt32 shortest_waitTime;  /* in seconds */
  UInt32 longest_waitTime;   /* in seconds */
  UInt32 average_waitTime;   /* in seconds */
  UInt32 numPcacheCmds;
  pCacheCmdInfo_t pCacheCmds[MAX_PCACHE_CMD_INFO];

public:
  PCacheStatsInfo(MErrno *errP);
  ~PCacheStatsInfo();

  PCacheStatsInfo& operator=(PCacheStatsInfo &c);

  void clearStats();

  pCacheCmdInfo_t *getPCacheCmdInfoP(int cmd);

  inline UInt64 getBytesRead() { return bytesRead; }
  inline UInt64 getBytesWritten() { return bytesWritten; }
  inline UInt32 getNumExpire() { return numExpire; }
  inline UInt32 getNumForce() { return numForce; }
  inline UInt32 getNumSync() { return numSync; }
  inline UInt32 getNumRevoke() { return numRevoke; }
  inline UInt32 getNumExecuted() { return numExecuted; }
  inline UInt32 getShortest_waitTime() { return shortest_waitTime; }
  inline UInt32 getLongest_waitTime() { return longest_waitTime; }
  inline UInt32 getAverage_waitTime() { return average_waitTime; }
  inline UInt32 getNumPacheCmds() { return numPcacheCmds; }

};

/* Node information */
class NodeInfo
{
  friend class PollingHandler;

  char name[NAME_STRING_LEN];
  char ipAddr[NAME_STRING_LEN];
  char platform[NAME_STRING_LEN];
  char endian[NAME_STRING_LEN];
  char type[NAME_STRING_LEN];
  char osname[NAME_STRING_LEN];
  char admin[NAME_STRING_LEN];
  char status[NAME_STRING_LEN];
  char version[NAME_STRING_LEN];
  UInt32 failureCount;
  UInt32 threadWait;
  char healthy[NAME_STRING_LEN];
  char diagnosis[NAME_STRING_LEN];
  UInt64 pagePoolSize;
  UInt32 prefetchThreads;
  UInt32 maxMBPS;
  UInt32 maxFilesToCache;
  UInt32 maxStatCache;
  UInt32 worker1Threads;
  UInt32 dmapiEventTimeout;
  UInt32 dmapiMountTimeout;
  UInt32 dmapiSessFailureTimeout;
  UInt32 nsdServerWaitTimeWindowOnMount;
  UInt32 nsdServerWaitTimeForMount;
  char unmountOnDiskFail[32];

  double readTime;
  double writeTime;

  Boolean_t found;

  std::vector<DiskAccessInfo *>diskAccessItems;

  void copyDiskAccesses(NodeInfo *nodeP);
  int getDiskAccessIndex(char *nameP);

  /* I/O statistics counted by context */ 
  IocStatsInfo *iocStatsP;

  /* vfs statistics */
  VfsStatsInfo *vfsStatsP;

  /* thread pool utilization */
  ThreadUtilInfo *threadUtilP;

  /* cache hit/miss stats */
  CacheStatsInfo *cacheStatsP;

  /* pcache gateway stats */
  PCacheStatsInfo *pCacheStatsP;
  

public:
  NodeInfo(MErrno *errP);

  ~NodeInfo();

  NodeInfo& operator=(NodeInfo &n);
  void clearStats();

  /* Node info from SDR */
  inline char *getName() { return name; }
  inline char *getIpAddr() { return ipAddr; }
  inline char *getType() { return type; }
  inline char *getEndian() { return endian; }
  inline char *getOsName() { return osname; }; 
  inline char *getVersion() { return version; }
  inline char *getPlatform() { return platform; }

  /* Node info from EE get nodes */
  inline char *getAdmin() { return admin; }
  inline char *getStatus() { return status; }
  inline UInt32 getFailureCount() { return failureCount; }
  inline UInt32 getThreadWait() { return threadWait; }
  inline char *getHealthy() { return healthy; }
  inline char *getDiagnosis() { return diagnosis; }

  inline UInt64 getPagePoolSize() { return pagePoolSize; }
  inline UInt32 getPrefetchThreads() { return prefetchThreads; }
  inline UInt32 getMaxMBPS() { return maxMBPS; }
  inline UInt32 getMaxFilesToCache() { return maxFilesToCache; }
  inline UInt32 getMaxStatCache() { return maxStatCache; }
  inline UInt32 getWorker1Threads() { return worker1Threads; }
  inline UInt32 getDmapiEventTimeout() { return dmapiEventTimeout; }
  inline UInt32 getDmapiMountTimeout() { return dmapiMountTimeout; }
  inline UInt32 getDmapiSessFailureTimeout() { return dmapiSessFailureTimeout; }
  inline UInt32 getNsdServerWaitTimeWindowOnMount() { return nsdServerWaitTimeWindowOnMount; }
  inline UInt32 getNsdServerWaitTimeForMount() { return nsdServerWaitTimeForMount; }
  inline char *getUnmountOnDiskFail() { return unmountOnDiskFail; }

  inline UInt32 getNumDiskAccesses() { return diskAccessItems.size(); }
  inline DiskAccessInfo *getDiskAccess(int d) { return diskAccessItems.at(d); }

  inline VfsStatsInfo *getVfsStatsInfo() { return vfsStatsP; }
  inline IocStatsInfo *getIocStatsInfo() { return iocStatsP; }
  inline ThreadUtilInfo *getThreadUtilInfo() { return threadUtilP; }
  inline CacheStatsInfo *getCacheStatsInfo() { return cacheStatsP; }
  inline PCacheStatsInfo *getPCacheStatsInfo() { return pCacheStatsP; }

  /* Currently unused */
  inline double getReadTime() { return readTime; }
  inline double getWriteTime() { return writeTime; }
};

/* Cluster information */
class ClusterInfo
{
  friend class PollingHandler;

  /* parsable from mmsdrfs */
  char name[NAME_STRING_LEN];
  char id[NAME_STRING_LEN];
  char type[NAME_STRING_LEN];
  char minReleaseLevel[NAME_STRING_LEN];
  char uidDomain[NAME_STRING_LEN];
  char remoteShellCommand[NAME_STRING_LEN];
  char remoteFileCopyCommand[NAME_STRING_LEN];
  char primaryServer[NAME_STRING_LEN];
  char secondaryServer[NAME_STRING_LEN];

  UInt32 maxBlockSize;
  UInt32 distributedTokenServer;
  /*UInt32 useDiskLease;*/
  UInt32 failureDetectionTime;
  UInt32 tcpPort;
  UInt32 minMissedPingTimeout;
  UInt32 maxMissedPingTimeout;

  UInt32 sdrfsGenNumber;

  struct timeval clusterRefreshTime;

  /* Store the list of node name - primary key */
  std::vector<NodeInfo *>nodeItems;
  struct timeval nodeRefreshTime;

  /* Store the list of file system name - primary key */
  std::vector<FilesystemInfo *>fsItems;
  struct timeval FSRefreshTime;
  struct timeval FSPerfRefreshTime;

  std::vector<DiskInfo *>freeDiskItems;

  void copyNodes(ClusterInfo *clP);
  void copyFS(ClusterInfo *clP);
  void copyFreeDisks(ClusterInfo *clP);
  int getNodeInfoIndex(char *ipAddrP);
  int getNodeInfoIndexByName(char *nameP);
  int getFilesystemInfoIndex(char *nameP);
  int getFreeDiskInfoIndex(char *nameP);

  struct timeval diskSDRRefreshTime;

public:
  ClusterInfo(MErrno *errP);

  ~ClusterInfo();

  ClusterInfo& operator=(ClusterInfo &cl);

  /* member accessors */
  inline char *getName() { return name; }
  inline char *getId() { return id; }
  inline char *getType() { return type; }
  inline char *getMinReleaseLevel() { return minReleaseLevel; }
  inline char *getUidDomain() { return uidDomain; }
  inline char *getRemoteShellCommand() { return remoteShellCommand; }
  inline char *getRemoteFileCopyCommand() { return remoteFileCopyCommand; }
  inline char *getPrimaryServer() { return primaryServer; }
  inline char *getSecondaryServer() { return secondaryServer; }
  inline UInt32 getMaxBlockSize() { return maxBlockSize; }
  inline struct timeval getClusterRefreshTime() { return clusterRefreshTime; }
  inline UInt32 getSdrfsGenNumber() { return sdrfsGenNumber; }

  inline UInt32 getNumNodes() { return nodeItems.size(); }
  inline NodeInfo *getNode(int n) { return nodeItems.at(n); }
  inline struct timeval getNodeRefreshTime() { return nodeRefreshTime; }
  inline UInt32 getNumFilesystems() { return fsItems.size(); }
  inline FilesystemInfo *getFilesystem(int f) { return fsItems.at(f); }
  inline struct timeval getFSRefreshTime() { return FSRefreshTime; }
  inline struct timeval getFSPerfRefreshTime() { return FSPerfRefreshTime; }
  inline UInt32 getDistributedTokenServer() { return distributedTokenServer; }
  inline UInt32 getFailureDetectionTime() { return failureDetectionTime; }
  inline UInt32 getTCPPort() { return tcpPort; }
  inline UInt32 getMinMissedPingTimeout() { return minMissedPingTimeout; }
  inline UInt32 getMaxMissedPingTimeout() { return maxMissedPingTimeout; }
  inline UInt32 getNumFreeDisks() { return freeDiskItems.size(); }
  inline DiskInfo *getFreeDisk(int d) { return freeDiskItems.at(d); }
};

/* Cluster status information */
class ClusterStatus
{
  friend class PollingHandler;

public:
  char managerNode[NAME_STRING_LEN];
  char managerIpAddr[NAME_STRING_LEN];
  UInt32 nLocalNodes;      /* number of nodes defined in the cluster */
  UInt32 nLocalJoined;     /* number of local nodes active in the cluster */
  UInt32 nRmtJoined;       /* number of remote nodes joined in this cluster */
  UInt32 nQNodesInCluster; /* number of quorum nodes defined in the cluster */
  UInt32 nQNodesJoined;    /* number of quorum nodes active in the cluster */
  UInt32 cfgMinQuorumNodes;/*  minimum no of nodes to reach quorum */
  UInt32 quorumAchieved ;  /* Quorum achieved (=1), not achieved (=0)*/

public:
  ClusterStatus();
  ~ClusterStatus();

  void init();

  /* member accessors */
  inline char *getManagerNode() { return managerNode; }
  inline char *getManagerIpAddr() { return managerIpAddr; }
  inline UInt32 getNLocalNodes() { return nLocalNodes; }
  inline UInt32 getNLocalJoined() { return nLocalJoined; }
  inline UInt32 getNRmtJoined() { return nRmtJoined; }
  inline UInt32 getNQNodesInCluster() { return nQNodesInCluster; }
  inline UInt32 getNQNodesJoined() { return nQNodesJoined; }
  inline UInt32 getCfgMinQuorumNodes() { return cfgMinQuorumNodes; }
  inline UInt32 getQuorumAchieved() { return quorumAchieved; }
};

/* MODS_START */
class FileSet
{

  friend class PollingHandler;

public:

  UInt32 gpfsFilesetVersion;
  char gpfsFilesetName[NAME_STRING_LEN];
  char gpfsFileSystemName[NAME_STRING_LEN];
  char gpfsFilesetID[NAME_STRING_LEN];
  char gpfsFilesetRootINode[NAME_STRING_LEN];
  char gpfsFilesetStatus[NAME_STRING_LEN];
  char gpfsFilesetPath[NAME_STRING_LEN];
  char gpfsFilesetParentID[NAME_STRING_LEN];
  UInt64 gpfsFilesetINodes;
  char gpfsFilesetCreated[TIME_STAMP_CHARS];
  UInt64 gpfsFilesetDataInKB;
  char gpfsFilesetComment[NAME_STRING_LEN];
  bool gpfsFilesetIsLinked;
  bool gpfsFilesetHasComment;

  // methods
  inline char* getName()
  {
    return gpfsFilesetName;
  }
  inline char* getId()
  {
    return gpfsFilesetID;
  }
  inline char* getRootINode()
  {
    return gpfsFilesetRootINode;
  }
  inline char* getParentId()
  {
    return gpfsFilesetParentID;
  }
  inline UInt64 getINodes()
  {
    return gpfsFilesetINodes;
  }
  inline UInt64 getData()
  {
    return gpfsFilesetDataInKB;
  }
  inline char* getComment()
  {
    return gpfsFilesetComment;
  }
  inline char* getFSName()
  {
    return gpfsFileSystemName;
  }
  inline char* getStatus()
  {
    return gpfsFilesetStatus;
  }
  inline char* getPath()
  {
    return gpfsFilesetPath;
  }
  inline char* getCreated()
  {
    return gpfsFilesetCreated;
  }
  inline UInt32 getVersion()
  {
    return gpfsFilesetVersion;
  }

private:
};

class User
{
  friend class PollingHandler;
public:

  User()
  {
    hasName = false;
  }

  char gpfsUserName[NAME_STRING_LEN];
  char gpfsUserFileSystemName[NAME_STRING_LEN];
  char gpfsUserClusterName[NAME_STRING_LEN];
  char gpfsUserHomePath[NAME_STRING_LEN];
  UInt32 gpfsUserId;
  UInt32 gpfsMainGroupId;

  // temporary flag to show that this user has a name
  bool hasName;

  inline char* getName()
  {
    return gpfsUserName;
  }
  inline char* getFSName()
  {
    return gpfsUserFileSystemName;
  }
  inline char* getCSName()
  {
    return gpfsUserClusterName;
  }
  inline char* getHomePath()
  {
    return gpfsUserHomePath;
  }
  inline UInt32 getUserId()
  {
    return  gpfsUserId;
  }
  inline UInt32 getMainGroupId()
  {
    return  gpfsMainGroupId;
  }

private:
};

class Group
{
  friend class PollingHandler;
public:

  Group()
  {
    hasName = false;
  }

  char gpfsGroupName[NAME_STRING_LEN];
  char gpfsGroupFileSystemName[NAME_STRING_LEN];
  char gpfsGroupClusterName[NAME_STRING_LEN];
  UInt32 gpfsGroupId;

  // temporary flag to show that this group has a name
  bool hasName;

  inline char* getName()
  {
    return gpfsGroupName;
  }
  inline char* getFSName()
  {
    return gpfsGroupFileSystemName;
  }
  inline char* getCSName()
  {
    return gpfsGroupClusterName;
  }
  inline UInt32 getGroupId()
  {
    return  gpfsGroupId;
  }

private:
};

/* DJ_MODS_START */
class FileOrDirOwner
{

    friend class PollingHandler;

public:

  char osOwnerName[NAME_STRING_LEN];
  char osGroupName[NAME_STRING_LEN];
  char osFileOrDirList[NAME_STRING_LEN]; // ',' separated list..same as chown
  Boolean_t dir;
  Boolean_t jnxn;

  inline char* getOwnerName()
  {
    return osOwnerName;
  }
  inline char* getGroupName()
  {
    return osGroupName;
  }
  inline char* getFileOrDirList()
  {
    return osFileOrDirList;
  }
  inline Boolean_t isDirectory()
  {
    return dir;
  }
  inline Boolean_t isJnxn()
  {
    return jnxn;
  }

private:
};
/* DJ_MODS_END*/

class Quota
{

public:

  Quota()
  {
    gpfsQuotaHeader = 0;
    gpfsQuotaVersion = 0;
    gpfsQuotaType = 0;
    gpfsQuotaID = 0;
    gpfsQuotaBlockUsage = 0;
    gpfsQuotaBlockQuota = 0;
    gpfsQuotaBlockLimit = 0;
    gpfsQuotaBlockInDoubt = 0;
    gpfsQuotaFilesUsage = 0;
    gpfsQuotaFilesQuota = 0;
    gpfsQuotaFilesLimit = 0;
    gpfsQuotaFilesInDoubt = 0;
    gpfsQuotaFilesInDoubt = 0;

    gpfsQuotaClusterName.clear();
    gpfsQuotaFileSystemName.clear();
    gpfsQuotaEntityName.clear();
    gpfsQuotaBlockGrace.clear();
    gpfsQuotaFilesGrace.clear();
    gpfsQuotaRemarks.clear();
  }

  std::string gpfsQuotaClusterName;
  UInt32 gpfsQuotaHeader;
  UInt32 gpfsQuotaVersion;
  std::string gpfsQuotaFileSystemName;
  UInt16 gpfsQuotaType;
  UInt32 gpfsQuotaID;
  std::string gpfsQuotaEntityName;
  UInt64 gpfsQuotaBlockUsage;
  UInt64 gpfsQuotaBlockQuota;
  UInt64 gpfsQuotaBlockLimit;
  UInt32 gpfsQuotaBlockInDoubt;
  std::string gpfsQuotaBlockGrace;
  UInt64 gpfsQuotaFilesUsage;
  UInt64 gpfsQuotaFilesQuota;
  UInt64 gpfsQuotaFilesLimit;
  UInt32 gpfsQuotaFilesInDoubt;
  std::string gpfsQuotaFilesGrace;
  std::string gpfsQuotaRemarks;

  inline std::string getClusterName()
  {
    return gpfsQuotaClusterName;
  }
  inline UInt32 getHeader()
  {
    return  gpfsQuotaHeader;
  }
  inline UInt32 getVersion()
  {
    return gpfsQuotaVersion;
  }
  inline std::string getFileSystemName()
  {
    return gpfsQuotaFileSystemName;
  }
  inline UInt16 getType()
  {
    return gpfsQuotaType;
  }
  inline UInt32 getId()
  {
    return gpfsQuotaID;
  }
  inline std::string getEntityName()
  {
    return gpfsQuotaEntityName;
  }
  inline UInt64 getBlockUsage()
  {
    return gpfsQuotaBlockUsage;
  }
  inline UInt64 getBlockQuota()
  {
    return gpfsQuotaBlockQuota;
  }
  inline UInt64 getBlockLimit()
  {
    return gpfsQuotaBlockLimit;
  }
  inline UInt32 getBlockInDoubt()
  {
    return gpfsQuotaBlockInDoubt;
  }
  inline std::string getBlockGrace()
  {
    return gpfsQuotaBlockGrace;
  }
  inline UInt64 getFilesUsage()
  {
    return gpfsQuotaFilesUsage;
  }
  inline UInt64 getFilesQuota()
  {
    return gpfsQuotaFilesQuota;
  }
  inline UInt64 getFilesLimit()
  {
    return gpfsQuotaFilesLimit;
  }
  inline UInt32 getFilesInDoubt()
  {
    return gpfsQuotaFilesInDoubt;
  }
  inline std::string getFilesGrace()
  {
    return gpfsQuotaFilesGrace;
  }
  inline std::string getRemarks()
  {
    return gpfsQuotaRemarks;
  }

private:

};
/* MODS_END */

#define dfprintf if (debug) fprintf

/* forward declaration */
class MmpmonWrapperUtils;
class CommandWrapperUtils;

/* Provide pull API to external tasks */
class PollingHandler
{
  friend class ClusterInfo;
  friend class NodeInfo;
  friend class FilesystemInfo;
  friend class DiskInfo;

  MmpmonWrapperUtils *wrapper;

  /* Thread for executing predefined command scripts to cache the results.
     Potentially long-time taking command scripts should be added here. */
  pthread_t cmdThread;

  /* Thread for doing things regularly. Currently, it wakes up a command
     thread periodically. */
  pthread_t timerThread;

  /* Thread for doing configurations. */
  pthread_t dispatchThread;

  CommandWrapperUtils *cmdWrapper;

  /* Flag that decides whether a command thread should terminate. */
  int terminate;

  /* Flag that decides whether thimer thread should terminate. */
  int timer_terminate;

  /* Flag that decides whether dispatch thread should terminate. */
  int execTerminate;

  ClusterInfo *recipe;

  /* Main routine for command thread. */
  static void *cmdHandlerBody(void *argP);

  /* Main routine for timer thread. */
  static void *timerHandlerBody(void *argP);

  /* Main routine for dispatch thread. */
  static void *dispatchHandlerBody(void *argP);

  MErrno initNodeList();

  void   initClusterRecipe(ClusterInfo *infoP);
  MErrno checkFailedNode();
  char *grabValue(char *buf, int index, char *answer);

  pthread_mutex_t mutex;

  /* Execution task list. It is added by external tasks. */
  pthread_mutex_t listMutex;
  std::vector<ExecutionTask *>execTaskItems;

  int debug;
  MgmtProtocol protocol;
  Int32 pid; /* external process id, to identify this connection */

  /* Update rule info in PolicyInfo */
  MErrno fillRuleInfo(FilesystemInfo *fsP, PolicyInfo *policyP);
  
  /* MODS_START */
  MErrno logInit();
  /* MODS_END */
  
public:

  Int32 getPid() { return pid; }

  MErrno cleanupNodeList();
  PollingHandler(MErrno *errP, MgmtProtocol proto, int debg=0);

  ~PollingHandler();

  static MErrno init(MgmtProtocol proto, int debg=0);
  static void term();

  MmpmonWrapperUtils *getMmpmonWrapper() { return wrapper; }

  /* Cluster recipe is ClusterInfo object which contains primary keys of
     nodes, file systems and disks. It is parsed from mmsdrfs file. */
  MErrno refreshClusterRecipe();

  MErrno parseClusterFile(ClusterInfo *cl);

  /* Get a copy of the cluster info */
  MErrno getClusterInfo(ClusterInfo *clP);

  /* current status of cluster */
  MErrno getClusterStatus(ClusterStatus *clStatusP, 
                          int flag = CLUSTER_STATE_ALL);

  MErrno updateDiskSDRInfo(int norefresh=0);

  /* The following update calls will update both the internal copy of the
     data and the caller's copy, which is pointed to by clP. */

  MErrno updateClusterInfo(ClusterInfo *clP, int norefresh=0);

  /* Update node list which belongs to the specified cluster */
  MErrno updateNodeInfo(ClusterInfo *clP, int norefresh=0);

  /* MODS_START */
  /* Method used to quickly populate mount point for nodes->file systems */
  MErrno updateFilesystemMountPointInfo(ClusterInfo *clP);
  /* MODS_END */    
  
  /* Update filesystem list which belongs to the specified cluster */
  MErrno updateFilesystemInfo(ClusterInfo *clP, int getPerf=0);

  /* Update storage pool list which belongs to the specified filesystem
     (NULL=all filesystems) */
  MErrno updateStoragePoolInfo(ClusterInfo *clP, char *fsName=NULL);

  /* Update disk list which belongs to the specified filesystem/pool
     (NULL=all pools in the filesystem) */
  MErrno updateDiskInfo(ClusterInfo *clP, char *fsName, char *poolName=NULL,
                        int getPerf=0);

  MErrno updateFreeDiskInfo(ClusterInfo *clP);

  /* Update per node ioc statistics */
  MErrno updateIocStatsInfo(ClusterInfo *clP);

  /* Update per node VFS statistics */
  MErrno updateVfsStatsInfo(ClusterInfo *clP);

  /* Update per node thread pool utilization  statistics */
  MErrno updateThreadUtilInfo(ClusterInfo *clP);

  /* Update per node cache hit miss statistics */
  MErrno updateCacheStatsInfo(ClusterInfo *clP);


  /* Update per node pcache gateway statistics */
  MErrno updatePCacheStatsInfo(ClusterInfo *clP);

  MErrno processCommand(const char *cmd);

  MErrno copyRecipe(ClusterInfo *clP);

  /* Update mounted node info in FilesystemInfo */
  MErrno updateMountedNodeInfo(ClusterInfo *clP);

  /* Update policy info in FilesystemInfo */
  MErrno updatePolicyInfo(ClusterInfo *clP);

  /* Update file system manager node info in FilesystemInfo */
  MErrno updateFilesystemManagerInfo(ClusterInfo *clP);

  /* Update file system configuration info in FilesystemInfo */
  MErrno updateFilesystemConfigInfo(ClusterInfo *clP);

  /* Update disk access info in NodeInfo */
  MErrno updateDiskAccessInfo(ClusterInfo *clP);

  /* Update NSD server info in DiskInfo */
  MErrno updateDiskServerInfo(DiskInfo *diskP, char *serverListP,
                              char *backupServerListP);

  /* Update indirect disk access info (through NSD servers) in NodeInfo */
  MErrno updateIndirectDiskAccessInfo(ClusterInfo *clP, DiskInfo *diskP);

  /* MODS_START */
  /* Update the file set list */
  MErrno getFileSet(char *fileSystemName, char *fileSetName, FileSet *fileSet);
  MErrno getFileSets(char *fileSystemName, std::vector<FileSet *>*fileSetList);

  MErrno getFileSets1(char *fileSystemNameP, 
                     FileSet *fileSetListP,  /* caller allocated/freed */
                     int *nElemP  /* in: size of fileSetListP
                                     out: number of filesets needed */
                     );
  /* type: users=1, group=2, fileset=3 */
  MErrno getQuota(int type, const char *fsName, 
                  const char *entityName, Quota *quota );
#ifdef MMANTRAS_QUOTAS
  MErrno getQuotas(int type, const char *fsName, 
                   std::vector <Quota *>*quotas );
#endif

  MErrno createFileSet(FileSet fileSet, 
                       std::string *gpfsMsg, bool isNull);

  MErrno deleteFileSet(FileSet fileSet, 
                       bool force, std::string *gpfsMs);

  MErrno editQuota(char *cFsName, char *cType, 
                   char *cEntityId, UInt64 *cNewFileSoftLim, 
                   UInt64 *cNewFileHardLim, UInt64 *cNewBlockSoftLim,
                   UInt64 *cNewBlockHardLim,  char *cNaramGracePeriod, 
                   std::string *gpfsMsg);

  MErrno editFileset(char *cFsName, char *cType, 
                     char *cEntityId, char *cNewName, char *cNewComment, 
                     std::string *gpfsMsg);

  /* DJ_MODS_START */
  // Link a fileset
  MErrno linkFileSet(FileSet jnxnFileset, std::string *gpfsMsg);

  // Unlink a fileset
  MErrno unlinkFileSet(const char *fsetNameOrJnxnPath, 
                       const char *tgt, bool isFsetName, bool force, 
                       std::string *gpfsMsg);

  // Change owner or group of a file
  // NOTE: This is not GPFS fucntionality per se .. it is a convenience for VSC
  MErrno changeOwnerAndOrGroup(FileOrDirOwner newOwnerGrp);

  // Change owner and group of a file/dir to match that of a template 
  // source file/dir
  MErrno changeFileOrDirOwnership(FileOrDirOwner src, 
                                  FileOrDirOwner tgt, std::string *gpfsMsg);

  // Change ACLs of a file/dir to match that of a template source file/dir
  MErrno changeFileOrDirACL(FileOrDirOwner src, 
                            FileOrDirOwner tgt, int aclType, 
                            std::string *gpfsMsg);
  /* DJ_MODS_END */

#ifdef MMANTRAS_QUOTAS
  MErrno getUsers(char *fsName, char *fsNameMntPt, 
                  char *csName, std::vector<User *> *userList);
    
  MErrno getGroups(char *fsName, char *fsNameMntPt, 
                   char *csName, std::vector<Group *> *groupList);
#endif

  MErrno getHomePath(char *user, char *path);
  MErrno getPrimaryId(char *user, UInt32 *pid);

  /* MODS_END */


  /* Get the SDRFS gen number from the local node */
  UInt32 getSdrfsGenNumber();
  UInt32 getSdrfsGenNumberFromRecipe();
  MErrno updateSdrfsGenNumber(UInt32 sdrGen);

  /* Called by a main thread. Wake up timer thread. */
  void wakeupTimerThread();

  /* Called by a timer thread. Wait a main thread to wake it up. */
  void waitMainThread();

  /* Called by a timer thread. Wake up command thread which
      executes several command scripts. */
  void wakeupCmdThread();

  /* Called by a command thread. When command thread starts,
      it waits timer thread to wake it up. */
  void waitTimerThread();

  /* Called by a command thread. When command thread finishes,
      wake up any waiter thread. */
  void notifyCmdThreadDone();

  /* Called by external tasks. Wait until the command thread finishes
      its work. */
  void waitCmdThreadDone();

  /* Called by a main thread. When an execution task is being added,
      it is called to wake up dispatch thread. */
  void wakeupDispatchThread();

  /* Called by a dispatch thread. Wait any execution task to be
     arrived. */
  void waitExecutionTask();

  /* Add asynchronous execution task. */
  MErrno addExecutionTask(const char *cmd, char *argP, int (*callbackFn)(void *),
                          void *callbackData);

  /* Extract an execution task from list. */
  MErrno getExecTaskFromList(ExecutionTask *taskP);

  /* Initialize buffer. */
  MErrno initBuf(char *buf);

  /* Get GPFS daemon state. */
  MErrno getDaemonState(); 
  
  /* MODS_START */
  char *getTimeStampInMilliseconds(char *timeStamp, char *cdateP);

  std::string buffer2string(char * buffer, int itemsToCopy);
  std::vector<std::string> tokenHelper(char *buf, int expectedTokens );

  void getPollingLock();
  void releasePollingLock();
  /* MODS_END */
  
};

extern PollingHandler *thePollingHandler;

void ts_log(int level, const char *component, const char* fmtString, ...);
long file_size(char * fname);
void log_update();

#endif /* _h_api_poll */
