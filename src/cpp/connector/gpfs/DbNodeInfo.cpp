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
#include "DbNodeInfo.h"
#include <iomanip>
namespace TEAL
{
DbNodeInfo::DbNodeInfo(DbInterface* dbi, vector<string>* cols, vector<string>* pk, tlgpfs_node_info_t* node):DbGpfsInfo(dbi,REGULAR_NODE_TABLE,TMP_NODE_TABLE,cols,pk,node)
{
    if (node)
    {
        if (!node->cluster_id) throw std::invalid_argument("Cluster id is NULL");
        if (!node->ip_addr) throw std::invalid_argument("node ip is NULL");
        if (!node->change) throw std::invalid_argument("Change is NULL");
        if (!node->health) throw std::invalid_argument("health is NULL");
    }
    if(cols)
    {
        cols->push_back("cluster_id");
        cols->push_back("ip_addr");
        cols->push_back("node_name");
        cols->push_back("type");
        cols->push_back("endian");
        cols->push_back("os_name");
        cols->push_back("version");
        cols->push_back("platform");
        cols->push_back("admin");
        cols->push_back("status");    
        cols->push_back("umnt_disk_fail");    
        cols->push_back("healthy");
        cols->push_back("diag");
        cols->push_back("pg_pool_size");
        cols->push_back("failure_count");
        cols->push_back("thread_wait");
        cols->push_back("pre_threads");
        cols->push_back("max_MBPS");
        cols->push_back("max_file_cache");
        cols->push_back("max_stat_cache");
        cols->push_back("work1_threads");
        cols->push_back("dm_evt_timeout");
        cols->push_back("dm_mnt_timeout");
        cols->push_back("dm_ses_timeout");
        cols->push_back("nsd_win_mnt");
        cols->push_back("nsd_time_mnt");
        cols->push_back("num_disk_access");
        cols->push_back("change");
        cols->push_back("health");
    }
    if(pk)
    {
        pk->push_back("cluster_id");
        pk->push_back("ip_addr");
    }

}

DbNodeInfo::~DbNodeInfo()
{
}

void DbNodeInfo::printStatus(tlgpfs_node_info_t* node, bool detailed)
{
    if(node == NULL)
        cerr<<"Can't print a null structure of status!"<<endl;

    cout<<setiosflags(ios::left)<<setw(20)<<"cluster_id"     <<setiosflags(ios::left)<<setw(40)<<"(cluster id)"                           <<": "<< node->cluster_id      <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"ip_addr"        <<setiosflags(ios::left)<<setw(40)<<"(node ip address)"                      <<": "<< node->ip_addr         <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"node_name"      <<setiosflags(ios::left)<<setw(40)<<"(node name)"                            <<": "<< node->name            <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"health"         <<setiosflags(ios::left)<<setw(40)<<"(health status)"                        <<": "<<string((*node->health == HEALTHY)?"healthy":((*node->health == UNHEALTHY)?"unhealthy":"unknown"))<<endl;    
    if(!detailed)
        return;
    cout<<setiosflags(ios::left)<<setw(20)<<"type"           <<setiosflags(ios::left)<<setw(40)<<"(node type)"                            <<": "<< node->type            <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"endian"         <<setiosflags(ios::left)<<setw(40)<<"(endian)"                               <<": "<< node->endian          <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"os_name"        <<setiosflags(ios::left)<<setw(40)<<"(os name)"                              <<": "<< node->os_name         <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"version"        <<setiosflags(ios::left)<<setw(40)<<"(sw version)"                           <<": "<< node->version         <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"platform"       <<setiosflags(ios::left)<<setw(40)<<"(os platform)"                          <<": "<< node->platform        <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"admin"          <<setiosflags(ios::left)<<setw(40)<<"(admin)"                                <<": "<< node->admin           <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"status"         <<setiosflags(ios::left)<<setw(40)<<"(current status)"                       <<": "<< node->status          <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"umnt_disk_fail" <<setiosflags(ios::left)<<setw(40)<<"(unmount on disk fail)"                 <<": "<< node->umnt_disk_fail  <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"healthy"        <<setiosflags(ios::left)<<setw(40)<<"(if healthy)"                           <<": "<< node->healthy         <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"diag"           <<setiosflags(ios::left)<<setw(40)<<"(diagnosis info)"                       <<": "<< node->diag            <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"pg_pool_size"   <<setiosflags(ios::left)<<setw(40)<<"(page pool size)"                       <<": "<<*node->pg_pool_size    <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"failure_count"  <<setiosflags(ios::left)<<setw(40)<<"(failure count)"                        <<": "<<*node->failure_count   <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"thread_wait"    <<setiosflags(ios::left)<<setw(40)<<"(thread wait time)"                     <<": "<<*node->thread_wait     <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"pre_threads"    <<setiosflags(ios::left)<<setw(40)<<"(prefetch threads number)"              <<": "<<*node->pre_threads     <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"max_MBPS"       <<setiosflags(ios::left)<<setw(40)<<"(max MBPS)"                             <<": "<<*node->max_MBPS        <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"max_file_cache" <<setiosflags(ios::left)<<setw(40)<<"(max files to cache)"                   <<": "<<*node->max_file_cache  <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"max_stat_cache" <<setiosflags(ios::left)<<setw(40)<<"(max stat cache)"                       <<": "<<*node->max_stat_cache  <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"work1_threads"  <<setiosflags(ios::left)<<setw(40)<<"(worker 1 threads)"                     <<": "<<*node->work1_threads   <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"dm_evt_timeout" <<setiosflags(ios::left)<<setw(40)<<"(dm api event time out)"                <<": "<<*node->dm_evt_timeout  <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"dm_mnt_timeout" <<setiosflags(ios::left)<<setw(40)<<"(dm api mount time out)"                <<": "<<*node->dm_mnt_timeout  <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"dm_ses_timeout" <<setiosflags(ios::left)<<setw(40)<<"(dm api session failure time out)"      <<": "<<*node->dm_ses_timeout  <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"nsd_win_mnt"    <<setiosflags(ios::left)<<setw(40)<<"(nsd server wait time window on mount)" <<": "<<*node->nsd_win_mnt     <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"nsd_time_mnt"   <<setiosflags(ios::left)<<setw(40)<<"(nsd server wait time for mount)"       <<": "<<*node->nsd_time_mnt    <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"num_disk_access"<<setiosflags(ios::left)<<setw(40)<<"(disk access items number)"             <<": "<<*node->num_disk_access <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"change"         <<setiosflags(ios::left)<<setw(40)<<"(change value)"                         <<": "<<*node->change          <<endl;

}

void DbNodeInfo::getResult(SQLHSTMT sqlStmt,void** holder)
{
    SQLRETURN ret;
    *holder = new vector<tlgpfs_node_info_t*>;
    vector<tlgpfs_node_info_t*>* status = (vector<tlgpfs_node_info_t*>*)* holder;
    tlgpfs_node_info_t* tmp = allocateMemory();


    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 1, SQL_C_CHAR, tmp->cluster_id, CLUSTER_ID_SIZE, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN ipAddrLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 2, SQL_C_CHAR, tmp->ip_addr, IP_ADDR_SIZE, &ipAddrLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN nameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 3, SQL_C_CHAR, tmp->name, NAME_SIZE, &nameLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN typeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 4, SQL_C_CHAR, tmp->type, TYPE_SIZE, &typeLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN endianLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 5, SQL_C_CHAR, tmp->endian, ENDIAN_SIZE, &endianLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN osNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 6, SQL_C_CHAR, tmp->os_name, OS_NAME_SIZE, &osNameLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN versionLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 7, SQL_C_CHAR, tmp->version, VERSION_SIZE, &versionLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN platformLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 8, SQL_C_CHAR, tmp->platform, PLATFORM_SIZE, &platformLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN adminLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 9, SQL_C_CHAR, tmp->admin, ADMIN_SIZE, &adminLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN statusLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 10, SQL_C_CHAR, tmp->status, STATUS_SIZE, &statusLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN umntDiskFailLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 11, SQL_C_CHAR, tmp->umnt_disk_fail, UMNT_DISK_FAIL_SIZE, &umntDiskFailLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN healthyLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 12, SQL_C_CHAR, tmp->healthy, HEALTHY_SIZE, &healthyLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 12 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN diagLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 13, SQL_C_CHAR, tmp->diag, DIAG_SIZE, &diagLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 13 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN pgPoolSizeLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 14, SQL_C_UBIGINT, tmp->pg_pool_size, 0, &pgPoolSizeLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 14 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN failureCountLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 15, SQL_C_SLONG, tmp->failure_count, 0, &failureCountLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 15 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN threadWaitLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 16, SQL_C_SLONG, tmp->thread_wait, 0, &threadWaitLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 16 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN preThreadsLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 17, SQL_C_SLONG, tmp->pre_threads, 0, &preThreadsLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 17 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN maxMBPSLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 18, SQL_C_SLONG, tmp->max_MBPS, 0, &maxMBPSLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 18 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN maxFileCacheLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 19, SQL_C_SLONG, tmp->max_file_cache, 0, &maxFileCacheLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 19 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN maxStatCacheLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 20, SQL_C_SLONG,tmp->max_stat_cache, 0, &maxStatCacheLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 20 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN work1ThreadsLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 21, SQL_C_SLONG, tmp->work1_threads, 0, &work1ThreadsLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 21 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN dmEvtTimeoutLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 22, SQL_C_SLONG, tmp->dm_evt_timeout, 0, &dmEvtTimeoutLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 22 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN dmMntTimeoutLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 23, SQL_C_SLONG, tmp->dm_mnt_timeout, 0, &dmMntTimeoutLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 23 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN dmSesTimeoutLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 24, SQL_C_SLONG,tmp->dm_ses_timeout, 0, &dmSesTimeoutLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 24 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN nsdWinMntLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 25, SQL_C_SLONG, tmp->nsd_win_mnt, 0, &nsdWinMntLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 25 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN nsdTimeMntLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 26, SQL_C_SLONG, tmp->nsd_time_mnt, 0, &nsdTimeMntLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 26 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN numDiskAccessLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 27, SQL_C_SLONG, tmp->num_disk_access, 0, &numDiskAccessLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 27 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN changeLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 28, SQL_C_SLONG, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 28 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 29, SQL_C_SLONG, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLBindCol 29 STMT",ret,sqlStmt,SQL_HANDLE_STMT);    
    
    ret = DbInterface::dbModule.SQLFetch(sqlStmt);
    if(ret != SQL_NO_DATA)//don't roll back even if empty row.
        DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    
    while((ret == SQL_SUCCESS || ret == SQL_SUCCESS_WITH_INFO))
    {
        
        tlgpfs_node_info_t* temp = allocateMemory();
        copyInfo(temp,tmp);
        status->push_back(temp);
        resetMemory(tmp);
        ret = DbInterface::dbModule.SQLFetch(sqlStmt);
        if(ret != SQL_NO_DATA)//don't roll back even if empty row.
            DbInterface::checkSqlRetcode("DbNodeInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    }


}

void DbNodeInfo::bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init)
{
    SQLRETURN ret;
    int x = 1;
    tlgpfs_node_info_t* tmp = (tlgpfs_node_info_t*)info;

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::bindPrimaryKey SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN ipAddrLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, IP_ADDR_SIZE, 0, tmp->ip_addr, 0, &ipAddrLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::bindPrimaryKey SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    if( init )
    {
        int changeValue = 100;//init to 100
        int healthValue = 100;
        
        SQLLEN changeLen = SQL_NTS;    
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &changeValue, 0, &changeLen);
        DbInterface::checkSqlRetcode("DbNodeInfo::bindPrimaryKey SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

        SQLLEN healthLen = SQL_NTS;        
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &healthValue, 0, &healthLen);
        DbInterface::checkSqlRetcode("DbNodeInfo::bindPrimaryKey SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);    
    }
    
    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)sql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbNodeInfo::bindPrimaryKey SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}


void DbNodeInfo::resetMemory(tlgpfs_node_info* tmpNodeInfo)
{
    if( tmpNodeInfo == NULL )
        return;
    
    memset(tmpNodeInfo->cluster_id, 0, CLUSTER_ID_SIZE);

    memset(tmpNodeInfo->ip_addr, 0, IP_ADDR_SIZE);

    memset(tmpNodeInfo->name, 0, NAME_SIZE);
    
    memset(tmpNodeInfo->type, 0, TYPE_SIZE);
    
    memset(tmpNodeInfo->endian, 0, ENDIAN_SIZE);
    
    memset(tmpNodeInfo->os_name, 0, OS_NAME_SIZE);
    
    memset(tmpNodeInfo->version, 0, VERSION_SIZE);
    
    memset(tmpNodeInfo->platform, 0, PLATFORM_SIZE);
    
    memset(tmpNodeInfo->admin, 0, ADMIN_SIZE);
    
    memset(tmpNodeInfo->status, 0, STATUS_SIZE);
    
    memset(tmpNodeInfo->umnt_disk_fail, 0, UMNT_DISK_FAIL_SIZE);
    
    memset(tmpNodeInfo->healthy, 0, HEALTHY_SIZE);
    
    memset(tmpNodeInfo->diag, 0, DIAG_SIZE);
        
    memset(tmpNodeInfo->pg_pool_size, 0, sizeof( unsigned long long));
    
    memset(tmpNodeInfo->failure_count, 0, sizeof( int));

    memset(tmpNodeInfo->thread_wait, 0, sizeof( int));
    
    memset(tmpNodeInfo->pre_threads, 0, sizeof( int));
    
    memset(tmpNodeInfo->max_MBPS, 0, sizeof( int));
    
    memset(tmpNodeInfo->max_file_cache, 0, sizeof( int));
    
    memset(tmpNodeInfo->max_stat_cache, 0, sizeof( int));
    
    memset(tmpNodeInfo->work1_threads, 0, sizeof( int));
    
    memset(tmpNodeInfo->dm_evt_timeout, 0, sizeof( int));
    
    memset(tmpNodeInfo->dm_mnt_timeout, 0, sizeof( int));
     
    memset(tmpNodeInfo->dm_ses_timeout, 0, sizeof( int));

    memset(tmpNodeInfo->nsd_win_mnt, 0, sizeof( int));
    
    memset(tmpNodeInfo->nsd_time_mnt, 0, sizeof( int));
    
    memset(tmpNodeInfo->num_disk_access, 0, sizeof( int));

    memset(tmpNodeInfo->change, 0, sizeof( int));
    
    memset(tmpNodeInfo->health, 0, sizeof( int));    

}

void DbNodeInfo::copyInfo(tlgpfs_node_info_t* dst, tlgpfs_node_info_t* src)
{
    strcpy(dst->cluster_id, src->cluster_id);
    strcpy(dst->ip_addr, src->ip_addr);
    strcpy(dst->name, src->name);
    strcpy(dst->type, src->type);
    strcpy(dst->endian, src->endian);
    strcpy(dst->os_name, src->os_name);
    strcpy(dst->version, src->version);
    strcpy(dst->platform, src->platform);
    strcpy(dst->admin, src->admin);
    strcpy(dst->status, src->status);
    strcpy(dst->umnt_disk_fail, src->umnt_disk_fail);
    strcpy(dst->healthy, src->healthy);
    strcpy(dst->diag, src->diag);
    *dst->pg_pool_size = *src->pg_pool_size;
    *dst->failure_count = *src->failure_count;
    *dst->thread_wait = *src->thread_wait;
    *dst->pre_threads = *src->pre_threads;
    *dst->max_MBPS = *src->max_MBPS;
    *dst->max_file_cache = *src->max_file_cache;
    *dst->max_stat_cache = *src->max_stat_cache;
    *dst->work1_threads = *src->work1_threads;
    *dst->dm_evt_timeout = *src->dm_evt_timeout;
    *dst->dm_mnt_timeout = *src->dm_mnt_timeout;
    *dst->dm_ses_timeout = *src->dm_ses_timeout;
    *dst->nsd_win_mnt = *src->nsd_win_mnt;
    *dst->nsd_time_mnt = *src->nsd_time_mnt;
    *dst->num_disk_access = *src->num_disk_access;
    *dst->change = *src->change;
    *dst->health = *src->health;

}


tlgpfs_node_info_t* DbNodeInfo::extract(NodeInfo* nodeInfo, string& clusterId)
{
    if(nodeInfo == NULL)
        return NULL;
    tlgpfs_node_info* tmpNodeInfo = allocateMemory();
    strcpy(tmpNodeInfo->cluster_id, clusterId.c_str());
    strcpy(tmpNodeInfo->ip_addr, nodeInfo->getIpAddr());
    strcpy(tmpNodeInfo->name, nodeInfo->getName());
    strcpy(tmpNodeInfo->type, nodeInfo->getType());
    strcpy(tmpNodeInfo->endian, nodeInfo->getEndian());
    strcpy(tmpNodeInfo->os_name, nodeInfo->getOsName());
    strcpy(tmpNodeInfo->version, nodeInfo->getVersion());
    strcpy(tmpNodeInfo->platform, nodeInfo->getPlatform());
    strcpy(tmpNodeInfo->admin, nodeInfo->getAdmin());
    strcpy(tmpNodeInfo->status, nodeInfo->getStatus());
    strcpy(tmpNodeInfo->umnt_disk_fail, nodeInfo->getUnmountOnDiskFail());
    strcpy(tmpNodeInfo->healthy, nodeInfo->getHealthy());
    strcpy(tmpNodeInfo->diag, nodeInfo->getDiagnosis());
    *tmpNodeInfo->pg_pool_size = nodeInfo->getPagePoolSize();
    *tmpNodeInfo->failure_count =nodeInfo->getFailureCount();
    *tmpNodeInfo->thread_wait = nodeInfo->getThreadWait();
    *tmpNodeInfo->pre_threads = nodeInfo->getPrefetchThreads();
    *tmpNodeInfo->max_MBPS = nodeInfo->getMaxMBPS();
    *tmpNodeInfo->max_file_cache = nodeInfo->getMaxFilesToCache();
    *tmpNodeInfo->max_stat_cache = nodeInfo->getMaxStatCache();
    *tmpNodeInfo->work1_threads = nodeInfo->getWorker1Threads();
    *tmpNodeInfo->dm_evt_timeout = nodeInfo->getDmapiEventTimeout();
    *tmpNodeInfo->dm_mnt_timeout = nodeInfo->getDmapiMountTimeout();
    *tmpNodeInfo->dm_ses_timeout = nodeInfo->getDmapiSessFailureTimeout();
    *tmpNodeInfo->nsd_win_mnt = nodeInfo->getNsdServerWaitTimeWindowOnMount();
    *tmpNodeInfo->nsd_time_mnt = nodeInfo->getNsdServerWaitTimeForMount();    
    *tmpNodeInfo->num_disk_access = nodeInfo->getNumDiskAccesses();

    return tmpNodeInfo;

}

tlgpfs_node_info_t* DbNodeInfo::allocateMemory()
{
    tlgpfs_node_info* tmpNodeInfo = new tlgpfs_node_info();
    
    tmpNodeInfo->cluster_id        = new char[CLUSTER_ID_SIZE];
    memset(tmpNodeInfo->cluster_id, 0, CLUSTER_ID_SIZE);

    tmpNodeInfo->ip_addr           = new char[IP_ADDR_SIZE];
    memset(tmpNodeInfo->ip_addr, 0, IP_ADDR_SIZE);

    tmpNodeInfo->name              = new char[NAME_SIZE];
    memset(tmpNodeInfo->name, 0, NAME_SIZE);
    
    tmpNodeInfo->type              = new char[TYPE_SIZE];
    memset(tmpNodeInfo->type, 0, TYPE_SIZE);
    
    tmpNodeInfo->endian            = new char[ENDIAN_SIZE];
    memset(tmpNodeInfo->endian, 0, ENDIAN_SIZE);
    
    tmpNodeInfo->os_name           = new char[OS_NAME_SIZE];
    memset(tmpNodeInfo->os_name, 0, OS_NAME_SIZE);
    
    tmpNodeInfo->version           = new char[VERSION_SIZE];
    memset(tmpNodeInfo->version, 0, VERSION_SIZE);
    
    tmpNodeInfo->platform          = new char[PLATFORM_SIZE];
    memset(tmpNodeInfo->platform, 0, PLATFORM_SIZE);
    
    tmpNodeInfo->admin             = new char[ADMIN_SIZE];
    memset(tmpNodeInfo->admin, 0, ADMIN_SIZE);
    
    tmpNodeInfo->status            = new char[STATUS_SIZE];
    memset(tmpNodeInfo->status, 0, STATUS_SIZE);
    
    tmpNodeInfo->umnt_disk_fail    = new char[UMNT_DISK_FAIL_SIZE];
    memset(tmpNodeInfo->umnt_disk_fail, 0, UMNT_DISK_FAIL_SIZE);
    
    tmpNodeInfo->healthy           = new char[HEALTHY_SIZE];
    memset(tmpNodeInfo->healthy, 0, HEALTHY_SIZE);
    
    tmpNodeInfo->diag              = new char[DIAG_SIZE];
    memset(tmpNodeInfo->diag, 0, DIAG_SIZE);
        
    tmpNodeInfo->pg_pool_size      = new unsigned long long;
    memset(tmpNodeInfo->pg_pool_size, 0, sizeof( unsigned long long));
    
    tmpNodeInfo->failure_count     = new  int;
    memset(tmpNodeInfo->failure_count, 0, sizeof( int));

    tmpNodeInfo->thread_wait       = new  int;
    memset(tmpNodeInfo->thread_wait, 0, sizeof( int));
    
    tmpNodeInfo->pre_threads       = new  int;
    memset(tmpNodeInfo->pre_threads, 0, sizeof( int));
    
    tmpNodeInfo->max_MBPS          = new  int;
    memset(tmpNodeInfo->max_MBPS, 0, sizeof( int));
    
    tmpNodeInfo->max_file_cache    = new  int;
    memset(tmpNodeInfo->max_file_cache, 0, sizeof( int));
    
    tmpNodeInfo->max_stat_cache    = new  int;
    memset(tmpNodeInfo->max_stat_cache, 0, sizeof( int));
    
    tmpNodeInfo->work1_threads     = new  int;
    memset(tmpNodeInfo->work1_threads, 0, sizeof( int));
    
    tmpNodeInfo->dm_evt_timeout    = new  int;
    memset(tmpNodeInfo->dm_evt_timeout, 0, sizeof( int));
    
    tmpNodeInfo->dm_mnt_timeout    = new  int;
    memset(tmpNodeInfo->dm_mnt_timeout, 0, sizeof( int));
     
    tmpNodeInfo->dm_ses_timeout    = new  int;
    memset(tmpNodeInfo->dm_ses_timeout, 0, sizeof( int));

    tmpNodeInfo->nsd_win_mnt       = new  int;
    memset(tmpNodeInfo->nsd_win_mnt, 0, sizeof( int));
    
    tmpNodeInfo->nsd_time_mnt      = new  int;
    memset(tmpNodeInfo->nsd_time_mnt, 0, sizeof( int));
    
    tmpNodeInfo->num_disk_access   = new  int;
    memset(tmpNodeInfo->num_disk_access, 0, sizeof( int));

    tmpNodeInfo->change            = new  int;
    memset(tmpNodeInfo->change, 0, sizeof( int));

    tmpNodeInfo->health            = new  int;
    memset(tmpNodeInfo->health, 0, sizeof( int));    
    return tmpNodeInfo;
    
}


void DbNodeInfo::Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info)
{
    SQLRETURN ret;
    if(opType != UPDATE && opType != INSERT)
        return;
    tlgpfs_node_info_t* tmp = (tlgpfs_node_info_t*)info;

    int x = (opType == UPDATE) ? colSize - pkSize : 0;   

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN ipAddrLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, IP_ADDR_SIZE, 0, tmp->ip_addr, 0, &ipAddrLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN nameLen = tmp->name ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, NAME_SIZE, 0, tmp->name, 0, &nameLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN typeLen = tmp->type ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, TYPE_SIZE, 0, tmp->type, 0, &typeLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN endianLen = tmp->endian ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, ENDIAN_SIZE, 0, tmp->endian, 0, &endianLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN osNameLen = tmp->os_name ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, OS_NAME_SIZE, 0, tmp->os_name, 0, &osNameLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN versionLen = tmp->version ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, VERSION_SIZE, 0, tmp->version, 0, &versionLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN platformLen = tmp->platform ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, PLATFORM_SIZE, 0, tmp->platform, 0, &platformLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN adminLen = tmp->admin ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, ADMIN_SIZE, 0, tmp->admin, 0, &adminLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN statusLen = tmp->status ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, STATUS_SIZE, 0, tmp->status, 0, &statusLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN umntDiskFailLen = tmp->umnt_disk_fail ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, UMNT_DISK_FAIL_SIZE, 0, tmp->umnt_disk_fail, 0, &umntDiskFailLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthyLen = tmp->healthy ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, HEALTHY_SIZE, 0, tmp->healthy, 0, &healthyLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 12 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN diagLen = tmp->diag ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, DIAG_SIZE, 0, tmp->diag, 0, &diagLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 13 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN pgPoolSizeLen = tmp->pg_pool_size ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, tmp->pg_pool_size, 0, &pgPoolSizeLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 14 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN failureCountLen = tmp->failure_count ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->failure_count, 0, &failureCountLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 15 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN threadWaitLen = tmp->thread_wait ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->thread_wait, 0, &threadWaitLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 16 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN preThreadsLen = tmp->pre_threads ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->pre_threads, 0, &preThreadsLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 17 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN maxMBPSLen = tmp->max_MBPS ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->max_MBPS, 0, &maxMBPSLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 18 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN maxFileCacheLen = tmp->max_file_cache ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->max_file_cache, 0, &maxFileCacheLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 19 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN maxStatCacheLen = tmp->max_stat_cache ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->max_stat_cache, 0, &maxStatCacheLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 20 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN wrok1ThreadsLen = tmp->work1_threads ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->work1_threads, 0, &wrok1ThreadsLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 21 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN dmEvtTimeoutLen = tmp->dm_evt_timeout ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->dm_evt_timeout, 0, &dmEvtTimeoutLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 22 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN dmMntTimeoutLen = tmp->dm_mnt_timeout ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->dm_mnt_timeout, 0, &dmMntTimeoutLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 23 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN dmSesTimeoutLen = tmp->dm_ses_timeout ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->dm_ses_timeout, 0, &dmSesTimeoutLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 24 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN nsdWinMntLen = tmp->nsd_win_mnt ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->nsd_win_mnt, 0, &nsdWinMntLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 25 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN nsdTimeMntLen = tmp->nsd_time_mnt ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->nsd_time_mnt, 0, &nsdTimeMntLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 26 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN numDiskAccessLen = tmp->num_disk_access ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->num_disk_access, 0, &numDiskAccessLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 27 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN changeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 28 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLBindParameter 29 STMT",ret,sqlStmt,SQL_HANDLE_STMT);        

    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)upsertSql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbNodeInfo::Upsert SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbNodeInfo::updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst)
{
    vector<tlgpfs_node_info_t*>* tempv = (vector<tlgpfs_node_info_t*>*)temp;
    vector<tlgpfs_node_info_t*>* lastv = (vector<tlgpfs_node_info_t*>*)lst;
    tlgpfs_node_info_t* last;

    tlgpfs_node_info_t* tmp = tempv->front();
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
   
   anyChange |= strcmp(tmp->name, last->name);
   anyChange |= strcmp(tmp->type, last->type);
   anyChange |= strcmp(tmp->endian, last->endian);
   anyChange |= strcmp(tmp->os_name, last->os_name);
   anyChange |= strcmp(tmp->version, last->version);
   anyChange |= strcmp(tmp->platform, last->platform);
   anyChange |= strcmp(tmp->admin, last->admin);
   anyChange |= strcmp(tmp->status, last->status);
   anyChange |= strcmp(tmp->umnt_disk_fail, last->umnt_disk_fail);
   anyChange |= strcmp(tmp->healthy, last->healthy);
   anyChange |= strcmp(tmp->diag, last->diag);   
   anyChange |= memcmp(tmp->pg_pool_size, last->pg_pool_size,sizeof( long long));
   anyChange |= memcmp(tmp->failure_count, last->failure_count,sizeof( int));
   anyChange |= memcmp(tmp->thread_wait, last->thread_wait,sizeof( int));
   anyChange |= memcmp(tmp->pre_threads, last->pre_threads,sizeof( int));
   anyChange |= memcmp(tmp->max_MBPS, last->max_MBPS,sizeof( int));
   anyChange |= memcmp(tmp->max_file_cache, last->max_file_cache,sizeof( int));
   anyChange |= memcmp(tmp->max_stat_cache, last->max_stat_cache,sizeof( int));
   anyChange |= memcmp(tmp->work1_threads, last->work1_threads,sizeof( int));
   anyChange |= memcmp(tmp->dm_evt_timeout, last->dm_evt_timeout,sizeof( int));
   anyChange |= memcmp(tmp->dm_mnt_timeout, last->dm_mnt_timeout,sizeof( int));
   anyChange |= memcmp(tmp->dm_ses_timeout, last->dm_ses_timeout,sizeof( int));
   anyChange |= memcmp(tmp->nsd_win_mnt, last->nsd_win_mnt,sizeof( int));
   anyChange |= memcmp(tmp->nsd_time_mnt, last->nsd_time_mnt,sizeof( int));
   anyChange |= memcmp(tmp->num_disk_access, last->num_disk_access,sizeof( int));

   *tmp->change = anyChange?CHANGE_MODIFIED:CHANGE_NONE;
   //"healthy": possible values are "yes", "no"
   //"status": possible values are "unknown", "down", "up", "failed","Unknown NodeStatus"
   //only when healthy == "yes" and status == "up", healthy status is healthy. Otherwise, unhealthy.
   if(!strcmp(tmp->healthy,"yes") && !strcmp(tmp->status,"up"))
       *tmp->health = HEALTHY;
   else
       *tmp->health = UNHEALTHY;
   updateTable(sqlStmt,table,tmp);

}
}

