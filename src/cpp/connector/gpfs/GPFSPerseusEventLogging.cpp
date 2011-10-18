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
#include "GPFSPerseusEventLogging.h"
#include "Log.h"
#include "GPFSEventHandler.h"
#include "GPFSConfigHandler.h"
#include "configuration.h"
#include "utils.h"
#include "teal_connect_api.h"
#include "teal_gpfs_connect.h"

GPFSPerseusEventLogging::GPFSPerseusEventLogging()
{

}

GPFSPerseusEventLogging::~GPFSPerseusEventLogging()
{

}

TLGPFS_ERR_T GPFSPerseusEventLogging::action(GPFSEvent* evt)
{
    int type = evt->getType();
    string eventName = GPFSEventHandler::getEventName(type);
    if(eventName == string(""))
    {
        log_error("Not supported perseus event!");
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

    std::string srcloc(GPFSEventHandler::getEventHandler()->getCluster()); //srcloc  == clustername 
    std::string rptloc(GPFSEventHandler::getEventHandler()->getHostName());  //rptloc == nodename
    struct timeval creation_time = evt->getEvent()->getCreationTime();
    
    tlgpfs_perseus_event_t *gpfsPerseusEvent = new tlgpfs_perseus_event_t();
    
    teal_cbe_t *cbe           = new teal_cbe_t();    
    char time[30]             = {0};
    char pidC[10]             = {0};
    unsigned int pid          = (unsigned int)getpid();    

    Utils::get_time_stamp(&creation_time,time);
    cbe->time_occurred        = time;
    cbe->src_comp             = "GPFS";
    cbe->src_loc_type         = "G";
    cbe->rpt_comp             = "TEAL";
    cbe->rpt_loc_type         = "A";    

    srcloc                   += ":"; //srcloc == clustername:
    rptloc                   += "##"; //rptloc == nodename##
    rptloc                   += GPFSEventHandler::getEventHandler()->getProcName(); //rptloc == nodename##tlgpfsmon
    rptloc                   += "##";// rptloc == nodename##tlgpfsmon##
    rptloc                   += Utils::int_to_char(pidC,10,&pid);// rptloc == nodename##tlgpfsmon##pid
    cbe->rpt_loc              = (char*)rptloc.c_str();

    gpfsPerseusEvent->severity = evt->getEvent()->getSeverity();
    int priority;    
    int remainingRedundancy;
    int error;
    if(type == RECOVERYGROUP_TAKEOVER)
    {
        RgTakeoverEvent* event       = (RgTakeoverEvent*)evt->getEvent();    
        cbe->event_id                = "GP000016";        
        srcloc                      += event->getRgName();  //srcloc == clustername:rgname
        cbe->src_loc                 = (char*)srcloc.c_str();
        gpfsPerseusEvent->node_name  = event->getNodeName();
        gpfsPerseusEvent->location   = NULL;
        gpfsPerseusEvent->fru        = NULL;
        gpfsPerseusEvent->wwn        = NULL;
        gpfsPerseusEvent->state      = NULL;
        gpfsPerseusEvent->priority   = NULL;
        error                        = event->getErr();
        gpfsPerseusEvent->rem_redund = NULL;
        gpfsPerseusEvent->err        = &error;
        gpfsPerseusEvent->dev_name   = NULL;
        gpfsPerseusEvent->reason     = event->getReason();

    }
    else if(type == RECOVERYGROUP_RELINQUISH)
    {
        RgRelinquishEvent* event     = (RgRelinquishEvent*)evt->getEvent();    
        cbe->event_id                = "GP000017";        
        srcloc                      += event->getRgName();  //srcloc == clustername:rgname
        cbe->src_loc                 = (char*)srcloc.c_str();
        gpfsPerseusEvent->node_name  = event->getNodeName();
        gpfsPerseusEvent->location   = NULL;
        gpfsPerseusEvent->fru        = NULL;
        gpfsPerseusEvent->wwn        = NULL;
        gpfsPerseusEvent->state      = NULL;
        gpfsPerseusEvent->priority   = NULL;
        error                        = event->getErr();
        gpfsPerseusEvent->rem_redund = NULL;
        gpfsPerseusEvent->err        = &error;
        gpfsPerseusEvent->dev_name   = NULL;
        gpfsPerseusEvent->reason     = event->getReason();

    }
    else if(type == RECOVERYGROUP_OPEN_FAILED)
    {
        RgOpenFailedEvent* event     = (RgOpenFailedEvent*)evt->getEvent();    
        cbe->event_id                = "GP000018";        
        srcloc                      += event->getRgName();  //srcloc == clustername:rgname
        cbe->src_loc                 = (char*)srcloc.c_str();
        gpfsPerseusEvent->node_name  = event->getNodeName();
        gpfsPerseusEvent->location   = NULL;
        gpfsPerseusEvent->fru        = NULL;
        gpfsPerseusEvent->wwn        = NULL;
        gpfsPerseusEvent->state      = NULL;
        gpfsPerseusEvent->priority   = NULL;
        error                        = event->getErr();
        gpfsPerseusEvent->rem_redund = NULL;
        gpfsPerseusEvent->err        = &error;
        gpfsPerseusEvent->dev_name   = NULL;
        gpfsPerseusEvent->reason     = event->getReason();
    }
    else if(type == RECOVERYGROUP_PANIC)
    {
        RgPanicEvent* event          = (RgPanicEvent*)evt->getEvent();    
        cbe->event_id                = "GP000019";        
        srcloc                      += event->getRgName();  //srcloc == clustername:rgname
        cbe->src_loc                 = (char*)srcloc.c_str();
        gpfsPerseusEvent->node_name  = event->getNodeName();
        gpfsPerseusEvent->location   = NULL;
        gpfsPerseusEvent->fru        = NULL;
        gpfsPerseusEvent->wwn        = NULL;
        gpfsPerseusEvent->state      = NULL;
        gpfsPerseusEvent->priority   = NULL;
        error                        = event->getErr();
        gpfsPerseusEvent->rem_redund = NULL;
        gpfsPerseusEvent->err        = &error;
        gpfsPerseusEvent->dev_name   = NULL;
        gpfsPerseusEvent->reason     = event->getReason();

    }
    else if(type == PDISK_FAILED)
    {
        PdFailedEvent* event         = (PdFailedEvent*)evt->getEvent();    
        cbe->event_id                = "GP000020";
        srcloc                      += event->getRgName();  //srcloc == clustername:rgname
        srcloc                      += ":";  //srcloc == clustername:rgname:
        srcloc                      += event->getDaName();  //srcloc == clustername:rgname:daname
        srcloc                      += ":";  //srcloc == clustername:rgname:daname:
        srcloc                      += event->getPdName();  //srcloc == clustername:rgname:daname:pdiskname
        cbe->src_loc                 = (char*)srcloc.c_str();
        gpfsPerseusEvent->node_name  = event->getNodeName();
        gpfsPerseusEvent->location   = event->getLocation();
        gpfsPerseusEvent->fru        = event->getFru();
        gpfsPerseusEvent->wwn        = event->getWwn();
        gpfsPerseusEvent->state      = event->getState();
        gpfsPerseusEvent->reason     = NULL;
        gpfsPerseusEvent->dev_name   = NULL;
        gpfsPerseusEvent->priority   = NULL;
        gpfsPerseusEvent->rem_redund = NULL;
        gpfsPerseusEvent->err        = NULL;
    }
    else if(type == PDISK_RECOVERED)
    {
        PdRecoveredEvent* event      = (PdRecoveredEvent*)evt->getEvent();    
        cbe->event_id                = "GP000021";        
        srcloc                      += event->getRgName();  //srcloc == clustername:rgname
        srcloc                      += ":";  //srcloc == clustername:rgname:
        srcloc                      += event->getDaName();  //srcloc == clustername:rgname:daname
        srcloc                      += ":";  //srcloc == clustername:rgname:daname:
        srcloc                      += event->getPdName();  //srcloc == clustername:rgname:daname:pdiskname
        cbe->src_loc                 = (char*)srcloc.c_str();
        gpfsPerseusEvent->node_name  = event->getNodeName();
        gpfsPerseusEvent->location   = event->getLocation();
        gpfsPerseusEvent->fru        = event->getFru();
        gpfsPerseusEvent->wwn        = event->getWwn();
        gpfsPerseusEvent->state      = NULL;
        gpfsPerseusEvent->reason     = NULL;
        gpfsPerseusEvent->dev_name   = NULL;
        gpfsPerseusEvent->priority   = NULL;
        gpfsPerseusEvent->rem_redund = NULL;
        gpfsPerseusEvent->err        = NULL;

    }
    else if(type == PDISK_REPLACE_PDISK)
    {
        PdReplacePdiskEvent* event   = (PdReplacePdiskEvent*)evt->getEvent();    
        cbe->event_id                = "GP000022";        
        srcloc                      += event->getRgName();  //srcloc == clustername:rgname
        srcloc                      += ":";  //srcloc == clustername:rgname:
        srcloc                      += event->getDaName();  //srcloc == clustername:rgname:daname
        srcloc                      += ":";  //srcloc == clustername:rgname:daname:
        srcloc                      += event->getPdName();  //srcloc == clustername:rgname:daname:pdiskname
        cbe->src_loc                 = (char*)srcloc.c_str();
        gpfsPerseusEvent->node_name  = event->getNodeName();
        gpfsPerseusEvent->location   = event->getLocation();
        gpfsPerseusEvent->fru        = event->getFru();
        gpfsPerseusEvent->wwn        = event->getWwn();
        gpfsPerseusEvent->state      = event->getState();
        priority                     = event->getPriority();
        gpfsPerseusEvent->priority   = &priority;
        gpfsPerseusEvent->rem_redund = NULL;
        gpfsPerseusEvent->err        = NULL;
        gpfsPerseusEvent->dev_name   = NULL;
        gpfsPerseusEvent->reason     = NULL;
    }
    else if(type == PDISK_PATH_FAILED)
    {
        PdPathFailedEvent* event     = (PdPathFailedEvent*)evt->getEvent();    
        cbe->event_id                = "GP000023";        
        srcloc                      += event->getRgName();  //srcloc == clustername:rgname
        srcloc                      += ":";  //srcloc == clustername:rgname:
        srcloc                      += event->getDaName();  //srcloc == clustername:rgname:daname
        srcloc                      += ":";  //srcloc == clustername:rgname:daname:
        srcloc                      += event->getPdName();  //srcloc == clustername:rgname:daname:pdiskname
        cbe->src_loc                 = (char*)srcloc.c_str();
        gpfsPerseusEvent->node_name  = event->getNodeName();
        gpfsPerseusEvent->location   = event->getLocation();
        gpfsPerseusEvent->fru        = event->getFru();
        gpfsPerseusEvent->wwn        = event->getWwn();
        gpfsPerseusEvent->state      = NULL;
        gpfsPerseusEvent->priority   = NULL;
        gpfsPerseusEvent->rem_redund = NULL;
        gpfsPerseusEvent->err        = NULL;
        gpfsPerseusEvent->dev_name   = event->getDeviceName();
        gpfsPerseusEvent->reason     = NULL;
    }
    else if(type == DA_REBUILD_FAILED)
    {
        DaRebuildFailedEvent* event  = (DaRebuildFailedEvent*)evt->getEvent();    
        cbe->event_id                = "GP000024";        
        srcloc                      += event->getRgName();  //srcloc == clustername:rgname
        srcloc                      += ":";  //srcloc == clustername:rgname:
        srcloc                      += event->getDaName();  //srcloc == clustername:rgname:daname
        cbe->src_loc                 = (char*)srcloc.c_str();
        gpfsPerseusEvent->node_name  = event->getNodeName();
        gpfsPerseusEvent->location   = NULL;
        gpfsPerseusEvent->fru        = NULL;
        gpfsPerseusEvent->wwn        = NULL;
        gpfsPerseusEvent->state      = NULL;
        gpfsPerseusEvent->priority   = NULL;
        remainingRedundancy          = event->getRemainingRedundancy();
        gpfsPerseusEvent->rem_redund = &remainingRedundancy;
        gpfsPerseusEvent->err        = NULL;
        gpfsPerseusEvent->dev_name   = NULL;
        gpfsPerseusEvent->reason     = NULL;
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
        string msg = "open gpfs connector failed with  ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        return ret;
    }
    ret = (TLGPFS_ERR_T)tlgpfs_write_perseus_event(conn_handle,cbe,gpfsPerseusEvent);
    if(ret != TL_SUCCESS)
    {
        char rc[10];
        string msg = "write gpfs perseus event failed with  ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);      
    }
    ret = (TLGPFS_ERR_T)teal_close_connector(conn_handle);
    if(ret != TL_SUCCESS)
    {
        char rc[10];
        string msg = "close gpfs connector failed with  ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
    }

    delete cbe;
    delete gpfsPerseusEvent;

    return ret;
}

