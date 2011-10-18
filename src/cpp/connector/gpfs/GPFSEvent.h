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
#ifndef _GPFSEVENT_H
#define _GPFSEVENT_H
#include "tlgpfs_error.h"
#include "api_poll.h"
#include "api_event.h"
#include "GPFSEventProcessorFactory.h"

using namespace std;
class GPFSEventProcessor;
class GPFSEvent
{
public:
    GPFSEvent(int evttype, int loggingtype, bool isRef);
    virtual ~GPFSEvent();
    void registerSelf();
    static void setHandler(EventsHandler* handler);
    int getType();
    Event* getEvent();
    GPFSEventProcessor* getProc();
    
private:
    static int sendTrap(Event* event, void* data);
    static EventsHandler* handle;
    int type;
    string name;
    Event* evt;
    GPFSEventProcessor* proc;
};
#endif
