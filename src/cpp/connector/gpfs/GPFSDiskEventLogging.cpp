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
#include "GPFSDiskEventLogging.h"
#include "Log.h"
#include "GPFSEventHandler.h"
#include "GPFSConfigHandler.h"
#include "teal_connect_api.h"
#include "configuration.h"
#include "teal_gpfs_connect.h"
#include "utils.h"

GPFSDiskEventLogging::GPFSDiskEventLogging()
{

}

GPFSDiskEventLogging::~GPFSDiskEventLogging()
{

}

TLGPFS_ERR_T GPFSDiskEventLogging::action(GPFSEvent* evt)
{
    int type = evt->getType();
    string eventName = GPFSEventHandler::getEventName(type);
    if(eventName == string(""))
    {
        log_error("Not supported disk event!");
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
    
    
    tlgpfs_disk_event_t *gpfsDiskEvent = new tlgpfs_disk_event_t();
    
    teal_cbe_t *cbe         = new teal_cbe_t();    
    char time[30]           = {0};
    char pidC[10]           = {0};
    unsigned int pid        = (unsigned int)getpid();  
    
    struct timeval creation_time = evt->getEvent()->getCreationTime();
    Utils::get_time_stamp(&creation_time,time);
    
    cbe->time_occurred      = time;
    cbe->src_comp           = "GPFS";
    cbe->src_loc_type       = "G";
    cbe->rpt_comp           = "TEAL";
    cbe->rpt_loc_type       = "A";    

    srcloc                 += ":"; //srcloc == clustername:
    rptloc                 += "##"; //rptloc == nodename##
    rptloc                 += GPFSEventHandler::getEventHandler()->getProcName(); //rptloc == nodename##tlgpfsmon
    rptloc                 += "##";// rptloc == nodename##tlgpfsmon##
    rptloc                 += Utils::int_to_char(pidC,10,&pid);// rptloc == nodename##tlgpfsmon##pid
    cbe->rpt_loc            = (char*)rptloc.c_str();

    gpfsDiskEvent->severity = evt->getEvent()->getSeverity();

    int  ioLength;
    long ioTime;
    unsigned long long startSector;
    unsigned int dataLen;
    unsigned int errCntClient;
    unsigned int errCntServ;
    unsigned int errCntNsd;
    unsigned int rptInterval;
    
    if(type == ADDDISK)
    {
        DiskActionEvent* event         = (DiskActionEvent*)evt->getEvent();
        srcloc                        += event->getDiskName(); // srcloc == clustername:diskname
        cbe->event_id                  = "GP000003";            
        cbe->src_loc                   = (char*)srcloc.c_str();
        
        gpfsDiskEvent->fs_name         = event->getFsName();
        gpfsDiskEvent->node_name       = NULL;
        gpfsDiskEvent->node_ip         = event->getNodeIpAddr();
        gpfsDiskEvent->status          = NULL;
        gpfsDiskEvent->availability    = NULL;
        gpfsDiskEvent->fg_name         = NULL;
        gpfsDiskEvent->meta            = NULL;
        gpfsDiskEvent->data            = NULL;
        gpfsDiskEvent->cmd             = NULL;
        gpfsDiskEvent->my_role         = NULL;
        gpfsDiskEvent->ck_reason       = NULL;
        gpfsDiskEvent->other_node      = NULL;
        gpfsDiskEvent->data_len        = NULL;
        gpfsDiskEvent->err_cnt_client  = NULL;
        gpfsDiskEvent->err_cnt_serv    = NULL;
        gpfsDiskEvent->err_cnt_nsd     = NULL;
        gpfsDiskEvent->rpt_interval    = NULL;
        gpfsDiskEvent->io_length       = NULL;
        gpfsDiskEvent->io_time         = NULL;
        gpfsDiskEvent->start_sector    = NULL;
    }    
    else if(type == DELDISK)
    {
        DiskActionEvent* event        = (DiskActionEvent*)evt->getEvent();
        srcloc                       += event->getDiskName(); // srcloc == clustername:diskname
        cbe->event_id                 = "GP000004";            
        cbe->src_loc                  = (char*)srcloc.c_str();
      
        gpfsDiskEvent->fs_name        = event->getFsName();
        gpfsDiskEvent->node_name      = NULL;
        gpfsDiskEvent->node_ip        = event->getNodeIpAddr();
        gpfsDiskEvent->status         = NULL;
        gpfsDiskEvent->availability   = NULL;
        gpfsDiskEvent->fg_name        = NULL;
        gpfsDiskEvent->meta           = NULL;
        gpfsDiskEvent->data           = NULL;
        gpfsDiskEvent->cmd            = NULL;
        gpfsDiskEvent->my_role        = NULL;
        gpfsDiskEvent->ck_reason      = NULL;
        gpfsDiskEvent->other_node     = NULL;
        gpfsDiskEvent->data_len       = NULL;
        gpfsDiskEvent->err_cnt_client = NULL;
        gpfsDiskEvent->err_cnt_serv   = NULL;
        gpfsDiskEvent->err_cnt_nsd    = NULL;
        gpfsDiskEvent->rpt_interval   = NULL;
        gpfsDiskEvent->io_length      = NULL;
        gpfsDiskEvent->io_time        = NULL;
        gpfsDiskEvent->start_sector   = NULL;
    }
    else if(type == CHDISK)
    {
        ChdiskEvent* event            = (ChdiskEvent*)evt->getEvent();
        srcloc                       += event->getDiskName(); // srcloc == clustername:diskname
        cbe->event_id                 = "GP000005";            
        cbe->src_loc                  = (char*)srcloc.c_str();
      
        gpfsDiskEvent->fs_name        = event->getFsName();
        gpfsDiskEvent->node_name      = NULL;
        gpfsDiskEvent->node_ip        = event->getNodeIpAddr();
        gpfsDiskEvent->status         = event->getStatus();
        gpfsDiskEvent->availability   = event->getAvailability();
        gpfsDiskEvent->fg_name        = event->getFgName();
        gpfsDiskEvent->meta           = event->getMeta();
        gpfsDiskEvent->data           = event->getData();
        gpfsDiskEvent->cmd            = NULL;
        gpfsDiskEvent->my_role        = NULL;
        gpfsDiskEvent->ck_reason      = NULL;
        gpfsDiskEvent->other_node     = NULL;
        gpfsDiskEvent->data_len       = NULL;
        gpfsDiskEvent->err_cnt_client = NULL;
        gpfsDiskEvent->err_cnt_serv   = NULL;
        gpfsDiskEvent->err_cnt_nsd    = NULL;
        gpfsDiskEvent->rpt_interval   = NULL;
        gpfsDiskEvent->io_length      = NULL;
        gpfsDiskEvent->io_time        = NULL;
        gpfsDiskEvent->start_sector   = NULL;

    }
    else if(type == LONG_IOTIME)
    {
        LongIoTimeEvent* event        = (LongIoTimeEvent*)evt->getEvent();
        srcloc                       += event->getDiskName(); // srcloc == clustername:diskname
        cbe->event_id                 = "GP000015";            
        cbe->src_loc                  = (char*)srcloc.c_str();
      
        gpfsDiskEvent->fs_name        = event->getFsName();
        gpfsDiskEvent->node_name      = event->getNodeName();
        gpfsDiskEvent->node_ip        = NULL;
        gpfsDiskEvent->status         = NULL;
        gpfsDiskEvent->availability   = NULL;
        gpfsDiskEvent->fg_name        = NULL;
        gpfsDiskEvent->meta           = NULL;
        gpfsDiskEvent->data           = NULL;
        gpfsDiskEvent->cmd            = event->getCmd();
        gpfsDiskEvent->my_role        = NULL;
        gpfsDiskEvent->ck_reason      = NULL;
        gpfsDiskEvent->other_node     = NULL;
        gpfsDiskEvent->data_len       = NULL;
        gpfsDiskEvent->err_cnt_client = NULL;
        gpfsDiskEvent->err_cnt_serv   = NULL;
        gpfsDiskEvent->err_cnt_nsd    = NULL;
        gpfsDiskEvent->rpt_interval   = NULL;
        ioLength                      = event->getIoLength();
        gpfsDiskEvent->io_length      = &ioLength;
        ioTime                        = event->getIoTime();
        gpfsDiskEvent->io_time        = &ioTime;
        gpfsDiskEvent->start_sector   = NULL;

    }
    else if(type == NSD_CKSUM_MISMATCH)
    {
        NsdCksumMismatchEvent* event   = (NsdCksumMismatchEvent*)evt->getEvent();
        srcloc                        += event->getCkNSD(); // srcloc == clustername:diskname
        cbe->event_id                  = "GP000025";            
        cbe->src_loc                   = (char*)srcloc.c_str();
      
        gpfsDiskEvent->fs_name         = NULL;
        gpfsDiskEvent->node_name       = event->getNodeName();
        gpfsDiskEvent->node_ip         = NULL;
        gpfsDiskEvent->status          = NULL;
        gpfsDiskEvent->availability    = NULL;
        gpfsDiskEvent->fg_name         = NULL;
        gpfsDiskEvent->meta            = NULL;
        gpfsDiskEvent->data            = NULL;
        gpfsDiskEvent->cmd             = NULL;
        gpfsDiskEvent->my_role         = event->getMyRole();
        gpfsDiskEvent->ck_reason       = event->getCkReason();
        gpfsDiskEvent->other_node      = event->getCkOtherNode();
        dataLen                        = event->getCkDataLen();
        gpfsDiskEvent->data_len        = &dataLen;
        errCntClient                   = event->getCkErrorCountClient();
        gpfsDiskEvent->err_cnt_client  = &errCntClient;
        errCntServ                     = event->getCkErrorCountServer();
        gpfsDiskEvent->err_cnt_serv    = &errCntServ;
        errCntNsd                      = event->getCkErrorCountNSD();
        gpfsDiskEvent->err_cnt_nsd     = &errCntNsd;
        rptInterval                    = event->getCkReportingInterval();
        gpfsDiskEvent->rpt_interval    = &rptInterval;

        gpfsDiskEvent->io_length       = NULL;
        gpfsDiskEvent->io_time         = NULL;
        startSector                    = event->getCkStartSector();
        gpfsDiskEvent->start_sector    = &startSector;
    }
    else
    {
        log_error("Unrecognized event!");
        return TL_ERR_EVENT_NOT_SUPPORT;
    }

    TLGPFS_ERR_T ret = TL_SUCCESS;
    teal_connector_handle conn_handle = NULL;
    ret = (TLGPFS_ERR_T)teal_open_connector(&conn_handle,"GPFS","/tmp");
    if(ret != TEAL_SUCCESS)
    {
        char rc[10];
        string msg = "open gpfs connector failed with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        return ret;
    }
    ret = (TLGPFS_ERR_T)tlgpfs_write_disk_event(conn_handle,cbe,gpfsDiskEvent);
    if(ret != TL_SUCCESS)
    {
        char rc[10];
        string msg = "Write disk event failed with ";
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
    delete gpfsDiskEvent;

    return ret;
}

