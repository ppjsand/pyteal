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
/*--------------------------------------------------------------------*/
/*  Includes                                                          */
/*--------------------------------------------------------------------*/

#include "DbCommonBaseEvent.h"
#include "DbInterface.h"
#include "teal_event.h"

#include <stdexcept>

/*--------------------------------------------------------------------*/
/*  User Types                                                        */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Constants                                                         */
/*--------------------------------------------------------------------*/

namespace TEAL
{

enum ColumnSize{
	EVENT_ID_SIZE = 8,
	SRC_COMP_SIZE = 128,
	SRC_LOC_TYPE_SIZE = 2,
	SRC_LOC_SIZE = 255,
	RPT_COMP_SIZE = 128,
	RPT_LOC_TYPE_SIZE = 2,
	RPT_LOC_SIZE = 255,
	RAW_DATA_SIZE = 1024
};

}

/*--------------------------------------------------------------------*/
/*  Macros                                                            */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Global Variables                                                  */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/* >>> Function <<<                                                   */
/*--------------------------------------------------------------------*/

namespace TEAL
{

/*--------------------------------------------------------------------*/

DbCommonBaseEvent::DbCommonBaseEvent(DbInterface& dbi,
			                         teal_common_base_event* cbe,
			                         unsigned long long fmt,
			                         unsigned rawDataLen,
			                         void* rawData)
	: DbEvent(dbi), ivBaseEvent(cbe), ivRawDataFormat(fmt), ivRawDataLen(rawDataLen), ivRawData(rawData)
{
	// Validate the base event required arguments
	if (!cbe) throw std::invalid_argument("TEAL base event is NULL");
	if (!cbe->event_id) throw std::invalid_argument("Event id is NULL");
	if (!cbe->time_occurred) throw std::invalid_argument("Time occurred is NULL");
	if (!cbe->src_comp) throw std::invalid_argument("Source component is NULL");
	if (!cbe->src_loc_type) throw std::invalid_argument("Source location type is NULL");
	if (!cbe->src_loc) throw std::invalid_argument("Source location is NULL");
	// Optional fields - if rpt_comp is specified all rpt fields must be specified
	if (!((cbe->rpt_comp && cbe->rpt_loc_type && cbe->rpt_loc) ||
		(!cbe->rpt_comp && !cbe->rpt_loc_type && !cbe->rpt_loc)))
		throw std::invalid_argument("Reporting Information Invalid");

	std::vector<std::string> fields;
	fields.push_back("event_id");
	fields.push_back("time_occurred");
	fields.push_back("src_comp");
	fields.push_back("src_loc_type");
	fields.push_back("src_loc");
	fields.push_back("rpt_comp");
	fields.push_back("rpt_loc_type");
	fields.push_back("rpt_loc");
	fields.push_back("elapsed_time");
	fields.push_back("event_cnt");
	fields.push_back("raw_data_fmt");
	fields.push_back("raw_data");

	std::string tableName = dbi.getEventLogTableName();
	ivInsertSql = dbi.genInsert(fields,tableName);
}

/*--------------------------------------------------------------------*/

DbCommonBaseEvent::~DbCommonBaseEvent()
{
	// Nothing to do
}

/*--------------------------------------------------------------------*/

void DbCommonBaseEvent::insert(SQLHSTMT sqlStmt)
{
	SQLRETURN ret;

	SQLLEN eventIdLen = SQL_NTS;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR, EVENT_ID_SIZE, 0, ivBaseEvent->event_id, 0, &eventIdLen);
    DbInterface::checkSqlRetcode("DbCommonBaseEvent::prepareInsert SQLBindParameter 1",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN timeOccurredLen = SQL_NTS;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_TIMESTAMP, 0, 0, ivBaseEvent->time_occurred, 0, &timeOccurredLen);
    DbInterface::checkSqlRetcode("DbCommonBaseEvent::prepareInsert SQLBindParameter 2",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN srcCompLen = SQL_NTS;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 3, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, SRC_COMP_SIZE, 0, ivBaseEvent->src_comp, 0, &srcCompLen);
    DbInterface::checkSqlRetcode("DbCommonBaseEvent::prepareInsert SQLBindParameter 3",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN srcLocTypeLen = SQL_NTS;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 4, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, SRC_LOC_TYPE_SIZE, 0, ivBaseEvent->src_loc_type, 0, &srcLocTypeLen);
    DbInterface::checkSqlRetcode("DbCommonBaseEvent::prepareInsert SQLBindParameter 4",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN srcLocLen = SQL_NTS;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 5, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, SRC_LOC_SIZE, 0, ivBaseEvent->src_loc, 0, &srcLocLen);
    DbInterface::checkSqlRetcode("DbCommonBaseEvent::prepareInsert SQLBindParameter 5",ret,sqlStmt,SQL_HANDLE_STMT);

    // Reporting component can be option which makes the reporting location information optional
    SQLLEN rpt_indicator = ivBaseEvent->rpt_comp ? SQL_NTS : SQL_NULL_DATA;
	SQLLEN rptCompLen = rpt_indicator;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 6, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, RPT_COMP_SIZE, 0, ivBaseEvent->rpt_comp, 0, &rptCompLen);
	DbInterface::checkSqlRetcode("DbCommonBaseEvent::prepareInsert SQLBindParameter 6",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN rptLocTypeLen = rpt_indicator;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 7, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, RPT_LOC_TYPE_SIZE, 0, ivBaseEvent->rpt_loc_type, 0, &rptLocTypeLen);
	DbInterface::checkSqlRetcode("DbCommonBaseEvent::prepareInsert SQLBindParameter 7",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN rptLocLen = rpt_indicator;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 8, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, RPT_LOC_SIZE, 0, ivBaseEvent->rpt_loc, 0, &rptLocLen);
	DbInterface::checkSqlRetcode("DbCommonBaseEvent::prepareInsert SQLBindParameter 8",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN elapsedTimeLen =  ivBaseEvent->elapsed_time ? 0 : SQL_NULL_DATA;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 9, SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, ivBaseEvent->elapsed_time, 0, &elapsedTimeLen);
	DbInterface::checkSqlRetcode("DbCommonBaseEvent::prepareInsert SQLBindParameter 9",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN eventCntLen =  ivBaseEvent->event_cnt ? 0 : SQL_NULL_DATA;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 10, SQL_PARAM_INPUT, SQL_C_LONG, SQL_INTEGER, 0, 0, ivBaseEvent->event_cnt, 0, &eventCntLen);
	DbInterface::checkSqlRetcode("DbCommonBaseEvent::prepareInsert SQLBindParameter 10",ret,sqlStmt,SQL_HANDLE_STMT);

	// Additional Base Event Bookkeeping

	SQLLEN rawDataFormatLen = 0;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 11, SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, &ivRawDataFormat, 0, &rawDataFormatLen);
	DbInterface::checkSqlRetcode("DbCommonBaseEvent::prepareInsert SQLBindParameter 11",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN rawDataLen = ivRawData ? (SQLLEN)ivRawDataLen : SQL_NULL_DATA;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 12, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, RAW_DATA_SIZE, 0, ivRawData, 0, &rawDataLen);
	DbInterface::checkSqlRetcode("DbCommonBaseEvent::prepareInsert SQLBindParameter 12",ret,sqlStmt,SQL_HANDLE_STMT);

	//  Preparation complete -- execute the insert

   	ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)ivInsertSql.c_str(), SQL_NTS);
    DbInterface::checkSqlRetcode("DbObject::insert SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);
}

}
