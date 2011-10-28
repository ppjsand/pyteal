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
#include "DbDiskEvent.h"
#include "teal_gpfs_connect.h"
#include "DbInterface.h"

#include <vector>

namespace TEAL
{

enum DiskEventColumnSizes
{
    SEVERITY_SIZE       = 256,
    FS_NAME_SIZE        = 256,
    NODE_NAME_SIZE      = 256,
    NODE_IP_SIZE        = 256,
    STATUS_SIZE         = 256,
    AVALABILITY_SIZE    = 256,
    FG_NAME_SIZE        = 256,
    META_SIZE           = 256,
    DATA_SIZE           = 256,
    CMD_SIZE            = 256,
    MY_ROLE_SIZE        = 256,
    CK_REASON_SIZE      = 256,
    OTHER_NODE_SIZE     = 256,
    DATA_LEN_SIZE       = 4,
    ERR_CNT_CLIENT_SIZE = 4,
    ERR_CNT_SERV_SIZE   = 4,
    ERR_CNT_NSD_SIZE    = 4,
    RPT_INTERVAL_SIZE   = 4,
    IO_LENGTH_SIZE      = 4,
    IO_TIME_SIZE        = 4,
    START_SECTOR_SIZE   = 8,
};

const std::string GPFS_DISK_TABLE_NAME("GPFS_1_2");
}

namespace TEAL {

DbDiskEvent::DbDiskEvent(DbInterface& dbi, tlgpfs_disk_event* gpfs_disk_event) : DbEvent(dbi), ivGpfsEvent(gpfs_disk_event)
{
    if (!gpfs_disk_event) throw std::invalid_argument("GPFS disk event is NULL");
    if (!gpfs_disk_event->severity) throw std::invalid_argument("Severity is NULL");
    if (!gpfs_disk_event->fs_name) throw std::invalid_argument("File system name is NULL");

    std::vector<std::string> fields;
    fields.push_back("rec_id");
    fields.push_back("severity");
    fields.push_back("fs_name");
    fields.push_back("node_name");
    fields.push_back("node_ip");
    fields.push_back("status");
    fields.push_back("availability");
    fields.push_back("fg_name");
    fields.push_back("meta");
    fields.push_back("data");
    fields.push_back("cmd");
    fields.push_back("my_role");
    fields.push_back("ck_reason");
    fields.push_back("other_node");
    fields.push_back("data_len");
    fields.push_back("err_cnt_client");
    fields.push_back("err_cnt_serv");
    fields.push_back("err_cnt_nsd");
    fields.push_back("rpt_interval");
    fields.push_back("io_length");
    fields.push_back("io_time");
    fields.push_back("start_sector");

    std::string tableName = dbi.getTablePrefix() + GPFS_DISK_TABLE_NAME;
    ivInsertSql = dbi.genSubtableInsert(fields,tableName);
}

DbDiskEvent::~DbDiskEvent()
{
    // Nothing to do
}

void DbDiskEvent::insert(SQLHSTMT sqlStmt)
{
    SQLRETURN ret;
    
    SQLLEN severityLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, SEVERITY_SIZE, 0, ivGpfsEvent->severity, 0, &severityLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN fsNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, FS_NAME_SIZE, 0, ivGpfsEvent->fs_name, 0, &fsNameLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN nodeNameLen = ivGpfsEvent->node_name ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 3, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, NODE_NAME_SIZE, 0, ivGpfsEvent->node_name, 0, &nodeNameLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN nodeIpLen = ivGpfsEvent->node_ip ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 4, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, NODE_IP_SIZE, 0, ivGpfsEvent->node_ip, 0, &nodeIpLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN statusLen = ivGpfsEvent->status ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 5, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, STATUS_SIZE, 0, ivGpfsEvent->status, 0, &statusLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN availabilityLen = ivGpfsEvent->availability ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 6, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, AVALABILITY_SIZE, 0, ivGpfsEvent->availability, 0, &availabilityLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN fgNameLen = ivGpfsEvent->fg_name ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 7, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, FG_NAME_SIZE, 0, ivGpfsEvent->fg_name, 0, &fgNameLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN metaLen = ivGpfsEvent->meta ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 8, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, META_SIZE, 0, ivGpfsEvent->meta, 0, &metaLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN dataLen = ivGpfsEvent->data ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 9, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, DATA_SIZE, 0, ivGpfsEvent->data, 0, &dataLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN cmdLen = ivGpfsEvent->cmd ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 10, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CMD_SIZE, 0, ivGpfsEvent->cmd, 0, &cmdLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);    

    SQLLEN myRoleLen = ivGpfsEvent->my_role ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 11, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, MY_ROLE_SIZE, 0, ivGpfsEvent->my_role, 0, &myRoleLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);  

    SQLLEN ckReasonLen = ivGpfsEvent->ck_reason ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 12, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CK_REASON_SIZE, 0, ivGpfsEvent->ck_reason, 0, &ckReasonLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 12 STMT",ret,sqlStmt,SQL_HANDLE_STMT);  

    SQLLEN otherNodeLen = ivGpfsEvent->other_node ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 13, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, OTHER_NODE_SIZE, 0, ivGpfsEvent->other_node, 0, &otherNodeLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 13 STMT",ret,sqlStmt,SQL_HANDLE_STMT);  

    SQLLEN dataLenLen = ivGpfsEvent->data_len ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 14, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, ivGpfsEvent->data_len, 0, &dataLenLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 14 STMT",ret,sqlStmt,SQL_HANDLE_STMT);  

    SQLLEN errCntClientLen = ivGpfsEvent->err_cnt_client ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 15, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, ivGpfsEvent->err_cnt_client, 0, &errCntClientLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 15 STMT",ret,sqlStmt,SQL_HANDLE_STMT);  

    SQLLEN errCntServLen = ivGpfsEvent->err_cnt_serv ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 16, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, ivGpfsEvent->err_cnt_serv, 0, &errCntServLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 16 STMT",ret,sqlStmt,SQL_HANDLE_STMT);  

    SQLLEN errCntNsdLen = ivGpfsEvent->err_cnt_nsd ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 17, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, ivGpfsEvent->err_cnt_nsd, 0, &errCntNsdLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 17 STMT",ret,sqlStmt,SQL_HANDLE_STMT);  

    SQLLEN rptIntervalLen = ivGpfsEvent->rpt_interval ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 18, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, ivGpfsEvent->rpt_interval, 0, &rptIntervalLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 18 STMT",ret,sqlStmt,SQL_HANDLE_STMT);  

    SQLLEN ioLengthLen = ivGpfsEvent->io_length ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 19, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, ivGpfsEvent->io_length, 0, &ioLengthLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 19 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
 
    SQLLEN ioTimeLen = ivGpfsEvent->io_time ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 20, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, ivGpfsEvent->io_time, 0, &ioTimeLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 20 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN startSectorLen = ivGpfsEvent->start_sector ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 21, SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, ivGpfsEvent->start_sector, 0, &startSectorLen);
    DbInterface::checkSqlRetcode("DbDiskEvent::SQLBindParameter 21 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)ivInsertSql.c_str(), SQL_NTS);
    DbInterface::checkSqlRetcode("DbDiskEvent::insert SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);


}

}

