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
#ifndef DBISNMEVENT_H_
#define DBISNMEVENT_H_

/*--------------------------------------------------------------------*/
/*  Includes                                                          */
/*--------------------------------------------------------------------*/

#include "DbEvent.h"
#include <sql.h>
#include <string>

struct teal_isnm_ext_event;
namespace TEAL {
	class DbInterface;
}

/*--------------------------------------------------------------------*/
/*  User Types                                                        */
/*--------------------------------------------------------------------*/

namespace TEAL
{
/**
 * This class is responsible for writing the ISNM event extended data
 * to the database
 *
 * It is assumed that the common base event information has been written
 * prior to using this class because it depends on the last INSERT
 * identity to tie this extended data to the base event
 *
 */
class DbIsnmEvent: public DbEvent {
	public:
		/**
		 * Constructor
		 *
		 * @param dbi the database interface to use to write the data
		 * @param isnm_event the ISNM event data
		 */
		DbIsnmEvent(DbInterface& dbi, teal_isnm_ext_event* isnm_event);

		/**
		 * Destructor
		 */
		virtual ~DbIsnmEvent();

		/**
		 * Insert the ISNM Event into its own table
		 *
		 * @param sqlStmt - the statement to use for insertion
		 */
		virtual void insert(SQLHSTMT sqlStmt);

	private:
		teal_isnm_ext_event* ivIsnmEvent; ///< The ISNM event from the user
		std::string ivInsertSql;          ///< The SQL insert statement
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

#endif /* DBISNMEVENT_H_ */
