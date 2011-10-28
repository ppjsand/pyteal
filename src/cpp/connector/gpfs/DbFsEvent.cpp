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
#include "DbFsEvent.h"
#include "teal_gpfs_connect.h"
#include "DbInterface.h"

#include <vector>

namespace TEAL {

DbFsEvent::DbFsEvent(DbInterface& dbi, tlgpfs_fs_event* gpfs_fs_event) : DbEvent(dbi), ivGpfsEvent(gpfs_fs_event)
{
    if (!gpfs_fs_event) throw std::invalid_argument("GPFS event is NULL");
    if (!gpfs_fs_event->severity) throw std::invalid_argument("Severity is NULL");
    
    std::vector<std::string> fields;
    fields.push_back("rec_id");
    fields.push_back("severity");
    fields.push_back("node_ip");
    fields.push_back("sgmgr_ip");
    fields.push_back("user_unba");
    fields.push_back("meta_unba");
    fields.push_back("user_ill_rep");
    fields.push_back("meta_ill_rep");
    fields.push_back("user_exposed");
    fields.push_back("meta_exposed");
    fields.push_back("pool_name");
    fields.push_back("pool_status");
    fields.push_back("pool_usage");

    std::string tableName = dbi.getTablePrefix() + GPFS_FS_TABLE_NAME;
    ivInsertSql = dbi.genSubtableInsert(fields,tableName);
}

DbFsEvent::~DbFsEvent()
{
    // Nothing to do
}

void DbFsEvent::insert(SQLHSTMT sqlStmt)
{
    SQLRETURN ret;
    
    SQLLEN severityLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, SEVERITY_SIZE, 0, ivGpfsEvent->severity, 0, &severityLen);
    DbInterface::checkSqlRetcode("DbFsEvent::SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN nodeIpLen = ivGpfsEvent->node_ip ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, NODE_IP_SIZE, 0, ivGpfsEvent->node_ip, 0, &nodeIpLen);
    DbInterface::checkSqlRetcode("DbFsEvent::SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN sgmgrIpLen = ivGpfsEvent->sgmgr_ip ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 3, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, SGMGR_IP_SIZE, 0, ivGpfsEvent->sgmgr_ip, 0, &sgmgrIpLen);
    DbInterface::checkSqlRetcode("DbFsEvent::SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN userUnbaLen = ivGpfsEvent->user_unbalanced ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 4, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, USER_UNBA_SIZE, 0, ivGpfsEvent->user_unbalanced, 0, &userUnbaLen);
    DbInterface::checkSqlRetcode("DbFsEvent::SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN metaUnbaLen = ivGpfsEvent->meta_unbalanced ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 5, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, META_UNBA_SIZE, 0, ivGpfsEvent->meta_unbalanced, 0, &metaUnbaLen);
    DbInterface::checkSqlRetcode("DbFsEvent::SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN userIllRepLen = ivGpfsEvent->user_ill_rep ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 6, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, USER_ILL_REP_SIZE, 0, ivGpfsEvent->user_ill_rep, 0, &userIllRepLen);
    DbInterface::checkSqlRetcode("DbFsEvent::SQLBindParameter 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN metaIllRepLen = ivGpfsEvent->meta_ill_rep ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 7, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, META_ILL_REP_SIZE, 0, ivGpfsEvent->meta_ill_rep, 0, &metaIllRepLen);
    DbInterface::checkSqlRetcode("DbFsEvent::SQLBindParameter 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN userExposedLen = ivGpfsEvent->user_exposed ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 8, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, USER_EXPOSED_SIZE, 0, ivGpfsEvent->user_exposed, 0, &userExposedLen);
    DbInterface::checkSqlRetcode("DbFsEvent::SQLBindParameter 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN metaExposedLen = ivGpfsEvent->meta_exposed ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 9, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, META_EXPOSED_SIZE, 0, ivGpfsEvent->meta_exposed, 0, &metaExposedLen);
    DbInterface::checkSqlRetcode("DbFsEvent::SQLBindParameter 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN poolNameLen = ivGpfsEvent->pool_name ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 10, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, POOL_NAME_SIZE, 0, ivGpfsEvent->pool_name, 0, &poolNameLen);
    DbInterface::checkSqlRetcode("DbFsEvent::SQLBindParameter 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN poolStatusLen = ivGpfsEvent->pool_status ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 11, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, POOL_STATUS_SIZE, 0, ivGpfsEvent->pool_status, 0, &poolStatusLen);
    DbInterface::checkSqlRetcode("DbFsEvent::SQLBindParameter 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN poolUsageLen = ivGpfsEvent->pool_usage ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 12, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, ivGpfsEvent->pool_usage, 0, &poolUsageLen);
    DbInterface::checkSqlRetcode("DbFsEvent::SQLBindParameter 12 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)ivInsertSql.c_str(), SQL_NTS);
    DbInterface::checkSqlRetcode("DbFsEvent::insert SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

}
