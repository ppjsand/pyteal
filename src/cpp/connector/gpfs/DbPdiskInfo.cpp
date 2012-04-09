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
#include "DbPdiskInfo.h"
#include <iomanip>
namespace TEAL
{
DbPdiskInfo::DbPdiskInfo(DbInterface* dbi, vector<string>* cols, vector<string>* pk, tlgpfs_pdisk_info_t* pdisk):DbGpfsInfo(dbi,REGULAR_PDISK_TABLE,TMP_PDISK_TABLE,cols,pk,pdisk)
{
    if (pdisk) 
    {
        if (!pdisk->cluster_id) throw std::invalid_argument("Cluster id is NULL");
        if (!pdisk->rg_name) throw std::invalid_argument("RG name is NULL");
        if (!pdisk->da_name) throw std::invalid_argument("DA name is NULL");
        if (!pdisk->pdisk_name) throw std::invalid_argument("pdisk name is NULL");
        if (!pdisk->change) throw std::invalid_argument("Change is NULL");
        if (!pdisk->health) throw std::invalid_argument("health is NULL");
    }
    if(cols)
    {
        cols->push_back("cluster_id");
        cols->push_back("rg_name");
        cols->push_back("da_name");
        cols->push_back("pdisk_name");
        cols->push_back("pdisk_dev_path");
        cols->push_back("pdisk_state");
        cols->push_back("pdisk_fru");
        cols->push_back("pdisk_location");
        cols->push_back("pdisk_repl_prior");
        cols->push_back("pdisk_free_space");
        cols->push_back("change");
        cols->push_back("health");
    }
    if(pk)
    {
        pk->push_back("cluster_id");
        pk->push_back("rg_name");
        pk->push_back("da_name");
        pk->push_back("pdisk_name");
    }

}

DbPdiskInfo::~DbPdiskInfo()
{
}


void DbPdiskInfo::printStatus(tlgpfs_pdisk_info_t* pdisk, bool detailed)
{
    if(pdisk == NULL)
        cerr<<"Can't print a null structure of status!"<<endl;

    cout<<setiosflags(ios::left)<<setw(20)<<"cluster_id"         <<setiosflags(ios::left)<<setw(40)<<"(cluster id)"                   <<": "<< pdisk->cluster_id               <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"rg_name"            <<setiosflags(ios::left)<<setw(40)<<"(recovery group name)"          <<": "<< pdisk->rg_name                  <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"da_name"            <<setiosflags(ios::left)<<setw(40)<<"(declustered array name)"       <<": "<< pdisk->da_name                  <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"pdisk_name"         <<setiosflags(ios::left)<<setw(40)<<"(pdisk name)"                   <<": "<< pdisk->pdisk_name               <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"health"             <<setiosflags(ios::left)<<setw(40)<<"(health status)"                <<": "<<string((*pdisk->health == HEALTHY)?"healthy":((*pdisk->health == UNHEALTHY)?"unhealthy":"unknown"))<<endl;    
    if(!detailed)
        return;
    cout<<setiosflags(ios::left)<<setw(20)<<"pdisk_dev_path"     <<setiosflags(ios::left)<<setw(40)<<"(pdisk device path)"            <<": "<< pdisk->pdisk_dev_path           <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"pdisk_state"        <<setiosflags(ios::left)<<setw(40)<<"(pdisk state)"                  <<": "<< pdisk->pdisk_state              <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"pdisk_fru"          <<setiosflags(ios::left)<<setw(40)<<"(pdisk fru)"                    <<": "<< pdisk->pdisk_fru                <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"pdisk_location"     <<setiosflags(ios::left)<<setw(40)<<"(pdisk location)"               <<": "<< pdisk->pdisk_location           <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"pdisk_repl_prior"   <<setiosflags(ios::left)<<setw(40)<<"(pdisk replacement priority)"   <<": "<<*pdisk->pdisk_repl_prior         <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"pdisk_free_space"   <<setiosflags(ios::left)<<setw(40)<<"(pdisk free space in bytes)"    <<": "<<*pdisk->pdisk_free_space         <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"change"             <<setiosflags(ios::left)<<setw(40)<<"(change value)"                 <<": "<<*pdisk->change                   <<endl;

}

void DbPdiskInfo::getResult(SQLHSTMT sqlStmt,void** holder)
{
    SQLRETURN ret;
    *holder = new vector<tlgpfs_pdisk_info_t*>;
    vector<tlgpfs_pdisk_info_t*>* status = (vector<tlgpfs_pdisk_info_t*>*)* holder;
    tlgpfs_pdisk_info_t* tmp = allocateMemory();


    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 1, SQL_C_CHAR, tmp->cluster_id, CLUSTER_ID_SIZE, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::getResult SQLBindCol 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN rgNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 2, SQL_C_CHAR, tmp->rg_name, RG_NAME_SIZE, &rgNameLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::getResult SQLBindCol 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN daNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 3, SQL_C_CHAR, tmp->da_name, DA_NAME_SIZE, &daNameLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::getResult SQLBindCol 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);  
    
    SQLLEN pdiskNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 4, SQL_C_CHAR, tmp->pdisk_name, PDISK_NAME_SIZE, &pdiskNameLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::getResult SQLBindCol 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN pdiskDevPathLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 5, SQL_C_CHAR, tmp->pdisk_dev_path, PDISK_DEV_PATH_SIZE, &pdiskDevPathLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::getResult SQLBindCol 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN pdiskStateLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 6, SQL_C_CHAR, tmp->pdisk_state, PDISK_STATE_SIZE, &pdiskStateLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::getResult SQLBindCol 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN pdiskFruLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 7, SQL_C_CHAR, tmp->pdisk_fru, PDISK_FRU_SIZE, &pdiskFruLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::getResult SQLBindCol 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN pdiskLocationLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 8, SQL_C_CHAR, tmp->pdisk_location, PDISK_LOCATION_SIZE, &pdiskLocationLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::getResult SQLBindCol 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN pdiskReplPriorLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 9, SQL_C_SLONG, tmp->pdisk_repl_prior, 0, &pdiskReplPriorLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::getResult SQLBindCol 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN pdiskFreeSpaceLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 10, SQL_C_UBIGINT, tmp->pdisk_free_space, 0, &pdiskFreeSpaceLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::getResult SQLBindCol 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN changeLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 11, SQL_C_SLONG, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::getResult SQLBindCol 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 12, SQL_C_SLONG, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::getResult SQLBindCol 12 STMT",ret,sqlStmt,SQL_HANDLE_STMT);    
    
    ret = DbInterface::dbModule.SQLFetch(sqlStmt);
    if(ret != SQL_NO_DATA)//don't roll back even if empty row.
        DbInterface::checkSqlRetcode("DbPdiskInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    
    while((ret == SQL_SUCCESS || ret == SQL_SUCCESS_WITH_INFO))
    {
        
        tlgpfs_pdisk_info_t* temp = allocateMemory();
        copyInfo(temp,tmp);
        status->push_back(temp);
        resetMemory(tmp);
        ret = DbInterface::dbModule.SQLFetch(sqlStmt);
        if(ret != SQL_NO_DATA)//don't roll back even if empty row.
            DbInterface::checkSqlRetcode("DbPdiskInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    }

}

void DbPdiskInfo::resetMemory(tlgpfs_pdisk_info* tmpPdiskInfo)
{
    if( tmpPdiskInfo == NULL )
        return;
    
    memset(tmpPdiskInfo->cluster_id, 0, CLUSTER_ID_SIZE);

    memset(tmpPdiskInfo->rg_name, 0, RG_NAME_SIZE);

    memset(tmpPdiskInfo->da_name, 0, DA_NAME_SIZE);

    memset(tmpPdiskInfo->pdisk_name, 0, PDISK_NAME_SIZE);  
    
    memset(tmpPdiskInfo->pdisk_dev_path, 0, PDISK_DEV_PATH_SIZE);
    
    memset(tmpPdiskInfo->pdisk_state, 0, PDISK_STATE_SIZE);
    
    memset(tmpPdiskInfo->pdisk_fru, 0, PDISK_FRU_SIZE);
    
    memset(tmpPdiskInfo->pdisk_location, 0, PDISK_LOCATION_SIZE);
    
    memset(tmpPdiskInfo->pdisk_repl_prior, 0, PDISK_REPL_PRIOR_SIZE);
    
    memset(tmpPdiskInfo->pdisk_free_space, 0, PDISK_FREE_SPACE_SIZE);
    
    memset(tmpPdiskInfo->change, 0, sizeof( int));
    
    memset(tmpPdiskInfo->health, 0, sizeof( int));    

}

void DbPdiskInfo::copyInfo(tlgpfs_pdisk_info_t* dst, tlgpfs_pdisk_info_t* src)
{
    strcpy(dst->cluster_id,      src->cluster_id);
    strcpy(dst->rg_name,         src->rg_name);
    strcpy(dst->da_name,         src->da_name);
    strcpy(dst->pdisk_name,      src->pdisk_name);
    strcpy(dst->pdisk_dev_path,  src->pdisk_dev_path);
    strcpy(dst->pdisk_state,     src->pdisk_state);
    strcpy(dst->pdisk_fru,       src->pdisk_fru);
    strcpy(dst->pdisk_location,  src->pdisk_location);    
    *dst->pdisk_repl_prior  = *src->pdisk_repl_prior;
    *dst->pdisk_free_space  = *src->pdisk_free_space;
    *dst->change            = *src->change;
    *dst->health            = *src->health;
}


tlgpfs_pdisk_info_t* DbPdiskInfo::extract(gpfsDeclusteredArrayPdisk* pdiskInfo, string& clusterId, string& rgName, string& daName)
{
    if(pdiskInfo == NULL)
        return NULL;
    tlgpfs_pdisk_info* tmpPdiskInfo = allocateMemory();
    strcpy(tmpPdiskInfo->cluster_id, clusterId.c_str());
    strcpy(tmpPdiskInfo->rg_name, rgName.c_str());
    strcpy(tmpPdiskInfo->da_name, daName.c_str());
    strcpy(tmpPdiskInfo->pdisk_name, pdiskInfo->getPdiskName());
    strcpy(tmpPdiskInfo->pdisk_dev_path, pdiskInfo->getPdiskDevicePath());
    strcpy(tmpPdiskInfo->pdisk_state, pdiskInfo->getPdiskState());
    strcpy(tmpPdiskInfo->pdisk_fru, pdiskInfo->getPdiskFru());
    strcpy(tmpPdiskInfo->pdisk_location, pdiskInfo->getPdiskLocation());

    *tmpPdiskInfo->pdisk_repl_prior    = pdiskInfo->getPdiskReplacementPriority();
    *tmpPdiskInfo->pdisk_free_space    = pdiskInfo->getPdiskFreeSpace();

    return tmpPdiskInfo;

}

tlgpfs_pdisk_info_t* DbPdiskInfo::allocateMemory()
{
    tlgpfs_pdisk_info* tmpPdiskInfo = new tlgpfs_pdisk_info();
    
    tmpPdiskInfo->cluster_id        = new char[CLUSTER_ID_SIZE];
    memset(tmpPdiskInfo->cluster_id, 0, CLUSTER_ID_SIZE);
    
    tmpPdiskInfo->rg_name           = new char[RG_NAME_SIZE];
    memset(tmpPdiskInfo->rg_name, 0, RG_NAME_SIZE);
    
    tmpPdiskInfo->da_name           = new char[DA_NAME_SIZE];
    memset(tmpPdiskInfo->da_name, 0, DA_NAME_SIZE);

    tmpPdiskInfo->pdisk_name        = new char[PDISK_NAME_SIZE];
    memset(tmpPdiskInfo->pdisk_name, 0, PDISK_NAME_SIZE);

    tmpPdiskInfo->pdisk_dev_path    = new char[PDISK_DEV_PATH_SIZE];
    memset(tmpPdiskInfo->pdisk_dev_path, 0, PDISK_DEV_PATH_SIZE);
    
    tmpPdiskInfo->pdisk_state       = new char[PDISK_STATE_SIZE];
    memset(tmpPdiskInfo->pdisk_state, 0, PDISK_STATE_SIZE);
    
    tmpPdiskInfo->pdisk_fru         = new char[PDISK_FRU_SIZE];
    memset(tmpPdiskInfo->pdisk_fru, 0, PDISK_FRU_SIZE);

    tmpPdiskInfo->pdisk_location    = new char[PDISK_LOCATION_SIZE];
    memset(tmpPdiskInfo->pdisk_fru, 0, PDISK_LOCATION_SIZE);       

    tmpPdiskInfo->pdisk_repl_prior  = new  int;
    memset(tmpPdiskInfo->pdisk_repl_prior, 0, sizeof( int));

    tmpPdiskInfo->pdisk_free_space     = new  unsigned long long;
    memset(tmpPdiskInfo->pdisk_free_space, 0, sizeof( unsigned long long));

    tmpPdiskInfo->change            = new  int;
    memset(tmpPdiskInfo->change, 0, sizeof( int));

    tmpPdiskInfo->health            = new  int;
    memset(tmpPdiskInfo->health, 0, sizeof( int));    
    return tmpPdiskInfo;
    
}


void DbPdiskInfo::Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info)
{
    SQLRETURN ret;
    if(opType != UPDATE && opType != INSERT)
        return;
    tlgpfs_pdisk_info_t* tmp = (tlgpfs_pdisk_info_t*)info;

    int x = (opType == UPDATE) ? colSize - pkSize : 0;   

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::Upsert SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rgNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, RG_NAME_SIZE, 0, tmp->rg_name, 0, &rgNameLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::Upsert SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, DA_NAME_SIZE, 0, tmp->da_name, 0, &daNameLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::Upsert SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN pdiskNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, PDISK_NAME_SIZE, 0, tmp->pdisk_name, 0, &pdiskNameLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::Upsert SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN pdiskDevPathLen = tmp->pdisk_dev_path ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, PDISK_DEV_PATH_SIZE, 0, tmp->pdisk_dev_path, 0, &pdiskDevPathLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::Upsert SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN pdiskStateLen = tmp->pdisk_state ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, PDISK_STATE_SIZE, 0, tmp->pdisk_state, 0, &pdiskStateLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::Upsert SQLBindParameter 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN pdiskFruLen = tmp->pdisk_fru ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, PDISK_FRU_SIZE, 0, tmp->pdisk_fru, 0, &pdiskFruLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::Upsert SQLBindParameter 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN pdiskLocationLen = tmp->pdisk_location ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, PDISK_LOCATION_SIZE, 0, tmp->pdisk_location, 0, &pdiskLocationLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::Upsert SQLBindParameter 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN pdiskReplPriorLen = tmp->pdisk_repl_prior ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->pdisk_repl_prior, 0, &pdiskReplPriorLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::Upsert SQLBindParameter 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN pdiskFreeSpaceLen = tmp->pdisk_free_space ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, tmp->pdisk_free_space, 0, &pdiskFreeSpaceLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::Upsert SQLBindParameter 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN changeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::Upsert SQLBindParameter 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::Upsert SQLBindParameter 12 STMT",ret,sqlStmt,SQL_HANDLE_STMT);        

    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)upsertSql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbPdiskInfo::Upsert SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbPdiskInfo::bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init)
{
    SQLRETURN ret;
    int x = 1;
    tlgpfs_pdisk_info_t* tmp = (tlgpfs_pdisk_info_t*)info;

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::bindPrimaryKey SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rgNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, RG_NAME_SIZE, 0, tmp->rg_name, 0, &rgNameLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::bindPrimaryKey SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, DA_NAME_SIZE, 0, tmp->da_name, 0, &daNameLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::bindPrimaryKey SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN pdiskNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, PDISK_NAME_SIZE, 0, tmp->pdisk_name, 0, &pdiskNameLen);
    DbInterface::checkSqlRetcode("DbPdiskInfo::bindPrimaryKey SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    if( init )
    {
        int changeValue = 100;//init to 100
        int healthValue = 100;
        
        SQLLEN changeLen = SQL_NTS;    
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &changeValue, 0, &changeLen);
        DbInterface::checkSqlRetcode("DbPdiskInfo::bindPrimaryKey SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

        SQLLEN healthLen = SQL_NTS;        
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &healthValue, 0, &healthLen);
        DbInterface::checkSqlRetcode("DbPdiskInfo::bindPrimaryKey SQLBindParameter 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);    
    }
    
    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)sql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbPdiskInfo::bindPrimaryKey SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbPdiskInfo::updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst)
{
    vector<tlgpfs_pdisk_info_t*>* tempv = (vector<tlgpfs_pdisk_info_t*>*)temp;
    vector<tlgpfs_pdisk_info_t*>* lastv = (vector<tlgpfs_pdisk_info_t*>*)lst;
    tlgpfs_pdisk_info_t* last;

    tlgpfs_pdisk_info_t* tmp = tempv->front();
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
   
   anyChange |= strcmp(tmp->pdisk_dev_path, last->pdisk_dev_path);
   anyChange |= strcmp(tmp->pdisk_state, last->pdisk_state);
   anyChange |= strcmp(tmp->pdisk_fru, last->pdisk_fru);
   anyChange |= strcmp(tmp->pdisk_location, last->pdisk_location);
   anyChange |= memcmp(tmp->pdisk_repl_prior, last->pdisk_repl_prior,sizeof( int));
   anyChange |= memcmp(tmp->pdisk_free_space, last->pdisk_free_space,sizeof( unsigned long long));

   *tmp->change = anyChange?CHANGE_MODIFIED:CHANGE_NONE;
   //"gpfsPdiskState": "ok" "formatting" "systemDrain" "adminDrain" "noData" "noVCD" "noRGD" "replace" "diagnosing" "init" "dead"
   //"missing" "suspended" "noPath" "abandoned" "readonly" "failing" "PTOW"
   //only when "gpfsPdiskState" == "systemDrain", "adminDrain", "readonly", "missing", "noPath", "PTOW", "diagnosing", "replace", "dead" or "failing", it's unhealthy
   if(strstr(tmp->pdisk_state, "systemDrain") || strstr(tmp->pdisk_state, "adminDrain") 
   || strstr(tmp->pdisk_state, "readonly") || strstr(tmp->pdisk_state, "missing")
   || strstr(tmp->pdisk_state, "noPath") || strstr(tmp->pdisk_state, "PTOW") || strstr(tmp->pdisk_state, "diagnosing")
   || strstr(tmp->pdisk_state, "replace") || strstr(tmp->pdisk_state, "dead") || strstr(tmp->pdisk_state, "failing"))
       *tmp->health = UNHEALTHY;
   else
       *tmp->health = HEALTHY;
   updateTable(sqlStmt,table,tmp);

}
}

