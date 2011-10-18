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
#ifndef DB_PERSEUS_EVENT_H_
#define DB_PERSEUS_EVENT_H_
#include "DbEvent.h"
#include <sql.h>
#include <string>

struct tlgpfs_perseus_event;
namespace TEAL {
    class DbInterface;
}

namespace TEAL
{
class DbPerseusEvent: public DbEvent {
    public:

        DbPerseusEvent(DbInterface& dbi, tlgpfs_perseus_event* gpfs_perseus_event);

        virtual ~DbPerseusEvent();

    protected:

        virtual void insert(SQLHSTMT sqlStmt);

    private:
        tlgpfs_perseus_event* ivGpfsEvent; 
        std::string ivInsertSql;        
};

}

#endif 

