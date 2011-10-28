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
#include "DbDiskInfo.h"
#include <iomanip>

namespace TEAL
{
DbDiskInfo::DbDiskInfo(DbInterface* dbi, vector<string>* cols, vector<string>* pk, tlgpfs_disk_info_t* disk):DbGpfsInfo(dbi,REGULAR_DISK_TABLE,TMP_DISK_TABLE,cols,pk,disk)
{
    if (disk) 
    {
        if (!disk->cluster_id) throw std::invalid_argument("Cluster id is NULL");
        if (!disk->disk_name) throw std::invalid_argument("Disk name is NULL");
        if (!disk->change) throw std::invalid_argument("Change is NULL");
        if (!disk->health) throw std::invalid_argument("health is NULL");
    }
    if(cols)
    {
        cols->push_back("cluster_id");
        cols->push_back("disk_name");
        cols->push_back("node_name");
        cols->push_back("status");
        cols->push_back("availability");
        cols->push_back("pool_name");
        cols->push_back("vol_id");
        cols->push_back("meta_data");
        cols->push_back("data");
        cols->push_back("disk_wait");    
        cols->push_back("total_space");    
        cols->push_back("full_blk_space");
        cols->push_back("sub_blk_space");
        cols->push_back("fail_group_id");
        cols->push_back("is_free");
        cols->push_back("change");
        cols->push_back("health");
    }    
    if(pk)
    {
        pk->push_back("cluster_id");
        pk->push_back("disk_name");
    }
}

DbDiskInfo::~DbDiskInfo()
{
}

void DbDiskInfo::copyInfo(tlgpfs_disk_info_t* dst, tlgpfs_disk_info_t* src)
{
    strcpy(dst->cluster_id, src->cluster_id);
    strcpy(dst->disk_name, src->disk_name);
    strcpy(dst->node_name, src->node_name);
    strcpy(dst->status, src->status);
    strcpy(dst->availability, src->availability);
    strcpy(dst->pool_name, src->pool_name);
    strcpy(dst->vol_id, src->vol_id);
    strcpy(dst->meta_data, src->meta_data);
    strcpy(dst->data, src->data);
    strcpy(dst->disk_wait, src->disk_wait);
    *dst->total_space       = *src->total_space;
    *dst->full_blk_space    = *src->full_blk_space;
    *dst->sub_blk_space     = *src->sub_blk_space;
    *dst->fail_group_id     = *src->fail_group_id;
    *dst->is_free           = *src->is_free;
    *dst->change            = *src->change;
    *dst->health            = *src->health;

}

void DbDiskInfo::printStatus(tlgpfs_disk_info_t* disk, bool detailed)
{
    if(disk == NULL)
        cerr<<"Can't print a null structure of status!"<<endl;

    cout<<setiosflags(ios::left)<<setw(20)<<"cluster_id"     <<setiosflags(ios::left)<<setw(40)<<"(cluster id)"             <<": "<< disk->cluster_id      <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"disk_name"      <<setiosflags(ios::left)<<setw(40)<<"(disk name)"              <<": "<< disk->disk_name       <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"health"         <<setiosflags(ios::left)<<setw(40)<<"(health status)"          <<": "<<string((*disk->health == HEALTHY)?"healthy":((*disk->health == UNHEALTHY)?"unhealthy":"unknown"))<<endl;
    if(!detailed)
        return;
    cout<<setiosflags(ios::left)<<setw(20)<<"node_name"      <<setiosflags(ios::left)<<setw(40)<<"(node name)"              <<": "<< disk->node_name       <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"status"         <<setiosflags(ios::left)<<setw(40)<<"(disk status)"            <<": "<< disk->status          <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"availability"   <<setiosflags(ios::left)<<setw(40)<<"(disk availability)"      <<": "<< disk->availability    <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"pool_name"      <<setiosflags(ios::left)<<setw(40)<<"(storage pool name)"      <<": "<< disk->pool_name       <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"vol_id"         <<setiosflags(ios::left)<<setw(40)<<"(volume id)"              <<": "<< disk->vol_id          <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"meta_data"      <<setiosflags(ios::left)<<setw(40)<<"(disk meta data)"         <<": "<< disk->meta_data       <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"data"           <<setiosflags(ios::left)<<setw(40)<<"(disk data)"              <<": "<< disk->data            <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"disk_wait"      <<setiosflags(ios::left)<<setw(40)<<"(disk wait)"              <<": "<< disk->disk_wait       <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"total_space"    <<setiosflags(ios::left)<<setw(40)<<"(total space)"            <<": "<<*disk->total_space     <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"full_blk_space" <<setiosflags(ios::left)<<setw(40)<<"(full block space)"       <<": "<<*disk->full_blk_space  <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"sub_blk_space"  <<setiosflags(ios::left)<<setw(40)<<"(sub block space)"        <<": "<<*disk->sub_blk_space   <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"fail_group_id"  <<setiosflags(ios::left)<<setw(40)<<"(failure group id)"       <<": "<<*disk->fail_group_id   <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"is_free"        <<setiosflags(ios::left)<<setw(40)<<"(if is free)"             <<": "<<*disk->is_free         <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"change"         <<setiosflags(ios::left)<<setw(40)<<"(change value)"           <<": "<<*disk->change          <<endl;

}

void DbDiskInfo::getResult(SQLHSTMT sqlStmt,void** holder)
{
    SQLRETURN ret;
    *holder = new vector<tlgpfs_disk_info_t*>;
    vector<tlgpfs_disk_info_t*>* status = (vector<tlgpfs_disk_info_t*>*)* holder;
    tlgpfs_disk_info_t* tmp = allocateMemory();

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 1, SQL_C_CHAR, tmp->cluster_id, CLUSTER_ID_SIZE, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::getResult SQLBindCol 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN diskNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 2, SQL_C_CHAR, tmp->disk_name, DISK_NAME_SIZE, &diskNameLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::getResult SQLBindCol 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN nodeNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 3, SQL_C_CHAR, tmp->node_name, NODE_NAME_SIZE, &nodeNameLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::getResult SQLBindCol 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN statusLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 4, SQL_C_CHAR, tmp->status, STATUS_SIZE, &statusLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::getResult SQLBindCol 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN availabilityLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 5, SQL_C_CHAR, tmp->availability, AVAILABILITY_SIZE, &availabilityLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::getResult SQLBindCol 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN poolNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 6, SQL_C_CHAR, tmp->pool_name, POOL_NAME_SIZE, &poolNameLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::getResult SQLBindCol 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN volIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 7, SQL_C_CHAR, tmp->vol_id, VOL_ID_SIZE, &volIdLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::getResult SQLBindCol 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN metaDataLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 8, SQL_C_CHAR, tmp->meta_data, META_DATA_SIZE, &metaDataLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::getResult SQLBindCol 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN dataLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 9, SQL_C_CHAR, tmp->data, DATA_SIZE, &dataLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::getResult SQLBindCol 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN diskWaitLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 10, SQL_C_CHAR, tmp->disk_wait, DISK_WAIT_SIZE, &diskWaitLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::getResult SQLBindCol 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN totalSpaceLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 11, SQL_C_UBIGINT, tmp->total_space, 0, &totalSpaceLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::getResult SQLBindCol 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN fullBlkSpaceLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 12, SQL_C_UBIGINT, tmp->full_blk_space, 0, &fullBlkSpaceLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::getResult SQLBindCol 12 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN subBlkSpaceLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 13, SQL_C_UBIGINT, tmp->sub_blk_space, 0, &subBlkSpaceLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::getResult SQLBindCol 13 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN failGroupIdLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 14, SQL_C_SLONG, tmp->fail_group_id, 0, &failGroupIdLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::getResult SQLBindCol 14 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN isFreeLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 15, SQL_C_SLONG, tmp->is_free, 0, &isFreeLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::getResult SQLBindCol 15 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN changeLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 16, SQL_C_SLONG, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::getResult SQLBindCol 16 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 17, SQL_C_SLONG, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::getResult SQLBindCol 17 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    ret = DbInterface::dbModule.SQLFetch(sqlStmt);
    if(ret != SQL_NO_DATA)//don't roll back even if empty row.
        DbInterface::checkSqlRetcode("DbDiskInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    while((ret == SQL_SUCCESS || ret == SQL_SUCCESS_WITH_INFO))
    {
        
        tlgpfs_disk_info_t* temp = allocateMemory();
        copyInfo(temp,tmp);
        status->push_back(temp);
        resetMemory(tmp);
        ret = DbInterface::dbModule.SQLFetch(sqlStmt);
        if(ret != SQL_NO_DATA)//don't roll back even if empty row.
            DbInterface::checkSqlRetcode("DbDiskInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    }

}

tlgpfs_disk_info_t* DbDiskInfo::extract(DiskInfo* diskInfo, string& clusterId)
{
    if(diskInfo == NULL)
        return NULL;
    tlgpfs_disk_info* tmpDiskInfo = allocateMemory();
    
    strcpy(tmpDiskInfo->cluster_id, clusterId.c_str());
    strcpy(tmpDiskInfo->disk_name, diskInfo->getName());
    strcpy(tmpDiskInfo->node_name, diskInfo->getNodeName());
    strcpy(tmpDiskInfo->status, diskInfo->getStatus());
    strcpy(tmpDiskInfo->availability, diskInfo->getAvailability());
    strcpy(tmpDiskInfo->pool_name, diskInfo->getPoolName());
    strcpy(tmpDiskInfo->vol_id, diskInfo->getVolumeId());
    strcpy(tmpDiskInfo->meta_data, diskInfo->getMetadata());
    strcpy(tmpDiskInfo->data, diskInfo->getData());
    strcpy(tmpDiskInfo->disk_wait, diskInfo->getDiskWait());
    *tmpDiskInfo->total_space     = diskInfo->getTotalSpace();
    *tmpDiskInfo->full_blk_space  = diskInfo->getFullBlockFreeSpace();
    *tmpDiskInfo->sub_blk_space   = diskInfo->getSubBlockFreeSpace();
    *tmpDiskInfo->fail_group_id   = diskInfo->getFailureGroupId();
    *tmpDiskInfo->is_free         = diskInfo->isFree();

    return tmpDiskInfo;

}

void DbDiskInfo::resetMemory(tlgpfs_disk_info* tmpDiskInfo)
{
    if( tmpDiskInfo == NULL )
        return;
    
    memset(tmpDiskInfo->cluster_id, 0, CLUSTER_ID_SIZE);

    memset(tmpDiskInfo->disk_name, 0, DISK_NAME_SIZE);

    memset(tmpDiskInfo->node_name, 0, NODE_NAME_SIZE);
    
    memset(tmpDiskInfo->status, 0, STATUS_SIZE);
    
    memset(tmpDiskInfo->availability, 0, AVAILABILITY_SIZE);
    
    memset(tmpDiskInfo->pool_name, 0, POOL_NAME_SIZE);
    
    memset(tmpDiskInfo->vol_id, 0, VOL_ID_SIZE);
    
    memset(tmpDiskInfo->meta_data, 0, META_DATA_SIZE);
    
    memset(tmpDiskInfo->data, 0, DATA_SIZE);

    memset(tmpDiskInfo->disk_wait, 0, DISK_WAIT_SIZE);
    
    memset(tmpDiskInfo->total_space, 0, sizeof( unsigned long long));
    
    memset(tmpDiskInfo->full_blk_space, 0, sizeof( unsigned long long));
    
    memset(tmpDiskInfo->sub_blk_space, 0, sizeof( unsigned long long));
    
    memset(tmpDiskInfo->fail_group_id, 0, sizeof( int));

    memset(tmpDiskInfo->is_free, 0, sizeof( int));
    
    memset(tmpDiskInfo->change, 0, sizeof( int));

    memset(tmpDiskInfo->health, 0, sizeof( int));    
    
}

tlgpfs_disk_info_t* DbDiskInfo::allocateMemory()
{
    tlgpfs_disk_info* tmpDiskInfo = new tlgpfs_disk_info();
    
    tmpDiskInfo->cluster_id        = new char[CLUSTER_ID_SIZE];
    memset(tmpDiskInfo->cluster_id, 0, CLUSTER_ID_SIZE);

    tmpDiskInfo->disk_name         = new char[DISK_NAME_SIZE];
    memset(tmpDiskInfo->disk_name, 0, DISK_NAME_SIZE);

    tmpDiskInfo->node_name         = new char[NODE_NAME_SIZE];
    memset(tmpDiskInfo->node_name, 0, NODE_NAME_SIZE);
    
    tmpDiskInfo->status            = new char[STATUS_SIZE];
    memset(tmpDiskInfo->status, 0, STATUS_SIZE);
    
    tmpDiskInfo->availability      = new char[AVAILABILITY_SIZE];
    memset(tmpDiskInfo->availability, 0, AVAILABILITY_SIZE);
    
    tmpDiskInfo->pool_name         = new char[POOL_NAME_SIZE];
    memset(tmpDiskInfo->pool_name, 0, POOL_NAME_SIZE);
    
    tmpDiskInfo->vol_id            = new char[VOL_ID_SIZE];
    memset(tmpDiskInfo->vol_id, 0, VOL_ID_SIZE);
    
    tmpDiskInfo->meta_data         = new char[META_DATA_SIZE];
    memset(tmpDiskInfo->meta_data, 0, META_DATA_SIZE);
    
    tmpDiskInfo->data              = new char[DATA_SIZE];
    memset(tmpDiskInfo->data, 0, DATA_SIZE);

    tmpDiskInfo->disk_wait         = new char[DISK_WAIT_SIZE];
    memset(tmpDiskInfo->disk_wait, 0, DISK_WAIT_SIZE);
    
    tmpDiskInfo->total_space       = new unsigned long long;
    memset(tmpDiskInfo->total_space, 0, sizeof( unsigned long long));
    
    tmpDiskInfo->full_blk_space    = new unsigned long long;
    memset(tmpDiskInfo->full_blk_space, 0, sizeof( unsigned long long));
    
    tmpDiskInfo->sub_blk_space     = new unsigned long long;
    memset(tmpDiskInfo->sub_blk_space, 0, sizeof( unsigned long long));
    
    tmpDiskInfo->fail_group_id     = new  int;
    memset(tmpDiskInfo->fail_group_id, 0, sizeof( int));

    tmpDiskInfo->is_free           = new  int;
    memset(tmpDiskInfo->is_free, 0, sizeof( int));
    
    tmpDiskInfo->change            = new  int;
    memset(tmpDiskInfo->change, 0, sizeof( int));

    tmpDiskInfo->health            = new  int;
    memset(tmpDiskInfo->health, 0, sizeof( int));    
    
    return tmpDiskInfo;
    
}


void DbDiskInfo::Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info)
{
    SQLRETURN ret;
    if(opType != UPDATE && opType != INSERT)
        return;
    tlgpfs_disk_info_t* tmp = (tlgpfs_disk_info_t*)info;

    int x = (opType == UPDATE) ? colSize - pkSize : 0;

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::Upsert SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN diskNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, DISK_NAME_SIZE, 0, tmp->disk_name, 0, &diskNameLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::Upsert SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN nodeNameLen = tmp->node_name ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, NODE_NAME_SIZE, 0, tmp->node_name, 0, &nodeNameLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::Upsert SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN statusLen = tmp->status ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, STATUS_SIZE, 0, tmp->status, 0, &statusLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::Upsert SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN availabilityLen = tmp->availability ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, AVAILABILITY_SIZE, 0, tmp->availability, 0, &availabilityLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::Upsert SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN poolNameLen = tmp->pool_name ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, POOL_NAME_SIZE, 0, tmp->pool_name, 0, &poolNameLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::Upsert SQLBindParameter 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN volIdLen = tmp->vol_id ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, VOL_ID_SIZE, 0, tmp->vol_id, 0, &volIdLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::Upsert SQLBindParameter 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN metaDataLen = tmp->meta_data ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, META_DATA_SIZE, 0, tmp->meta_data, 0, &metaDataLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::Upsert SQLBindParameter 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN dataLen = tmp->data ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, DATA_SIZE, 0, tmp->data, 0, &dataLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::Upsert SQLBindParameter 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN diskWaitLen = tmp->disk_wait ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, DISK_WAIT_SIZE, 0, tmp->disk_wait, 0, &diskWaitLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::Upsert SQLBindParameter 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN totalSpaceLen = tmp->total_space ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, tmp->total_space, 0, &totalSpaceLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::Upsert SQLBindParameter 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN fullBlkSpaceLen = tmp->full_blk_space ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, tmp->full_blk_space, 0, &fullBlkSpaceLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::Upsert SQLBindParameter 12 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN subBlkSpaceLen = tmp->sub_blk_space ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, tmp->sub_blk_space, 0, &subBlkSpaceLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::Upsert SQLBindParameter 13 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN failGroupIdLen = tmp->fail_group_id ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->fail_group_id, 0, &failGroupIdLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::Upsert SQLBindParameter 14 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN isFreeLen = tmp->is_free ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->is_free, 0, &isFreeLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::Upsert SQLBindParameter 15 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN changeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::Upsert SQLBindParameter 16 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::Upsert SQLBindParameter 17 STMT",ret,sqlStmt,SQL_HANDLE_STMT);                

    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)upsertSql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbDiskInfo::Upsert SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbDiskInfo::bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init)
{
    SQLRETURN ret;
    int x = 1;
    tlgpfs_disk_info_t* tmp = (tlgpfs_disk_info_t*)info;
    
    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::bindPrimaryKey SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN diskNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, DISK_NAME_SIZE, 0, tmp->disk_name, 0, &diskNameLen);
    DbInterface::checkSqlRetcode("DbDiskInfo::bindPrimaryKey SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    if( init )
    {
        int changeValue = 100;//init to 100
        int healthValue = 100;
        
        SQLLEN changeLen = SQL_NTS;    
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &changeValue, 0, &changeLen);
        DbInterface::checkSqlRetcode("DbDiskInfo::bindPrimaryKey SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

        SQLLEN healthLen = SQL_NTS;        
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &healthValue, 0, &healthLen);
        DbInterface::checkSqlRetcode("DbDiskInfo::bindPrimaryKey SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);    
    }
    
    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)sql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbDiskInfo::bindPrimaryKey SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbDiskInfo::updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst)
{
    vector<tlgpfs_disk_info_t*>* tempv = (vector<tlgpfs_disk_info_t*>*)temp;
    vector<tlgpfs_disk_info_t*>* lastv = (vector<tlgpfs_disk_info_t*>*)lst;
    tlgpfs_disk_info_t* last;
    tlgpfs_disk_info_t* tmp = tempv->front();
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
   
   anyChange |= strcmp(tmp->node_name, last->node_name);
   anyChange |= strcmp(tmp->status, last->status);
   anyChange |= strcmp(tmp->availability, last->availability);
   anyChange |= strcmp(tmp->pool_name, last->pool_name);
   anyChange |= strcmp(tmp->vol_id, last->vol_id);
   anyChange |= strcmp(tmp->meta_data, last->meta_data);
   anyChange |= strcmp(tmp->data, last->data);
   anyChange |= strcmp(tmp->disk_wait, last->disk_wait);
   anyChange |= memcmp(tmp->total_space, last->total_space, sizeof( long long));
   anyChange |= memcmp(tmp->full_blk_space, last->full_blk_space, sizeof( long long));
   anyChange |= memcmp(tmp->sub_blk_space, last->sub_blk_space, sizeof( long long));   
   anyChange |= memcmp(tmp->fail_group_id, last->fail_group_id, sizeof( int));
   anyChange |= memcmp(tmp->is_free, last->is_free,sizeof( int));

   *tmp->change = anyChange?CHANGE_MODIFIED:CHANGE_NONE;
   //"status": "Unchanged" "Uninitialized" "NotInUse" "InUse" "Suspended" "BeingFormatted" "BeingAdded" "BeingEmptied" "BeingDeleted" "BeingDeleted-p" "ReferencesBeingRemoved" "BeingReplaced" "Replacement" "Unknown DiskConfigStatus"
   //"availability": "Unchanged" "OK" "Unavailable" "Recovering" "Unknown DiskAvailability"
   //only when "availability"=="OK" and "status" == "InUse", it's healthy
   if(!strcmp(tmp->availability,"OK") && !strcmp(tmp->status,"InUse"))
   {
       *tmp->health = HEALTHY;
   }
   else
       *tmp->health = UNHEALTHY;
   updateTable(sqlStmt,table,tmp);

}
}

