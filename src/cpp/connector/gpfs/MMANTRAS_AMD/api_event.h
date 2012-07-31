/* @(#)46       1.19  src/avs/fs/mmfs/ts/mmantras/api_event.h, mmfs, avs_rhrz1, rhrz1base 9/29/11 18:42:06 */

#ifndef _h_api_event
#define _h_api_event



#include <stdio.h>
#include <errno.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/time.h>

/* Define event types */
enum
{
  /* Internal events */
  MOUNT = 0,
  UNMOUNT = 1,
  ADDDISK = 2,
  DELDISK = 3,
  CHDISK = 4,
  SGMGR_TAKEOVER = 5,
  NODE_FAILURE = 6,
  NODE_RECOVERY = 7,
  FILESYSTEM_CREATION = 8,
  FILESYSTEM_DELETION = 9,
  FILESYSTEM_STATE_CHANGE = 10,
  NEW_CONNECTION = 11,
  EVENT_COLLECTION_BUFFER_OVERFLOW = 12,
  TOKEN_MANAGER_STATUS = 13,
  HUNG_THREAD = 14,
  STGPOOL_UTILIZATION = 15,
  SDR_CHANGED = 16,
  /* Command events */
  MMADDDISK = 17,
  MMDELDISK = 18,
  /* Console log events */
  CONSOLE_LOG  = 19,
  /* Long ioTime warning */
  LONG_IOTIME = 20,

  /* User generated event */
  USER_EVENT = 21,

  /* NSD RAID related events */
  RECOVERYGROUP_TAKEOVER = 22,         /* RG server takeover */
  RECOVERYGROUP_RELINQUISH = 23,       /* RG server relinquish */
  RECOVERYGROUP_OPEN_FAILED = 24,      /* RG open failed */
  RECOVERYGROUP_PANIC = 25,            /* RG panic resign */
  PDISK_FAILED = 26,                   /* pdisk declared dead */
  PDISK_RECOVERED = 27,                /* pdisk recovered */
  PDISK_REPLACE_PDISK = 28,            /* pdisk disk replacement */
  PDISK_PATH_FAILED = 29,              /* pdisk path failed */
  DA_REBUILD_FAILED = 30,              /* DA rebuild failed */
  NSD_CKSUM_MISMATCH = 31,             /* checksum error on an NSD RPC */

  /* last event: MAX_EVENT_CLASSES */
  MAX_EVENT_CLASSES = 32
};

#define MAX_EVENT_FIELD           256 // string lengh

struct EventNameTableEntry
{
  const char *name;
  int len;
};


/* Define event names */
const struct EventNameTableEntry EventNamesP[MAX_EVENT_CLASSES + 1] =
{
  /*  0 */   { "mount",          5 },
  /*  1 */   { "unmount",        7 },
  /*  2 */   { "adddisk",        7 },
  /*  3 */   { "deldisk",        7 },
  /*  4 */   { "chdisk",         6 },
  /*  5 */   { "takeover",       8 },
  /*  6 */   { "failure",        7 },
  /*  7 */   { "recovery",       8 },
  /*  8 */   { "createfs",       8 },
  /*  9 */   { "deletefs",       8 },
  /*  10 */  { "fsstatechange",  13 },
  /*  11 */  { "newconnection",  13 },
  /*  12 */  { "exception",      9 },
  /*  13 */  { "sgStats",        7 },
  /*  14 */  { "hungthread",     10 },
  /*  15 */  { "poolutil",       8 },
  /*  16 */  { "sdrChanged",     10 },
  /*  17 */  { "mmadddisk",      9 },
  /*  18 */  { "mmdeldisk",      9 },
  /*  19 */  { "consoleLog",     10 },
  /*  20 */  { "longIO",         6 },
  /*  21 */  { "userEvent",      9 },
  /*  22 */  { "rgTakeover",     10 },
  /*  23 */  { "rgRelinquish",   12 },
  /*  24 */  { "rgOpenFailed",   12 },
  /*  25 */  { "rgPanic",        7 },
  /*  26 */  { "pdFailed",       8 },
  /*  27 */  { "pdRecovered",    11 },
  /*  28 */  { "pdReplacePdisk", 14 },
  /*  29 */  { "pdPathFailed",   12 },
  /*  30 */  { "daRebuildFailed",15 },
  /*  31 */  { "nsdCksumMismatch",16 },
             { 0, 0 }
};


#if 0
/* Data for callback for response from each node. */
typedef struct MyData
{
  char *responseBuffer;
  int   responseBufferSize;
  char *asyncEvents;
  int   asyncEventsSize;
  Mmpmon_Callback_String callback;
  FILE       *file;
  const char *command;
} MyData;
#endif


/* Super class of all events classes. */
class Event
{
  friend class EventsHandler;

  struct timeval creationTime;
  char severity[MAX_EVENT_FIELD];

public:
  Event();
  ~Event();

  inline struct timeval getCreationTime() { return creationTime; }
  inline char *getSeverity() { return severity; }
};


/* Mount, unmount events */
class MountActionEvent : public Event
{
private:
  char  nodeIpAddr[MAX_EVENT_FIELD];
  char  fsName[MAX_EVENT_FIELD];

public:
  MountActionEvent(char *nodeIpAddr, char *fsName);
  ~MountActionEvent();

  inline char *getNodeIpAddr() { return nodeIpAddr; }
  inline char *getFsName() { return fsName; }
};


/* Adddisk, deldisk events */
class DiskActionEvent : public Event
{
private:
  char  nodeIpAddr[MAX_EVENT_FIELD];
  char  fsName[MAX_EVENT_FIELD];
  char  diskName[MAX_EVENT_FIELD];

public:
  DiskActionEvent(char *nodeIpAddr, char *fsName, char *diskName);
  ~DiskActionEvent();

  inline char *getNodeIpAddr() { return nodeIpAddr; }
  inline char *getFsName() { return fsName; }
  inline char *getDiskName() { return diskName; }
};


/* Chdisk event */
class ChdiskEvent : public Event
{
private:
  char  nodeIpAddr[MAX_EVENT_FIELD];
  char  fsName[MAX_EVENT_FIELD];
  char  diskName[MAX_EVENT_FIELD];
  char  status[MAX_EVENT_FIELD];
  char  availability[MAX_EVENT_FIELD];
  char  fgName[MAX_EVENT_FIELD];
  char  meta[MAX_EVENT_FIELD];
  char  data[MAX_EVENT_FIELD];

public:
  ChdiskEvent(char *nodeIpAddr, char *fsName, char *diskName,
              char *status, char *availability, char *fgName,
              char *meta, char *data);
  ~ChdiskEvent();

  inline char *getNodeIpAddr() { return nodeIpAddr; }
  inline char *getFsName() { return fsName; }
  inline char *getDiskName() { return diskName; }
  inline char *getStatus() { return status; }
  inline char *getAvailability() { return availability; }
  inline char *getFgName() { return fgName; }
  inline char *getMeta() { return meta; }
  inline char *getData() { return data; }
};


/* Stripe group manager takeover event */
class SgmgrTakeoverEvent : public Event
{
private:
  char sgmgrIpAddr[MAX_EVENT_FIELD];
  char prevSgmgrIpAddr[MAX_EVENT_FIELD];
  char fsName[MAX_EVENT_FIELD];

public:
  SgmgrTakeoverEvent(char *sgmgrIpAddr, char *prevSgmgrIpAddr, char *fsName);
  ~SgmgrTakeoverEvent();

  inline char *getSgmgrIpAddr() { return sgmgrIpAddr; }
  inline char *getPrevSgmgrIpAddr() { return prevSgmgrIpAddr; }
  inline char *getFsName() { return fsName; }
};


/* Node failure, recovery events */
class NodeStatusEvent : public Event
{
private:
  char nodeIpAddr[MAX_EVENT_FIELD];

public:
  NodeStatusEvent(char *nodeIpAddr);
  ~NodeStatusEvent();

  inline char *getNodeIpAddr() { return nodeIpAddr; }
};


/* File system creation, deletion events */
class FilesystemActionEvent : public Event
{
private:
  char sgmgrIpAddr[MAX_EVENT_FIELD];
  char fsName[MAX_EVENT_FIELD];

public:
  FilesystemActionEvent(char *sgmgrIpAddr, char *fsName);
  ~FilesystemActionEvent();

  inline char *getSgmgrIpAddr() { return sgmgrIpAddr; }
  inline char *getFsName() { return fsName; }
};


/* File system state change event */
class FilesystemStateChangeEvent : public Event
{
private:
  char fsName[MAX_EVENT_FIELD];
  char userUnbalanced[MAX_EVENT_FIELD];
  char metaUnbalanced[MAX_EVENT_FIELD];
  char userIllreplicated[MAX_EVENT_FIELD];
  char metaIllreplicated[MAX_EVENT_FIELD];
  char userExposed[MAX_EVENT_FIELD];
  char metaExposed[MAX_EVENT_FIELD];

public:
  FilesystemStateChangeEvent(char *fsName, char *userUnbalanced, 
                             char *metaUnbalanced, char *userIllreplicated, 
                             char *metaIllreplicated, char *userExposed, 
                             char *metaExposed);
  ~FilesystemStateChangeEvent();

  inline char *getFsName() { return fsName; }
  inline char *getUserUnbalanced() { return userUnbalanced; }
  inline char *getMetaUnbalanced() { return metaUnbalanced; }
  inline char *getUserIllreplicated() { return userIllreplicated; }
  inline char *getMetaIllreplicated() { return metaIllreplicated; }
  inline char *getUserExposed() { return userExposed; }
  inline char *getMetaExposed() { return metaExposed; }
};


/* Hung thread event */
class HungThreadEvent : public Event
{
private:
  char nodeIpAddr[MAX_EVENT_FIELD];
  time_t waitTime;
  char diagnosis[MAX_EVENT_FIELD];

public:
  HungThreadEvent(char *nodeAddr, time_t time, char *desc);
  ~HungThreadEvent();

  inline char *getNodeIpAddr() { return nodeIpAddr; }
  inline time_t getWaitTime() { return waitTime; }
  inline char *getDiagnosis() { return diagnosis; }
};


/* tm stats event */
class TmStatsEvent: public Event
{
private:
  char nodeIpAddr[MAX_EVENT_FIELD];
  char fsName[MAX_EVENT_FIELD];
  int  tmSpace;
  int  tmRequest;

public:
  TmStatsEvent(char *nodeAddr, char *fsName, int tmSpace, int tmRequest); 
  ~TmStatsEvent();

  inline char *getNodeIpAddr() { return nodeIpAddr; }
  inline char *getFsName() { return fsName; }
  inline int   getTmSpace() { return tmSpace; }
  inline int   getTmRequest() { return tmRequest; }
};

#if 0
/* File system utilization event */
class FilesystemUtilizationEvent : public Event
{
private:
  char fsName[MAX_EVENT_FIELD];
  int fsUsage;

public:
  FilesystemUtilizationEvent(char *name, int usage);
  ~FilesystemUtilizationEvent();

  inline char *getFsName() { return fsName; }
  inline int getFsUsage() { return fsUsage; }
};
#endif


/* Storage pool utilization event */
class StgPoolUtilizationEvent : public Event
{
private:
  char fsName[MAX_EVENT_FIELD];
  char poolName[MAX_EVENT_FIELD];
  char status[MAX_EVENT_FIELD];
  int poolUsage;

public:
  StgPoolUtilizationEvent(char *fsname, char *poolname, char *status, 
                          int usage);
  ~StgPoolUtilizationEvent();

  inline char *getFsName() { return fsName; }
  inline char *getPoolName() { return poolName; }
  inline char *getStatus() { return status; }
  inline int getPoolUsage() { return poolUsage; }
};

class SDRChangedEvent : public Event
{
  private:
  char nodeName[MAX_EVENT_FIELD];

public:
  SDRChangedEvent(char *nodeName);
  ~SDRChangedEvent();

  inline char *getNodeName() { return nodeName; }
};

class UserGeneratedEvent : public Event
{
  private:
  char nodeName[MAX_EVENT_FIELD];
  char data[MAX_EVENT_FIELD];

public:
  UserGeneratedEvent(char *nodeName, char *data);
  ~UserGeneratedEvent();

  inline char *getNodeName() { return nodeName; }
  inline char *getData() { return data; }
};

/* Adddisk, deldisk command events */
class DiskCmdEvent : public Event
{
private:
  char nodeName[MAX_EVENT_FIELD];
  char fsName[MAX_EVENT_FIELD];
  char diskName[MAX_EVENT_FIELD];
  char cmd[MAX_EVENT_FIELD];
  char status[MAX_EVENT_FIELD];
  int result;

public:
  DiskCmdEvent(char *nodeName, char *fsName, char *diskName, char *cmd,
               char *status, int result);
  ~DiskCmdEvent();

  inline char *getNodeName() { return nodeName; }
  inline char *getFsName() { return fsName; }
  inline char *getDiskName() { return diskName; }
  inline char *getCmd() { return cmd; }
  inline char *getStatus() { return status; }
  inline int getResult() { return result; }
};


/* Console message events */
class ConsoleLogEvent : public Event
{
private:
  char nodeName[MAX_EVENT_FIELD];
  char msgTxt[MAX_EVENT_FIELD];
  int  msgLevel;

public:
  ConsoleLogEvent(char *nodeName, char *msgTxt, int msgLevel);
  ~ConsoleLogEvent() {};

  inline char *getNodeName() { return nodeName; }
  inline char *getMsgTxt() { return msgTxt; }
  inline int getMsgLevel() { return msgLevel; }
};


/* Long ioTime warning events */
class LongIoTimeEvent : public Event
{
private:
  char nodeName[MAX_EVENT_FIELD];
  char fsName[MAX_EVENT_FIELD];
  char diskName[MAX_EVENT_FIELD];
  char cmd[MAX_EVENT_FIELD];
  int    ioLength;  
  time_t ioTime; /* in microseconds */


public:
  LongIoTimeEvent(char *nodeName, char *fsName, char *diskName,  char *cmd, 
                  int ioLength, time_t ioTime_us);
  ~LongIoTimeEvent() {};

  inline char *getNodeName() { return nodeName; }
  inline char *getFsName() { return fsName; }
  inline char *getDiskName() { return diskName; }
  inline char *getCmd() { return cmd; }
  inline int   getIoLength() { return ioLength; }
  inline time_t getIoTime() { return ioTime; }

};

/* NSD RAID related events */

/* Recovery Group Takeveover:
     RG server has begun serving an RG 
*/
class RgTakeoverEvent : public Event
{
private:
  char nodeName[MAX_EVENT_FIELD];
  char rgName[MAX_EVENT_FIELD];
  char reason[MAX_EVENT_FIELD];
  int  err;

public:
  RgTakeoverEvent(char *nodeName, char *rgName, char *reason, int err);
  ~RgTakeoverEvent() {};

  inline char *getNodeName() { return nodeName; }
  inline char *getRgName()   { return rgName; }
  inline char *getReason()   { return reason; }
  inline int   getErr()      { return err; }

};

/* Recovery Group Relinquish 
     RG server has stopped serving an RG
 */
class RgRelinquishEvent: public Event
{  
private:
  char nodeName[MAX_EVENT_FIELD];
  char rgName[MAX_EVENT_FIELD];
  char reason[MAX_EVENT_FIELD];
  int  err;

public:
  RgRelinquishEvent(char *nodeName, char *rgName, char *reason, int err);
  ~RgRelinquishEvent() {};

  inline char *getNodeName() { return nodeName; }
  inline char *getRgName()   { return rgName; }
  inline char *getReason()   { return reason; }
  inline int   getErr()      { return err; }
};

/* Recovery Group OpenFailed 
   rgOpenFailed event will always be followed by rgTakeover with an error 
   code (and the same reason string.)
 */
class RgOpenFailedEvent: public Event
{  
private:
  char nodeName[MAX_EVENT_FIELD];
  char rgName[MAX_EVENT_FIELD];
  char reason[MAX_EVENT_FIELD];
  int  err;

public:
  RgOpenFailedEvent(char *nodeName, char *rgName, char *reason, int err);
  ~RgOpenFailedEvent() {};

  inline char *getNodeName() { return nodeName; }
  inline char *getRgName()   { return rgName; }
  inline char *getReason()   { return reason; }
  inline int   getErr()      { return err; }
};

/* Recovery Group Panic 
   rgPanic
 */

class RgPanicEvent: public Event
{  
private:
  char nodeName[MAX_EVENT_FIELD];
  char rgName[MAX_EVENT_FIELD];
  char reason[MAX_EVENT_FIELD];
  int  err;

public:
  RgPanicEvent(char *nodeName, char *rgName, char *reason, int err);
  ~RgPanicEvent() {};

  inline char *getNodeName() { return nodeName; }
  inline char *getRgName()   { return rgName; }
  inline char *getReason()   { return reason; }
  inline int   getErr()      { return err; }
};

/* disk array requires disk replacement */
class PdReplacePdiskEvent : public Event
{
private:
  char nodeName[MAX_EVENT_FIELD];
  char location[MAX_EVENT_FIELD];
  char fru[MAX_EVENT_FIELD];
  char wwn[MAX_EVENT_FIELD];  /* SCSI World Wide Name */ 
  char rgName[MAX_EVENT_FIELD];
  char daName[MAX_EVENT_FIELD];
  char pdName[MAX_EVENT_FIELD];
  char state[MAX_EVENT_FIELD];
  int  priority;

public:
  PdReplacePdiskEvent(char *nodeName, char *location, char *fru,
                            char *wwn, char *rgName, char *daName,
                            char *pdName, char *state, int priority);
  ~PdReplacePdiskEvent() {};

  inline char *getNodeName() { return nodeName; }
  inline char *getLocation()  { return location; }
  inline char *getFru()       { return fru; }
  inline char *getWwn()       { return wwn; }
  inline char *getRgName()    { return rgName; }
  inline char *getDaName()    { return daName; }
  inline char *getPdName()    { return pdName; }
  inline char *getState()     { return state; }
  inline int   getPriority()  { return priority; }
};

/* 
 * a pDisk has failed 
 */
class PdFailedEvent : public Event
{
private:
  char nodeName[MAX_EVENT_FIELD];
  char location[MAX_EVENT_FIELD];
  char fru[MAX_EVENT_FIELD];
  char wwn[MAX_EVENT_FIELD];  /* SCSI World Wide Name */ 
  char rgName[MAX_EVENT_FIELD];
  char daName[MAX_EVENT_FIELD];
  char pdName[MAX_EVENT_FIELD];
  char state[MAX_EVENT_FIELD];

public:
  PdFailedEvent(char *nodeName, char *location, char *fru, char *wwn, 
                char *rgName, char *daName, char *pdName, char *state);
  ~PdFailedEvent() {};

  inline char *getNodeName() { return nodeName; }
  inline char *getLocation()  { return location; }
  inline char *getFru()       { return fru; }
  inline char *getWwn()       { return wwn; }
  inline char *getRgName()    { return rgName; }
  inline char *getDaName()    { return daName; }
  inline char *getPdName()    { return pdName; }
  inline char *getState()     { return state; }
};

/* 
 * a pDisk has recovered 
 */
class PdRecoveredEvent : public Event
{
private:
  char nodeName[MAX_EVENT_FIELD];
  char location[MAX_EVENT_FIELD];
  char fru[MAX_EVENT_FIELD];
  char wwn[MAX_EVENT_FIELD];  /* SCSI World Wide Name */
  char rgName[MAX_EVENT_FIELD];
  char daName[MAX_EVENT_FIELD];
  char pdName[MAX_EVENT_FIELD];

public:
  PdRecoveredEvent(char *nodeName, char *location, char *fru, char *wwn, 
                   char *rgName, char *daName, char *pdName);
  ~PdRecoveredEvent() {};

  inline char *getNodeName() { return nodeName; }
  inline char *getLocation()  { return location; }
  inline char *getFru()       { return fru; }
  inline char *getWwn()       { return wwn; }
  inline char *getRgName()    { return rgName; }
  inline char *getDaName()    { return daName; }
  inline char *getPdName()    { return pdName; }
};

/* 
 * pdPathFailed
 */
class PdPathFailedEvent : public Event
{
private:
  char nodeName[MAX_EVENT_FIELD];
  char location[MAX_EVENT_FIELD];
  char fru[MAX_EVENT_FIELD];
  char wwn[MAX_EVENT_FIELD];  /* SCSI World Wide Name */
  char rgName[MAX_EVENT_FIELD];
  char daName[MAX_EVENT_FIELD];
  char pdName[MAX_EVENT_FIELD];
  char deviceName[MAX_EVENT_FIELD];

public:
  PdPathFailedEvent(char *nodeName, char *location, char *fru, char *wwn, 
                    char *rgName, char *daName, char *pdName, 
                    char *deviceName);
  ~PdPathFailedEvent() {};

  inline char *getNodeName() { return nodeName; }
  inline char *getLocation()  { return location; }
  inline char *getFru()       { return fru; }
  inline char *getWwn()       { return wwn; }
  inline char *getRgName()    { return rgName; }
  inline char *getDaName()    { return daName; }
  inline char *getPdName()    { return pdName; }
  inline char *getDeviceName(){ return deviceName; }
};


/* 
 * daRebuildFailed: Decluster Array rebuild failed
 */
class DaRebuildFailedEvent : public Event
{
private:
  char nodeName[MAX_EVENT_FIELD];
  char rgName[MAX_EVENT_FIELD];
  char daName[MAX_EVENT_FIELD];
  int  remainingRedundancy;

public:
  DaRebuildFailedEvent(char *nodeName, char *rgName, char *daName, 
                       int remainingRedundancy);
  ~DaRebuildFailedEvent() {};

  inline char *getNodeName() { return nodeName; }
  inline char *getRgName()    { return rgName; }
  inline char *getDaName()    { return daName; }
  inline int   getRemainingRedundancy()    { return remainingRedundancy; }
};

/* 
 * nsdCksumMismatch: checksum error detected on an NSD RPC transaction
 */

class NsdCksumMismatchEvent : public Event
{
private:
  char nodeName[MAX_EVENT_FIELD]; /* reporting node */
  char myRole[MAX_EVENT_FIELD];   /* reporting side of the event:
                                     "client" or "server" */
  char ckOtherNode[MAX_EVENT_FIELD]; /* address of the other side involved */
  char ckNSD[MAX_EVENT_FIELD];    /* NSD name of the NSD/Vdisk in question */
  char ckReason[MAX_EVENT_FIELD]; /* reason for checksum error:
                           "server_detected_error_receiving_for_write" or
                           "client_detected_error_receiving_on_read" */
  Int64 ckStartSector;  /* starting sector of the failing transmission */
  Int32 ckDataLen;      /* data length of the failing transmission */
  UInt32 ckErrorCountClient; /* cumulative number of errors for the involved 
                                client since server has begun serving */
  UInt32 ckErrorCountServer; /* cumulative number of errors for the server */
  UInt32 ckErrorCountNSD;    /* cumulative number of errors for the involved 
                                NSD since server has begun serving */
  Int32 ckReportingInterval; /* value of the reporting interval at the 
                                time the event was generated */
public:
  NsdCksumMismatchEvent(char *nodeName, char *myRole, char *ckOtherNode,
                        char *ckNSD, char *ckReason, 
                        Int64 ckStartSector, Int32 ckDataLen,
                        UInt32 ckErrorCountClient, UInt32 ckErrorCountServer,
                        UInt32 ckErrorCountNSD, Int32 ckReportingInterval);
  ~NsdCksumMismatchEvent() {};

  inline char *getNodeName()    { return nodeName; }
  inline char *getMyRole()      { return myRole; }
  inline char *getCkReason()    { return ckReason; }
  inline char *getCkNSD()       { return ckNSD; }
  inline char *getCkOtherNode() { return ckOtherNode; }
  inline UInt64 getCkStartSector()      { return ckStartSector; }
  inline Int32  getCkDataLen()  { return ckDataLen; }
  inline UInt32 getCkErrorCountClient() { return ckErrorCountClient; }
  inline UInt32 getCkErrorCountServer() { return ckErrorCountServer; }
  inline UInt32 getCkErrorCountNSD()   { return ckErrorCountNSD; }
  inline Int32  getCkReportingInterval(){ return ckReportingInterval; }
};

/* 
 * Derived event classes
 */
#define MountEvent                         MountActionEvent
#define UnmountEvent                       MountActionEvent
#define AdddiskEvent                       DiskActionEvent
#define DeldiskEvent                       DiskActionEvent
#define NodeFailureEvent                   NodeStatusEvent
#define NodeRecoveryEvent                  NodeStatusEvent
#define FilesystemCreationEvent            FilesystemActionEvent
#define FilesystemDeletionEvent            FilesystemActionEvent
#define NewConnectionEvent                 NodeStatusEvent
#define EventCollectionBufferOverflowEvent NodeStatusEvent
#define MmAdddiskEvent                     DiskCmdEvent
#define MmDeldiskEvent                     DiskCmdEvent


/* Description of linked list struct for holding an event */
class EventItem
{
private:

  /* Ptr to null-terminated string associated with this object */
  char      *bufP;
  /* Ptr to prev item -or- NULL if front of list */
  EventItem *prevP;
  /* Ptr to next item -or- NULL if end of list */
  EventItem *nextP;

public:

  /* Constructor */
  EventItem();

  /* Destructor */
  ~EventItem();

  /* Access member functions */
  void copyBuf(char* _bufP);
  inline char* getBufP() const { return bufP; }
  inline EventItem* getNextP() const { return nextP; }

  /* Given a string as input, duplicate the string and
     create an associated linked list descriptor. */
  static EventItem* strdup(const char *strP);

  /* Append item(s) after this item
     which must be current end-of-list. */
  void append(EventItem* _nextP);

  /* Destroy list */
  static void destroyList(EventItem* listP);
};


typedef struct
{
  int (*fn)(Event *event, void *data);
  void *data;
} CallbackInfo;

#ifndef dfprintf
#define dfprintf if (debug) fprintf
#endif

/* It manages two threads:
   1. receiveHandler: It connects to GPFS daemon and listens to events
    genereated in GPFS. When an event occurs, it stores this event to list.
   2. sendHandler: It extracts an event one by one and invokes callback
    function registered with each event type. */
class EventsHandler
{
private:

  pthread_t sendThread;
  pthread_t receiveThread;

  EventItem listAnchor;     // nextP points to first in list; prevP always NULL
  EventItem* lastInListP;   // ptr to last EventItem in list

  CallbackInfo eventCallback[MAX_EVENT_CLASSES];
  MmpmonWrapperUtils *wrapper;

  int debug;
  PollingHandler *pollingHandler;  // notify polling handler of certain events

  int terminate;

  /* It sleeps until somebody wakes it up. If it is woken up, it checks if there
     are events in list. If there are, it extracts an event one by one,
     find out event type and invokes callback function of each event. */
  static void *sendHandlerBody(void *arg);

  /* It connects to GPFS daemon and listens to events generated in GPFS. If an
     event occurs, it stores this event to list and wakes up sendHandler thread. */
  static void *receiveHandlerBody(void *arg);

  /* Extract an event from list */
  char *getEventFromList(char* bufP, const int bufSize);

  /* Wake up sendHandler thread */
  void wakeSendThread();

  /* Wait receiveHandler thread */
  void waitReceiveThread();

  /* Get event type */
  int getEventType(char* response);

  /* Create event object of corresponding type */
  Event *createEventObject(int type, char *response);

public:

  static MErrno init(PollingHandler *pollH, int debg=0);

  static void term();

  EventsHandler(MErrno *errP, int debg=0);

  ~EventsHandler();

  /* Append an event to list */
  void appendEventToList(EventItem* firstItemP,  // first item in list to append
                         EventItem* lastItemP,   // last item in list to append
                         int numItems,           // number items being appended
                         int numBytes);          // total bytes being appended

  /* Create threads and wait until they finish */
  void run();

  /* refresh event registration */
  void refreshEvents();

  /* External management application registers its callback function by invoking
     this function. */
  void registerEventCallback(int type, int (*callback)(Event *event, void *data), void *callbackData);

  MmpmonWrapperUtils *getMmpmonWrapper() { return wrapper; }
};


/* Pointer to EventsHandler object */
extern EventsHandler *theEventsHandler;


/* Callback function which is invoked when we get events. It creates EventItem
   object and make it be added to list. */
static int receiveEvent(char *buf, void *data);


#endif /* _h_api_event */
