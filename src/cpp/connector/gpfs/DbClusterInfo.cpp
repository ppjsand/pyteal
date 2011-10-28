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
#include "DbClusterInfo.h"
#include <iomanip>
namespace TEAL
{
DbClusterInfo::DbClusterInfo(DbInterface* dbi, vector<string>* cols, vector<string>* pk, tlgpfs_cluster_info_t* cluster):DbGpfsInfo(dbi,REGULAR_CLUSTER_TABLE,TMP_CLUSTER_TABLE,cols,pk,cluster)
{ 
    if (cluster)
    {
        if (!cluster->cluster_id) throw std::invalid_argument("Cluster id is NULL");
        if (!cluster->change) throw std::invalid_argument("Change is NULL");
        if (!cluster->health) throw std::invalid_argument("health is NULL");
    }
    if(cols)
    {
        cols->push_back("cluster_id");
        cols->push_back("cluster_name");
        cols->push_back("cluster_type");
        cols->push_back("min_rel_level");
        cols->push_back("uid_domain");
        cols->push_back("rsh_cmd");
        cols->push_back("rcp_cmd");
        cols->push_back("prim_server");
        cols->push_back("sec_server");        
        cols->push_back("c_ref_time");        
        cols->push_back("n_ref_time");
        cols->push_back("f_ref_time");
        cols->push_back("fp_ref_time");
        cols->push_back("sdr_fs_num");
        cols->push_back("num_nodes");
        cols->push_back("max_blk_size");
        cols->push_back("num_fs");
        cols->push_back("token_server");
        cols->push_back("fail_det_time");
        cols->push_back("tcp_port");
        cols->push_back("min_timeout");
        cols->push_back("max_timeout");
        cols->push_back("num_free_disk");
        cols->push_back("change");
        cols->push_back("health");
    }
    if(pk)
        pk->push_back("cluster_id");
}

DbClusterInfo::~DbClusterInfo()
{
}

void DbClusterInfo::bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init)
{
    SQLRETURN ret;
    int x = 1;
    tlgpfs_cluster_info_t* tmp = (tlgpfs_cluster_info_t*)info;

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::bindPrimaryKey SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    if( init )
    {
        int changeValue = 100;//init to 100
        int healthValue = 100;
        
        SQLLEN changeLen = SQL_NTS;    
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &changeValue, 0, &changeLen);
        DbInterface::checkSqlRetcode("DbClusterInfo::bindPrimaryKey SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

        SQLLEN healthLen = SQL_NTS;        
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &healthValue, 0, &healthLen);
        DbInterface::checkSqlRetcode("DbClusterInfo::bindPrimaryKey SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);    
    }
    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)sql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbClusterInfo::bindPrimaryKey SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbClusterInfo::getResult(SQLHSTMT sqlStmt,void** holder)//query all the columns
{
    SQLRETURN ret;
    *holder = new vector<tlgpfs_cluster_info_t*>;
    vector<tlgpfs_cluster_info_t*>* status = (vector<tlgpfs_cluster_info_t*>*)* holder;
    tlgpfs_cluster_info_t* tmp = allocateMemory();
    
    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 1, SQL_C_CHAR, tmp->cluster_id, CLUSTER_ID_SIZE, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN clusterNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 2, SQL_C_CHAR, tmp->cluster_name, CLUSTER_NAME_SIZE, &clusterNameLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN clusterTypeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 3, SQL_C_CHAR, tmp->cluster_type, CLUSTER_TYPE_SIZE, &clusterTypeLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN minRelLevelLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 4, SQL_C_CHAR, tmp->min_rel_level, MIN_REL_LEVEL_SIZE, &minRelLevelLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN uidDomainLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 5, SQL_C_CHAR, tmp->uid_domain, UID_DOMAIN_SIZE, &uidDomainLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rshCmdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 6, SQL_C_CHAR, tmp->rsh_cmd, RSH_CMD_SIZE, &rshCmdLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rcpCmdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 7, SQL_C_CHAR, tmp->rcp_cmd, RCP_CMD_SIZE, &rcpCmdLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN primServerLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 8, SQL_C_CHAR, tmp->prim_server, PRIM_SERVER_SIZE, &primServerLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN secServerLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 9, SQL_C_CHAR, tmp->sec_server, SEC_SERVER_SIZE, &secServerLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN cRefTimeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 10, SQL_C_CHAR, tmp->c_ref_time, C_REF_TIME_SIZE, &cRefTimeLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN nRefTimeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 11, SQL_C_CHAR, tmp->n_ref_time, N_REF_TIME_SIZE, &nRefTimeLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN fRefTimeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 12, SQL_C_CHAR, tmp->f_ref_time, F_REF_TIME_SIZE, &fRefTimeLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 12 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN fpRefTimeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 13, SQL_C_CHAR, tmp->fp_ref_time, FP_REF_TIME_SIZE, &fpRefTimeLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 13 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN sdrFsNumLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 14, SQL_C_SLONG, tmp->sdr_fs_num, 0, &sdrFsNumLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 14 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN numNodesLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 15, SQL_C_SLONG, tmp->num_nodes, 0, &numNodesLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 15 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN maxBlkSizeLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 16, SQL_C_SLONG, tmp->max_blk_size, 0, &maxBlkSizeLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 16 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN numFsLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 17, SQL_C_SLONG, tmp->num_fs, 0, &numFsLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 17 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN tokenServerLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 18, SQL_C_SLONG, tmp->token_server, 0, &tokenServerLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 18 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN failDetTimeLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 19, SQL_C_SLONG, tmp->fail_det_time, 0, &failDetTimeLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 19 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN tcpPortLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 20, SQL_C_SLONG,tmp->tcp_port, 0, &tcpPortLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 20 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN minTimeoutLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 21, SQL_C_SLONG, tmp->min_timeout, 0, &minTimeoutLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 21 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN maxTimeoutLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 22, SQL_C_SLONG, tmp->max_timeout, 0, &maxTimeoutLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 22 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN numFreeDiskLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 23, SQL_C_SLONG, tmp->num_free_disk, 0, &numFreeDiskLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 23 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN changeLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 24, SQL_C_SLONG, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 24 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 25, SQL_C_SLONG, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLBindCol 25 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    ret = DbInterface::dbModule.SQLFetch(sqlStmt);
    if(ret != SQL_NO_DATA)//don't roll back even if empty row.
        DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    while((ret == SQL_SUCCESS || ret == SQL_SUCCESS_WITH_INFO))
    {
        tlgpfs_cluster_info_t* temp = allocateMemory();
        copyInfo(temp,tmp); //copy away data fetched for next fetch
        status->push_back(temp);
        resetMemory(tmp);  //clear memory for next fetch
        ret = DbInterface::dbModule.SQLFetch(sqlStmt);
        if(ret != SQL_NO_DATA)//don't roll back even if empty row.
            DbInterface::checkSqlRetcode("DbClusterInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    }
}

void DbClusterInfo::printStatus(tlgpfs_cluster_info_t* cluster, bool detailed)
{
    if(cluster == NULL)
        cerr<<"Can't print a null structure of status!"<<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"cluster_id"     <<setiosflags(ios::left)<<setw(40)<<"(cluster id)"                              <<": "<<cluster->cluster_id     <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"cluster_name"   <<setiosflags(ios::left)<<setw(40)<<"(cluster name)"                            <<": "<< cluster->cluster_name  <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"health"         <<setiosflags(ios::left)<<setw(40)<<"(health status)"                           <<": "<<string((*cluster->health == HEALTHY)?"healthy":((*cluster->health == UNHEALTHY)?"unhealthy":"unknown"))<<endl;
    if(!detailed)
        return;
    cout<<setiosflags(ios::left)<<setw(20)<<"cluster_type"   <<setiosflags(ios::left)<<setw(40)<<"(cluster type)"                            <<": "<< cluster->cluster_type  <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"min_rel_level"  <<setiosflags(ios::left)<<setw(40)<<"(minimum release level)"                   <<": "<< cluster->min_rel_level <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"uid_domain"     <<setiosflags(ios::left)<<setw(40)<<"(uid domain)"                              <<": "<< cluster->uid_domain    <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"rsh_cmd"        <<setiosflags(ios::left)<<setw(40)<<"(remote shell command)"                    <<": "<< cluster->rsh_cmd       <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"rcp_cmd"        <<setiosflags(ios::left)<<setw(40)<<"(remote copy command)"                     <<": "<< cluster->rcp_cmd       <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"prim_server"    <<setiosflags(ios::left)<<setw(40)<<"(primary server)"                          <<": "<< cluster->prim_server   <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"sec_server"     <<setiosflags(ios::left)<<setw(40)<<"(secondary server)"                        <<": "<<cluster->sec_server     <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"c_ref_time"     <<setiosflags(ios::left)<<setw(40)<<"(cluster refresh time)"                    <<": "<< cluster->c_ref_time    <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"n_ref_time"     <<setiosflags(ios::left)<<setw(40)<<"(node refresh time)"                       <<": "<< cluster->n_ref_time    <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"f_ref_time"     <<setiosflags(ios::left)<<setw(40)<<"(file system refresh time)"                <<": "<< cluster->f_ref_time    <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"fp_ref_time"    <<setiosflags(ios::left)<<setw(40)<<"(file system performance refresh time)"    <<": "<< cluster->fp_ref_time   <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"sdr_fs_num"     <<setiosflags(ios::left)<<setw(40)<<"(sdr file system generated number)"        <<": "<<*cluster->sdr_fs_num    <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"num_nodes"      <<setiosflags(ios::left)<<setw(40)<<"(node items number)"                       <<": "<<*cluster->num_nodes     <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"max_blk_size"   <<setiosflags(ios::left)<<setw(40)<<"(maximum block size)"                      <<": "<<*cluster->max_blk_size  <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"num_fs"         <<setiosflags(ios::left)<<setw(40)<<"(file system items number)"                <<": "<<*cluster->num_fs        <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"token_server"   <<setiosflags(ios::left)<<setw(40)<<"(distributed token server number)"         <<": "<<*cluster->token_server  <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"fail_det_time"  <<setiosflags(ios::left)<<setw(40)<<"(failure detection time)"                  <<": "<<*cluster->fail_det_time <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"tcp_port"       <<setiosflags(ios::left)<<setw(40)<<"(tcp port number)"                         <<": "<<*cluster->tcp_port      <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"min_timeout"    <<setiosflags(ios::left)<<setw(40)<<"(minimum missed ping time out)"            <<": "<<*cluster->min_timeout   <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"max_timeout"    <<setiosflags(ios::left)<<setw(40)<<"(maximum missed ping time out)"            <<": "<<*cluster->max_timeout   <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"num_free_disk"  <<setiosflags(ios::left)<<setw(40)<<"(free disk items number)"                  <<": "<<*cluster->num_free_disk <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"change"         <<setiosflags(ios::left)<<setw(40)<<"(change value)"                            <<": "<<*cluster->change        <<endl;

}

void DbClusterInfo::copyInfo(tlgpfs_cluster_info_t* dst, tlgpfs_cluster_info_t* src)
{
    strcpy(dst->cluster_id, src->cluster_id);
    strcpy(dst->cluster_name, src->cluster_name);
    strcpy(dst->cluster_type, src->cluster_type);
    strcpy(dst->min_rel_level, src->min_rel_level);
    strcpy(dst->uid_domain, src->uid_domain);
    strcpy(dst->rsh_cmd, src->rsh_cmd);
    strcpy(dst->rcp_cmd, src->rcp_cmd);
    strcpy(dst->prim_server, src->prim_server);
    strcpy(dst->sec_server, src->sec_server);
    strcpy(dst->c_ref_time, src->c_ref_time);
    strcpy(dst->n_ref_time, src->n_ref_time);
    strcpy(dst->f_ref_time, src->f_ref_time);
    strcpy(dst->fp_ref_time, src->fp_ref_time);
    *dst->sdr_fs_num = *src->sdr_fs_num;
    *dst->num_nodes = *src->num_nodes;
    *dst->max_blk_size = *src->max_blk_size;
    *dst->num_fs = *src->num_fs;
    *dst->token_server = *src->token_server;
    *dst->fail_det_time = *src->fail_det_time;
    *dst->tcp_port = *src->tcp_port;
    *dst->min_timeout = *src->min_timeout;
    *dst->max_timeout = *src->max_timeout;
    *dst->num_free_disk = *src->num_free_disk;
    *dst->change = *src->change;
    *dst->health = *src->health;

}

tlgpfs_cluster_info_t* DbClusterInfo::extract(ClusterInfo* clusterInfo)
{
    if(clusterInfo == NULL)
        return NULL;
    tlgpfs_cluster_info* tmpClusterInfo = allocateMemory();
    strcpy(tmpClusterInfo->cluster_id, clusterInfo->getId());
    strcpy(tmpClusterInfo->cluster_name, clusterInfo->getName());
    strcpy(tmpClusterInfo->cluster_type, clusterInfo->getType());
    strcpy(tmpClusterInfo->min_rel_level, clusterInfo->getMinReleaseLevel());
    strcpy(tmpClusterInfo->uid_domain, clusterInfo->getUidDomain());
    strcpy(tmpClusterInfo->rsh_cmd, clusterInfo->getRemoteShellCommand());
    strcpy(tmpClusterInfo->rcp_cmd, clusterInfo->getRemoteFileCopyCommand());
    strcpy(tmpClusterInfo->prim_server, clusterInfo->getPrimaryServer());
    strcpy(tmpClusterInfo->sec_server, clusterInfo->getSecondaryServer());
    struct timeval c_ref_time = clusterInfo->getClusterRefreshTime();
    Utils::timeval_to_char(&c_ref_time,tmpClusterInfo->c_ref_time);
    struct timeval n_ref_time = clusterInfo->getNodeRefreshTime();
    Utils::timeval_to_char(&n_ref_time,tmpClusterInfo->n_ref_time);
    struct timeval fs_ref_time = clusterInfo->getFSRefreshTime();
    Utils::timeval_to_char(&fs_ref_time,tmpClusterInfo->f_ref_time);
    struct timeval fp_ref_time = clusterInfo->getFSPerfRefreshTime();
    Utils::timeval_to_char(&fp_ref_time,tmpClusterInfo->fp_ref_time);
    *tmpClusterInfo->sdr_fs_num = clusterInfo->getSdrfsGenNumber();
    *tmpClusterInfo->num_nodes =clusterInfo->getNumNodes();
    *tmpClusterInfo->max_blk_size = clusterInfo->getMaxBlockSize();
    *tmpClusterInfo->num_fs = clusterInfo->getNumFilesystems();
    *tmpClusterInfo->token_server = clusterInfo->getDistributedTokenServer();
    *tmpClusterInfo->fail_det_time = clusterInfo->getFailureDetectionTime();
    *tmpClusterInfo->tcp_port = clusterInfo->getTCPPort();
    *tmpClusterInfo->min_timeout = clusterInfo->getMinMissedPingTimeout();
    *tmpClusterInfo->max_timeout = clusterInfo->getMaxMissedPingTimeout();
    *tmpClusterInfo->num_free_disk = clusterInfo->getNumFreeDisks();

    return tmpClusterInfo;

}

tlgpfs_cluster_info_t* DbClusterInfo::allocateMemory()
{
    tlgpfs_cluster_info* tmpClusterInfo = new tlgpfs_cluster_info();
    
    tmpClusterInfo->cluster_id        = new char[CLUSTER_ID_SIZE];
    memset(tmpClusterInfo->cluster_id, 0, CLUSTER_ID_SIZE);
    
    tmpClusterInfo->cluster_name      = new char[CLUSTER_NAME_SIZE];
    memset(tmpClusterInfo->cluster_name, 0, CLUSTER_NAME_SIZE);
    
    tmpClusterInfo->cluster_type      = new char[CLUSTER_TYPE_SIZE];
    memset(tmpClusterInfo->cluster_type, 0, CLUSTER_TYPE_SIZE);
    
    tmpClusterInfo->min_rel_level     = new char[MIN_REL_LEVEL_SIZE];
    memset(tmpClusterInfo->min_rel_level, 0, MIN_REL_LEVEL_SIZE);
    
    tmpClusterInfo->uid_domain        = new char[UID_DOMAIN_SIZE];
    memset(tmpClusterInfo->uid_domain, 0, UID_DOMAIN_SIZE);
    
    tmpClusterInfo->rsh_cmd           = new char[RSH_CMD_SIZE];
    memset(tmpClusterInfo->rsh_cmd, 0, RSH_CMD_SIZE);
    
    tmpClusterInfo->rcp_cmd           = new char[RCP_CMD_SIZE];
    memset(tmpClusterInfo->rcp_cmd, 0, RCP_CMD_SIZE);
    
    tmpClusterInfo->prim_server       = new char[PRIM_SERVER_SIZE];
    memset(tmpClusterInfo->prim_server, 0, PRIM_SERVER_SIZE);
    
    tmpClusterInfo->sec_server        = new char[SEC_SERVER_SIZE];
    memset(tmpClusterInfo->sec_server, 0, SEC_SERVER_SIZE);
    
    tmpClusterInfo->c_ref_time        = new char[C_REF_TIME_SIZE];
    memset(tmpClusterInfo->c_ref_time, 0, C_REF_TIME_SIZE);
    
    tmpClusterInfo->n_ref_time        = new char[N_REF_TIME_SIZE];
    memset(tmpClusterInfo->n_ref_time, 0, N_REF_TIME_SIZE);
    
    tmpClusterInfo->f_ref_time        = new char[F_REF_TIME_SIZE];
    memset(tmpClusterInfo->f_ref_time, 0, F_REF_TIME_SIZE);
    
    tmpClusterInfo->fp_ref_time       = new char[FP_REF_TIME_SIZE];
    memset(tmpClusterInfo->fp_ref_time, 0, FP_REF_TIME_SIZE);
    
    tmpClusterInfo->sdr_fs_num        = new  int;
    memset(tmpClusterInfo->sdr_fs_num, 0, sizeof( int));

    tmpClusterInfo->num_nodes         = new  int;
    memset(tmpClusterInfo->num_nodes, 0, sizeof( int));
    
    tmpClusterInfo->max_blk_size      = new  int;
    memset(tmpClusterInfo->max_blk_size, 0, sizeof( int));
    
    tmpClusterInfo->num_fs            = new  int;
    memset(tmpClusterInfo->num_fs, 0, sizeof( int));
    
    tmpClusterInfo->token_server      = new  int;
    memset(tmpClusterInfo->token_server, 0, sizeof( int));
    
    tmpClusterInfo->fail_det_time     = new  int;
    memset(tmpClusterInfo->fail_det_time, 0, sizeof( int));
    
    tmpClusterInfo->tcp_port          = new  int;
    memset(tmpClusterInfo->tcp_port, 0, sizeof( int));
    
    tmpClusterInfo->min_timeout       = new  int;
    memset(tmpClusterInfo->min_timeout, 0, sizeof( int));
    
    tmpClusterInfo->max_timeout       = new  int;
    memset(tmpClusterInfo->max_timeout, 0, sizeof( int));
     
    tmpClusterInfo->num_free_disk     = new  int;
    memset(tmpClusterInfo->num_free_disk, 0, sizeof( int));

    tmpClusterInfo->change            = new  int;
    memset(tmpClusterInfo->change, 0, sizeof( int));

    tmpClusterInfo->health            = new  int;
    memset(tmpClusterInfo->health, 0, sizeof( int));
    return tmpClusterInfo;
    
}


void DbClusterInfo::resetMemory(tlgpfs_cluster_info* tmpClusterInfo)
{
    if( tmpClusterInfo == NULL )
        return;
    
    memset(tmpClusterInfo->cluster_id, 0, CLUSTER_ID_SIZE);
    
    memset(tmpClusterInfo->cluster_name, 0, CLUSTER_NAME_SIZE);
    
    memset(tmpClusterInfo->cluster_type, 0, CLUSTER_TYPE_SIZE);
    
    memset(tmpClusterInfo->min_rel_level, 0, MIN_REL_LEVEL_SIZE);
    
    memset(tmpClusterInfo->uid_domain, 0, UID_DOMAIN_SIZE);
    
    memset(tmpClusterInfo->rsh_cmd, 0, RSH_CMD_SIZE);
    
    memset(tmpClusterInfo->rcp_cmd, 0, RCP_CMD_SIZE);
    
    memset(tmpClusterInfo->prim_server, 0, PRIM_SERVER_SIZE);
    
    memset(tmpClusterInfo->sec_server, 0, SEC_SERVER_SIZE);
    
    memset(tmpClusterInfo->c_ref_time, 0, C_REF_TIME_SIZE);
    
    memset(tmpClusterInfo->n_ref_time, 0, N_REF_TIME_SIZE);
    
    memset(tmpClusterInfo->f_ref_time, 0, F_REF_TIME_SIZE);
    
    memset(tmpClusterInfo->fp_ref_time, 0, FP_REF_TIME_SIZE);
    
    memset(tmpClusterInfo->sdr_fs_num, 0, sizeof( int));

    memset(tmpClusterInfo->num_nodes, 0, sizeof( int));
    
    memset(tmpClusterInfo->max_blk_size, 0, sizeof( int));
    
    memset(tmpClusterInfo->num_fs, 0, sizeof( int));
    
    memset(tmpClusterInfo->token_server, 0, sizeof( int));
    
    memset(tmpClusterInfo->fail_det_time, 0, sizeof( int));
    
    memset(tmpClusterInfo->tcp_port, 0, sizeof( int));
    
    memset(tmpClusterInfo->min_timeout, 0, sizeof( int));
    
    memset(tmpClusterInfo->max_timeout, 0, sizeof( int));
     
    memset(tmpClusterInfo->num_free_disk, 0, sizeof( int));

    memset(tmpClusterInfo->change, 0, sizeof( int));

    memset(tmpClusterInfo->health, 0, sizeof( int));
    
}

void DbClusterInfo::Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info)
{
    SQLRETURN ret;
    if(opType != UPDATE && opType != INSERT)
        return;
    tlgpfs_cluster_info_t* tmp = (tlgpfs_cluster_info_t*)info;

    int x = (opType == UPDATE) ? colSize - pkSize : 0;
   
    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN clusterNameLen = tmp->cluster_name ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_NAME_SIZE, 0, tmp->cluster_name, 0, &clusterNameLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN clusterTypeLen = tmp->cluster_type ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_TYPE_SIZE, 0, tmp->cluster_type, 0, &clusterTypeLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN minRelLevelLen = tmp->min_rel_level ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, MIN_REL_LEVEL_SIZE, 0, tmp->min_rel_level, 0, &minRelLevelLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN uidDomainLen = tmp->uid_domain ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, UID_DOMAIN_SIZE, 0, tmp->uid_domain, 0, &uidDomainLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rshCmdLen = tmp->rsh_cmd ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, RSH_CMD_SIZE, 0, tmp->rsh_cmd, 0, &rshCmdLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rcpCmdLen = tmp->rcp_cmd ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, RCP_CMD_SIZE, 0, tmp->rcp_cmd, 0, &rcpCmdLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN primServerLen = tmp->prim_server ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, PRIM_SERVER_SIZE, 0, tmp->prim_server, 0, &primServerLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN secServerLen = tmp->sec_server ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, SEC_SERVER_SIZE, 0, tmp->sec_server, 0, &secServerLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN cRefTimeLen = tmp->c_ref_time ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, C_REF_TIME_SIZE, 0, tmp->c_ref_time, 0, &cRefTimeLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN nRefTimeLen = tmp->n_ref_time ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, N_REF_TIME_SIZE, 0, tmp->n_ref_time, 0, &nRefTimeLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN fRefTimeLen = tmp->f_ref_time ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, F_REF_TIME_SIZE, 0, tmp->f_ref_time, 0, &fRefTimeLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 12 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN fpRefTimeLen = tmp->fp_ref_time ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, FP_REF_TIME_SIZE, 0, tmp->fp_ref_time, 0, &fpRefTimeLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 13 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN sdrFsNumLen = tmp->sdr_fs_num ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->sdr_fs_num, 0, &sdrFsNumLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 14 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN numNodesLen = tmp->num_nodes ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->num_nodes, 0, &numNodesLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 15 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN maxBlkSizeLen = tmp->max_blk_size ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->max_blk_size, 0, &maxBlkSizeLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 16 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN numFsLen = tmp->num_fs ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->num_fs, 0, &numFsLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 17 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN tokenServerLen = tmp->token_server ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->token_server, 0, &tokenServerLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 18 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN failDetTimeLen = tmp->fail_det_time ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->fail_det_time, 0, &failDetTimeLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 19 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN tcpPortLen = tmp->tcp_port ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->tcp_port, 0, &tcpPortLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 20 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN minTimeoutLen = tmp->min_timeout ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->min_timeout, 0, &minTimeoutLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 21 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN maxTimeoutLen = tmp->max_timeout ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->max_timeout, 0, &maxTimeoutLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 22 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN numFreeDiskLen = tmp->num_free_disk ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->num_free_disk, 0, &numFreeDiskLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 23 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN changeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 24 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLBindParameter 25 STMT",ret,sqlStmt,SQL_HANDLE_STMT);        
   
    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)upsertSql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbClusterInfo::Upsert SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbClusterInfo::updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst)
{

   vector<tlgpfs_cluster_info_t*>* tempv = (vector<tlgpfs_cluster_info_t*>*)temp;
   vector<tlgpfs_cluster_info_t*>* lastv = (vector<tlgpfs_cluster_info_t*>*)lst;
   tlgpfs_cluster_info_t* last;
   tlgpfs_cluster_info_t* tmp = tempv->front();
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
   
   anyChange |= strcmp(tmp->cluster_name, last->cluster_name);
   anyChange |= strcmp(tmp->cluster_type, last->cluster_type);
   anyChange |= strcmp(tmp->min_rel_level, last->min_rel_level);
   anyChange |= strcmp(tmp->uid_domain, last->uid_domain);
   anyChange |= strcmp(tmp->rsh_cmd, last->rsh_cmd);
   anyChange |= strcmp(tmp->rcp_cmd, last->rcp_cmd);
   anyChange |= strcmp(tmp->prim_server, last->prim_server);
   anyChange |= strcmp(tmp->sec_server, last->sec_server);
   anyChange |= strcmp(tmp->c_ref_time, last->c_ref_time);
   anyChange |= strcmp(tmp->n_ref_time, last->n_ref_time);
   anyChange |= strcmp(tmp->f_ref_time, last->f_ref_time);
   anyChange |= strcmp(tmp->fp_ref_time, last->fp_ref_time);
   anyChange |= memcmp(tmp->sdr_fs_num, last->sdr_fs_num,sizeof( int));
   anyChange |= memcmp(tmp->num_nodes, last->num_nodes,sizeof( int));
   anyChange |= memcmp(tmp->max_blk_size, last->max_blk_size,sizeof( int));
   anyChange |= memcmp(tmp->num_fs, last->num_fs,sizeof( int));
   anyChange |= memcmp(tmp->token_server, last->token_server,sizeof( int));
   anyChange |= memcmp(tmp->fail_det_time, last->fail_det_time,sizeof( int));
   anyChange |= memcmp(tmp->tcp_port, last->tcp_port,sizeof( int));
   anyChange |= memcmp(tmp->min_timeout, last->min_timeout,sizeof( int));
   anyChange |= memcmp(tmp->max_timeout, last->max_timeout,sizeof( int));
   anyChange |= memcmp(tmp->num_free_disk, last->num_free_disk,sizeof( int));

   *tmp->change = anyChange?CHANGE_MODIFIED:CHANGE_NONE;
   updateTable(sqlStmt,table,tmp);

}

}
