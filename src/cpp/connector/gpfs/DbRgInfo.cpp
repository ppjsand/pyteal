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
#include "DbRgInfo.h"
#include <iomanip>
namespace TEAL
{
DbRgInfo::DbRgInfo(DbInterface* dbi, vector<string>* cols, vector<string>* pk, tlgpfs_rg_info_t* rg):DbGpfsInfo(dbi,REGULAR_RG_TABLE,TMP_RG_TABLE,cols,pk,rg)
{
    if (rg) 
    {
        if (!rg->cluster_id) throw std::invalid_argument("Cluster id is NULL");
        if (!rg->rg_name) throw std::invalid_argument("RG name is NULL");
        if (!rg->change) throw std::invalid_argument("Change is NULL");
        if (!rg->health) throw std::invalid_argument("health is NULL");
    }
    if(cols)
    {
        cols->push_back("cluster_id");
        cols->push_back("rg_name");
        cols->push_back("rg_act_svr");
        cols->push_back("rg_svrs");
        cols->push_back("rg_id");
        cols->push_back("rg_das");
        cols->push_back("rg_vdisks");
        cols->push_back("rg_pdisks");
        cols->push_back("change");
        cols->push_back("health");
    }
    if(pk)
    {
        pk->push_back("cluster_id");
        pk->push_back("rg_name");
    }

}

DbRgInfo::~DbRgInfo()
{
}


void DbRgInfo::printStatus(tlgpfs_rg_info_t* rg, bool detailed)
{
    if(rg == NULL)
        cerr<<"Can't print a null structure of status!"<<endl;

    cout<<setiosflags(ios::left)<<setw(20)<<"cluster_id"     <<setiosflags(ios::left)<<setw(40)<<"(cluster id)"                                   <<": "<< rg->cluster_id      <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"rg_name"        <<setiosflags(ios::left)<<setw(40)<<"(recovery group name)"                          <<": "<< rg->rg_name         <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"health"         <<setiosflags(ios::left)<<setw(40)<<"(health status)"                                <<": "<<string((*rg->health == HEALTHY)?"healthy":((*rg->health == UNHEALTHY)?"unhealthy":"unknown"))<<endl;    
    if(!detailed)
        return;
    cout<<setiosflags(ios::left)<<setw(20)<<"rg_act_svr"     <<setiosflags(ios::left)<<setw(40)<<"(recovery group active server)"                 <<": "<< rg->rg_act_svr      <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"rg_svrs"        <<setiosflags(ios::left)<<setw(40)<<"(recovery group servers)"                       <<": "<< rg->rg_svrs         <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"rg_id"          <<setiosflags(ios::left)<<setw(40)<<"(recovery group id number)"                     <<": "<< rg->rg_id           <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"rg_das"         <<setiosflags(ios::left)<<setw(40)<<"(recovery group DA number)"                     <<": "<<*rg->rg_das          <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"rg_vdisks"      <<setiosflags(ios::left)<<setw(40)<<"(recovery group vdisk number)"                  <<": "<<*rg->rg_vdisks       <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"rg_pdisks"      <<setiosflags(ios::left)<<setw(40)<<"(recovery group pdisk number)"                  <<": "<<*rg->rg_pdisks       <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"change"         <<setiosflags(ios::left)<<setw(40)<<"(change value)"                                 <<": "<<*rg->change          <<endl;

}

void DbRgInfo::getResult(SQLHSTMT sqlStmt,void** holder)
{
    SQLRETURN ret;
    *holder = new vector<tlgpfs_rg_info_t*>;
    vector<tlgpfs_rg_info_t*>* status = (vector<tlgpfs_rg_info_t*>*)* holder;
    tlgpfs_rg_info_t* tmp = allocateMemory();


    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 1, SQL_C_CHAR, tmp->cluster_id, CLUSTER_ID_SIZE, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbRgInfo::getResult SQLBindCol 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN rgNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 2, SQL_C_CHAR, tmp->rg_name, RG_NAME_SIZE, &rgNameLen);
    DbInterface::checkSqlRetcode("DbRgInfo::getResult SQLBindCol 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN rgActSvrLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 3, SQL_C_CHAR, tmp->rg_act_svr, RG_ACT_SVR_SIZE, &rgActSvrLen);
    DbInterface::checkSqlRetcode("DbRgInfo::getResult SQLBindCol 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rgSvrsLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 4, SQL_C_CHAR, tmp->rg_svrs, RG_SVRS_SIZE, &rgSvrsLen);
    DbInterface::checkSqlRetcode("DbRgInfo::getResult SQLBindCol 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rgIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 5, SQL_C_CHAR, tmp->rg_id, RG_ID_SIZE, &rgIdLen);
    DbInterface::checkSqlRetcode("DbRgInfo::getResult SQLBindCol 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rgDasLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 6, SQL_C_SLONG, tmp->rg_das, 0, &rgDasLen);
    DbInterface::checkSqlRetcode("DbRgInfo::getResult SQLBindCol 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rgVdisksLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 7, SQL_C_SLONG, tmp->rg_vdisks, 0, &rgVdisksLen);
    DbInterface::checkSqlRetcode("DbRgInfo::getResult SQLBindCol 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rgPdisksLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 8, SQL_C_SLONG, tmp->rg_pdisks, 0, &rgPdisksLen);
    DbInterface::checkSqlRetcode("DbRgInfo::getResult SQLBindCol 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN changeLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 9, SQL_C_SLONG, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbRgInfo::getResult SQLBindCol 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 10, SQL_C_SLONG, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbRgInfo::getResult SQLBindCol 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);    
    
    ret = DbInterface::dbModule.SQLFetch(sqlStmt);
    if(ret != SQL_NO_DATA)//don't roll back even if empty row.
        DbInterface::checkSqlRetcode("DbRgInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    
    while((ret == SQL_SUCCESS || ret == SQL_SUCCESS_WITH_INFO))
    {
        
        tlgpfs_rg_info_t* temp = allocateMemory();
        copyInfo(temp,tmp);
        status->push_back(temp);
        resetMemory(tmp);
        ret = DbInterface::dbModule.SQLFetch(sqlStmt);
        if(ret != SQL_NO_DATA)//don't roll back even if empty row.
            DbInterface::checkSqlRetcode("DbRgInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    }


}

void DbRgInfo::resetMemory(tlgpfs_rg_info* tmpRgInfo)
{
    if( tmpRgInfo == NULL )
        return;
    
    memset(tmpRgInfo->cluster_id, 0, CLUSTER_ID_SIZE);

    memset(tmpRgInfo->rg_name, 0, RG_NAME_SIZE);

    memset(tmpRgInfo->rg_act_svr, 0, RG_ACT_SVR_SIZE);
    
    memset(tmpRgInfo->rg_svrs, 0, RG_SVRS_SIZE);
    
    memset(tmpRgInfo->rg_id, 0, RG_ID_SIZE);
    
    memset(tmpRgInfo->rg_das, 0, RG_DAS_SIZE);
    
    memset(tmpRgInfo->rg_vdisks, 0, RG_VDISKS_SIZE);
    
    memset(tmpRgInfo->rg_pdisks, 0, RG_PDISKS_SIZE);
    
    memset(tmpRgInfo->change, 0, sizeof( int));
    
    memset(tmpRgInfo->health, 0, sizeof( int));    

}

void DbRgInfo::copyInfo(tlgpfs_rg_info_t* dst, tlgpfs_rg_info_t* src)
{
    strcpy(dst->cluster_id, src->cluster_id);
    strcpy(dst->rg_name,    src->rg_name);
    strcpy(dst->rg_act_svr, src->rg_act_svr);
    strcpy(dst->rg_svrs,    src->rg_svrs);
    strcpy(dst->rg_id,      src->rg_id);
    *dst->rg_das    = *src->rg_das;
    *dst->rg_vdisks = *src->rg_vdisks;
    *dst->rg_pdisks = *src->rg_pdisks;
    *dst->change    = *src->change;
    *dst->health    = *src->health;
}


tlgpfs_rg_info_t* DbRgInfo::extract(gpfsRecoveryGroup* rgInfo, string& clusterId)
{
    if(rgInfo == NULL)
        return NULL;
    tlgpfs_rg_info* tmpRgInfo = allocateMemory();
    strcpy(tmpRgInfo->cluster_id, clusterId.c_str());
    strcpy(tmpRgInfo->rg_name, rgInfo->getRecoveryGroupName());
    strcpy(tmpRgInfo->rg_act_svr, rgInfo->getRecoveryGroupActiveServer());
    strcpy(tmpRgInfo->rg_svrs, rgInfo->getRecoveryGroupServers());
    strcpy(tmpRgInfo->rg_id, rgInfo->getRecoveryGroupId());

    *tmpRgInfo->rg_das    = rgInfo->getRecoveryGroupDeclusterArrays();
    *tmpRgInfo->rg_vdisks = rgInfo->getRecoveryGroupVdisks();
    *tmpRgInfo->rg_pdisks = rgInfo->getRecoveryGroupPdisks();

    return tmpRgInfo;

}

tlgpfs_rg_info_t* DbRgInfo::allocateMemory()
{
    tlgpfs_rg_info* tmpRgInfo = new tlgpfs_rg_info();
    
    tmpRgInfo->cluster_id        = new char[CLUSTER_ID_SIZE];
    memset(tmpRgInfo->cluster_id, 0, CLUSTER_ID_SIZE);

    tmpRgInfo->rg_name           = new char[RG_NAME_SIZE];
    memset(tmpRgInfo->rg_name, 0, RG_NAME_SIZE);

    tmpRgInfo->rg_act_svr        = new char[RG_ACT_SVR_SIZE];
    memset(tmpRgInfo->rg_act_svr, 0, RG_ACT_SVR_SIZE);
    
    tmpRgInfo->rg_svrs           = new char[RG_SVRS_SIZE];
    memset(tmpRgInfo->rg_svrs, 0, RG_SVRS_SIZE);
    
    tmpRgInfo->rg_id             = new char[RG_ID_SIZE];
    memset(tmpRgInfo->rg_id, 0, RG_ID_SIZE);
        
    tmpRgInfo->rg_das            = new int;
    memset(tmpRgInfo->rg_das, 0, sizeof( int));
    
    tmpRgInfo->rg_vdisks         = new  int;
    memset(tmpRgInfo->rg_vdisks, 0, sizeof( int));

    tmpRgInfo->rg_pdisks         = new  int;
    memset(tmpRgInfo->rg_pdisks, 0, sizeof( int));

    tmpRgInfo->change            = new  int;
    memset(tmpRgInfo->change, 0, sizeof( int));

    tmpRgInfo->health            = new  int;
    memset(tmpRgInfo->health, 0, sizeof( int));    
    return tmpRgInfo;
    
}


void DbRgInfo::Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info)
{
    SQLRETURN ret;
    if(opType != UPDATE && opType != INSERT)
        return;
    tlgpfs_rg_info_t* tmp = (tlgpfs_rg_info_t*)info;

    int x = (opType == UPDATE) ? colSize - pkSize : 0;   

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbRgInfo::Upsert SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rgNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, RG_NAME_SIZE, 0, tmp->rg_name, 0, &rgNameLen);
    DbInterface::checkSqlRetcode("DbRgInfo::Upsert SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rgActSvrLen = tmp->rg_act_svr ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, RG_ACT_SVR_SIZE, 0, tmp->rg_act_svr, 0, &rgActSvrLen);
    DbInterface::checkSqlRetcode("DbRgInfo::Upsert SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rgSvrsLen = tmp->rg_svrs ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, RG_SVRS_SIZE, 0, tmp->rg_svrs, 0, &rgSvrsLen);
    DbInterface::checkSqlRetcode("DbRgInfo::Upsert SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rgIdLen = tmp->rg_id ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, RG_ID_SIZE, 0, tmp->rg_id, 0, &rgIdLen);
    DbInterface::checkSqlRetcode("DbRgInfo::Upsert SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rgDasLen = tmp->rg_das ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->rg_das, 0, &rgDasLen);
    DbInterface::checkSqlRetcode("DbRgInfo::Upsert SQLBindParameter 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN rgVdisksLen = tmp->rg_vdisks ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->rg_vdisks, 0, &rgVdisksLen);
    DbInterface::checkSqlRetcode("DbRgInfo::Upsert SQLBindParameter 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN rgPdisksLen = tmp->rg_pdisks ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->rg_pdisks, 0, &rgPdisksLen);
    DbInterface::checkSqlRetcode("DbRgInfo::Upsert SQLBindParameter 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
   
    SQLLEN changeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbRgInfo::Upsert SQLBindParameter 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbRgInfo::Upsert SQLBindParameter 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);        

    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)upsertSql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbRgInfo::Upsert SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbRgInfo::bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init)
{
    SQLRETURN ret;
    int x = 1;
    tlgpfs_rg_info_t* tmp = (tlgpfs_rg_info_t*)info;

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbRgInfo::bindPrimaryKey SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rgNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, RG_NAME_SIZE, 0, tmp->rg_name, 0, &rgNameLen);
    DbInterface::checkSqlRetcode("DbRgInfo::bindPrimaryKey SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    if( init )
    {
        int changeValue = 100;//init to 100
        int healthValue = 100;
        
        SQLLEN changeLen = SQL_NTS;    
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &changeValue, 0, &changeLen);
        DbInterface::checkSqlRetcode("DbRgInfo::bindPrimaryKey SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

        SQLLEN healthLen = SQL_NTS;        
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &healthValue, 0, &healthLen);
        DbInterface::checkSqlRetcode("DbRgInfo::bindPrimaryKey SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);    
    }
    
    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)sql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbRgInfo::bindPrimaryKey SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbRgInfo::updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst)
{
    vector<tlgpfs_rg_info_t*>* tempv = (vector<tlgpfs_rg_info_t*>*)temp;
    vector<tlgpfs_rg_info_t*>* lastv = (vector<tlgpfs_rg_info_t*>*)lst;
    tlgpfs_rg_info_t* last;

    tlgpfs_rg_info_t* tmp = tempv->front();
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
   
   anyChange |= strcmp(tmp->rg_act_svr, last->rg_act_svr);
   anyChange |= strcmp(tmp->rg_svrs, last->rg_svrs);
   anyChange |= strcmp(tmp->rg_id, last->rg_id);
   anyChange |= memcmp(tmp->rg_das, last->rg_das,sizeof( int));
   anyChange |= memcmp(tmp->rg_vdisks, last->rg_vdisks,sizeof( int));
   anyChange |= memcmp(tmp->rg_pdisks, last->rg_pdisks,sizeof( int));
   
   *tmp->change = anyChange?CHANGE_MODIFIED:CHANGE_NONE;
   //identify healthy status in GPFSConfigHandler.cpp due to convenience
   #if 0
   //if rg has an active server, it's healthy
   if(tmp->rg_act_svr && strlen(tmp->rg_act_svr))
       *tmp->health = HEALTHY;
   else
       *tmp->health = UNHEALTHY;
   #endif
   updateTable(sqlStmt,table,tmp);

}
}

