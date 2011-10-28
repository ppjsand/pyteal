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
#include "DbPerseusEvent.h"
#include "teal_gpfs_connect.h"
#include "DbInterface.h"

#include <vector>

namespace TEAL
{

enum PerseusEventColumnSizes
{
    SEVERITY_SIZE   = 256,
    NODE_NAME_SIZE  = 256,
    LOCATION_SIZE   = 256,
    FRU_SIZE        = 256,
    WWN_SIZE        = 256,
    STATE_SIZE      = 256,
    REASON_SIZE     = 256,
    DEV_NAME_SIZE   = 256,
    PRIORITY_SIZE   = 4,
    REM_REDUND_SIZE = 4,
    ERR_SIZE        = 4,
};

const std::string GPFS_PERSEUS_TABLE_NAME("GPFS_1_3");
}

namespace TEAL {

DbPerseusEvent::DbPerseusEvent(DbInterface& dbi, tlgpfs_perseus_event* gpfs_perseus_event) : DbEvent(dbi), ivGpfsEvent(gpfs_perseus_event)
{
    if (!gpfs_perseus_event) throw std::invalid_argument("GPFS event is NULL");
    if (!gpfs_perseus_event->severity) throw std::invalid_argument("Severity is NULL");
    if (!gpfs_perseus_event->node_name) throw std::invalid_argument("Node name is NULL");
    std::vector<std::string> fields;
    fields.push_back("rec_id");
    fields.push_back("severity");
    fields.push_back("node_name");
    fields.push_back("location");
    fields.push_back("fru");
    fields.push_back("wwn");
    fields.push_back("state");
    fields.push_back("reason");
    fields.push_back("dev_name");
    fields.push_back("priority");
    fields.push_back("rem_redund");
    fields.push_back("err");

    std::string tableName = dbi.getTablePrefix() + GPFS_PERSEUS_TABLE_NAME;
    ivInsertSql = dbi.genSubtableInsert(fields,tableName);
}

DbPerseusEvent::~DbPerseusEvent()
{
    // Nothing to do
}

void DbPerseusEvent::insert(SQLHSTMT sqlStmt)
{
    SQLRETURN ret;
    
    SQLLEN severityLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, SEVERITY_SIZE, 0, ivGpfsEvent->severity, 0, &severityLen);
    DbInterface::checkSqlRetcode("DbPerseusEvent::SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN nodeNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, NODE_NAME_SIZE, 0, ivGpfsEvent->node_name, 0, &nodeNameLen);
    DbInterface::checkSqlRetcode("DbPerseusEvent::SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN locationLen = ivGpfsEvent->location ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 3, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, LOCATION_SIZE, 0, ivGpfsEvent->location, 0, &locationLen);
    DbInterface::checkSqlRetcode("DbPerseusEvent::SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN fruLen = ivGpfsEvent->fru ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 4, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, FRU_SIZE, 0, ivGpfsEvent->fru, 0, &fruLen);
    DbInterface::checkSqlRetcode("DbPerseusEvent::SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN wwnLen = ivGpfsEvent->wwn ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 5, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, WWN_SIZE, 0, ivGpfsEvent->wwn, 0, &wwnLen);
    DbInterface::checkSqlRetcode("DbPerseusEvent::SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN stateLen = ivGpfsEvent->state ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 6, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, STATE_SIZE, 0, ivGpfsEvent->state, 0, &stateLen);
    DbInterface::checkSqlRetcode("DbPerseusEvent::SQLBindParameter 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN reasonLen = ivGpfsEvent->reason ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 7, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, REASON_SIZE, 0, ivGpfsEvent->reason, 0, &reasonLen);
    DbInterface::checkSqlRetcode("DbPerseusEvent::SQLBindParameter 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN devNameLen = ivGpfsEvent->dev_name ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 8, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, DEV_NAME_SIZE, 0, ivGpfsEvent->dev_name, 0, &devNameLen);
    DbInterface::checkSqlRetcode("DbPerseusEvent::SQLBindParameter 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN priorityLen = ivGpfsEvent->priority ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 9, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, ivGpfsEvent->priority, 0, &priorityLen);
    DbInterface::checkSqlRetcode("DbPerseusEvent::SQLBindParameter 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN remRedundLen = ivGpfsEvent->rem_redund ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 10, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, ivGpfsEvent->rem_redund, 0, &remRedundLen);
    DbInterface::checkSqlRetcode("DbPerseusEvent::SQLBindParameter 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN errLen = ivGpfsEvent->err ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 11, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, ivGpfsEvent->err, 0, &errLen);
    DbInterface::checkSqlRetcode("DbPerseusEvent::SQLBindParameter 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)ivInsertSql.c_str(), SQL_NTS);
    DbInterface::checkSqlRetcode("DbPerseusEvent::insert SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

}

