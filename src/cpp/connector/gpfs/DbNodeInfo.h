/* begin_generated_IBM_copyright_prolog                             */
/*                                                                  */
/* This is an automatically generated copyright prolog.             */
/* After initializing,  DO NOT MODIFY OR MOVE                       */
/* ================================================================ */
/*                                                                  */
/* (C) Copyright IBM Corp.  2011                                    */
/* Eclipse Public License (EPL)                                     */
/*                                                                  */
/* ================================================================ */
/*                                                                  */
/* end_generated_IBM_copyright_prolog                               */
#ifndef DBNODEINFO_H_
#define DBNODEINFO_H_

#include "DbGpfsInfo.h"
#include "teal_gpfs_connect.h"
#include <sql.h>
#include <string>
#include "api_poll.h"
#include "utils.h"
typedef struct tlgpfs_node_info tlgpfs_node_info_t;
class Utils;

namespace TEAL {
class DbInterface;
}
using namespace std;
namespace TEAL {

const string REGULAR_NODE_TABLE = "x_nodeinfo";
const string TMP_NODE_TABLE     = "x_nodeinfo_tmp";



class DbNodeInfo: public DbGpfsInfo
{
enum NodeInfoColumnSizes
{
    CLUSTER_ID_SIZE      = 128,
    IP_ADDR_SIZE         = 128,
    NAME_SIZE            = 128,
    TYPE_SIZE            = 128,
    ENDIAN_SIZE          = 128,
    OS_NAME_SIZE         = 128,
    VERSION_SIZE         = 128,
    PLATFORM_SIZE        = 128,
    ADMIN_SIZE           = 128,
    STATUS_SIZE          = 128,
    UMNT_DISK_FAIL_SIZE  = 128,
    HEALTHY_SIZE         = 128,
    DIAG_SIZE            = 128,
    PG_POOL_SIZE         = 8,
    FAILURE_COUNT_SIZE   = 4,
    THREAD_WAIT_SIZE     = 4,
    PRE_THREADS_SIZE     = 4,
    MAX_MBPS_SIZE        = 4,
    MAX_FILE_CACHE_SIZE  = 4,
    MAX_STAT_CACHE_SIZE  = 4,
    WORK1_THREADS_SIZE   = 4,
    DM_EVT_TIMEOUT_SIZE  = 4,
    DM_MNT_TIMEOUT_SIZE  = 4,
    DM_SES_TIMEOUT_SIZE  = 4,
    NSD_WIN_MNT_SIZE     = 4,
    NSD_TIME_MNT_SIZE    = 4,
    NUM_DISK_ACCESS_SIZE = 4,

};
public:
    DbNodeInfo(DbInterface* dbi = NULL, vector<string>* cols = NULL, vector<string>* pk = NULL, tlgpfs_node_info_t* node = NULL);
    
    virtual ~DbNodeInfo();
    static tlgpfs_node_info_t* extract(NodeInfo* node,string& clusterId);
    static tlgpfs_node_info_t* allocateMemory();
    static void printStatus(tlgpfs_node_info_t* node,bool detailed);

private:
    virtual void Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info);     
    virtual void bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init);
    virtual void updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst);
    virtual void getResult(SQLHSTMT sqlStmt,void** holder);

    void copyInfo(tlgpfs_node_info_t* dst, tlgpfs_node_info_t* src);
    void resetMemory(tlgpfs_node_info* tmpNodeInfo);
        
};

}

#endif 

