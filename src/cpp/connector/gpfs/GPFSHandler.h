/* begin_generated_IBM_copyright_prolog                             */
/*                                                                  */
/* This is an automatically generated copyright prolog.             */
/* After initializing,  DO NOT MODIFY OR MOVE                       */
/* ================================================================ */
/*                                                                  */
/* (C) Copyright IBM Corp.  2011                                    */
/* Eclipse Public License (EPL)                                     */
/*                                                                  */
/* ================================================================ */
/*                                                                  */
/* end_generated_IBM_copyright_prolog                               */
#ifndef _GPFS_HANDLER_H
#define _GPFS_HANDLER_H
#include "tlgpfs_error.h"
#include "api_poll.h"
#include "api_event.h"
#include "api_types.h"
#include "api_nsdRAID.h"
#include "thread.h"
#include <iostream>
class GPFSHandler
{
public:
    static TLGPFS_ERR_T init(MgmtProtocol protocol = MGMT_SNMP, int verbosedebug = 1, int interval = 86400);
    TLGPFS_ERR_T start();
    TLGPFS_ERR_T join();
    Thread* getThread();
    virtual void action(GPFSHandler* handle)=0;
    GPFSHandler();
    virtual ~GPFSHandler();    
    static PollingHandler* getPollHandler();
    static EventsHandler* getEventHandler();
    int getInterv();
    static std::string& getHostName();
    static std::string& getProcName();
    static std::string& getCluster();
private:
    static PollingHandler* pollinghandler;
    static EventsHandler* eventhandler;
    Thread* thr;
    static bool setBasicInfo();
    static void* runner(void *data);    
    static int debug;
    static MgmtProtocol prot;
    static int interv;
    static std::string cluster;//need to be used in event logging
    static std::string procname;//need to be used in event logging
    static std::string hostname;//need to be used in event logging
};

#endif

