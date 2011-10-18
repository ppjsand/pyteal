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
#include "GPFSEventProcessorFactory.h"
#include "GPFSRefreshProcessor.h"
#include "GPFSFsEventLogging.h"
#include "GPFSMiscEventLogging.h"
#include "GPFSPerseusEventLogging.h"
#include "GPFSDiskEventLogging.h"

#include <memory>
using namespace std;
GPFSEventProcessor* GPFSEventProcessorFactory::getEventProcessor(int type, bool isRef)
{
    auto_ptr<GPFSEventProcessor> processor;
    
    if(type == LOGGINGDISK)
        processor = auto_ptr<GPFSEventProcessor>(new GPFSDiskEventLogging());
    else if(type == LOGGINGFS)
        processor = auto_ptr<GPFSEventProcessor>(new GPFSFsEventLogging());
    else if(type == LOGGINGPS)
        processor = auto_ptr<GPFSEventProcessor>(new GPFSPerseusEventLogging());
    else if(type == LOGGINGMISC)
        processor = auto_ptr<GPFSEventProcessor>(new GPFSMiscEventLogging());
    else if(type == REFRESHONLY)
        processor = auto_ptr<GPFSEventProcessor>(NULL);
    else
        return NULL; //not recognised
    if( isRef )
        processor = auto_ptr<GPFSEventProcessor>(new GPFSRefreshProcessor(processor.release()));
    return processor.release();
}

