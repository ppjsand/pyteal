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
#ifndef DBDISKEVENT_H_
#define DBDISKEVENT_H_
#include "DbEvent.h"
#include <sql.h>
#include <string>
struct tlgpfs_disk_event;
namespace TEAL {
    class DbInterface;
}

namespace TEAL
{
class DbDiskEvent: public DbEvent {
    public:

        DbDiskEvent(DbInterface& dbi, tlgpfs_disk_event* gpfs_disk_event);

        virtual ~DbDiskEvent();

    protected:

        virtual void insert(SQLHSTMT sqlStmt);

    private:
        tlgpfs_disk_event* ivGpfsEvent; // The GPFS disk event from the user
        std::string ivInsertSql;          // The SQL insert statement
};

}

#endif 


