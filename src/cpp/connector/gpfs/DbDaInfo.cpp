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
#include "DbDaInfo.h"
#include <iomanip>
namespace TEAL
{
DbDaInfo::DbDaInfo(DbInterface* dbi, vector<string>* cols, vector<string>* pk, tlgpfs_da_info_t* da):DbGpfsInfo(dbi,REGULAR_DA_TABLE,TMP_DA_TABLE,cols,pk,da)
{
    if (da)
    {
        if (!da->cluster_id) throw std::invalid_argument("Cluster id is NULL");
        if (!da->rg_name) throw std::invalid_argument("RG name is NULL");
        if (!da->da_name) throw std::invalid_argument("DA name is NULL");
        if (!da->change) throw std::invalid_argument("Change is NULL");
        if (!da->health) throw std::invalid_argument("health is NULL");
    }
    if(cols)
    {
        cols->push_back("cluster_id");
        cols->push_back("rg_name");
        cols->push_back("da_name");
        cols->push_back("da_bg_task");
        cols->push_back("da_task_priority");
        cols->push_back("da_need_service");
        cols->push_back("da_task_percent");
        cols->push_back("da_vdisks");
        cols->push_back("da_pdisks");
        cols->push_back("da_spares");
        cols->push_back("da_replace_thres");
        cols->push_back("da_free_space");
        cols->push_back("da_scrub_dura");
        cols->push_back("change");
        cols->push_back("health");
    }
    if(pk)
    {
        pk->push_back("cluster_id");
        pk->push_back("rg_name");
        pk->push_back("da_name");
    }

}

DbDaInfo::~DbDaInfo()
{
}


void DbDaInfo::printStatus(tlgpfs_da_info_t* da, bool detailed)
{
    if(da == NULL)
        cerr<<"Can't print a null structure of status!"<<endl;

    cout<<setiosflags(ios::left)<<setw(20)<<"cluster_id"              <<setiosflags(ios::left)<<setw(40)<<"(cluster id)"                                   <<": "<< da->cluster_id               <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"rg_name"                 <<setiosflags(ios::left)<<setw(40)<<"(recovery group name)"                          <<": "<< da->rg_name                  <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"da_name"                 <<setiosflags(ios::left)<<setw(40)<<"(declustered array name)"                       <<": "<< da->da_name                  <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"health"                  <<setiosflags(ios::left)<<setw(40)<<"(health status)"                                <<": "<<string((*da->health == HEALTHY)?"healthy":((*da->health == UNHEALTHY)?"unhealthy":"unknown"))<<endl;    
    if(!detailed)
        return;
    cout<<setiosflags(ios::left)<<setw(20)<<"da_bg_task"              <<setiosflags(ios::left)<<setw(40)<<"(declustered array background task)"            <<": "<< da->da_bg_task               <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"da_task_priority"        <<setiosflags(ios::left)<<setw(40)<<"(declustered array task priority)"              <<": "<< da->da_task_priority         <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"da_need_service"         <<setiosflags(ios::left)<<setw(40)<<"(declustered array needs service)"              <<": "<< da->da_need_service          <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"da_task_percent"         <<setiosflags(ios::left)<<setw(40)<<"(da task percent completed)"                    <<": "<<*da->da_task_percent          <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"da_vdisks"               <<setiosflags(ios::left)<<setw(40)<<"(declustered array vdisk number)"               <<": "<<*da->da_vdisks                <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"da_pdisks"               <<setiosflags(ios::left)<<setw(40)<<"(declustered array pdisk number)"               <<": "<<*da->da_pdisks                <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"da_spares"               <<setiosflags(ios::left)<<setw(40)<<"(declustered array spares)"                     <<": "<<*da->da_spares                <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"da_replace_thres"        <<setiosflags(ios::left)<<setw(40)<<"(declustered array replace threshold)"          <<": "<<*da->da_replace_thres         <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"da_free_space"           <<setiosflags(ios::left)<<setw(40)<<"(declustered array free space)"                 <<": "<<*da->da_free_space            <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"da_scrub_dura"           <<setiosflags(ios::left)<<setw(40)<<"(declustered array scrub duration)"             <<": "<<*da->da_scrub_dura            <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"change"                  <<setiosflags(ios::left)<<setw(40)<<"(change value)"                                 <<": "<<*da->change                   <<endl;

}

void DbDaInfo::getResult(SQLHSTMT sqlStmt,void** holder)
{
    SQLRETURN ret;
    *holder = new vector<tlgpfs_da_info_t*>;
    vector<tlgpfs_da_info_t*>* status = (vector<tlgpfs_da_info_t*>*)* holder;
    tlgpfs_da_info_t* tmp = allocateMemory();


    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 1, SQL_C_CHAR, tmp->cluster_id, CLUSTER_ID_SIZE, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbDaInfo::getResult SQLBindCol 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN rgNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 2, SQL_C_CHAR, tmp->rg_name, RG_NAME_SIZE, &rgNameLen);
    DbInterface::checkSqlRetcode("DbDaInfo::getResult SQLBindCol 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN daNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 3, SQL_C_CHAR, tmp->da_name, DA_NAME_SIZE, &daNameLen);
    DbInterface::checkSqlRetcode("DbDaInfo::getResult SQLBindCol 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daBgTaskLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 4, SQL_C_CHAR, tmp->da_bg_task, DA_BG_TASK_SIZE, &daBgTaskLen);
    DbInterface::checkSqlRetcode("DbDaInfo::getResult SQLBindCol 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daTaskPriorityLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 5, SQL_C_CHAR, tmp->da_task_priority, DA_TASK_PRIORITY_SIZE, &daTaskPriorityLen);
    DbInterface::checkSqlRetcode("DbDaInfo::getResult SQLBindCol 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daNeedServiceLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 6, SQL_C_CHAR, tmp->da_need_service, DA_NEED_SERVICE_SIZE, &daNeedServiceLen);
    DbInterface::checkSqlRetcode("DbDaInfo::getResult SQLBindCol 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daTaskPercentLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 7, SQL_C_SLONG, tmp->da_task_percent, 0, &daTaskPercentLen);
    DbInterface::checkSqlRetcode("DbDaInfo::getResult SQLBindCol 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daVdisksLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 8, SQL_C_SLONG, tmp->da_vdisks, 0, &daVdisksLen);
    DbInterface::checkSqlRetcode("DbDaInfo::getResult SQLBindCol 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daPdisksLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 9, SQL_C_SLONG, tmp->da_pdisks, 0, &daPdisksLen);
    DbInterface::checkSqlRetcode("DbDaInfo::getResult SQLBindCol 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daSparesLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 10, SQL_C_SLONG, tmp->da_spares, 0, &daSparesLen);
    DbInterface::checkSqlRetcode("DbDaInfo::getResult SQLBindCol 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daReplaceThresLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 11, SQL_C_SLONG, tmp->da_replace_thres, 0, &daReplaceThresLen);
    DbInterface::checkSqlRetcode("DbDaInfo::getResult SQLBindCol 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN daFreeSpaceLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 12, SQL_C_UBIGINT, tmp->da_free_space, 0, &daFreeSpaceLen);
    DbInterface::checkSqlRetcode("DbDaInfo::getResult SQLBindCol 12 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN daScrubDuraLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 13, SQL_C_SLONG, tmp->da_scrub_dura, 0, &daScrubDuraLen);
    DbInterface::checkSqlRetcode("DbDaInfo::getResult SQLBindCol 13 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN changeLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 14, SQL_C_SLONG, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbDaInfo::getResult SQLBindCol 14 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 15, SQL_C_SLONG, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbDaInfo::getResult SQLBindCol 15 STMT",ret,sqlStmt,SQL_HANDLE_STMT);    
    
    ret = DbInterface::dbModule.SQLFetch(sqlStmt);
    if(ret != SQL_NO_DATA)//don't roll back even if empty row.
        DbInterface::checkSqlRetcode("DbDaInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    
    while((ret == SQL_SUCCESS || ret == SQL_SUCCESS_WITH_INFO))
    {
        
        tlgpfs_da_info_t* temp = allocateMemory();
        copyInfo(temp,tmp);
        status->push_back(temp);
        resetMemory(tmp);
        ret = DbInterface::dbModule.SQLFetch(sqlStmt);
        if(ret != SQL_NO_DATA)//don't roll back even if empty row.
            DbInterface::checkSqlRetcode("DbDaInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    }


}

void DbDaInfo::resetMemory(tlgpfs_da_info* tmpDaInfo)
{
    if( tmpDaInfo == NULL )
        return;
    
    memset(tmpDaInfo->cluster_id, 0, CLUSTER_ID_SIZE);

    memset(tmpDaInfo->rg_name, 0, RG_NAME_SIZE);

    memset(tmpDaInfo->da_name, 0, DA_NAME_SIZE);  
    
    memset(tmpDaInfo->da_bg_task, 0, DA_BG_TASK_SIZE);
    
    memset(tmpDaInfo->da_task_priority, 0, DA_TASK_PRIORITY_SIZE);
    
    memset(tmpDaInfo->da_need_service, 0, DA_NEED_SERVICE_SIZE);    
    
    memset(tmpDaInfo->da_task_percent, 0, DA_TASK_PERCENT_SIZE);
    
    memset(tmpDaInfo->da_vdisks, 0, DA_VDISKS_SIZE);
    
    memset(tmpDaInfo->da_pdisks, 0, DA_PDISKS_SIZE);
    
    memset(tmpDaInfo->da_spares, 0, DA_SPARES_SIZE);
    
    memset(tmpDaInfo->da_replace_thres, 0, DA_REPLACE_THRES_SIZE);
    
    memset(tmpDaInfo->da_free_space, 0, DA_FREE_SPACE_SIZE);
    
    memset(tmpDaInfo->da_scrub_dura, 0, DA_SCRUB_DURA_SIZE);
 
    memset(tmpDaInfo->change, 0, sizeof( int));
    
    memset(tmpDaInfo->health, 0, sizeof( int));    

}

void DbDaInfo::copyInfo(tlgpfs_da_info_t* dst, tlgpfs_da_info_t* src)
{
    strcpy(dst->cluster_id,          src->cluster_id);
    strcpy(dst->rg_name,             src->rg_name);
    strcpy(dst->da_name,             src->da_name);
    strcpy(dst->da_bg_task,          src->da_bg_task);
    strcpy(dst->da_task_priority,    src->da_task_priority);
    strcpy(dst->da_need_service,     src->da_need_service);
    
    *dst->da_task_percent  = *src->da_task_percent;
    *dst->da_vdisks        = *src->da_vdisks;
    *dst->da_pdisks        = *src->da_pdisks;
    *dst->da_spares        = *src->da_spares;
    *dst->da_replace_thres = *src->da_replace_thres;
    *dst->da_free_space    = *src->da_free_space;
    *dst->da_scrub_dura    = *src->da_scrub_dura;
    *dst->change           = *src->change;
    *dst->health           = *src->health;
}


tlgpfs_da_info_t* DbDaInfo::extract(gpfsRecoveryGroupDeclusteredArray* daInfo, string& clusterId, string& rgName)
{
    if(daInfo == NULL)
        return NULL;
    tlgpfs_da_info* tmpDaInfo = allocateMemory();
    strcpy(tmpDaInfo->cluster_id, clusterId.c_str());
    strcpy(tmpDaInfo->rg_name, rgName.c_str());
    strcpy(tmpDaInfo->da_name, daInfo->getDeclusteredArrayName());
    strcpy(tmpDaInfo->da_bg_task, daInfo->getDeclusteredArrayBackgroundTask());
    strcpy(tmpDaInfo->da_task_priority, daInfo->getDeclusteredArrayTaskPrioriy());
    strcpy(tmpDaInfo->da_need_service, daInfo->getDeclusteredNeedsService());
    
    *tmpDaInfo->da_task_percent  = daInfo->getDeclusteredArrayTaskPercentComplete();
    *tmpDaInfo->da_vdisks        = daInfo->getDeclusteredArrayVdisks();
    *tmpDaInfo->da_pdisks        = daInfo->getDeclusteredArrayPdisks();
    *tmpDaInfo->da_spares        = daInfo->getDeclusteredArraySpares();
    *tmpDaInfo->da_replace_thres = daInfo->getDeclusteredArrayReplaceThreshold();
    *tmpDaInfo->da_free_space    = daInfo->getDeclusteredArrayFreeSpace();
    *tmpDaInfo->da_scrub_dura    = daInfo->getDeclusteredArrayScrubDuration();

    return tmpDaInfo;

}

tlgpfs_da_info_t* DbDaInfo::allocateMemory()
{
    tlgpfs_da_info* tmpDaInfo = new tlgpfs_da_info();
    
    tmpDaInfo->cluster_id        = new char[CLUSTER_ID_SIZE];
    memset(tmpDaInfo->cluster_id, 0, CLUSTER_ID_SIZE);
    
    tmpDaInfo->rg_name           = new char[RG_NAME_SIZE];
    memset(tmpDaInfo->rg_name, 0, RG_NAME_SIZE);

    tmpDaInfo->da_name           = new char[DA_NAME_SIZE];
    memset(tmpDaInfo->da_name, 0, DA_NAME_SIZE);

    tmpDaInfo->da_bg_task        = new char[DA_BG_TASK_SIZE];
    memset(tmpDaInfo->da_bg_task, 0, DA_BG_TASK_SIZE);
    
    tmpDaInfo->da_task_priority  = new char[DA_TASK_PRIORITY_SIZE];
    memset(tmpDaInfo->da_task_priority, 0, DA_TASK_PRIORITY_SIZE);
    
    tmpDaInfo->da_need_service  = new char[DA_NEED_SERVICE_SIZE];
    memset(tmpDaInfo->da_need_service, 0, DA_NEED_SERVICE_SIZE);
    
    tmpDaInfo->da_task_percent   = new int;
    memset(tmpDaInfo->da_task_percent, 0, sizeof( int));
        
    tmpDaInfo->da_vdisks         = new int;
    memset(tmpDaInfo->da_vdisks, 0, sizeof( int));
    
    tmpDaInfo->da_pdisks         = new  int;
    memset(tmpDaInfo->da_pdisks, 0, sizeof( int));

    tmpDaInfo->da_spares         = new  int;
    memset(tmpDaInfo->da_spares, 0, sizeof( int));
    
    tmpDaInfo->da_replace_thres  = new  int;
    memset(tmpDaInfo->da_replace_thres, 0, sizeof( int));

    tmpDaInfo->da_free_space     = new  unsigned long long;
    memset(tmpDaInfo->da_free_space, 0, sizeof( unsigned long long));
    
    tmpDaInfo->da_scrub_dura     = new  int;
    memset(tmpDaInfo->da_pdisks, 0, sizeof( int));

    tmpDaInfo->change            = new  int;
    memset(tmpDaInfo->change, 0, sizeof( int));

    tmpDaInfo->health            = new  int;
    memset(tmpDaInfo->health, 0, sizeof( int));    
    return tmpDaInfo;
    
}


void DbDaInfo::Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info)
{
    SQLRETURN ret;
    if(opType != UPDATE && opType != INSERT)
        return;
    tlgpfs_da_info_t* tmp = (tlgpfs_da_info_t*)info;

    int x = (opType == UPDATE) ? colSize - pkSize : 0;   

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbDaInfo::Upsert SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rgNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, RG_NAME_SIZE, 0, tmp->rg_name, 0, &rgNameLen);
    DbInterface::checkSqlRetcode("DbDaInfo::Upsert SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, DA_NAME_SIZE, 0, tmp->da_name, 0, &daNameLen);
    DbInterface::checkSqlRetcode("DbDaInfo::Upsert SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daBgTaskLen = tmp->da_bg_task ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, DA_BG_TASK_SIZE, 0, tmp->da_bg_task, 0, &daBgTaskLen);
    DbInterface::checkSqlRetcode("DbDaInfo::Upsert SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daTaskPriorityLen = tmp->da_task_priority ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, DA_TASK_PRIORITY_SIZE, 0, tmp->da_task_priority, 0, &daTaskPriorityLen);
    DbInterface::checkSqlRetcode("DbDaInfo::Upsert SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daNeedServiceLen = tmp->da_need_service ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, DA_NEED_SERVICE_SIZE, 0, tmp->da_need_service, 0, &daNeedServiceLen);
    DbInterface::checkSqlRetcode("DbDaInfo::Upsert SQLBindParameter 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daTaskPercentLen = tmp->da_task_percent ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->da_task_percent, 0, &daTaskPercentLen);
    DbInterface::checkSqlRetcode("DbDaInfo::Upsert SQLBindParameter 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN daVdisksLen = tmp->da_vdisks ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->da_vdisks, 0, &daVdisksLen);
    DbInterface::checkSqlRetcode("DbDaInfo::Upsert SQLBindParameter 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN daPdisksLen = tmp->da_pdisks ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->da_pdisks, 0, &daPdisksLen);
    DbInterface::checkSqlRetcode("DbDaInfo::Upsert SQLBindParameter 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daSparesLen = tmp->da_spares ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->da_spares, 0, &daSparesLen);
    DbInterface::checkSqlRetcode("DbDaInfo::Upsert SQLBindParameter 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN daReplaceThresLen = tmp->da_replace_thres ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->da_replace_thres, 0, &daReplaceThresLen);
    DbInterface::checkSqlRetcode("DbDaInfo::Upsert SQLBindParameter 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daFreeSpaceLen = tmp->da_free_space ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, tmp->da_free_space, 0, &daFreeSpaceLen);
    DbInterface::checkSqlRetcode("DbDaInfo::Upsert SQLBindParameter 12 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN daScrubDuraLen = tmp->da_scrub_dura ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->da_scrub_dura, 0, &daScrubDuraLen);
    DbInterface::checkSqlRetcode("DbDaInfo::Upsert SQLBindParameter 13 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN changeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbDaInfo::Upsert SQLBindParameter 14 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbDaInfo::Upsert SQLBindParameter 15 STMT",ret,sqlStmt,SQL_HANDLE_STMT);        

    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)upsertSql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbDaInfo::Upsert SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbDaInfo::bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init)
{
    SQLRETURN ret;
    int x = 1;
    tlgpfs_da_info_t* tmp = (tlgpfs_da_info_t*)info;

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbDaInfo::bindPrimaryKey SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rgNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, RG_NAME_SIZE, 0, tmp->rg_name, 0, &rgNameLen);
    DbInterface::checkSqlRetcode("DbDaInfo::bindPrimaryKey SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, DA_NAME_SIZE, 0, tmp->da_name, 0, &daNameLen);
    DbInterface::checkSqlRetcode("DbDaInfo::bindPrimaryKey SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    if( init )
    {
        int changeValue = 100;//init to 100
        int healthValue = 100;
        
        SQLLEN changeLen = SQL_NTS;    
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &changeValue, 0, &changeLen);
        DbInterface::checkSqlRetcode("DbDaInfo::bindPrimaryKey SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

        SQLLEN healthLen = SQL_NTS;        
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &healthValue, 0, &healthLen);
        DbInterface::checkSqlRetcode("DbDaInfo::bindPrimaryKey SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);    
    }
    
    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)sql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbDaInfo::bindPrimaryKey SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbDaInfo::updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst)
{
    vector<tlgpfs_da_info_t*>* tempv = (vector<tlgpfs_da_info_t*>*)temp;
    vector<tlgpfs_da_info_t*>* lastv = (vector<tlgpfs_da_info_t*>*)lst;
    tlgpfs_da_info_t* last;

    tlgpfs_da_info_t* tmp = tempv->front();
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
   
   anyChange |= strcmp(tmp->da_bg_task, last->da_bg_task);
   anyChange |= strcmp(tmp->da_task_priority, last->da_task_priority);
   anyChange |= strcmp(tmp->da_need_service, last->da_need_service);
   anyChange |= memcmp(tmp->da_task_percent, last->da_task_percent,sizeof( int));
   anyChange |= memcmp(tmp->da_vdisks, last->da_vdisks,sizeof( int));
   anyChange |= memcmp(tmp->da_pdisks, last->da_pdisks,sizeof( int));
   anyChange |= memcmp(tmp->da_spares, last->da_spares,sizeof( int));
   anyChange |= memcmp(tmp->da_replace_thres, last->da_replace_thres,sizeof( int));
   anyChange |= memcmp(tmp->da_free_space, last->da_free_space,sizeof( unsigned long long));
   anyChange |= memcmp(tmp->da_scrub_dura, last->da_scrub_dura,sizeof( int));

   *tmp->change = anyChange?CHANGE_MODIFIED:CHANGE_NONE;
   //if da_need_service == yes, it's unhealthy
   *tmp->health = strstr(tmp->da_need_service,"yes")?UNHEALTHY:HEALTHY;
   updateTable(sqlStmt,table,tmp);

}
}

