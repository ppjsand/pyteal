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
#include "teal_gpfs_connect.h"
#include "DbClusterInfo.h"
#include "DbFsInfo.h"
#include "DbDiskInfo.h"
#include "DbStgPoolInfo.h"
#include "DbFsetInfo.h"
#include "DbNodeInfo.h"
#include "DbPdiskInfo.h"
#include "DbVdiskInfo.h"
#include "DbDaInfo.h"
#include "DbRgInfo.h"
#include "Log.h"
#include <time.h>
using namespace std;

#define NODE_NAME   "ERRM_NODE_NAME" //node name where sensor detects
#define EVENT_TYPE  "ERRM_TYPEID"   //0 for event, 1 for rearm event
#define LOG_DIR     "TEAL_LOG_DIR"   //use the same directory of teal_common log
#define VALUE       "ERRM_VALUE"    //contains pid info, format: [current pid cout,previous pid count,{current pid},{previous pid}]
#define COND_NAME   "ERRM_COND_NAME" //condition name triggered


int main()
{
    
    char* logPath      = getenv(LOG_DIR);
    string msg;
    char tmp[10];
    if(!logPath)
        logPath        = "/tmp";
    bool ignore        = false;
    char* nodeName     = getenv(NODE_NAME);
    char* eventType    = getenv(EVENT_TYPE);
    char* value        = getenv(VALUE);
    char* condName     = getenv(COND_NAME);
    char hname[50]     = {0};
    struct timeval creation_time;
    if(gettimeofday(&creation_time,NULL) < 0)
    {
        log_error("get event creation time error!"); //note: this creation time is on EMS node while other events creation time is on compute node.
        return -1;
    }
    if(gethostname(hname,50) < 0)
    {
        log_error("error to get ems node name");
        return -2;
    }

    if(!nodeName || !eventType || !value || !condName)
    {
        log_error("at least one of node name, event type, condition name and value environment variable is set, return!");
        return -3;
    }
    msg = "event from node ";
    msg += nodeName;
    msg += ", event type is ";
    msg += eventType;
    msg += ", process value is ";
    msg += value;
    msg += ", condition name is ";
    msg += condName;
    log_info(msg);
    teal_connector_handle conn_handle = NULL;
    TEAL_ERR_T ret = TEAL_SUCCESS;
    ret = teal_open_connector(&conn_handle,"GPFS","/tmp");
    if(ret != TEAL_SUCCESS)
    {
        msg = "open gpfs connector failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
        log_error(msg);
        return ret;
    }
    
    string srcloc(nodeName); //srcloc  == collector node name   
    string rptloc(hname);  //rptloc == ems nodename
   
    tlgpfs_misc_event_t *gpfsMiscEvent = new tlgpfs_misc_event_t();
    
    teal_cbe_t *cbe          = new teal_cbe_t();    
    char time[30]            = {0};
    string pid(value);
    string prev_pid(value);
    pid.erase(pid.begin(), pid.begin() + pid.find_first_of('{') + 1);
    pid.erase(pid.begin() + pid.find_first_of('}'),pid.end());
    pid.erase(pid.begin(), pid.begin() + pid.find_first_of(',') + 1);

    prev_pid.erase(prev_pid.begin(), prev_pid.begin() + prev_pid.find_last_of('{') + 1);
    prev_pid.erase(prev_pid.begin() + prev_pid.find_first_of('}'),prev_pid.end());
    prev_pid.erase(prev_pid.begin(), prev_pid.begin() + prev_pid.find_first_of(',') + 1);

    Utils::get_time_stamp(&creation_time,time);
    cbe->time_occurred       = time;
    cbe->src_comp            = "GPFS";
    cbe->src_loc_type        = "A";
    cbe->rpt_comp            = "TEAL";
    cbe->rpt_loc_type        = "A";    

    srcloc                  += "##";        //srcloc == collector node name##
    rptloc                  += "##";        //rptloc == ems nodename##
    rptloc                  += condName;        //rptloc == ems nodename##condtion name
    srcloc                  += "tlgpfsmon"; //srcloc == collector nodename##tlgpfsmon
    cbe->rpt_loc             = (char*)rptloc.c_str();
    

    if(atoi(eventType) == 1)
    {
        log_info("Rearm event captured, daemon is running, logging daemon started event!");
        gpfsMiscEvent->severity  = "Informational";
        cbe->event_id            = "GP010001";
        if(!pid.empty())
        {
            srcloc += "##";        // srcloc == collector nodename##tlgpfsmon##
            srcloc += pid.c_str();// srcloc == collector nodename##tlgpfsmon##pid
            cbe->src_loc             = (char*)srcloc.c_str();
            ret = tlgpfs_write_misc_event(conn_handle,cbe, gpfsMiscEvent);
            if(ret != TEAL_SUCCESS)
            {
                msg = "write misc event failed with ";
                msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
                log_error(msg);
            }
        }
        else
        {
            msg  = "Unexpected event, ignore it!";
            log_info(msg);
            ignore = true;
        }
        delete cbe;
        delete gpfsMiscEvent;
    }
    else if(atoi(eventType) == 0)
    {
        log_info("Event captured, daemon is stopped, logging daemon stopped event!");
        gpfsMiscEvent->severity  = "Fatal";
        cbe->event_id            = "GP010002";
        if(!prev_pid.empty())
        {
            srcloc += "##";        // srcloc == collector nodename##tlgpfsmon##
            srcloc += prev_pid.c_str();// srcloc == collector nodename##tlgpfsmon##pid
            cbe->src_loc             = (char*)srcloc.c_str();
            ret = tlgpfs_write_misc_event(conn_handle,cbe, gpfsMiscEvent);
            if(ret != TEAL_SUCCESS)
            {
                msg = "write misc event failed with ";
                msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
                log_error(msg);
            }
        }
        else
        {
            msg  = "Unexpected event, ignore it!";
            log_info(msg);
            ignore = true;
        }
        delete cbe;
        delete gpfsMiscEvent;
    }
    else
    {
        msg = "Unrecognized event type  ";
        msg += eventType;
        msg += ", do nothing!";
        log_error(msg);
        ignore = true;
    }
    ret = teal_close_connector(conn_handle);
    if(ret != TEAL_SUCCESS)
    {
        msg = "close gpfs connector error with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
        log_error(msg);
    }  
    if(atoi(eventType) == 1)
    {
        log_info("Realarm event, no need to update cluster status, exit!");
        return TEAL_SUCCESS;
    }
    if(ignore == true)
    {
        log_info("Unexpected event, no need to log, exit!");
        return TEAL_SUCCESS;
    }
    string node(nodeName);
    //find out the GPFS cluster facing node name here
    
    FILE *fP;
    string cmd = "/opt/xcat/bin/xdsh ";
    cmd       += node;
    cmd       += " \"grep home /var/mmfs/gen/mmfsNodeData | cut -d: -f8\" 2>/dev/null | head -1 | tr -d ' ' | cut -d: -f2";
    msg        = "Get GPFS facing node name via command: ";
    msg       += cmd;
    log_info(msg);
    
    fP = popen(cmd.c_str(), "r");    
    if (fP == NULL)
    {
        msg = "popen failed!";
        log_error(msg);
        pclose(fP);
        return TEAL_ERR_ARG;
    }
    char myBuf[100];
    char str[100];
    fgets(myBuf, 100, fP);
    // trim the new line symbol '\n' here
    memcpy(str, myBuf, strlen(myBuf)-1);
    pclose(fP);
    if(str == "")
    {
        msg  = "Can not get GPFS facing node name of ";
        msg += node;
        msg += ", exit...";
        log_error(msg);
        return TEAL_ERR_ARG;
    }
    msg  = "Node ";
    msg += node;
    msg += " has the GPFS facing name of ";
    msg += str;
    log_info(msg);
    node = str; // replace node with GPFS cluster facing name here
    vector<tlgpfs_node_info_t*>* nodes = NULL; 
    string queryColName("node_name");
    msg  = "Start to query cluster id via node name ";
    msg += node;
    log_info(msg);
    
    //reopen it
    ret = teal_open_connector(&conn_handle,"GPFS","/tmp");
    if(ret != TEAL_SUCCESS)
    {
        msg = "open gpfs connector failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
        log_error(msg);
        return ret;
    }  
    ret = tlgpfs_query_node_status(conn_handle,&nodes,queryColName,node); // do query to find out cluster_id
    if(ret != TEAL_SUCCESS)
    {
        msg = "Query node status error with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
        log_error(msg);
    }
    ret = teal_close_connector(conn_handle);
    if(ret != TEAL_SUCCESS)
    {
        msg = "close gpfs connector error with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
        log_error(msg);
    }
    if(!nodes || nodes->empty())
    {
        log_info("No such node info! Can't determin which cluster this node belongs to, exit....");
        return 0;
    }
    
    //reopen it
    ret = teal_open_connector(&conn_handle,"GPFS","/tmp");
    if(ret != TEAL_SUCCESS)
    {
        msg = "open gpfs connector failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
        log_error(msg);
        return ret;
    }
    
    vector<tlgpfs_node_info_t*>::iterator itr;
    string colName("health");
    char buf[5] = {0};
    sprintf(buf,"%d",TEAL::UNKNOWN);
    string colValue(buf); //unknown
    string keyName("cluster_id");
    for(itr = nodes->begin(); itr != nodes->end(); itr++)
    {
        string clusterid((*itr)->cluster_id);
        msg  = "Start to update cluster status via cluster id ";
        msg += clusterid;
        log_info(msg);
        ret  = tlgpfs_update_overall_status(conn_handle,colName,colValue,keyName,clusterid);
        if(ret != TEAL_SUCCESS)
        {
            msg  = "Update cluster ";
            msg += clusterid;
            msg += " health status error with ";
            msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
            log_error(msg);
        }
    }

    ret = teal_close_connector(conn_handle);
    if(ret != TEAL_SUCCESS)
    {
        msg  = "close gpfs connector error with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
        log_error(msg);
    }
    return ret;

}

