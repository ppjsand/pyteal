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
#ifndef DB_FS_EVENT_H_
#define DB_FS_EVENT_H_
#include "DbEvent.h"
#include <sql.h>
#include <string>

struct tlgpfs_fs_event;
namespace TEAL {
    class DbInterface;
    const std::string GPFS_FS_TABLE_NAME("GPFS_1_1");
}

namespace TEAL
{
class DbFsEvent: public DbEvent {
enum FSEventColumnSizes
{
    SEVERITY_SIZE      = 256,
    NODE_IP_SIZE       = 256,
    SGMGR_IP_SIZE      = 256,
    USER_UNBA_SIZE     = 256,
    META_UNBA_SIZE     = 256,
    USER_ILL_REP_SIZE  = 256,
    META_ILL_REP_SIZE  = 256,
    USER_EXPOSED_SIZE  = 256,
    META_EXPOSED_SIZE  = 256,
    POOL_NAME_SIZE     = 256,
    POOL_STATUS_SIZE   = 256,
    POOL_USAGE_SIZE    = 4,
};
    public:

        DbFsEvent(DbInterface& dbi, tlgpfs_fs_event* gpfs_fs_event);

        virtual ~DbFsEvent();

    protected:

        virtual void insert(SQLHSTMT sqlStmt);

    private:
        tlgpfs_fs_event* ivGpfsEvent; 
        std::string ivInsertSql;        
};

}

#endif 

