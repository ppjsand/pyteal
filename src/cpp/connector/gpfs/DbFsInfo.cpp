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
#include "DbFsInfo.h"
#include <iomanip>
namespace TEAL
{
DbFsInfo::DbFsInfo(DbInterface* dbi, vector<string>* cols, vector<string>* pk, tlgpfs_fs_info_t* fs):DbGpfsInfo(dbi,REGULAR_FS_TABLE,TMP_FS_TABLE,cols,pk,fs)
{ 
    if (fs)
    {
        if (!fs->cluster_id) throw std::invalid_argument("Cluster id is NULL");
        if (!fs->fs_name) throw std::invalid_argument("FS name is NULL");
        if (!fs->change) throw std::invalid_argument("Change is NULL");
        if (!fs->health) throw std::invalid_argument("health is NULL");
    }
    if(cols)
    {
        cols->push_back("cluster_id");
        cols->push_back("fs_name");
        cols->push_back("manager");
        cols->push_back("status");
        cols->push_back("x_status");
        cols->push_back("pool_ref_time");
        cols->push_back("total_space");
        cols->push_back("total_inodes");
        cols->push_back("free_inodes");    
        cols->push_back("free_space");    
        cols->push_back("full_blk_space");
        cols->push_back("sub_blk_space");
        cols->push_back("stg_pool_num");
        cols->push_back("num_mgmt");
        cols->push_back("read_duration");
        cols->push_back("num_mnt_nodes");
        cols->push_back("num_policies");
        cols->push_back("write_duration");
        cols->push_back("was_updated");
        cols->push_back("num_mgr_chg");
        cols->push_back("change");
        cols->push_back("health");
    }
    
    if(pk)
    {
        pk->push_back("cluster_id");
        pk->push_back("fs_name");
    }
}

DbFsInfo::~DbFsInfo()
{
}

void DbFsInfo::getResult(SQLHSTMT sqlStmt,void** holder)
{
    SQLRETURN ret;
    *holder = new vector<tlgpfs_fs_info_t*>;
    vector<tlgpfs_fs_info_t*>* status = (vector<tlgpfs_fs_info_t*>*)* holder;
    tlgpfs_fs_info_t* tmp = allocateMemory();

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 1, SQL_C_CHAR, tmp->cluster_id, CLUSTER_ID_SIZE, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN fsNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 2, SQL_C_CHAR, tmp->fs_name, FS_NAME_SIZE, &fsNameLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN managerLen = tmp->manager ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 3, SQL_C_CHAR, tmp->manager, MANAGER_SIZE, &managerLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN statusLen = tmp->status ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 4, SQL_C_CHAR, tmp->status, STATUS_SIZE, &statusLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN xStatusLen = tmp->x_status ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 5, SQL_C_CHAR, tmp->x_status, X_STATUS_SIZE, &xStatusLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN poolRefTimeLen = tmp->pool_ref_time ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 6, SQL_C_CHAR, tmp->pool_ref_time, POOL_REF_TIME_SIZE, &poolRefTimeLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN totalSpaceLen = tmp->total_space ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 7, SQL_C_UBIGINT, tmp->total_space, 0, &totalSpaceLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN totalInodesLen = tmp->total_inodes ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 8, SQL_C_UBIGINT, tmp->total_inodes, 0, &totalInodesLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN freeInodesLen = tmp->free_inodes ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 9, SQL_C_UBIGINT, tmp->free_inodes, 0, &freeInodesLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN freeSpaceLen = tmp->free_space ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 10, SQL_C_UBIGINT, tmp->free_space, 0, &freeSpaceLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN fullBlkSpaceLen = tmp->full_blk_space ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 11, SQL_C_UBIGINT, tmp->full_blk_space, 0, &fullBlkSpaceLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN subBlkSpaceLen = tmp->sub_blk_space ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 12, SQL_C_UBIGINT, tmp->sub_blk_space, 0, &subBlkSpaceLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 12 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN stgPoolNumLen = tmp->stg_pool_num ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 13, SQL_C_SLONG, tmp->stg_pool_num, 0, &stgPoolNumLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 13 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN numMgmtLen = tmp->num_mgmt ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 14, SQL_C_SLONG, tmp->num_mgmt, 0, &numMgmtLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 14 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN readDurationLen = tmp->read_duration ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 15, SQL_C_SLONG, tmp->read_duration, 0, &readDurationLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 15 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN numMntNodesLen = tmp->num_mnt_nodes ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 16, SQL_C_SLONG, tmp->num_mnt_nodes, 0, &numMntNodesLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 16 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN numPoliciesLen = tmp->num_policies ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 17, SQL_C_SLONG, tmp->num_policies, 0, &numPoliciesLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 17 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN writeDurationLen = tmp->write_duration ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 18, SQL_C_SLONG, tmp->write_duration, 0, &writeDurationLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 18 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN wasUpdatedLen = tmp->was_updated ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 19, SQL_C_SLONG,tmp->was_updated, 0, &wasUpdatedLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 19 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN numMgrChgLen = tmp->num_mgr_chg ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 20, SQL_C_SLONG, tmp->num_mgr_chg, 0, &numMgrChgLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 20 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN changeLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 21, SQL_C_SLONG, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 21 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 22, SQL_C_SLONG, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLBindCol 22 STMT",ret,sqlStmt,SQL_HANDLE_STMT);    
    
    ret = DbInterface::dbModule.SQLFetch(sqlStmt);
    if(ret != SQL_NO_DATA)//don't roll back even if empty row.
        DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    
    while((ret == SQL_SUCCESS || ret == SQL_SUCCESS_WITH_INFO))
    {
        
        tlgpfs_fs_info_t* temp = allocateMemory();
        copyInfo(temp,tmp);
        status->push_back(temp);
        resetMemory(tmp);
        ret = DbInterface::dbModule.SQLFetch(sqlStmt);
        if(ret != SQL_NO_DATA)//don't roll back even if empty row.
            DbInterface::checkSqlRetcode("DbFsInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    }

}

tlgpfs_fs_info_t* DbFsInfo::extract(FilesystemInfo* fsInfo, string& clusterId)
{
    if(fsInfo == NULL)
        return NULL;
    tlgpfs_fs_info* tmpFsInfo = allocateMemory();
    
    strcpy(tmpFsInfo->cluster_id, clusterId.c_str());
    strcpy(tmpFsInfo->fs_name, fsInfo->getName());
    strcpy(tmpFsInfo->manager, fsInfo->getManager());
    strcpy(tmpFsInfo->status, fsInfo->getStatus());
    strcpy(tmpFsInfo->x_status, fsInfo->getXstatus());
    struct timeval pool_ref_time = fsInfo->getPoolRefreshTime();
    Utils::timeval_to_char(&pool_ref_time,tmpFsInfo->pool_ref_time);
    *tmpFsInfo->total_space     = fsInfo->getTotalSpace();
    *tmpFsInfo->total_inodes    = fsInfo->getNumTotalInodes();
    *tmpFsInfo->free_inodes     = fsInfo->getNumFreeInodes();
    *tmpFsInfo->free_space      = fsInfo->getFreeSpace();
    *tmpFsInfo->full_blk_space  = fsInfo->getFullBlockFreeSpace();
    *tmpFsInfo->sub_blk_space   = fsInfo->getSubBlockFreeSpace();
    *tmpFsInfo->stg_pool_num    = fsInfo->getNumStoragePools();
    *tmpFsInfo->num_mgmt        = fsInfo->getNumMgmt();
    *tmpFsInfo->read_duration   = fsInfo->getReadDuration();
    *tmpFsInfo->num_mnt_nodes   = fsInfo->getNumMountedNodes();
    *tmpFsInfo->num_policies    = fsInfo->getNumPolicies();
    *tmpFsInfo->write_duration  = fsInfo->getWriteDuration();
    *tmpFsInfo->was_updated     = fsInfo->wasUpdated();    
    *tmpFsInfo->num_mgr_chg     = fsInfo->getNumMgrChange();

    return tmpFsInfo;

}

tlgpfs_fs_info_t* DbFsInfo::allocateMemory()
{
    tlgpfs_fs_info* tmpFsInfo = new tlgpfs_fs_info();
    
    tmpFsInfo->cluster_id        = new char[CLUSTER_ID_SIZE];
    memset(tmpFsInfo->cluster_id, 0, CLUSTER_ID_SIZE);

    tmpFsInfo->fs_name           = new char[FS_NAME_SIZE];
    memset(tmpFsInfo->fs_name, 0, FS_NAME_SIZE);

    tmpFsInfo->manager           = new char[MANAGER_SIZE];
    memset(tmpFsInfo->manager, 0, MANAGER_SIZE);
    
    tmpFsInfo->status            = new char[STATUS_SIZE];
    memset(tmpFsInfo->status, 0, STATUS_SIZE);
    
    tmpFsInfo->x_status          = new char[X_STATUS_SIZE];
    memset(tmpFsInfo->x_status, 0, X_STATUS_SIZE);
        
    tmpFsInfo->pool_ref_time     = new char[POOL_REF_TIME_SIZE];
    memset(tmpFsInfo->pool_ref_time, 0, POOL_REF_TIME_SIZE);
    
    tmpFsInfo->total_space       = new unsigned long long;
    memset(tmpFsInfo->total_space, 0, sizeof( unsigned long long));
    
    tmpFsInfo->total_inodes       = new unsigned long long;
    memset(tmpFsInfo->total_inodes, 0, sizeof( unsigned long long));
    
    tmpFsInfo->free_inodes       = new unsigned long long;
    memset(tmpFsInfo->free_inodes, 0, sizeof( unsigned long long));
    
    tmpFsInfo->free_space        = new unsigned long long;
    memset(tmpFsInfo->free_space, 0, sizeof( unsigned long long));
    
    tmpFsInfo->full_blk_space    = new unsigned long long;
    memset(tmpFsInfo->full_blk_space, 0, sizeof( unsigned long long));
    
    tmpFsInfo->sub_blk_space     = new unsigned long long;
    memset(tmpFsInfo->sub_blk_space, 0, sizeof( unsigned long long));
    
    tmpFsInfo->stg_pool_num      = new  int;
    memset(tmpFsInfo->stg_pool_num, 0, sizeof( int));

    tmpFsInfo->num_mgmt          = new  int;
    memset(tmpFsInfo->num_mgmt, 0, sizeof( int));
    
    tmpFsInfo->read_duration     = new  int;
    memset(tmpFsInfo->read_duration, 0, sizeof( int));
    
    tmpFsInfo->num_mnt_nodes     = new  int;
    memset(tmpFsInfo->num_mnt_nodes, 0, sizeof( int));
    
    tmpFsInfo->num_policies      = new  int;
    memset(tmpFsInfo->num_policies, 0, sizeof( int));
    
    tmpFsInfo->write_duration    = new  int;
    memset(tmpFsInfo->write_duration, 0, sizeof( int));
    
    tmpFsInfo->was_updated       = new  int;
    memset(tmpFsInfo->was_updated, 0, sizeof( int));
    
    tmpFsInfo->num_mgr_chg       = new  int;
    memset(tmpFsInfo->num_mgr_chg, 0, sizeof( int));

    tmpFsInfo->change            = new  int;
    memset(tmpFsInfo->change, 0, sizeof( int));

    tmpFsInfo->health            = new  int;
    memset(tmpFsInfo->health, 0, sizeof( int));    

    return tmpFsInfo;
    
}


void DbFsInfo::Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info)
{
    SQLRETURN ret;
    
    if(opType != UPDATE && opType != INSERT)
        return;
    tlgpfs_fs_info_t* tmp = (tlgpfs_fs_info_t*)info;

    int x = (opType == UPDATE) ? colSize - pkSize : 0;    

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN fsNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, FS_NAME_SIZE, 0, tmp->fs_name, 0, &fsNameLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN managerLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, MANAGER_SIZE, 0, tmp->manager, 0, &managerLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN statusLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, STATUS_SIZE, 0, tmp->status, 0, &statusLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN xStatusLen = tmp->x_status ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, X_STATUS_SIZE, 0, tmp->x_status, 0, &xStatusLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN poolRefTimeLen = tmp->pool_ref_time ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, POOL_REF_TIME_SIZE, 0, tmp->pool_ref_time, 0, &poolRefTimeLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN totalSpaceLen = tmp->total_space ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, tmp->total_space, 0, &totalSpaceLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN totalInodesLen = tmp->total_inodes ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, tmp->total_inodes, 0, &totalInodesLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN freeInodesLen = tmp->free_inodes ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, tmp->free_inodes, 0, &freeInodesLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN freeSpaceLen = tmp->free_space ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, tmp->free_space, 0, &freeSpaceLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN fullBlkSpaceLen = tmp->full_blk_space ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, tmp->full_blk_space, 0, &fullBlkSpaceLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN subBlkSpaceLen = tmp->sub_blk_space ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, tmp->sub_blk_space, 0, &subBlkSpaceLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 12 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN stgPoolNumLen = tmp->stg_pool_num ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->stg_pool_num, 0, &stgPoolNumLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 13 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN numMgmtLen = tmp->num_mgmt ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->num_mgmt, 0, &numMgmtLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 14 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN readDurationLen = tmp->read_duration ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->read_duration, 0, &readDurationLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 15 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN numMntNodesLen = tmp->num_mnt_nodes ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->num_mnt_nodes, 0, &numMntNodesLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 16 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN numPoliciesLen = tmp->num_policies ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->num_policies, 0, &numPoliciesLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 17 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN writeDurationLen = tmp->write_duration ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->write_duration, 0, &writeDurationLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 18 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN wasUpdatedLen = tmp->was_updated ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->was_updated, 0, &wasUpdatedLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 19 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN numMgrChgLen = tmp->num_mgr_chg ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->num_mgr_chg, 0, &numMgrChgLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 20 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN changeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 21 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLBindParameter 22 STMT",ret,sqlStmt,SQL_HANDLE_STMT);                

    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)upsertSql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbFsInfo::Upsert SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbFsInfo::copyInfo(tlgpfs_fs_info_t* dst, tlgpfs_fs_info_t* src)
{
    strcpy(dst->cluster_id, src->cluster_id);
    strcpy(dst->fs_name, src->fs_name);
    strcpy(dst->manager, src->manager);
    strcpy(dst->status, src->status);
    strcpy(dst->x_status, src->x_status);
    strcpy(dst->pool_ref_time, src->pool_ref_time);
    *dst->total_space      = *src->total_space;
    *dst->total_inodes     = *src->total_inodes;
    *dst->free_inodes      = *src->free_inodes;
    *dst->free_space       = *src->free_space;
    *dst->full_blk_space   = *src->full_blk_space;
    *dst->sub_blk_space    = *src->sub_blk_space;
    *dst->stg_pool_num     = *src->stg_pool_num;
    *dst->num_mgmt         = *src->num_mgmt;
    *dst->read_duration    = *src->read_duration;
    *dst->num_mnt_nodes    = *src->num_mnt_nodes;
    *dst->num_policies     = *src->num_policies;
    *dst->write_duration   = *src->write_duration;
    *dst->was_updated      = *src->was_updated;
    *dst->num_mgr_chg      = *src->num_mgr_chg;
    *dst->change           = *src->change;
    *dst->health           = *src->health;

}

void DbFsInfo::resetMemory(tlgpfs_fs_info* tmpFsInfo)
{
    if( tmpFsInfo == NULL )
        return;
    
    memset(tmpFsInfo->cluster_id, 0, CLUSTER_ID_SIZE);

    memset(tmpFsInfo->fs_name, 0, FS_NAME_SIZE);

    memset(tmpFsInfo->manager, 0, MANAGER_SIZE);
    
    memset(tmpFsInfo->status, 0, STATUS_SIZE);
    
    memset(tmpFsInfo->x_status, 0, X_STATUS_SIZE);
        
    memset(tmpFsInfo->pool_ref_time, 0, POOL_REF_TIME_SIZE);
    
    memset(tmpFsInfo->total_space, 0, sizeof( unsigned long long));
    
    memset(tmpFsInfo->total_inodes, 0, sizeof( unsigned long long));
    
    memset(tmpFsInfo->free_inodes, 0, sizeof( unsigned long long));
    
    memset(tmpFsInfo->free_space, 0, sizeof( unsigned long long));
    
    memset(tmpFsInfo->full_blk_space, 0, sizeof( unsigned long long));
    
    memset(tmpFsInfo->sub_blk_space, 0, sizeof( unsigned long long));
    
    memset(tmpFsInfo->stg_pool_num, 0, sizeof( int));

    memset(tmpFsInfo->num_mgmt, 0, sizeof( int));
    
    memset(tmpFsInfo->read_duration, 0, sizeof( int));
    
    memset(tmpFsInfo->num_mnt_nodes, 0, sizeof( int));
    
    memset(tmpFsInfo->num_policies, 0, sizeof( int));
    
    memset(tmpFsInfo->write_duration, 0, sizeof( int));
    
    memset(tmpFsInfo->was_updated, 0, sizeof( int));
    
    memset(tmpFsInfo->num_mgr_chg, 0, sizeof( int));

    memset(tmpFsInfo->change, 0, sizeof( int));

    memset(tmpFsInfo->health, 0, sizeof( int));        
}

void DbFsInfo::printStatus(tlgpfs_fs_info_t* fs, bool detailed)
{
    if(fs == NULL)
        cerr<<"Can't print a null structure of status!"<<endl;

    cout<<setiosflags(ios::left)<<setw(20)<<"cluster_id"     <<setiosflags(ios::left)<<setw(40)<<"(cluster id)"                            <<": "<< fs->cluster_id         <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"fs_name"        <<setiosflags(ios::left)<<setw(40)<<"(file system name)"                      <<": "<< fs->fs_name            <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"health"         <<setiosflags(ios::left)<<setw(40)<<"(health status)"                         <<": "<<string((*fs->health == HEALTHY)?"healthy":((*fs->health == UNHEALTHY)?"unhealthy":"unknown"))<<endl;    
    if(!detailed)
        return;
    cout<<setiosflags(ios::left)<<setw(20)<<"manager"        <<setiosflags(ios::left)<<setw(40)<<"(file system manager)"                   <<": "<<  fs->manager           <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"status"         <<setiosflags(ios::left)<<setw(40)<<"(file system status)"                    <<": "<<  fs->status            <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"x_status"       <<setiosflags(ios::left)<<setw(40)<<"(file system x status)"                  <<": "<<  fs->x_status          <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"pool_ref_time"  <<setiosflags(ios::left)<<setw(40)<<"(last storage pool data refresh time)"   <<": "<<  fs->pool_ref_time     <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"total_space"    <<setiosflags(ios::left)<<setw(40)<<"(total space)"                           <<": "<< *fs->total_space       <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"total_inodes"   <<setiosflags(ios::left)<<setw(40)<<"(total inodes)"                          <<": "<< *fs->total_inodes      <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"free_inodes"    <<setiosflags(ios::left)<<setw(40)<<"(free inodes)"                           <<": "<< *fs->free_inodes       <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"free_space"     <<setiosflags(ios::left)<<setw(40)<<"(free space)"                            <<": "<< *fs->free_space        <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"full_blk_space" <<setiosflags(ios::left)<<setw(40)<<"(full block space)"                      <<": "<< *fs->full_blk_space    <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"sub_blk_space"  <<setiosflags(ios::left)<<setw(40)<<"(sub block space)"                       <<": "<< *fs->sub_blk_space     <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"stg_pool_num"   <<setiosflags(ios::left)<<setw(40)<<"(storage pool items number)"             <<": "<< *fs->stg_pool_num      <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"num_mgmt"       <<setiosflags(ios::left)<<setw(40)<<"(management number)"                     <<": "<< *fs->num_mgmt          <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"read_duration"  <<setiosflags(ios::left)<<setw(40)<<"(read duration)"                         <<": "<< *fs->read_duration     <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"num_mnt_nodes"  <<setiosflags(ios::left)<<setw(40)<<"(mounted nodes items number)"            <<": "<< *fs->num_mnt_nodes     <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"num_policies"   <<setiosflags(ios::left)<<setw(40)<<"(policy itmes number)"                   <<": "<< *fs->num_policies      <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"write_duration" <<setiosflags(ios::left)<<setw(40)<<"(write duration)"                        <<": "<< *fs->write_duration    <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"was_updated"    <<setiosflags(ios::left)<<setw(40)<<"(if was updated)"                        <<": "<< *fs->was_updated       <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"num_mgr_chg"    <<setiosflags(ios::left)<<setw(40)<<"(file system manger changed number)"     <<": "<< *fs->num_mgr_chg       <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"change"         <<setiosflags(ios::left)<<setw(40)<<"(change value)"                          <<": "<< *fs->change            <<endl;

}

void DbFsInfo::bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init)
{
    SQLRETURN ret;
    int x = 1;
    tlgpfs_fs_info_t* tmp = (tlgpfs_fs_info_t*)info;

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbFsInfo::bindPrimaryKey SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN fsNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, FS_NAME_SIZE, 0, tmp->fs_name, 0, &fsNameLen);
    DbInterface::checkSqlRetcode("DbFsInfo::bindPrimaryKey SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    if( init )
    {
        int changeValue = 100;//init to 100
        int healthValue = 100;
        
        SQLLEN changeLen = SQL_NTS;    
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &changeValue, 0, &changeLen);
        DbInterface::checkSqlRetcode("DbFsInfo::bindPrimaryKey SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

        SQLLEN healthLen = SQL_NTS;        
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &healthValue, 0, &healthLen);
        DbInterface::checkSqlRetcode("DbFsInfo::bindPrimaryKey SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);    
    }
    
    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)sql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbFsInfo::bindPrimaryKey SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}


void DbFsInfo::updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst)
{
    vector<tlgpfs_fs_info_t*>* tempv = (vector<tlgpfs_fs_info_t*>*)temp;
    vector<tlgpfs_fs_info_t*>* lastv = (vector<tlgpfs_fs_info_t*>*)lst;
    tlgpfs_fs_info_t* last;
    tlgpfs_fs_info_t* tmp = tempv->front();
    *tmp->change = CHANGE_NA;
    bool isNew = false;
    if(tempv->size() > 0 && lastv->size() == 0)
    {
        isNew = true;
        *tmp->change = CHANGE_ADDED;
        last = allocateMemory();
        lastv->push_back(last);
    }
    else
    {
        last = lastv->front();
    }

   if(isNew)
       initTable(sqlStmt, table); //init regular table

   bool anyChange = false;
   
   anyChange |= strcmp(tmp->manager, last->manager);
   anyChange |= strcmp(tmp->status, last->status);
   anyChange |= strcmp(tmp->x_status, last->x_status);
   anyChange |= strcmp(tmp->pool_ref_time, last->pool_ref_time);
   anyChange |= memcmp(tmp->total_space, last->total_space, sizeof( long long));
   anyChange |= memcmp(tmp->total_inodes, last->total_inodes, sizeof( long long));
   anyChange |= memcmp(tmp->free_inodes, last->free_inodes, sizeof( long long));
   anyChange |= memcmp(tmp->free_space, last->free_space, sizeof( long long));
   anyChange |= memcmp(tmp->full_blk_space, last->full_blk_space, sizeof( long long));
   anyChange |= memcmp(tmp->sub_blk_space, last->sub_blk_space, sizeof( long long));   
   anyChange |= memcmp(tmp->stg_pool_num, last->stg_pool_num, sizeof( int));
   anyChange |= memcmp(tmp->num_mgmt, last->num_mgmt,sizeof( int));
   anyChange |= memcmp(tmp->read_duration, last->read_duration,sizeof( int));
   anyChange |= memcmp(tmp->num_mnt_nodes, last->num_mnt_nodes,sizeof( int));
   anyChange |= memcmp(tmp->num_policies, last->num_policies,sizeof( int));
   anyChange |= memcmp(tmp->write_duration, last->write_duration,sizeof( int));
   anyChange |= memcmp(tmp->was_updated, last->was_updated,sizeof( int));
   anyChange |= memcmp(tmp->num_mgr_chg, last->num_mgr_chg,sizeof( int));

   *tmp->change = anyChange?CHANGE_MODIFIED:CHANGE_NONE;
   // "status": possible values are "state_unknown" "needs_recovery" "recovering_phase1" "recovering_phase2" "recovering_phase3" "recovery_failed" "recovered" "Unknown SGStatus"
   //only when "status"=="recovered", declare it's healthy
   *tmp->health = strcmp(tmp->status,"recovered")?UNHEALTHY:HEALTHY;
   updateTable(sqlStmt,table,tmp);

}
}

