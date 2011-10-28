// begin_generated_IBM_copyright_prolog
//
// This is an automatically generated copyright prolog.
// After initializing,  DO NOT MODIFY OR MOVE
// ================================================================
//
// (C) Copyright IBM Corp.  2011     
// Eclipse Public License (EPL)
//
// ================================================================
//
// end_generated_IBM_copyright_prolog
#include "DbMiscEvent.h"
#include "teal_gpfs_connect.h"
#include "DbInterface.h"

#include <vector>

namespace TEAL
{

enum MiscEventColumnSizes
{
    SEVERITY_SIZE   = 256,
    MSG_TEXT_SIZE   = 256,
    DIAGNOSIS_SIZE  = 256,
    WAIT_TIME_SIZE  = 4,
    MSG_LEVEL_SIZE  = 4,
};

const std::string GPFS_MISC_TABLE_NAME("GPFS_1_4");
}

namespace TEAL {

DbMiscEvent::DbMiscEvent(DbInterface& dbi, tlgpfs_misc_event* gpfs_misc_event) : DbEvent(dbi), ivGpfsEvent(gpfs_misc_event)
{
    if (!gpfs_misc_event) throw std::invalid_argument("GPFS event is NULL");
    if (!gpfs_misc_event->severity) throw std::invalid_argument("Severity is NULL");
    
    std::vector<std::string> fields;
    fields.push_back("rec_id");
    fields.push_back("severity");
    fields.push_back("msg_text");
    fields.push_back("diagnosis");
    fields.push_back("wait_time");
    fields.push_back("msg_level");

    std::string tableName = dbi.getTablePrefix() + GPFS_MISC_TABLE_NAME;
    ivInsertSql = dbi.genSubtableInsert(fields,tableName);
}

DbMiscEvent::~DbMiscEvent()
{
    // Nothing to do
}

void DbMiscEvent::insert(SQLHSTMT sqlStmt)
{
    SQLRETURN ret;
    
    SQLLEN severityLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, SEVERITY_SIZE, 0, ivGpfsEvent->severity, 0, &severityLen);
    DbInterface::checkSqlRetcode("DbMiscEvent::SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN msgTextLen = ivGpfsEvent->msg_text ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, MSG_TEXT_SIZE, 0, ivGpfsEvent->msg_text, 0, &msgTextLen);
    DbInterface::checkSqlRetcode("DbMiscEvent::SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN diagnosisLen = ivGpfsEvent->diagnosis ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 3, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, DIAGNOSIS_SIZE, 0, ivGpfsEvent->diagnosis, 0, &diagnosisLen);
    DbInterface::checkSqlRetcode("DbMiscEvent::SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN waitTimeLen = ivGpfsEvent->wait_time ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 4, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, ivGpfsEvent->wait_time, 0, &waitTimeLen);
    DbInterface::checkSqlRetcode("DbMiscEvent::SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN msgLevelLen = ivGpfsEvent->msg_level ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 5, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, ivGpfsEvent->msg_level, 0, &msgLevelLen);
    DbInterface::checkSqlRetcode("DbMiscEvent::SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)ivInsertSql.c_str(), SQL_NTS);
    DbInterface::checkSqlRetcode("DbMiscEvent::insert SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

}

