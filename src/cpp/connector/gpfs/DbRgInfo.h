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
#ifndef DBRGINFO_H_
#define DBRGINFO_H_

#include "DbGpfsInfo.h"
#include "teal_gpfs_connect.h"
#include <sql.h>
#include <string>
#include "utils.h"
#include "api_types.h"
#include "api_nsdRAID.h"
typedef struct tlgpfs_rg_info tlgpfs_rg_info_t;
class Utils;

namespace TEAL {
class DbInterface;
}
using namespace std;
namespace TEAL {

const string REGULAR_RG_TABLE = "x_rginfo";
const string TMP_RG_TABLE     = "x_rginfo_tmp";



class DbRgInfo: public DbGpfsInfo
{
enum RgInfoColumnSizes
{
    CLUSTER_ID_SIZE      = 128,
    RG_NAME_SIZE         = 64,
    RG_ACT_SVR_SIZE      = 64,
    RG_SVRS_SIZE         = 128,
    RG_ID_SIZE           = 20,
    RG_DAS_SIZE          = 4,
    RG_VDISKS_SIZE       = 4,
    RG_PDISKS_SIZE       = 4,
};
public:
    DbRgInfo(DbInterface* dbi = NULL, vector<string>* cols = NULL, vector<string>* pk = NULL, tlgpfs_rg_info_t* rg = NULL);
    
    virtual ~DbRgInfo();
    static tlgpfs_rg_info_t* extract(gpfsRecoveryGroup* rg,string& clusterId);
    static tlgpfs_rg_info_t* allocateMemory();
    static void printStatus(tlgpfs_rg_info_t* rg,bool detailed);

private:
    virtual void Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info);     
    virtual void bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init);
    virtual void updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst);
    virtual void getResult(SQLHSTMT sqlStmt,void** holder);

    void copyInfo(tlgpfs_rg_info_t* dst, tlgpfs_rg_info_t* src);
    void resetMemory(tlgpfs_rg_info* tmpRgInfo);
        
};

}

#endif 

