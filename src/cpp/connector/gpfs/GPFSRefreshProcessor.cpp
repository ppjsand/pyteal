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
#include "GPFSRefreshProcessor.h"
#include <iostream>
#include "Log.h"
#include "GPFSConfigHandler.h"
#include "teal_connect_api.h"
#include "GPFSEventHandler.h"
#include "configuration.h"
#include "teal_gpfs_connect.h"
#include "utils.h"
GPFSRefreshProcessor::GPFSRefreshProcessor(GPFSEventProcessor* evtProc)
{
    _eventProc = evtProc;
}

GPFSRefreshProcessor::~GPFSRefreshProcessor()
{

}

TLGPFS_ERR_T GPFSRefreshProcessor::action(GPFSEvent* evt)
{    
    string name = GPFSEventHandler::getEventName(evt->getType());
    string msg = "It's event: ";
    msg += name.c_str();
    msg += " that requesting refresh configuration!";
    log_debug(msg);
    if(!Configuration::getInstance().isPoll())
    {
        log_warn("Polling not enabled, can't refresh configuration, skipping....");
    }
    else if(!GPFSConfigHandler::getConfigHandler()->getThread()->sendSignal())
    {
            log_error("send signal to polling thread failed!");
            return TL_ERR_REFRESH_FAILED;
    }
    if(_eventProc)
        return _eventProc->action(evt);
    return TL_SUCCESS;
}
