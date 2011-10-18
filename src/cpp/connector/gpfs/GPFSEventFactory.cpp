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
#include "GPFSEventFactory.h"
#include "GPFSDiskEvent.h"
#include "GPFSMiscEvent.h"
#include "GPFSPerseusEvent.h"
#include "GPFSFsEvent.h"
#include "Logging.h"

#include <memory>

GPFSEvent* GPFSEventFactory::getEvent(int type, bool isRef, int logtype)
{
    auto_ptr<GPFSEvent> event;
    if( logtype == LOGGINGDISK )  
        event = auto_ptr<GPFSEvent>(new GPFSDiskEvent(type, LOGGINGDISK, isRef));
   
    else if( logtype == LOGGINGFS )
        event = auto_ptr<GPFSEvent>(new GPFSFsEvent(type, LOGGINGFS, isRef));   
    
    else if( logtype == LOGGINGPS )
        event = auto_ptr<GPFSEvent>(new GPFSPerseusEvent(type, LOGGINGPS, isRef));
    
    else if( logtype == LOGGINGMISC )
        event = auto_ptr<GPFSEvent>(new GPFSMiscEvent(type, LOGGINGMISC, isRef));
    
    else if( logtype == 0 )
        event = auto_ptr<GPFSEvent>(new GPFSMiscEvent(type, REFRESHONLY, isRef));
    
    else 
        return NULL; //not supported

    return event.release();
}
