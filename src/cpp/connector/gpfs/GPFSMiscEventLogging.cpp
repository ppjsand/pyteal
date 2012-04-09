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
#include "GPFSMiscEventLogging.h"
#include "Log.h"
#include "GPFSEventHandler.h"
#include "GPFSConfigHandler.h"
#include "configuration.h"
#include "teal_connect_api.h"
#include "teal_gpfs_connect.h"
#include "utils.h"

GPFSMiscEventLogging::GPFSMiscEventLogging()
{

}

GPFSMiscEventLogging::~GPFSMiscEventLogging()
{

}

TLGPFS_ERR_T GPFSMiscEventLogging::action(GPFSEvent* evt)
{
    int type = evt->getType();
    string eventName = GPFSEventHandler::getEventName(type);
    if(eventName == string(""))
    {
        log_error("Not supported misc event!");
        return TL_ERR_EVENT_NOT_SUPPORT;
    }
    string msg = "Event: ";
    msg += eventName.c_str();
    msg += " received!";
    log_info(msg);
    int behavior = GPFSEventHandler::getEventBehavior(type);
    if(behavior > 9)
    {
        log_debug("Need to refresh configuration!");
        behavior -= 10;
    }
    if(behavior > 1)
        log_debug("Need to log this event!");
    
    std::string srcloc("C:"); //srcloc  == C:
    srcloc += GPFSEventHandler::getEventHandler()->getCluster(); //srcloc  == C:clustername 
    std::string rptloc(GPFSEventHandler::getEventHandler()->getHostName());  //rptloc == nodename
    struct timeval creation_time = evt->getEvent()->getCreationTime();
    
    tlgpfs_misc_event_t *gpfsMiscEvent = new tlgpfs_misc_event_t();
    
    teal_cbe_t *cbe            = new teal_cbe_t();    
    char time[30]              = {0};
    char node[MAX_EVENT_FIELD] = {0}; // the size complies with the size defined in api_event.h
    char pidC[10]              = {0};
    unsigned int pid           = (unsigned int)getpid();    

    Utils::get_time_stamp(&creation_time,time);
    cbe->time_occurred         = time;
    cbe->src_comp              = "GPFS";
    cbe->src_loc_type          = "G";
    cbe->rpt_comp              = "TEAL";
    cbe->rpt_loc_type          = "A";    

    srcloc                    += "|N:"; //srcloc == C:clustername|N:
    rptloc                    += "##"; //rptloc == nodename##
    rptloc                    += GPFSEventHandler::getEventHandler()->getProcName(); //rptloc == nodename##tlgpfsmon
    rptloc                    += "##";// rptloc == nodename##tlgpfsmon##
    rptloc                    += Utils::int_to_char(pidC,10,&pid);// rptloc == nodename##tlgpfsmon##pid
    cbe->rpt_loc               = (char*)rptloc.c_str();

    gpfsMiscEvent->severity    = evt->getEvent()->getSeverity();
    long waitTime;
    int  msgLevel;
    if(type == NODE_FAILURE )
    {
        NodeStatusEvent* event       = (NodeStatusEvent*)evt->getEvent();    
        cbe->event_id                = "GP000007";        
        srcloc                      += Utils::get_hostname_by_ip(node, MAX_EVENT_FIELD, event->getNodeIpAddr()); //srcloc == C:clustername|N:nodename
        cbe->src_loc                 = (char*)srcloc.c_str();
        gpfsMiscEvent->msg_text      = NULL;
        gpfsMiscEvent->diagnosis     = NULL;
        gpfsMiscEvent->wait_time     = NULL;
        gpfsMiscEvent->msg_level     = NULL;
    }    
    else if(type == NODE_RECOVERY )
    {
        NodeStatusEvent* event       = (NodeStatusEvent*)evt->getEvent();    
        cbe->event_id                = "GP000008";
        srcloc                      += Utils::get_hostname_by_ip(node, MAX_EVENT_FIELD, event->getNodeIpAddr()); //srcloc == C:clustername|N:nodename
        cbe->src_loc                 = (char*)srcloc.c_str();
        gpfsMiscEvent->msg_text      = NULL;
        gpfsMiscEvent->diagnosis     = NULL;
        gpfsMiscEvent->wait_time     = NULL;
        gpfsMiscEvent->msg_level     = NULL;
    }    
    else if(type == EVENT_COLLECTION_BUFFER_OVERFLOW )
    {
        NodeStatusEvent* event       = (NodeStatusEvent*)evt->getEvent();    
        cbe->event_id                = "GP00000D";        
        srcloc                      += Utils::get_hostname_by_ip(node, MAX_EVENT_FIELD, event->getNodeIpAddr()); //srcloc == C:clustername|N:nodename
        cbe->src_loc                 = (char*)srcloc.c_str();
        gpfsMiscEvent->msg_text      = NULL;
        gpfsMiscEvent->diagnosis     = NULL;
        gpfsMiscEvent->wait_time     = NULL;
        gpfsMiscEvent->msg_level     = NULL;
    }
    else if(type == HUNG_THREAD )
    {
        HungThreadEvent* event       = (HungThreadEvent*)evt->getEvent();    
        cbe->event_id                = "GP00000F";        
        srcloc                      += Utils::get_hostname_by_ip(node, MAX_EVENT_FIELD, event->getNodeIpAddr()); //srcloc == C:clustername|N:nodename
        cbe->src_loc                 = (char*)srcloc.c_str();
        gpfsMiscEvent->msg_text      = NULL;
        gpfsMiscEvent->diagnosis     = event->getDiagnosis();
        waitTime                     = event->getWaitTime();
        gpfsMiscEvent->wait_time     = &waitTime;
        gpfsMiscEvent->msg_level     = NULL;
    }
    else if(type == CONSOLE_LOG )
    {
        ConsoleLogEvent* event       = (ConsoleLogEvent*)evt->getEvent();    
        cbe->event_id                = "GP000014";        
        srcloc                      += event->getNodeName(); //srcloc == C:clustername|N:nodename
        cbe->src_loc                 = (char*)srcloc.c_str();
        gpfsMiscEvent->msg_text      = event->getMsgTxt();
        gpfsMiscEvent->diagnosis     = NULL;
        gpfsMiscEvent->wait_time     = NULL;
        msgLevel                     = event->getMsgLevel();
        gpfsMiscEvent->msg_level     = &msgLevel;
    }
    else
    {
        log_error("Unrecognized event!");
        return TL_ERR_EVENT_NOT_SUPPORT;
    }

    TLGPFS_ERR_T ret = TL_SUCCESS;
    teal_connector_handle conn_handle = NULL;
    ret = (TLGPFS_ERR_T)teal_open_connector(&conn_handle,"GPFS","/tmp");
    if(ret != TL_SUCCESS)
    {
        char rc[10];
        msg = "open gpfs connector failed with   ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        return ret;
    }
    ret = (TLGPFS_ERR_T)tlgpfs_write_misc_event(conn_handle,cbe,gpfsMiscEvent);
    if(ret != TL_SUCCESS)
    {
        char rc[10];
        msg = "Write misc event failed with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);     
    }
    ret = (TLGPFS_ERR_T)teal_close_connector(conn_handle);
    if(ret != TL_SUCCESS)
    {
        char rc[10];
        msg = "close gpfs connector error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
    }
    delete cbe;
    delete gpfsMiscEvent;

    return ret;

}

