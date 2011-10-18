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
#ifndef DB_MISC_EVENT_H_
#define DB_MISC_EVENT_H_
#include "DbEvent.h"
#include <sql.h>
#include <string>

struct tlgpfs_misc_event;
namespace TEAL {
    class DbInterface;
}

namespace TEAL
{
class DbMiscEvent: public DbEvent {
    public:

        DbMiscEvent(DbInterface& dbi, tlgpfs_misc_event* gpfs_misc_event);

        virtual ~DbMiscEvent();

    protected:

        virtual void insert(SQLHSTMT sqlStmt);

    private:
        tlgpfs_misc_event* ivGpfsEvent; 
        std::string ivInsertSql;        
};

}

#endif 

