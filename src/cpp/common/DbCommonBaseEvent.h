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
#ifndef DBCOMMONBASEEVENT_H_
#define DBCOMMONBASEEVENT_H_

/*--------------------------------------------------------------------*/
/*  Includes                                                          */
/*--------------------------------------------------------------------*/

#include "DbEvent.h"

#include <sql.h>
#include <string>

struct teal_common_base_event;

namespace TEAL {
	class DbInterface;
}

/*--------------------------------------------------------------------*/
/*  User Types                                                        */
/*--------------------------------------------------------------------*/

namespace TEAL {

/**
 * This class is responsible for writing the TEAL base event data to the
 * database
 */
class DbCommonBaseEvent: public DbEvent
{
	public:
		/**
		 * Constructor
		 *
		 * @param dbi Database Interface
		 * @param cbe TEAL base event
		 * @param fmt Format control word
		 * @param rawDataLen Length of raw data to write
		 * @param rawData binary data to write. Can be null in which case the
		 * rawDataLen is ignored
		 */
		DbCommonBaseEvent(DbInterface& dbi,
						  teal_common_base_event* cbe,
				          unsigned long long fmt,
				          unsigned rawDataLen,
				          void* rawData);
		/**
		 * Destructor
		 */
		virtual ~DbCommonBaseEvent();

		/**
		 * Insert the Common Base Event into its own table
		 *
		 * @param sqlStmt - the statement to use for insertion
		 */
		virtual void insert(SQLHSTMT sqlStmt);

	private:
		teal_common_base_event* ivBaseEvent; ///< Base event passed in by user
		unsigned long long ivRawDataFormat;  ///< Format of raw data used by framework
		unsigned ivRawDataLen;				 ///< Actual length of raw data
		void* ivRawData;					 ///< Raw data - can be NULL
		std::string ivInsertSql;			 ///< Cached insert string
};

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

}

#endif /* DBCOMMONBASEEVENT_H_ */
