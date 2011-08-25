// begin_generated_IBM_copyright_prolog
//
// This is an automatically generated copyright prolog.
// After initializing,  DO NOT MODIFY OR MOVE
// ================================================================
//
// (C) Copyright IBM Corp.  2010,2011
// Eclipse Public License (EPL)
//
// ================================================================
//
// end_generated_IBM_copyright_prolog
#ifndef DBEVENT_H_
#define DBEVENT_H_

/*--------------------------------------------------------------------*/
/*  Includes                                                          */
/*--------------------------------------------------------------------*/

#include <sql.h>
#include <string>

namespace TEAL {
	class DbInterface;
}

/*--------------------------------------------------------------------*/
/*  User Types                                                        */
/*--------------------------------------------------------------------*/

namespace TEAL {

/**
 * This is the base class for the various database tables for event data.
 * It is responsible for executing the insert.
 */
class DbEvent
{
	public:
		/**
		 * Constructor
		 *
		 * @param dbi Database interface used for execution
		 */
		DbEvent(DbInterface& dbi);

		/**
		 * Destructor
		 */
		virtual ~DbEvent();

		/**
		 * Insert the object into the database
		 *
		 * @param sqlStmt - The Statement to use for the insert
		 */
		virtual void insert(SQLHSTMT sqlStmt) = 0;
};

}

/*--------------------------------------------------------------------*/
/*  Constants                                                         */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Macros                                                            */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Global Variables                                                  */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Function Prototypes                                               */
/*--------------------------------------------------------------------*/

#endif /* DBOBJECT_H_ */
