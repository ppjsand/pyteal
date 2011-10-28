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

void usage(const string &processName)
{
    cerr<<"Usage: "<< processName<<"[{options}]"<<endl;
    cerr<<"Purge unknown status cluster info by default. Specify -f option to purge cluster info with other status"  <<endl;
    cerr<<"  [options] can be any of (-c and -i can not co-exist)"                                                   <<endl;
    cerr<<"    -c                       - cluster name whose items are needs to be removed"                          <<endl;
    cerr<<"    -i                       - cluster id whose items are needs to be removed"                            <<endl;
    cerr<<"    -f                       - force to purge no matter what status the cluster is"                       <<endl;
    cerr<<"    -h                       - print this message"                                                        <<endl;

}

int main(int argc, char* argv[])
{
    if(argc == 1)
    {
        cerr<<"Please specify at least one option!"<<endl;
        usage(argv[0]);
        exit(1);
    }   
    string clusterName     = "";
    string clusterId       = "";
    bool   force           = false;
    string msg;
    char tmp[10];
    int op;
    while ( (op = getopt(argc, argv, "i:c:fh")) != -1 ) {
        switch (op) {

            case 'c':
                clusterName = optarg;
                break;

            case 'f':
                force       = true;
                break;

            case 'i':
                clusterId = optarg;
                break;

            case 'h':
                usage(argv[0]);
                exit(0);

            default:
                usage(argv[0]);
                exit(1);
        }
    }
    if(clusterName != "" && clusterId != "")
    {
        cerr<<"-i and -c can't co-exist!"<<endl;
        usage(argv[0]);
        exit(1);
    }
    teal_connector_handle conn_handle = NULL;
    TEAL_ERR_T ret = TEAL_SUCCESS;
    ret = teal_open_connector(&conn_handle,"GPFS","/tmp");
    if(ret != TEAL_SUCCESS)
    {
        msg = "close gpfs connector error with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
        log_error(msg);
        cerr << msg << endl;
        return ret;
    }
    vector<tlgpfs_cluster_info_t*>*  clusters = NULL; 
    string queryColName  = "";
    string queryColValue = "";
    msg  =  "Start to purge cluster has a ";
    if(clusterName != "")
    {
        queryColName  = "cluster_name";
        queryColValue = clusterName;
    }
    else
    {
        queryColName  = "cluster_id";
        queryColValue = clusterId;
    }
    msg += queryColName;
    msg += " of ";
    msg += queryColValue;
    log_info(msg);
    ret = tlgpfs_query_cluster_status(conn_handle,&clusters,queryColName,queryColValue);
    if(ret != TEAL_SUCCESS)
    {
        msg = "Query cluster status error with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
        log_error(msg);
        cerr << msg << endl;
    }
    if(!clusters)
    {
        log_error("No such cluster info!");
        ret = teal_close_connector(conn_handle);
        if(ret != TEAL_SUCCESS)
        {
            msg = "close gpfs connector error with ";
            msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
            log_error(msg);
            cerr << msg << endl;
        }
        return -4;
    }
    vector<tlgpfs_cluster_info_t*>::iterator itr;

    string colName("health");
    char buf[5] = {0};
    sprintf(buf,"%d",TEAL::UNKNOWN);
    string colValue(buf); //unknown
    string keyName("cluster_id");

    for(itr = clusters->begin(); itr != clusters->end(); itr++)
    {
        string clusterid((*itr)->cluster_id);
        if(force && *(*itr)->health != TEAL::UNKNOWN)
        {
            msg  = "Force to purge cluster info, firstly, start to update cluster status via cluster id ";
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
                cerr << msg << endl;
                continue;
            }
        }
        else if(*(*itr)->health != TEAL::UNKNOWN)
        {
            msg  = "Can not purge a cluster which has a status other than unknown without option -f! skip...";
            log_warn(msg);
            cerr << msg << endl;
            continue;
        }
        ret  = tlgpfs_purge_cluster(conn_handle,clusterid);
        msg  = "Purge cluster ";
        msg += clusterid;
        if(ret != TEAL_SUCCESS)
        {        
            
            msg += " error with ";
            msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
            cerr<< msg <<endl;
            log_error(msg);
            continue;
        }
        msg += " succeeded!";
        log_info(msg);
        cout << msg << endl;
    }
    
    ret = teal_close_connector(conn_handle);
    if(ret != TEAL_SUCCESS)
    {
        msg = "close gpfs connector error with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
        log_error(msg);
        cerr << msg << endl;
    }

    return ret;

}

