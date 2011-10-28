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
#ifndef DBCLUSTERINFO_H_
#define DBCLUSTERINFO_H_

#include "DbGpfsInfo.h"
#include "teal_gpfs_connect.h"
#include <sql.h>
#include <string>
#include "api_poll.h"
#include "utils.h"
typedef struct tlgpfs_cluster_info tlgpfs_cluster_info_t;
class Utils;

namespace TEAL {
class DbInterface;
}
using namespace std;
namespace TEAL {

const string REGULAR_CLUSTER_TABLE = "x_clusterinfo";
const string TMP_CLUSTER_TABLE       = "x_clusterinfo_tmp";



class DbClusterInfo: public DbGpfsInfo
{
enum ClusterInfoColumnSizes
{
    CLUSTER_ID_SIZE       = 128,
    CLUSTER_NAME_SIZE     = 128,
    CLUSTER_TYPE_SIZE     = 128,
    MIN_REL_LEVEL_SIZE    = 128,
    UID_DOMAIN_SIZE       = 128,
    RSH_CMD_SIZE          = 128,
    RCP_CMD_SIZE          = 128,
    PRIM_SERVER_SIZE      = 128,
    SEC_SERVER_SIZE       = 128,
    C_REF_TIME_SIZE       = 128,
    N_REF_TIME_SIZE       = 128,
    F_REF_TIME_SIZE       = 128,
    FP_REF_TIME_SIZE      = 128,
    SDR_FS_NUM_SIZE       = 4,
    NUM_NODES_SIZE        = 4,
    MAX_BLK_SIZE_SIZE     = 4,
    NUM_FS_SIZE           = 4,
    TOKEN_SERVER_SIZE     = 4,
    FAIL_DET_TIME_SIZE    = 4,
    TCP_PORT_SIZE         = 4,
    MIN_TIMEOUT_SIZE      = 4,
    MAX_TIMEOUT_SIZE      = 4,
    NUM_FREE_DISK_SIZE    = 4,
    CHNAGE_SIZE           = 2,
    HEALTH_SIZE           = 2,

};
public:
    DbClusterInfo(DbInterface* dbi = NULL, vector<string>* cols = NULL, vector<string>* pk = NULL, tlgpfs_cluster_info_t* cluster = NULL);
    virtual ~DbClusterInfo();
    static tlgpfs_cluster_info_t* extract(ClusterInfo* cluster);
    static tlgpfs_cluster_info_t* allocateMemory();
    static void printStatus(tlgpfs_cluster_info_t* cluster,bool detailed);

private:
    virtual void Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info);    
    virtual void bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init);
    virtual void updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst);
    virtual void getResult(SQLHSTMT sqlStmt,void** holder);
    
    void resetMemory(tlgpfs_cluster_info* tmpClusterInfo);   
    void copyInfo(tlgpfs_cluster_info_t* dst, tlgpfs_cluster_info_t* src);
};

}

#endif 
