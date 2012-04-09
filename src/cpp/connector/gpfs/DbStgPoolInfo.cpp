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
#include "DbStgPoolInfo.h"
#include <iomanip>

namespace TEAL
{
DbStgPoolInfo::DbStgPoolInfo(DbInterface* dbi, vector<string>* cols, vector<string>* pk, tlgpfs_stg_info_t* stg):DbGpfsInfo(dbi,REGULAR_STG_TABLE,TMP_STG_TABLE,cols,pk,stg)
{
    if (stg) 
    {
        if (!stg->cluster_id) throw std::invalid_argument("Cluster id is NULL");
        if (!stg->fs_name) throw std::invalid_argument("FS name is NULL");
        if (!stg->stg_name) throw std::invalid_argument("STG name is NULL");
        if (!stg->change) throw std::invalid_argument("Change is NULL");
        if (!stg->health) throw std::invalid_argument("health is NULL");
    }
    if(cols)
    {
        cols->push_back("cluster_id");
        cols->push_back("fs_name");
        cols->push_back("stg_name");
        cols->push_back("status");
        cols->push_back("refresh_time");
        cols->push_back("perf_ref_time");
        cols->push_back("total_space");    
        cols->push_back("free_space");    
        cols->push_back("parent_fs");
        cols->push_back("num_disks");
        cols->push_back("num_disk_items");
        cols->push_back("change");
        cols->push_back("health");
    }
    if(pk)
    {
        pk->push_back("cluster_id");
        pk->push_back("fs_name");
        pk->push_back("stg_name");
    }
}


void DbStgPoolInfo::printStatus(tlgpfs_stg_info_t* stg, bool detailed)
{
    if(stg == NULL)
        cerr<<"Can't print a null structure of status!"<<endl;

    cout<<setiosflags(ios::left)<<setw(20)<<"cluster_id"        <<setiosflags(ios::left)<<setw(40)<<"(cluster id)"                          <<": "<< stg->cluster_id       <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"fs_name"           <<setiosflags(ios::left)<<setw(40)<<"(file system name)"                    <<": "<< stg->fs_name          <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"stg_name"          <<setiosflags(ios::left)<<setw(40)<<"(storage pool name)"                   <<": "<< stg->stg_name         <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"health"            <<setiosflags(ios::left)<<setw(40)<<"(health status)"                       <<": "<<string((*stg->health == HEALTHY)?"healthy":((*stg->health == UNHEALTHY)?"unhealthy":"unknown"))<<endl;    
    if(!detailed)
        return;
    cout<<setiosflags(ios::left)<<setw(20)<<"status"            <<setiosflags(ios::left)<<setw(40)<<"(storage pool status)"                 <<": "<< stg->status           <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"refresh_time"      <<setiosflags(ios::left)<<setw(40)<<"(last refresh time)"                   <<": "<< stg->refresh_time     <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"perf_ref_time"     <<setiosflags(ios::left)<<setw(40)<<"(performance statics refresh time)"    <<": "<< stg->perf_ref_time    <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"total_space"       <<setiosflags(ios::left)<<setw(40)<<"(total space)"                         <<": "<<*stg->total_space      <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"free_space"        <<setiosflags(ios::left)<<setw(40)<<"(free space)"                          <<": "<<*stg->free_space       <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"parent_fs"         <<setiosflags(ios::left)<<setw(40)<<"(parent file system)"                  <<": "<<*stg->parent_fs        <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"num_disks"         <<setiosflags(ios::left)<<setw(40)<<"(mounted disks number)"                <<": "<<*stg->num_disks        <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"num_disk_items"    <<setiosflags(ios::left)<<setw(40)<<"(disk items number)"                   <<": "<<*stg->num_disk_items   <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"change"            <<setiosflags(ios::left)<<setw(40)<<"(change value)"                        <<": "<<*stg->change           <<endl;

}

DbStgPoolInfo::~DbStgPoolInfo()
{
}

void DbStgPoolInfo::getResult(SQLHSTMT sqlStmt,void** holder)
{
    SQLRETURN ret;
    *holder = new vector<tlgpfs_stg_info_t*>;
    vector<tlgpfs_stg_info_t*>* status = (vector<tlgpfs_stg_info_t*>*)* holder;
    tlgpfs_stg_info_t* tmp = allocateMemory();

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 1, SQL_C_CHAR, tmp->cluster_id, CLUSTER_ID_SIZE, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::getResult SQLBindCol 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN fsNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 2, SQL_C_CHAR, tmp->fs_name, FS_NAME_SIZE, &fsNameLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::getResult SQLBindCol 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN stgNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 3, SQL_C_CHAR, tmp->stg_name, STG_NAME_SIZE, &stgNameLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::getResult SQLBindCol 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN statusLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 4, SQL_C_CHAR, tmp->status, STATUS_SIZE, &statusLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::getResult SQLBindCol 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN refreshTimeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 5, SQL_C_CHAR, tmp->refresh_time, REFRESH_TIME_SIZE, &refreshTimeLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::getResult SQLBindCol 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN perfRefTimeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 6, SQL_C_CHAR, tmp->perf_ref_time, PERF_REF_TIME_SIZE, &perfRefTimeLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::getResult SQLBindCol 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN totalSpaceLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 7, SQL_C_UBIGINT, tmp->total_space, 0, &totalSpaceLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::getResult SQLBindCol 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN freeSpaceLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 8, SQL_C_UBIGINT, tmp->free_space, 0, &freeSpaceLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::getResult SQLBindCol 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN parentFsLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 9, SQL_C_SLONG, tmp->parent_fs, 0, &parentFsLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::getResult SQLBindCol 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN numDisksLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 10, SQL_C_SLONG,tmp->num_disks, 0, &numDisksLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::getResult SQLBindCol 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN numDiskItemsLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 11, SQL_C_SLONG, tmp->num_disk_items, 0, &numDiskItemsLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::getResult SQLBindCol 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN changeLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 12, SQL_C_SLONG, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::getResult SQLBindCol 12 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 13, SQL_C_SLONG, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::getResult SQLBindCol 13 STMT",ret,sqlStmt,SQL_HANDLE_STMT);    
    
    ret = DbInterface::dbModule.SQLFetch(sqlStmt);
    if(ret != SQL_NO_DATA)//don't roll back even if empty row.
        DbInterface::checkSqlRetcode("DbStgPoolInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    
    while((ret == SQL_SUCCESS || ret == SQL_SUCCESS_WITH_INFO))
    {
        
        tlgpfs_stg_info_t* temp = allocateMemory();
        copyInfo(temp,tmp);
        status->push_back(temp);
        resetMemory(tmp);
        ret = DbInterface::dbModule.SQLFetch(sqlStmt);
        if(ret != SQL_NO_DATA)//don't roll back even if empty row.
            DbInterface::checkSqlRetcode("DbStgPoolInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    }


}

tlgpfs_stg_info_t* DbStgPoolInfo::extract(StoragePoolInfo* stgInfo, string& clusterId, string& fsName)
{
    if(stgInfo == NULL)
        return NULL;
    tlgpfs_stg_info* tmpStgInfo = allocateMemory();
    
    strcpy(tmpStgInfo->cluster_id, clusterId.c_str());
    strcpy(tmpStgInfo->fs_name, fsName.c_str());
    strcpy(tmpStgInfo->stg_name, stgInfo->getName());
    strcpy(tmpStgInfo->status, stgInfo->getStatus());
    struct timeval d_ref_time = stgInfo->getDiskRefreshTime();
    Utils::timeval_to_char(&d_ref_time,tmpStgInfo->refresh_time);
    struct timeval perf_ref_time = stgInfo->getDiskPerfRefreshTime();
    Utils::timeval_to_char(&perf_ref_time,tmpStgInfo->perf_ref_time);
    *tmpStgInfo->total_space     = stgInfo->getTotalSpace();
    *tmpStgInfo->free_space      = stgInfo->getFreeSpace();
    *tmpStgInfo->parent_fs       = stgInfo->getParent();
    *tmpStgInfo->num_disks       = stgInfo->getNumDisks();
    *tmpStgInfo->num_disk_items  = stgInfo->getNumDiskItems();

    return tmpStgInfo;

}

tlgpfs_stg_info_t* DbStgPoolInfo::allocateMemory()
{
    tlgpfs_stg_info* tmpStgInfo = new tlgpfs_stg_info();
    
    tmpStgInfo->cluster_id        = new char[CLUSTER_ID_SIZE];
    memset(tmpStgInfo->cluster_id, 0, CLUSTER_ID_SIZE);

    tmpStgInfo->fs_name           = new char[FS_NAME_SIZE];
    memset(tmpStgInfo->fs_name, 0, FS_NAME_SIZE);

    tmpStgInfo->stg_name          = new char[STG_NAME_SIZE];
    memset(tmpStgInfo->stg_name, 0, STG_NAME_SIZE);
    
    tmpStgInfo->status            = new char[STATUS_SIZE];
    memset(tmpStgInfo->status, 0, STATUS_SIZE);
    
    tmpStgInfo->refresh_time      = new char[REFRESH_TIME_SIZE];
    memset(tmpStgInfo->refresh_time, 0, REFRESH_TIME_SIZE);
    
    tmpStgInfo->perf_ref_time     = new char[PERF_REF_TIME_SIZE];
    memset(tmpStgInfo->perf_ref_time, 0, PERF_REF_TIME_SIZE);
    
    tmpStgInfo->total_space       = new unsigned long long;
    memset(tmpStgInfo->total_space, 0, sizeof( unsigned long long));

    tmpStgInfo->free_space        = new unsigned long long;
    memset(tmpStgInfo->free_space, 0, sizeof( unsigned long long));
    
    tmpStgInfo->parent_fs         = new int;
    memset(tmpStgInfo->parent_fs, 0, sizeof( int));
    
    tmpStgInfo->num_disks         = new int;
    memset(tmpStgInfo->num_disks, 0, sizeof( int));
    
    tmpStgInfo->num_disk_items    = new  int;
    memset(tmpStgInfo->num_disk_items, 0, sizeof( int));
    
    tmpStgInfo->change            = new  int;
    memset(tmpStgInfo->change, 0, sizeof( int));

    tmpStgInfo->health            = new  int;
    memset(tmpStgInfo->health, 0, sizeof( int));         
    return tmpStgInfo;
    
}


void DbStgPoolInfo::Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info)
{
    SQLRETURN ret;
    if(opType != UPDATE && opType != INSERT)
        return;
    tlgpfs_stg_info_t* tmp = (tlgpfs_stg_info_t*)info;

    int x = (opType == UPDATE) ? colSize - pkSize : 0;

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::Upsert SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN fsNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, FS_NAME_SIZE, 0, tmp->fs_name, 0, &fsNameLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::Upsert SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN stgNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, STG_NAME_SIZE, 0, tmp->stg_name, 0, &stgNameLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::Upsert SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN statusLen = tmp->status ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, STATUS_SIZE, 0, tmp->status, 0, &statusLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::Upsert SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN refreshTimeLen = tmp->refresh_time ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, REFRESH_TIME_SIZE, 0, tmp->refresh_time, 0, &refreshTimeLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::Upsert SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN perfRefTimeLen = tmp->perf_ref_time ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, PERF_REF_TIME_SIZE, 0, tmp->perf_ref_time, 0, &perfRefTimeLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::Upsert SQLBindParameter 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN totalSpaceLen = tmp->total_space ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, tmp->total_space, 0, &totalSpaceLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::Upsert SQLBindParameter 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN freeSpaceLen = tmp->free_space ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, tmp->free_space, 0, &freeSpaceLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::Upsert SQLBindParameter 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN parentFsLen = tmp->parent_fs ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->parent_fs, 0, &parentFsLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::Upsert SQLBindParameter 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN numDisksLen = tmp->num_disks ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->num_disks, 0, &numDisksLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::Upsert SQLBindParameter 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN numDiskItemsLen = tmp->num_disk_items ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->num_disk_items, 0, &numDiskItemsLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::Upsert SQLBindParameter 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN changeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::Upsert SQLBindParameter 12 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::Upsert SQLBindParameter 13 STMT",ret,sqlStmt,SQL_HANDLE_STMT);                

    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)upsertSql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbStgPoolInfo::Upsert SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbStgPoolInfo::copyInfo(tlgpfs_stg_info_t* dst, tlgpfs_stg_info_t* src)
{
    strcpy(dst->cluster_id, src->cluster_id);
    strcpy(dst->fs_name, src->fs_name);
    strcpy(dst->stg_name, src->stg_name);
    strcpy(dst->status, src->status);
    strcpy(dst->refresh_time, src->refresh_time);
    strcpy(dst->perf_ref_time, src->perf_ref_time);
    *dst->total_space = *src->total_space;
    *dst->free_space = *src->free_space;
    *dst->parent_fs = *src->parent_fs;
    *dst->num_disks = *src->num_disks;
    *dst->num_disk_items = *src->num_disk_items;
    *dst->change = *src->change;
    *dst->health = *src->health;

}

void DbStgPoolInfo::resetMemory(tlgpfs_stg_info* tmpStgInfo)
{
    if( tmpStgInfo == NULL )
        return;
    
    memset(tmpStgInfo->cluster_id, 0, CLUSTER_ID_SIZE);

    memset(tmpStgInfo->fs_name, 0, FS_NAME_SIZE);

    memset(tmpStgInfo->stg_name, 0, STG_NAME_SIZE);
    
    memset(tmpStgInfo->status, 0, STATUS_SIZE);
    
    memset(tmpStgInfo->refresh_time, 0, REFRESH_TIME_SIZE);
    
    memset(tmpStgInfo->perf_ref_time, 0, PERF_REF_TIME_SIZE);
    
    memset(tmpStgInfo->total_space, 0, sizeof( unsigned long long));

    memset(tmpStgInfo->free_space, 0, sizeof( unsigned long long));
    
    memset(tmpStgInfo->parent_fs, 0, sizeof( int));
    
    memset(tmpStgInfo->num_disks, 0, sizeof( int));
    
    memset(tmpStgInfo->num_disk_items, 0, sizeof( int));
    
    memset(tmpStgInfo->change, 0, sizeof( int));

    memset(tmpStgInfo->health, 0, sizeof( int));    


}

void DbStgPoolInfo::bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init)
{
    SQLRETURN ret;
    int x = 1;
    tlgpfs_stg_info_t* tmp = (tlgpfs_stg_info_t*)info;

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::bindPrimaryKey SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN fsNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, FS_NAME_SIZE, 0, tmp->fs_name, 0, &fsNameLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::bindPrimaryKey SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN stgNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, STG_NAME_SIZE, 0, tmp->stg_name, 0, &stgNameLen);
    DbInterface::checkSqlRetcode("DbStgPoolInfo::bindPrimaryKey SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    if( init )
    {
        int changeValue = 100;//init to 100
        int healthValue = 100;
        
        SQLLEN changeLen = SQL_NTS;    
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &changeValue, 0, &changeLen);
        DbInterface::checkSqlRetcode("DbStgPoolInfo::bindPrimaryKey SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

        SQLLEN healthLen = SQL_NTS;        
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &healthValue, 0, &healthLen);
        DbInterface::checkSqlRetcode("DbStgPoolInfo::bindPrimaryKey SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);    
    }
    
    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)sql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbStgPoolInfo::bindPrimaryKey SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbStgPoolInfo::updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst)
{
    vector<tlgpfs_stg_info_t*>* tempv = (vector<tlgpfs_stg_info_t*>*)temp;
    vector<tlgpfs_stg_info_t*>* lastv = (vector<tlgpfs_stg_info_t*>*)lst;
    tlgpfs_stg_info_t* last;

    tlgpfs_stg_info_t* tmp = tempv->front();
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
   
   anyChange |= strcmp(tmp->status, last->status);
   anyChange |= strcmp(tmp->refresh_time, last->refresh_time);
   anyChange |= strcmp(tmp->perf_ref_time, last->perf_ref_time);
   anyChange |= memcmp(tmp->total_space, last->total_space, sizeof( long long));
   anyChange |= memcmp(tmp->free_space, last->free_space, sizeof( long long));
   anyChange |= memcmp(tmp->parent_fs, last->parent_fs, sizeof( int));
   anyChange |= memcmp(tmp->num_disks, last->num_disks, sizeof( int));
   anyChange |= memcmp(tmp->num_disk_items, last->num_disk_items, sizeof( int));

   *tmp->change = anyChange?CHANGE_MODIFIED:CHANGE_NONE;
   //"status": "Invalid" "NotInUse" "BeingAdded" "Valid" "BeingDeleted"
   //only when "status"=="Invalid", it's unhealthy
   *tmp->health = strstr(tmp->status,"Invalid")?UNHEALTHY:HEALTHY;
   updateTable(sqlStmt,table,tmp);
}
}

