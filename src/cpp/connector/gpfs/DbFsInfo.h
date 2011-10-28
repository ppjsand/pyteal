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
#ifndef DBFSINFO_H_
#define DBFSINFO_H_

#include "DbGpfsInfo.h"
#include "teal_gpfs_connect.h"
#include <sql.h>
#include <string>
#include "api_poll.h"
#include "utils.h"
typedef struct tlgpfs_fs_info tlgpfs_fs_info_t;
class Utils;

namespace TEAL {
class DbInterface;
}
using namespace std;
namespace TEAL {

const string REGULAR_FS_TABLE   = "x_fsinfo";
const string TMP_FS_TABLE      = "x_fsinfo_tmp";



class DbFsInfo: public DbGpfsInfo
{
enum FsInfoColumnSizes
{
    CLUSTER_ID_SIZE      = 128,
    FS_NAME_SIZE         = 128,
    MANAGER_SIZE         = 128,
    STATUS_SIZE          = 128,
    X_STATUS_SIZE        = 128,
    POOL_REF_TIME_SIZE   = 128,
    TOTAL_SPACE_SIZE     = 8,
    TOTAL_INODES_SIZE    = 8,
    FREE_INODES_SIZE     = 8,
    FREE_SPACE_SIZE      = 8,
    FULL_BLK_SPACE_SIZE  = 8,
    SUB_BLK_SPACE_SIZE   = 8,
    STG_POOL_NUM_SIZE    = 4,
    NUM_MGMT_SIZE        = 4,
    READ_DURATION_SIZE   = 4,
    NUM_MNT_NODES_SIZE   = 4,
    NUM_POLICIES_SIZE    = 4,
    WRITE_DURATION_SIZE  = 4,
    WAS_UPDATED_SIZE     = 4,
    NUM_MGR_CHG_SIZE     = 4,

};
public:
    DbFsInfo(DbInterface* dbi = NULL, vector<string>* cols = NULL, vector<string>* pk = NULL, tlgpfs_fs_info_t* fs = NULL);
    static void printStatus(tlgpfs_fs_info_t* fs, bool detailed);
    virtual ~DbFsInfo();
    static tlgpfs_fs_info_t* extract(FilesystemInfo* fs,string& clusterId);
    static tlgpfs_fs_info_t* allocateMemory();

private:
    virtual void Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info);     
    virtual void bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init);
    virtual void updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst);
    virtual void getResult(SQLHSTMT sqlStmt,void** holder);

    void copyInfo(tlgpfs_fs_info_t* dst, tlgpfs_fs_info_t* src);
    void resetMemory(tlgpfs_fs_info* tmpFsInfo);    
};

}

#endif 

