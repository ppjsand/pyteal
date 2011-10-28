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
#include "GPFSHandler.h"
#include "configuration.h"
#include <unistd.h>
#include <string.h>
PollingHandler* GPFSHandler::pollinghandler = NULL;
EventsHandler* GPFSHandler::eventhandler = NULL;
int GPFSHandler::debug = 1;
MgmtProtocol GPFSHandler::prot = MGMT_SNMP;
int GPFSHandler::interv = 86400;
std::string GPFSHandler::cluster;
std::string GPFSHandler::procname;
std::string GPFSHandler::hostname;

GPFSHandler::GPFSHandler()
{
    thr = NULL;
}

PollingHandler* GPFSHandler::getPollHandler()
{
    return pollinghandler;
}
EventsHandler* GPFSHandler::getEventHandler()
{
    return eventhandler;
}

Thread* GPFSHandler::getThread()
{
    return thr;
}

std::string& GPFSHandler::getHostName()
{
    return hostname;
}

std::string& GPFSHandler::getProcName()
{
    return procname;
}

std::string& GPFSHandler::getCluster()
{
    return cluster;
}

bool GPFSHandler::setBasicInfo()
{
// do an initial polling here to get some cluster info
    if(pollinghandler == NULL)
        return false;
    pollinghandler->refreshClusterRecipe();
    MErrno err = M_OK;
    ClusterInfo* clusterInfo = new ClusterInfo(&err);
    pollinghandler->updateClusterInfo(clusterInfo);
    char cname[30] = {0};
    strcpy(cname,clusterInfo->getName());
    cluster = cname;
    delete clusterInfo;
    procname = DAEMON_NAME;
    char hname[50] = {0};
    if(gethostname(hname,50) < 0)
        return false;
    hostname = hname;
    return true;

}


TLGPFS_ERR_T GPFSHandler::init(MgmtProtocol protocol, int verbosedebug, int interval)
{
    prot = protocol;
    debug = verbosedebug;
    interv = interval;
    if(pollinghandler == NULL)
    {
        if(PollingHandler::init(prot, debug))
            return TL_ERR_POLL_INIT_FAILED;
        pollinghandler = thePollingHandler;
    }
    
    if(Configuration::getInstance().isEvent())
    {
        if(eventhandler == NULL)
        {
            if(EventsHandler::init(pollinghandler, debug))
                return TL_ERR_EVENT_INIT_FAILED;
            eventhandler = theEventsHandler;
            if(!setBasicInfo())
                return TL_ERR_EVENT_INIT_FAILED;
        }
    }
    return TL_SUCCESS;
}

TLGPFS_ERR_T GPFSHandler::start()
{
    if(thr)
        delete thr;
    thr = new Thread();
    if(!thr->start(runner,this))
        return TL_ERR_THREAD_CREATE_FAILED;
    return TL_SUCCESS;

}
int GPFSHandler::getInterv()
{
    return interv;
}

TLGPFS_ERR_T GPFSHandler::join()
{
    if(!thr->join())
        return TL_ERR_THREAD_JOIN_FAILED;
    return TL_SUCCESS;

}

void* GPFSHandler::runner(void *data)
{
    GPFSHandler* handler = (GPFSHandler*)data;
    handler->action(handler);
    return NULL;
}

GPFSHandler::~GPFSHandler()
{

    if(pollinghandler)
        pollinghandler->term();
    if(eventhandler)
        eventhandler->term();
    if(thr)
        delete thr;
}


