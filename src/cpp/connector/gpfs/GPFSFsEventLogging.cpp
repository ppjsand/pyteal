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
#include "GPFSFsEventLogging.h"
#include "Log.h"
#include "GPFSEventHandler.h"
#include "GPFSConfigHandler.h"
#include "configuration.h"
#include "utils.h"
#include "teal_connect_api.h"
#include "teal_gpfs_connect.h"

GPFSFsEventLogging::GPFSFsEventLogging()
{

}

GPFSFsEventLogging::~GPFSFsEventLogging()
{

}

TLGPFS_ERR_T GPFSFsEventLogging::action(GPFSEvent* evt)
{
    int type = evt->getType();
    string eventName = GPFSEventHandler::getEventName(type);
    if(eventName == string(""))
    {
        log_error("Not supported fs event!");
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
    
    tlgpfs_fs_event_t *gpfsFsEvent = new tlgpfs_fs_event_t();
    
    teal_cbe_t *cbe       = new teal_cbe_t();    
    char time[30]         = {0};
    char pidC[10]         = {0};
    unsigned int pid      = (unsigned int)getpid();    

    Utils::get_time_stamp(&creation_time,time);
    cbe->time_occurred    = time;
    cbe->src_comp         = "GPFS";
    cbe->src_loc_type     = "G";
    cbe->rpt_comp         = "TEAL";
    cbe->rpt_loc_type     = "A";    

    srcloc               += "|FS:"; //srcloc  == C:clustername|FS: 
    rptloc               += "##"; //rptloc == nodename##
    rptloc               += GPFSEventHandler::getEventHandler()->getProcName(); //rptloc == nodename##tlgpfsmon
    rptloc               += "##";// rptloc == nodename##tlgpfsmon##
    rptloc               += Utils::int_to_char(pidC,10,&pid);// rptloc == nodename##tlgpfsmon##pid
    cbe->rpt_loc          = (char*)rptloc.c_str();

    gpfsFsEvent->severity = evt->getEvent()->getSeverity();
    
    int poolUsage;  
    
    if(type == MOUNT)
    {
        MountActionEvent* event        = (MountActionEvent*)evt->getEvent();    
        cbe->event_id                  = "GP000001";        
        srcloc                        += event->getFsName(); //srcloc == C:clustername|FS:fsname
        cbe->src_loc                   = (char*)srcloc.c_str();
        gpfsFsEvent->node_ip           = event->getNodeIpAddr();
        gpfsFsEvent->sgmgr_ip          = NULL;
        gpfsFsEvent->user_unbalanced   = NULL;
        gpfsFsEvent->meta_unbalanced   = NULL;
        gpfsFsEvent->user_ill_rep      = NULL;
        gpfsFsEvent->meta_ill_rep      = NULL;
        gpfsFsEvent->user_exposed      = NULL;
        gpfsFsEvent->meta_exposed      = NULL;
        gpfsFsEvent->pool_name         = NULL;
        gpfsFsEvent->pool_status       = NULL;
        gpfsFsEvent->pool_usage        = NULL;

    }
    else if(type == UNMOUNT)
    {
        MountActionEvent* event        = (MountActionEvent*)evt->getEvent();    
        cbe->event_id                  = "GP000002";        
        srcloc                        += event->getFsName(); //srcloc == C:clustername|FS:fsname
        cbe->src_loc                   = (char*)srcloc.c_str();
        gpfsFsEvent->node_ip           = event->getNodeIpAddr();
        gpfsFsEvent->sgmgr_ip          = NULL;
        gpfsFsEvent->user_unbalanced   = NULL;
        gpfsFsEvent->meta_unbalanced   = NULL;
        gpfsFsEvent->user_ill_rep      = NULL;
        gpfsFsEvent->meta_ill_rep      = NULL;
        gpfsFsEvent->user_exposed      = NULL;
        gpfsFsEvent->meta_exposed      = NULL;
        gpfsFsEvent->pool_name         = NULL;
        gpfsFsEvent->pool_status       = NULL;
        gpfsFsEvent->pool_usage        = NULL;

    }
    else if(type == SGMGR_TAKEOVER)
    {
        SgmgrTakeoverEvent* event      = (SgmgrTakeoverEvent*)evt->getEvent();    
        cbe->event_id                  = "GP000006";        
        srcloc                        += event->getFsName(); //srcloc == C:clustername|FS:fsname
        cbe->src_loc                   = (char*)srcloc.c_str();
        gpfsFsEvent->node_ip           = event->getPrevSgmgrIpAddr();
        gpfsFsEvent->sgmgr_ip          = event->getSgmgrIpAddr();
        gpfsFsEvent->user_unbalanced   = NULL;
        gpfsFsEvent->meta_unbalanced   = NULL;
        gpfsFsEvent->user_ill_rep      = NULL;
        gpfsFsEvent->meta_ill_rep      = NULL;
        gpfsFsEvent->user_exposed      = NULL;
        gpfsFsEvent->meta_exposed      = NULL;
        gpfsFsEvent->pool_name         = NULL;
        gpfsFsEvent->pool_status       = NULL;
        gpfsFsEvent->pool_usage        = NULL;

    }
    else if(type == FILESYSTEM_CREATION)
    {      
        FilesystemActionEvent* event   = (FilesystemActionEvent*)evt->getEvent();    
        cbe->event_id                  = "GP000009";
        srcloc                        += event->getFsName();  //srcloc == C:clustername|FS:fsname
        cbe->src_loc                   = (char*)srcloc.c_str();
        gpfsFsEvent->node_ip           = NULL;
        gpfsFsEvent->sgmgr_ip          = event->getSgmgrIpAddr();
        gpfsFsEvent->user_unbalanced   = NULL;
        gpfsFsEvent->meta_unbalanced   = NULL;
        gpfsFsEvent->user_ill_rep      = NULL;
        gpfsFsEvent->meta_ill_rep      = NULL;
        gpfsFsEvent->user_exposed      = NULL;
        gpfsFsEvent->meta_exposed      = NULL;
        gpfsFsEvent->pool_name         = NULL;
        gpfsFsEvent->pool_status       = NULL;
        gpfsFsEvent->pool_usage        = NULL;
    }
    else if(type == STGPOOL_UTILIZATION)
    {
        StgPoolUtilizationEvent* event = (StgPoolUtilizationEvent*)evt->getEvent();    
        cbe->event_id                  = "GP000010";        
        srcloc                        += event->getFsName(); //srcloc == C:clustername|FS:fsname
        srcloc                        += "|SP:";   //srcloc == C:clustername|FS:fsname|SP:
        srcloc                        += event->getPoolName();  //srcloc == C:clustername|FS:fsname|SP:stgpoolname
        cbe->src_loc                   = (char*)srcloc.c_str();
        gpfsFsEvent->node_ip           = NULL;
        gpfsFsEvent->sgmgr_ip          = NULL;
        gpfsFsEvent->user_unbalanced   = NULL;
        gpfsFsEvent->meta_unbalanced   = NULL;
        gpfsFsEvent->user_ill_rep      = NULL;
        gpfsFsEvent->meta_ill_rep      = NULL;
        gpfsFsEvent->user_exposed      = NULL;
        gpfsFsEvent->meta_exposed      = NULL;
        gpfsFsEvent->pool_name         = event->getPoolName();
        gpfsFsEvent->pool_status       = event->getStatus();
        poolUsage                      = event->getPoolUsage();
        gpfsFsEvent->pool_usage        = &poolUsage;

    }
    else if(type == FILESYSTEM_DELETION)
    {      
        FilesystemActionEvent* event   = (FilesystemActionEvent*)evt->getEvent();    
        cbe->event_id                  = "GP00000A";
        srcloc                        += event->getFsName();  //srcloc == C:clustername|FS:fsname
        cbe->src_loc                   = (char*)srcloc.c_str();
        gpfsFsEvent->node_ip           = NULL;
        gpfsFsEvent->sgmgr_ip          = event->getSgmgrIpAddr();
        gpfsFsEvent->user_unbalanced   = NULL;
        gpfsFsEvent->meta_unbalanced   = NULL;
        gpfsFsEvent->user_ill_rep      = NULL;
        gpfsFsEvent->meta_ill_rep      = NULL;
        gpfsFsEvent->user_exposed      = NULL;
        gpfsFsEvent->meta_exposed      = NULL;
        gpfsFsEvent->pool_name         = NULL;
        gpfsFsEvent->pool_status       = NULL;
        gpfsFsEvent->pool_usage        = NULL;
    }    
    else if(type == FILESYSTEM_STATE_CHANGE)
    {      
        FilesystemStateChangeEvent* event = (FilesystemStateChangeEvent*)evt->getEvent();    
        cbe->event_id                     = "GP00000B";
        srcloc                           += event->getFsName();  //srcloc == C:clustername|FS:fsname
        cbe->src_loc                      = (char*)srcloc.c_str();
        gpfsFsEvent->node_ip              = NULL;
        gpfsFsEvent->sgmgr_ip             = NULL;
        gpfsFsEvent->user_unbalanced      = event->getUserUnbalanced();
        gpfsFsEvent->meta_unbalanced      = event->getMetaUnbalanced();
        gpfsFsEvent->user_ill_rep         = event->getUserIllreplicated();
        gpfsFsEvent->meta_ill_rep         = event->getMetaIllreplicated();
        gpfsFsEvent->user_exposed         = event->getUserExposed();
        gpfsFsEvent->meta_exposed         = event->getMetaExposed();
        gpfsFsEvent->pool_name            = NULL;
        gpfsFsEvent->pool_status          = NULL;
        gpfsFsEvent->pool_usage           = NULL;
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
        string msg = "open gpfs connector failed with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        return ret;
    }
    ret = (TLGPFS_ERR_T)tlgpfs_write_fs_event(conn_handle,cbe,gpfsFsEvent);
    if(ret != TL_SUCCESS)
    {
        char rc[10];
        string msg = "Write file system event failed with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        return ret;
    }
    ret = (TLGPFS_ERR_T)teal_close_connector(conn_handle);
    if(ret != TL_SUCCESS)
    {
        char rc[10];
        string msg = "close gpfs connector error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        return ret;
    }
    delete cbe;
    delete gpfsFsEvent;

    return ret;
}

