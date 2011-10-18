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
#ifndef DBDAINFO_H_
#define DBDAINFO_H_

#include "DbGpfsInfo.h"
#include "teal_gpfs_connect.h"
#include <sql.h>
#include <string>
#include "api_types.h"
#include "api_nsdRAID.h"
#include "utils.h"
typedef struct tlgpfs_da_info tlgpfs_da_info_t;
class Utils;

namespace TEAL {
class DbInterface;
}
using namespace std;
namespace TEAL {

const string REGULAR_DA_TABLE = "x_dainfo";
const string TMP_DA_TABLE     = "x_dainfo_tmp";



class DbDaInfo: public DbGpfsInfo
{
enum DaInfoColumnSizes
{
    CLUSTER_ID_SIZE           = 128,
    RG_NAME_SIZE              = 64,
    DA_NAME_SIZE              = 64,
    DA_BG_TASK_SIZE           = 32,
    DA_TASK_PRIORITY_SIZE     = 32,
    DA_NEED_SERVICE_SIZE      = 8,
    DA_TASK_PERCENT_SIZE      = 4,
    DA_VDISKS_SIZE            = 4,
    DA_PDISKS_SIZE            = 4,
    DA_SPARES_SIZE            = 4,
    DA_REPLACE_THRES_SIZE     = 4,
    DA_FREE_SPACE_SIZE        = 8,
    DA_SCRUB_DURA_SIZE        = 4,

};
public:
    DbDaInfo(DbInterface* dbi = NULL, vector<string>* cols = NULL, vector<string>* pk = NULL, tlgpfs_da_info_t* da = NULL);
    
    virtual ~DbDaInfo();
    static tlgpfs_da_info_t* extract(gpfsRecoveryGroupDeclusteredArray* da,string& clusterId,string& rgName);
    static tlgpfs_da_info_t* allocateMemory();
    static void printStatus(tlgpfs_da_info_t* da,bool detailed);

private:
    virtual void Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info);     
    virtual void bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init);
    virtual void updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst);
    virtual void getResult(SQLHSTMT sqlStmt,void** holder);

    void copyInfo(tlgpfs_da_info_t* dst, tlgpfs_da_info_t* src);
    void resetMemory(tlgpfs_da_info* tmpDaInfo);
        
};

}

#endif 

