// begin_generated_IBM_copyright_prolog
//
// This is an automatically generated copyright prolog.
// After initializing,  DO NOT MODIFY OR MOVE
// ================================================================
//
// (C) Copyright IBM Corp.  2011     
// Eclipse Public License (EPL)
//
// ================================================================
//
// end_generated_IBM_copyright_prolog
#include "GPFSEvent.h"

EventsHandler* GPFSEvent::handle = NULL;

GPFSEvent::GPFSEvent(int evttype, int loggingtype, bool isRef)
{
    type    = evttype;
    proc    = GPFSEventProcessorFactory::getEventProcessor(loggingtype,isRef);
    evt     = NULL;
}

GPFSEventProcessor* GPFSEvent::getProc()
{
    return proc;
}

Event* GPFSEvent::getEvent()
{
    return evt;
}

GPFSEvent::~GPFSEvent()
{
    if(proc)
        delete proc;
}
void GPFSEvent::setHandler(EventsHandler* handler)
{
    handle = handler;
}
int GPFSEvent::sendTrap(Event* event, void* data)
{
    GPFSEvent* gevent = (GPFSEvent*) data;
    gevent->evt = event;
    gevent->proc->action(gevent);
    return (int)TL_SUCCESS;
    
}
int GPFSEvent::getType()
{
    return type;
}

void GPFSEvent::registerSelf()
{
    if(handle)
        handle->registerEventCallback(type,sendTrap,this);
}


