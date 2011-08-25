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

#include "DbIsnmEvent.h"
#include "teal_isnm_connect.h"
#include "DbInterface.h"

#include <vector>

/*--------------------------------------------------------------------*/
/*  User Types                                                        */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Constants                                                         */
/*--------------------------------------------------------------------*/

namespace TEAL
{

enum ColumnSizes
{
	EED_LOC_INFO_SIZE = 64,
	ENCL_MTMS_SIZE = 20,
	PWR_CTRL_MTMS_SIZE = 20,
	NEIGHBOR_LOC_TYPE_SIZE = 2,
	NEIGHBOR_LOC_SIZE = 256,
	RECOVERY_FILE_PATH_SIZE = 32,
	ISNM_RAW_DATA_SIZE = 1024,
	LOCAL_PORT_SIZE = 256,
	LOCAL_TORRENT_SIZE = 256,
	LOCAL_PLANAR_SIZE = 256,
	LOCAL_OM1_SIZE = 256,
	LOCAL_OM2_SIZE = 256,
	NBR_PORT_SIZE = 256,
	NBR_TORRENT_SIZE = 256,
	NBR_PLANAR_SIZE = 256,
	NBR_OM1_SIZE = 256,
	NBR_OM2_SIZE = 256,
	GLOBAL_COUNTER_SIZE = 8,
};

const std::string ISNM_TABLE_NAME("CNM_1_2");

}

/*--------------------------------------------------------------------*/
/*  Macros                                                            */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Internal Function Prototypes                                      */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Global Variables                                                  */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/* >>> Function <<<                                                   */
/*--------------------------------------------------------------------*/


namespace TEAL {


DbIsnmEvent::DbIsnmEvent(DbInterface& dbi, teal_isnm_ext_event* isnm_event) : DbEvent(dbi), ivIsnmEvent(isnm_event)
{
	if (!isnm_event) throw std::invalid_argument("ISNM event is NULL");
	if (!isnm_event->eed_loc_info) throw std::invalid_argument("EED location info is NULL");
	if (!isnm_event->encl_mtms) throw std::invalid_argument("Enclosure MTMS is NULL");
	if (!isnm_event->pwr_ctrl_mtms) throw std::invalid_argument("Power controlling MTMS is NULL");
	if ((isnm_event->neighbor_loc_type && !isnm_event->neighbor_loc_code) || (!isnm_event->neighbor_loc_type && isnm_event->neighbor_loc_code))
		throw std::invalid_argument("Location is invalid");
	if (!isnm_event->recovery_file_path) throw std::invalid_argument("Recovery file path is NULL");
	if ((isnm_event->isnm_raw_data_len > 0) && !isnm_event->isnm_raw_data) throw std::invalid_argument("Raw data is NULL");

	std::vector<std::string> fields;
	fields.push_back("rec_id");
	fields.push_back("eed_loc_info");
	fields.push_back("encl_mtms");
	fields.push_back("pwr_ctrl_mtms");
	fields.push_back("neighbor_loc_type");
	fields.push_back("neighbor_loc");
	fields.push_back("recovery_file_path");
	fields.push_back("isnm_raw_data");
	fields.push_back("local_port");
	fields.push_back("local_torrent");
	fields.push_back("local_planar");
	fields.push_back("local_om1");
	fields.push_back("local_om2");
	fields.push_back("nbr_port");
	fields.push_back("nbr_torrent");
	fields.push_back("nbr_planar");
	fields.push_back("nbr_om1");
	fields.push_back("nbr_om2");
	fields.push_back("global_counter");

	std::string tableName = dbi.getTablePrefix() + ISNM_TABLE_NAME;
	ivInsertSql = dbi.genSubtableInsert(fields,tableName);
}

DbIsnmEvent::~DbIsnmEvent()
{
	// Nothing to do
}

void DbIsnmEvent::insert(SQLHSTMT sqlStmt)
{
	SQLRETURN ret;

	SQLLEN eedLocInfoLen = SQL_NTS;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, EED_LOC_INFO_SIZE, 0, ivIsnmEvent->eed_loc_info, 0, &eedLocInfoLen);
    DbInterface::checkSqlRetcode("SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN enclMtmsLen = SQL_NTS;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, ENCL_MTMS_SIZE, 0, ivIsnmEvent->encl_mtms, 0, &enclMtmsLen);
	DbInterface::checkSqlRetcode("SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN pwrCtrlMtmsLen = SQL_NTS;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 3, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, PWR_CTRL_MTMS_SIZE, 0, ivIsnmEvent->pwr_ctrl_mtms, 0, &pwrCtrlMtmsLen);
	DbInterface::checkSqlRetcode("SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN neighborLocTypeLen = ivIsnmEvent->neighbor_loc_type ? SQL_NTS : SQL_NULL_DATA;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 4, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, NEIGHBOR_LOC_TYPE_SIZE, 0, ivIsnmEvent->neighbor_loc_type, 0, &neighborLocTypeLen);
	DbInterface::checkSqlRetcode("SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN neighborLocLen = ivIsnmEvent->neighbor_loc_code ? SQL_NTS : SQL_NULL_DATA;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 5, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, NEIGHBOR_LOC_SIZE, 0, ivIsnmEvent->neighbor_loc_code, 0, &neighborLocLen);
	DbInterface::checkSqlRetcode("SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN recoveryFilePathLen = SQL_NTS;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 6, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, RECOVERY_FILE_PATH_SIZE, 0, ivIsnmEvent->recovery_file_path, 0, &recoveryFilePathLen);
	DbInterface::checkSqlRetcode("SQLBindParameter 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN isnmRawDataLen = ivIsnmEvent->isnm_raw_data_len > 0 ? ivIsnmEvent->isnm_raw_data_len : SQL_NULL_DATA;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 7, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, ISNM_RAW_DATA_SIZE, 0, ivIsnmEvent->isnm_raw_data, 0, &isnmRawDataLen);
	DbInterface::checkSqlRetcode("SQLBindParameter 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN localPortLen = ivIsnmEvent->local_port ? SQL_NTS : SQL_NULL_DATA;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 8, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, LOCAL_PORT_SIZE, 0, ivIsnmEvent->local_port, 0, &localPortLen);
	DbInterface::checkSqlRetcode("SQLBindParameter 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN localTorrentLen = ivIsnmEvent->local_torrent ? SQL_NTS : SQL_NULL_DATA;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 9, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, LOCAL_TORRENT_SIZE, 0, ivIsnmEvent->local_torrent, 0, &localTorrentLen);
	DbInterface::checkSqlRetcode("SQLBindParameter 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN localPlanarLen = ivIsnmEvent->local_planar ? SQL_NTS : SQL_NULL_DATA;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 10, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, LOCAL_PLANAR_SIZE, 0, ivIsnmEvent->local_planar, 0, &localPlanarLen);
	DbInterface::checkSqlRetcode("SQLBindParameter 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN localOm1Len = ivIsnmEvent->local_om1 ? SQL_NTS : SQL_NULL_DATA;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 11, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, LOCAL_OM1_SIZE, 0, ivIsnmEvent->local_om1, 0, &localOm1Len);
	DbInterface::checkSqlRetcode("SQLBindParameter 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN localOm2Len = ivIsnmEvent->local_om2 ? SQL_NTS : SQL_NULL_DATA;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 12, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, LOCAL_OM2_SIZE, 0, ivIsnmEvent->local_om2, 0, &localOm2Len);
	DbInterface::checkSqlRetcode("SQLBindParameter 12 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN nbrPortLen = ivIsnmEvent->nbr_port ? SQL_NTS : SQL_NULL_DATA;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 13, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, NBR_PORT_SIZE, 0, ivIsnmEvent->nbr_port, 0, &nbrPortLen);
	DbInterface::checkSqlRetcode("SQLBindParameter 13 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN nbrTorrentLen = ivIsnmEvent->nbr_torrent ? SQL_NTS : SQL_NULL_DATA;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 14, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, NBR_TORRENT_SIZE, 0, ivIsnmEvent->nbr_torrent, 0, &nbrTorrentLen);
	DbInterface::checkSqlRetcode("SQLBindParameter 14 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN nbrPlanarLen = ivIsnmEvent->nbr_planar ? SQL_NTS : SQL_NULL_DATA;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 15, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, NBR_PLANAR_SIZE, 0, ivIsnmEvent->nbr_planar, 0, &nbrPlanarLen);
	DbInterface::checkSqlRetcode("SQLBindParameter 15 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN nbrOm1Len = ivIsnmEvent->nbr_om1 ? SQL_NTS : SQL_NULL_DATA;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 16, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, NBR_OM1_SIZE, 0, ivIsnmEvent->nbr_om1, 0, &nbrOm1Len);
	DbInterface::checkSqlRetcode("SQLBindParameter 16 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN nbrOm2Len = ivIsnmEvent->nbr_om2 ? SQL_NTS : SQL_NULL_DATA;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 17, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, NBR_OM2_SIZE, 0, ivIsnmEvent->nbr_om2, 0, &nbrOm2Len);
	DbInterface::checkSqlRetcode("SQLBindParameter 17 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

	SQLLEN globalCounterLen = ivIsnmEvent->global_counter ? 0 : SQL_NULL_DATA;
	ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 18, SQL_PARAM_INPUT, SQL_C_SBIGINT, SQL_BIGINT, 0, 0, ivIsnmEvent->global_counter, 0, &globalCounterLen);
	DbInterface::checkSqlRetcode("SQLBindParameter 18 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

	// Preparation complete - execute the insert

   	ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)ivInsertSql.c_str(), SQL_NTS);
    DbInterface::checkSqlRetcode("DbObject::insert SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);
}

}
