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
#ifndef DBDISKINFO_H_
#define DBDISKINFO_H_

#include "DbGpfsInfo.h"
#include "teal_gpfs_connect.h"
#include <sql.h>
#include <string>
#include "api_poll.h"
#include "utils.h"
typedef struct tlgpfs_disk_info tlgpfs_disk_info_t;
class Utils;

namespace TEAL {
class DbInterface;
}
using namespace std;
namespace TEAL {

const string REGULAR_DISK_TABLE   = "x_diskinfo";
const string TMP_DISK_TABLE          = "x_diskinfo_tmp";



class DbDiskInfo: public DbGpfsInfo
{
enum DiskInfoColumnSizes
{
    CLUSTER_ID_SIZE      = 128,
    DISK_NAME_SIZE       = 128,
    NODE_NAME_SIZE       = 128,
    STATUS_SIZE          = 128,
    AVAILABILITY_SIZE    = 128,
    POOL_NAME_SIZE       = 128,
    VOL_ID_SIZE          = 128,
    META_DATA_SIZE       = 128,
    DATA_SIZE            = 128,
    DISK_WAIT_SIZE       = 128,
    TOTAL_SPACE_SIZE     = 8,
    FULL_BLK_SPACE_SIZE  = 8,
    SUB_BLK_SPACE_SIZE   = 8,
    FAIL_GROUP_ID_SIZE   = 4,
    IS_FREE_SIZE         = 4,

};
public:
    DbDiskInfo(DbInterface* dbi = NULL, vector<string>* cols = NULL, vector<string>* pk = NULL, tlgpfs_disk_info_t* disk = NULL);
    virtual ~DbDiskInfo();
    static tlgpfs_disk_info_t* extract(DiskInfo* disk,string& clusterId);
    static tlgpfs_disk_info_t* allocateMemory();
    static void printStatus(tlgpfs_disk_info_t* disk, bool detailed);
       
private:
    virtual void Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info);     
    virtual void bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init);
    virtual void updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst);
    virtual void getResult(SQLHSTMT sqlStmt,void** holder);

    void copyInfo(tlgpfs_disk_info_t* dst, tlgpfs_disk_info_t* src);        
    void resetMemory(tlgpfs_disk_info* tmpDiskInfo);

};

}

#endif 

