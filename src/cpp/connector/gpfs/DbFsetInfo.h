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
#ifndef DBFSETINFO_H_
#define DBFSETINFO_H_

#include "DbGpfsInfo.h"
#include "teal_gpfs_connect.h"
#include <sql.h>
#include <string>
#include "api_poll.h"
#include "utils.h"
typedef struct tlgpfs_fset_info tlgpfs_fset_info_t;
class Utils;

namespace TEAL {
class DbInterface;
}
using namespace std;
namespace TEAL {

const string REGULAR_FSET_TABLE   = "x_fsetinfo";
const string TMP_FSET_TABLE        = "x_fsetinfo_tmp";



class DbFsetInfo: public DbGpfsInfo
{
enum FsetInfoColumnSizes
{
    CLUSTER_ID_SIZE      = 128,
    FS_NAME_SIZE         = 128,
    ID_SIZE              = 128,
    FSET_NAME_SIZE       = 128,
    ROOT_INODE_SIZE      = 128,
    PARENT_ID_SIZE       = 128,
    COMMENT_SIZE         = 128,    
    STATUS_SIZE          = 128,
    PATH_SIZE            = 128,
    CREATED_SIZE         = 128,
    INODES_SIZE          = 8,
    DATA_SIZE            = 8,
    VERSION_SIZE         = 4,
};
public:
    DbFsetInfo(DbInterface* dbi = NULL, vector<string>* cols = NULL, vector<string>* pk = NULL, tlgpfs_fset_info_t* fset = NULL);
    virtual ~DbFsetInfo();
    static tlgpfs_fset_info_t* extract(FileSet* fset,string& clusterId);
    static tlgpfs_fset_info_t* allocateMemory();
    static void printStatus(tlgpfs_fset_info_t* fset, bool detailed);
        
private:
    virtual void Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info);     
    virtual void bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init);
    virtual void updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst);
    virtual void getResult(SQLHSTMT sqlStmt,void** holder);

    void resetMemory(tlgpfs_fset_info* tmpFsetInfo);
    void copyInfo(tlgpfs_fset_info_t* dst, tlgpfs_fset_info_t* src);

};

}

#endif 

