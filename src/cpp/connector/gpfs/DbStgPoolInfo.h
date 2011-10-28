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
#ifndef DBSTGPOOLINFO_H_
#define DBSTGPOOLINFO_H_

#include "DbGpfsInfo.h"
#include "teal_gpfs_connect.h"
#include <sql.h>
#include <string>
#include "api_poll.h"
#include "utils.h"
typedef struct tlgpfs_stg_info tlgpfs_stg_info_t;
class Utils;

namespace TEAL {
class DbInterface;
}
using namespace std;
namespace TEAL {

const string REGULAR_STG_TABLE   = "x_stgpoolinfo";
const string TMP_STG_TABLE         = "x_stgpoolinfo_tmp";



class DbStgPoolInfo: public DbGpfsInfo
{
enum StgInfoColumnSizes
{
    CLUSTER_ID_SIZE          = 128,
    FS_NAME_SIZE             = 128,
    STG_NAME_SIZE            = 128,
    STATUS_SIZE              = 128,
    REFRESH_TIME_SIZE        = 128,
    PERF_REF_TIME_SIZE       = 128,
    TOTAL_SPACE_SIZE         = 8,
    FREE_SPACE_SIZE          = 8,
    PARENT_FS_SIZE           = 4,
    NUM_DISKS_SIZE           = 4,
    NUM_DISK_ITEMS_SIZE      = 4,

};
public:
    DbStgPoolInfo(DbInterface* dbi = NULL, vector<string>* cols = NULL, vector<string>* pk = NULL, tlgpfs_stg_info_t* stg = NULL);
    virtual ~DbStgPoolInfo();
    static tlgpfs_stg_info_t* extract(StoragePoolInfo* stg,string& clusterId, string& fsName);
    static tlgpfs_stg_info_t* allocateMemory();
    static void printStatus(tlgpfs_stg_info_t* stg, bool detailed);

private:
    virtual void Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info);     
    virtual void bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init);
    virtual void updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst);
    virtual void getResult(SQLHSTMT sqlStmt,void** holder);        

    void copyInfo(tlgpfs_stg_info_t* dst, tlgpfs_stg_info_t* src);
    void resetMemory(tlgpfs_stg_info* tmpStgInfo);
        
};

}

#endif 

