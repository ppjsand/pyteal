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
#ifndef DBPDISKINFO_H_
#define DBPDISKINFO_H_

#include "DbGpfsInfo.h"
#include "teal_gpfs_connect.h"
#include <sql.h>
#include <string>
#include "api_types.h"
#include "api_nsdRAID.h"
#include "utils.h"
typedef struct tlgpfs_pdisk_info tlgpfs_pdisk_info_t;
class Utils;

namespace TEAL {
class DbInterface;
}
using namespace std;
namespace TEAL {

const string REGULAR_PDISK_TABLE = "x_pdiskinfo";
const string TMP_PDISK_TABLE     = "x_pdiskinfo_tmp";



class DbPdiskInfo: public DbGpfsInfo
{
enum PdiskInfoColumnSizes
{
    CLUSTER_ID_SIZE              = 128,
    RG_NAME_SIZE                 = 64,
    DA_NAME_SIZE                 = 64,    
    PDISK_NAME_SIZE              = 64,
    PDISK_DEV_PATH_SIZE          = 64,
    PDISK_STATE_SIZE             = 160,
    PDISK_FRU_SIZE               = 32,
    PDISK_LOCATION_SIZE          = 32,
    PDISK_REPL_PRIOR_SIZE        = 4,
    PDISK_FREE_SPACE_SIZE        = 8,

};
public:
    DbPdiskInfo(DbInterface* dbi = NULL, vector<string>* cols = NULL, vector<string>* pk = NULL, tlgpfs_pdisk_info_t* pdisk = NULL);
    
    virtual ~DbPdiskInfo();
    static tlgpfs_pdisk_info_t* extract(gpfsDeclusteredArrayPdisk* pdisk,string& clusterId,string& rgName,string& daName);
    static tlgpfs_pdisk_info_t* allocateMemory();
    static void printStatus(tlgpfs_pdisk_info_t* pdisk,bool detailed);

private:
    virtual void Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info);     
    virtual void bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init);
    virtual void updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst);
    virtual void getResult(SQLHSTMT sqlStmt,void** holder);

    void copyInfo(tlgpfs_pdisk_info_t* dst, tlgpfs_pdisk_info_t* src);
    void resetMemory(tlgpfs_pdisk_info* tmpPdiskInfo);
        
};

}

#endif 

