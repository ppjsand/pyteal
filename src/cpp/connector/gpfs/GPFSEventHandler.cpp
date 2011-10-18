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
#include "GPFSEventHandler.h"
#include "GPFSEventFactory.h"
#include "configuration.h"
#include <fstream>
#include <string.h>
#include "Log.h"
#include "utils.h"
#include "commandlistener.h"

GPFSEventHandler* GPFSEventHandler::instance  = NULL;
map<int,int>* GPFSEventHandler::behaviors = NULL;
map<int,string>* GPFSEventHandler::events     = NULL;

GPFSEventHandler::GPFSEventHandler()
{
}

int GPFSEventHandler::getLogType(int type)
{
    if(type == 22
    || type == 23
    || type == 24
    || type == 25
    || type == 26
    || type == 27
    || type == 28
    || type == 29
    || type == 30)
        return LOGGINGPS;
    else if(type == 2
         || type == 3
         || type == 4
         || type == 17
         || type == 18
         || type == 20)
        return LOGGINGDISK;
    else if(type == 0
         || type == 1
         || type == 5
         || type == 8
         || type == 9
         || type == 10
         || type == 13
         || type == 15)
        return LOGGINGFS;
    else if(type == 6
         || type == 7
         || type == 11
         || type == 12
         || type == 14
         || type == 16
         || type == 19)
        return LOGGINGMISC;
    else 
        return (int)TL_ERR_EVENT_NOT_SUPPORT;
}

TEAL_ERR_T GPFSEventHandler::initBehaviorMap(const std::string& name, const std::string& behavior)
{
    string msg;
    if(!events)
    {
        msg = "events mapping are not initiated...";
        log_error(msg);
        return TEAL_ERR_ARG;
    }
    if(!behaviors)
        behaviors = new map<int,int>();
    
    int evttype = getEventType(name);
    if(evttype < 0)
    {
        msg = "Don't support such event: ";
        msg += name.c_str();
        return TEAL_ERR_ARG;
    }
    if(!strcmp(behavior.c_str(),"refreshonly"))
    {
        behaviors->insert(pair<int, int>(evttype,REFRESHONLY));
        return TEAL_SUCCESS;
    }
    else if(!strcmp(behavior.c_str(),"ignore"))
    {
        behaviors->insert(pair<int, int>(evttype,IGNORE));
        return TEAL_SUCCESS; 
    }
    else if(!strcmp(behavior.c_str(),"logrefresh"))
    {
        int logtype = getLogType(evttype);
        if(logtype < 0)
            return (TEAL_ERR_T)logtype;
        behaviors->insert(pair<int, int>(evttype,logtype+REFRESHONLY));
        return TEAL_SUCCESS;            
    }
    else if(!strcmp(behavior.c_str(),"logonly"))
    {
        int logtype = getLogType(evttype);
        if(logtype < 0)
            return (TEAL_ERR_T)logtype;
        behaviors->insert(pair<int, int>(evttype,logtype));
        return TEAL_SUCCESS;            
    }
    msg = "Unrecognized behahvior: ";
    msg += behavior.c_str();
    msg += ", supported behaviors are refreshonly/logonly/logrefresh/ignore, please double check...";
    return TEAL_ERR_ARG;

}
TEAL_ERR_T GPFSEventHandler::processGPFSConfFile(const std::string& path)
{

    fstream confFile;
    string msg;
    confFile.open(path.c_str());
    if(!confFile) 
    {
        msg = "Unable to open configuration file: ";
        msg = msg + path;
        log_error(msg.c_str());
        cerr<<msg<<endl;
        return TEAL_ERR_SYS_FILE;
    }

    // Read in the line.
    string strToParse;
    msg = "Start reading configure file: ";
    msg += path.c_str();
    log_info(msg);
    while(getline(confFile,strToParse))
    {
        if(strToParse[0] != '#' && !strToParse.empty()) 
        {
            //  format: "name=<eventname>;behavior=<refreshonly/logonly/logrefresh/ignore>;"
            string::size_type idx1,idx2;
            idx1 = strToParse.find("name=");
            idx1 = idx1 + strlen("name=");
            idx2 = strToParse.find(';',idx1);
            string eventName = strToParse.substr(idx1,idx2-idx1);
            idx1 = strToParse.find("behavior=");
            idx1 = idx1 + strlen("behavior=");
            idx2 = strToParse.find(';',idx1);
            string behavior = strToParse.substr(idx1,idx2-idx1);
            if(initBehaviorMap(eventName,behavior) != TEAL_SUCCESS)
                continue;

            string behaveString = "event: "+eventName+", behavior: " + behavior;
            log_debug(behaveString.c_str());
        } 
        else 
        {
            continue;
        }
    }
    confFile.close();
    return TEAL_SUCCESS;
}

GPFSEventHandler* GPFSEventHandler::getEventHandler()
{
    if(instance == NULL)
    {
        GPFSHandler::init(MGMT_SNMP,1,Configuration::getInstance().getInterval());
        
        initEventMap();
        TEAL_ERR_T ret = TEAL_SUCCESS;
        if((ret = processGPFSConfFile(Configuration::getInstance().getConfPath())) != TEAL_SUCCESS)
        {
            unlink(PID_FILE);
            unlink(GPFS_SOCK_FILE);
            exit(ret);
        }
        instance = new GPFSEventHandler();
    }
    return instance;
}

string GPFSEventHandler::getEventName(int type)
{
    string msg;
    if(!events)
    {
        msg = "events mapping are not initiated...";
        log_error(msg);
        return string("");
    }
    map<int, string>::iterator itr;
    for(itr = events->begin(); itr != events->end(); itr++)
    {
        if(itr->first == type)
        {           
            return itr->second;
        }
    }
    char strtype[10];
    msg = "Can't find event name for type: ";
    msg += Utils::int_to_char(strtype,10,(unsigned int*)&type);
    log_error(msg);
    return string("");
    
}

int GPFSEventHandler::getEventType(string name)
{
    string msg;
    if(!events)
    {
        msg = "events mapping are not initiated...";
        log_error(msg);
        return (int)TL_ERR_EVENT_NOT_SUPPORT;
    }
    map<int, string>::iterator itr;
    for(itr = events->begin(); itr != events->end(); itr++)
    {
        if(itr->second == name)
        {           
            return itr->first;
        }
    }
    msg = "Can't find event type for event: ";
    msg += name.c_str();
    log_error(msg);
    return (int)TL_ERR_EVENT_NOT_SUPPORT;
    
}

int GPFSEventHandler::getEventBehavior(int type)
{
    string msg;
    if(!behaviors)
    {
        msg = "events behavior mapping are not initiated...";
        log_error(msg);
        return (int)TL_ERR_EVENT_NOT_SUPPORT;
    }
    map<int, int>::iterator itr;
    for(itr = behaviors->begin(); itr != behaviors->end(); itr++)
    {
        if(itr->first == type)
        {           
            return itr->second;
        }
    }
    char strtype[10];
    msg = "Can't find behavior for event type: ";
    msg += Utils::int_to_char(strtype,10,(unsigned int*)&type);
    log_error(msg);

    return (int)TL_ERR_EVENT_NOT_SUPPORT;
    
}

GPFSEventHandler::~GPFSEventHandler()
{
    if(behaviors)
        delete behaviors;
    if(events)
        delete events;
}

void GPFSEventHandler::initEventMap()
{
    if(!events)
        events = new map<int,string>();
    else
        events->clear();

    events->insert(pair<int, string>(0,"MOUNT")); 
    events->insert(pair<int, string>(1,"UNMOUNT")); 
    events->insert(pair<int, string>(2,"ADDDISK")); 
    events->insert(pair<int, string>(3,"DELDISK")); 
    events->insert(pair<int, string>(4,"CHDISK"));  
    events->insert(pair<int, string>(5,"SGMGR_TAKEOVER")); 
    events->insert(pair<int, string>(6,"NODE_FAILURE")); 
    events->insert(pair<int, string>(7,"NODE_RECOVERY")); 
    events->insert(pair<int, string>(8,"FILESYSTEM_CREATION")); 
    events->insert(pair<int, string>(9,"FILESYSTEM_DELETION")); 
    events->insert(pair<int, string>(10,"FILESYSTEM_STATE_CHANGE")); 
    //events->insert(pair<int, string>(11,"NEW_CONNECTION")); 
    events->insert(pair<int, string>(12,"EVENT_COLLECTION_BUFFER_OVERFLOW")); 
    //events->insert(pair<int, string>(13,"TOKEN_MANAGER_STATUS")); 
    events->insert(pair<int, string>(14,"HUNG_THREAD")); 
    events->insert(pair<int, string>(15,"STGPOOL_UTILIZATION")); 
    events->insert(pair<int, string>(16,"SDR_CHANGED")); 
    //events->insert(pair<int, string>(17,"MMADDDISK")); 
    //events->insert(pair<int, string>(18,"MMDELDISK")); 
    events->insert(pair<int, string>(19,"CONSOLE_LOG")); 
    events->insert(pair<int, string>(20,"LONG_IOTIME")); 
    //events->insert(pair<int, string>(21,"USER_EVENT")); 
    events->insert(pair<int, string>(22,"RECOVERYGROUP_TAKEOVER")); 
    events->insert(pair<int, string>(23,"RECOVERYGROUP_RELINQUISH")); 
    events->insert(pair<int, string>(24,"RECOVERYGROUP_OPEN_FAILED")); 
    events->insert(pair<int, string>(25,"RECOVERYGROUP_PANIC")); 
    events->insert(pair<int, string>(26,"PDISK_FAILED")); 
    events->insert(pair<int, string>(27,"PDISK_RECOVERED")); 
    events->insert(pair<int, string>(28,"PDISK_REPLACE_PDISK")); 
    events->insert(pair<int, string>(29,"PDISK_PATH_FAILED"));
    events->insert(pair<int, string>(30,"DA_REBUILD_FAILED"));
    events->insert(pair<int, string>(31,"NSD_CKSUM_MISMATCH"));

}

void GPFSEventHandler::registerEvent()
{
    map<int, int>::iterator itr;
    GPFSEvent* event = NULL;
    string msg;
    char type[10];
    GPFSEvent::setHandler(GPFSHandler::getEventHandler());
    for(itr = behaviors->begin(); itr != behaviors->end(); itr++)
    {
        int logtype = itr->second;
        bool isRef = false;
        if(logtype > 9) // logtype > 10, refersh
        {
            isRef = true;
            logtype = logtype - 10;
        }
        event = GPFSEventFactory::getEvent(itr->first, isRef, logtype);
        if(event) //only listen to supported events
        {
            msg = "Register event type: ";
            msg += Utils::int_to_char(type,10,(unsigned int*)&itr->first);
            log_debug(msg);
            if(isRef)
            {
                msg = "Need refresh configuration.";
                log_debug(msg);
            }
            else
            {            
                msg = "No need to refresh configuration.";
                log_debug(msg);
            }
            event->registerSelf();
        }
    }
}

void GPFSEventHandler::action(GPFSHandler* handler)
{
    registerEvent();
    
    GPFSHandler::getEventHandler()->run();
}

