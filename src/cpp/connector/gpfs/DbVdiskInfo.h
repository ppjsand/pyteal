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
#ifndef DBVDISKINFO_H_
#define DBVDISKINFO_H_

#include "DbGpfsInfo.h"
#include "teal_gpfs_connect.h"
#include <sql.h>
#include <string>
#include "utils.h"
#include "api_types.h"
#include "api_nsdRAID.h"
typedef struct tlgpfs_vdisk_info tlgpfs_vdisk_info_t;
class Utils;

namespace TEAL {
class DbInterface;
}
using namespace std;
namespace TEAL {

const string REGULAR_VDISK_TABLE = "x_vdiskinfo";
const string TMP_VDISK_TABLE     = "x_vdiskinfo_tmp";



class DbVdiskInfo: public DbGpfsInfo
{
enum VdiskInfoColumnSizes
{
    CLUSTER_ID_SIZE              = 128,
    RG_NAME_SIZE                 = 64,
    DA_NAME_SIZE                 = 64,    
    VDISK_NAME_SIZE              = 64,
    VDISK_RAID_CODE_SIZE         = 32,
    VDISK_STATE_SIZE             = 64,
    VDISK_REMARKS_SIZE           = 32,
    VDISK_BLOCK_SIZE_SIZE        = 4,
    VDISK_SIZE_SIZE              = 8,

};
public:
    DbVdiskInfo(DbInterface* dbi = NULL, vector<string>* cols = NULL, vector<string>* pk = NULL, tlgpfs_vdisk_info_t* vdisk = NULL);
    
    virtual ~DbVdiskInfo();
    static tlgpfs_vdisk_info_t* extract(gpfsDeclusteredArrayVdisk* vdisk,string& clusterId,string& rgName,string& daName);
    static tlgpfs_vdisk_info_t* allocateMemory();
    static void printStatus(tlgpfs_vdisk_info_t* vdisk,bool detailed);

private:
    virtual void Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info);     
    virtual void bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init);
    virtual void updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst);
    virtual void getResult(SQLHSTMT sqlStmt,void** holder);

    void copyInfo(tlgpfs_vdisk_info_t* dst, tlgpfs_vdisk_info_t* src);
    void resetMemory(tlgpfs_vdisk_info* tmpVdiskInfo);
        
};

}

#endif 

