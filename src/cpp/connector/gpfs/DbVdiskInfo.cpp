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
#include "DbVdiskInfo.h"
#include <iomanip>
namespace TEAL
{
DbVdiskInfo::DbVdiskInfo(DbInterface* dbi, vector<string>* cols, vector<string>* pk, tlgpfs_vdisk_info_t* vdisk):DbGpfsInfo(dbi,REGULAR_VDISK_TABLE,TMP_VDISK_TABLE,cols,pk,vdisk)
{
    if (vdisk)
    {
        if (!vdisk->cluster_id) throw std::invalid_argument("Cluster id is NULL");
        if (!vdisk->rg_name) throw std::invalid_argument("RG name is NULL");
        if (!vdisk->da_name) throw std::invalid_argument("DA name is NULL");
        if (!vdisk->vdisk_name) throw std::invalid_argument("vdisk name is NULL");
        if (!vdisk->change) throw std::invalid_argument("Change is NULL");
        if (!vdisk->health) throw std::invalid_argument("health is NULL");
    }
    if(cols)
    {
        cols->push_back("cluster_id");
        cols->push_back("rg_name");
        cols->push_back("da_name");
        cols->push_back("vdisk_name");
        cols->push_back("vdisk_raid_code");
        cols->push_back("vdisk_state");
        cols->push_back("vdisk_remarks");
        cols->push_back("vdisk_block_size");
        cols->push_back("vdisk_size");
        cols->push_back("change");
        cols->push_back("health");
    }
    if(pk)
    {
        pk->push_back("cluster_id");
        pk->push_back("rg_name");
        pk->push_back("da_name");
        pk->push_back("vdisk_name");
    }

}

DbVdiskInfo::~DbVdiskInfo()
{
}


void DbVdiskInfo::printStatus(tlgpfs_vdisk_info_t* vdisk, bool detailed)
{
    if(vdisk == NULL)
        cerr<<"Can't print a null structure of status!"<<endl;

    cout<<setiosflags(ios::left)<<setw(20)<<"cluster_id"         <<setiosflags(ios::left)<<setw(40)<<"(cluster id)"                   <<": "<< vdisk->cluster_id               <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"rg_name"            <<setiosflags(ios::left)<<setw(40)<<"(recovery group name)"          <<": "<< vdisk->rg_name                  <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"da_name"            <<setiosflags(ios::left)<<setw(40)<<"(declustered array name)"       <<": "<< vdisk->da_name                  <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"vdisk_name"         <<setiosflags(ios::left)<<setw(40)<<"(vdisk name)"                   <<": "<< vdisk->vdisk_name               <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"health"             <<setiosflags(ios::left)<<setw(40)<<"(health status)"                <<": "<<string((*vdisk->health == HEALTHY)?"healthy":((*vdisk->health == UNHEALTHY)?"unhealthy":"unknown"))<<endl;    
    if(!detailed)
        return;
    cout<<setiosflags(ios::left)<<setw(20)<<"vdisk_raid_code"    <<setiosflags(ios::left)<<setw(40)<<"(vdisk RAID code)"              <<": "<< vdisk->vdisk_raid_code          <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"vdisk_state"        <<setiosflags(ios::left)<<setw(40)<<"(vdisk state)"                  <<": "<< vdisk->vdisk_state              <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"vdisk_remarks"      <<setiosflags(ios::left)<<setw(40)<<"(vdisk remarks)"                <<": "<< vdisk->vdisk_remarks            <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"vdisk_block_size"   <<setiosflags(ios::left)<<setw(40)<<"(vdisk block size in KiB)"      <<": "<<*vdisk->vdisk_block_size         <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"vdisk_size"         <<setiosflags(ios::left)<<setw(40)<<"(vdisk size in bytes)"          <<": "<<*vdisk->vdisk_size               <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"change"             <<setiosflags(ios::left)<<setw(40)<<"(change value)"                 <<": "<<*vdisk->change                   <<endl;

}

void DbVdiskInfo::getResult(SQLHSTMT sqlStmt,void** holder)
{
    SQLRETURN ret;
    *holder = new vector<tlgpfs_vdisk_info_t*>;
    vector<tlgpfs_vdisk_info_t*>* status = (vector<tlgpfs_vdisk_info_t*>*)* holder;
    tlgpfs_vdisk_info_t* tmp = allocateMemory();


    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 1, SQL_C_CHAR, tmp->cluster_id, CLUSTER_ID_SIZE, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::getResult SQLBindCol 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN rgNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 2, SQL_C_CHAR, tmp->rg_name, RG_NAME_SIZE, &rgNameLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::getResult SQLBindCol 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN daNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 3, SQL_C_CHAR, tmp->da_name, DA_NAME_SIZE, &daNameLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::getResult SQLBindCol 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);  
    
    SQLLEN vdiskNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 4, SQL_C_CHAR, tmp->vdisk_name, VDISK_NAME_SIZE, &vdiskNameLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::getResult SQLBindCol 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN vdiskRaidCodeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 5, SQL_C_CHAR, tmp->vdisk_raid_code, VDISK_RAID_CODE_SIZE, &vdiskRaidCodeLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::getResult SQLBindCol 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN vdiskStateLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 6, SQL_C_CHAR, tmp->vdisk_state, VDISK_STATE_SIZE, &vdiskStateLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::getResult SQLBindCol 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN vdiskRemarksLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 7, SQL_C_CHAR, tmp->vdisk_remarks, VDISK_REMARKS_SIZE, &vdiskRemarksLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::getResult SQLBindCol 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN vdiskBlockSizeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 8, SQL_C_SLONG, tmp->vdisk_block_size, 0, &vdiskBlockSizeLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::getResult SQLBindCol 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN vdiskSizeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 9, SQL_C_UBIGINT, tmp->vdisk_size, 0, &vdiskSizeLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::getResult SQLBindCol 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN changeLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 10, SQL_C_SLONG, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::getResult SQLBindCol 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 11, SQL_C_SLONG, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::getResult SQLBindCol 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);    
    
    ret = DbInterface::dbModule.SQLFetch(sqlStmt);
    if(ret != SQL_NO_DATA)//don't roll back even if empty row.
        DbInterface::checkSqlRetcode("DbVdiskInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    
    while((ret == SQL_SUCCESS || ret == SQL_SUCCESS_WITH_INFO))
    {
        
        tlgpfs_vdisk_info_t* temp = allocateMemory();
        copyInfo(temp,tmp);
        status->push_back(temp);
        resetMemory(tmp);
        ret = DbInterface::dbModule.SQLFetch(sqlStmt);
        if(ret != SQL_NO_DATA)//don't roll back even if empty row.
            DbInterface::checkSqlRetcode("DbVdiskInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    }

}

void DbVdiskInfo::resetMemory(tlgpfs_vdisk_info* tmpVdiskInfo)
{
    if( tmpVdiskInfo == NULL )
        return;
    
    memset(tmpVdiskInfo->cluster_id, 0, CLUSTER_ID_SIZE);

    memset(tmpVdiskInfo->rg_name, 0, RG_NAME_SIZE);

    memset(tmpVdiskInfo->da_name, 0, DA_NAME_SIZE);

    memset(tmpVdiskInfo->vdisk_name, 0, VDISK_NAME_SIZE);  
    
    memset(tmpVdiskInfo->vdisk_raid_code, 0, VDISK_RAID_CODE_SIZE);
    
    memset(tmpVdiskInfo->vdisk_state, 0, VDISK_STATE_SIZE);
    
    memset(tmpVdiskInfo->vdisk_remarks, 0, VDISK_REMARKS_SIZE);
    
    memset(tmpVdiskInfo->vdisk_block_size, 0, VDISK_BLOCK_SIZE_SIZE);
    
    memset(tmpVdiskInfo->vdisk_size, 0, VDISK_SIZE_SIZE);
    
    memset(tmpVdiskInfo->change, 0, sizeof( int));
    
    memset(tmpVdiskInfo->health, 0, sizeof( int));    

}

void DbVdiskInfo::copyInfo(tlgpfs_vdisk_info_t* dst, tlgpfs_vdisk_info_t* src)
{
    strcpy(dst->cluster_id,      src->cluster_id);
    strcpy(dst->rg_name,         src->rg_name);
    strcpy(dst->da_name,         src->da_name);
    strcpy(dst->vdisk_name,      src->vdisk_name);
    strcpy(dst->vdisk_raid_code, src->vdisk_raid_code);
    strcpy(dst->vdisk_state,     src->vdisk_state);
    strcpy(dst->vdisk_remarks,   src->vdisk_remarks);
    *dst->vdisk_block_size  = *src->vdisk_block_size;    
    *dst->vdisk_size        = *src->vdisk_size;
    *dst->change            = *src->change;
    *dst->health            = *src->health;
}


tlgpfs_vdisk_info_t* DbVdiskInfo::extract(gpfsDeclusteredArrayVdisk* vdiskInfo, string& clusterId, string& rgName, string& daName)
{
    if(vdiskInfo == NULL)
        return NULL;
    tlgpfs_vdisk_info* tmpVdiskInfo = allocateMemory();
    strcpy(tmpVdiskInfo->cluster_id,      clusterId.c_str());
    strcpy(tmpVdiskInfo->rg_name,         rgName.c_str());
    strcpy(tmpVdiskInfo->da_name,         daName.c_str());
    strcpy(tmpVdiskInfo->vdisk_name,      vdiskInfo->getVdiskName());
    strcpy(tmpVdiskInfo->vdisk_raid_code, vdiskInfo->getVdiskRaidCode());
    strcpy(tmpVdiskInfo->vdisk_state,     vdiskInfo->getVdiskState());
    strcpy(tmpVdiskInfo->vdisk_remarks,   vdiskInfo->getVdiskRemarks());
    
    *tmpVdiskInfo->vdisk_block_size     = vdiskInfo->getVdiskBlockSizeInKiB();
    *tmpVdiskInfo->vdisk_size           = vdiskInfo->getVdiskSize();

    return tmpVdiskInfo;

}

tlgpfs_vdisk_info_t* DbVdiskInfo::allocateMemory()
{
    tlgpfs_vdisk_info* tmpVdiskInfo = new tlgpfs_vdisk_info();
    
    tmpVdiskInfo->cluster_id        = new char[CLUSTER_ID_SIZE];
    memset(tmpVdiskInfo->cluster_id, 0, CLUSTER_ID_SIZE);
    
    tmpVdiskInfo->rg_name           = new char[RG_NAME_SIZE];
    memset(tmpVdiskInfo->rg_name, 0, RG_NAME_SIZE);
    
    tmpVdiskInfo->da_name           = new char[DA_NAME_SIZE];
    memset(tmpVdiskInfo->da_name, 0, DA_NAME_SIZE);

    tmpVdiskInfo->vdisk_name        = new char[VDISK_NAME_SIZE];
    memset(tmpVdiskInfo->vdisk_name, 0, VDISK_NAME_SIZE);

    tmpVdiskInfo->vdisk_raid_code   = new char[VDISK_RAID_CODE_SIZE];
    memset(tmpVdiskInfo->vdisk_raid_code, 0, VDISK_RAID_CODE_SIZE);
    
    tmpVdiskInfo->vdisk_state       = new char[VDISK_STATE_SIZE];
    memset(tmpVdiskInfo->vdisk_state, 0, VDISK_STATE_SIZE);
    
    tmpVdiskInfo->vdisk_remarks     = new char[VDISK_REMARKS_SIZE];
    memset(tmpVdiskInfo->vdisk_remarks, 0, VDISK_REMARKS_SIZE);

    tmpVdiskInfo->vdisk_block_size  = new int;
    memset(tmpVdiskInfo->vdisk_block_size, 0, sizeof(int));       

    tmpVdiskInfo->vdisk_size        = new unsigned long long;
    memset(tmpVdiskInfo->vdisk_size, 0, sizeof(unsigned long long));

    tmpVdiskInfo->change            = new  int;
    memset(tmpVdiskInfo->change, 0, sizeof( int));

    tmpVdiskInfo->health            = new  int;
    memset(tmpVdiskInfo->health, 0, sizeof( int)); 
    
    return tmpVdiskInfo;
    
}


void DbVdiskInfo::Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info)
{
    SQLRETURN ret;
    if(opType != UPDATE && opType != INSERT)
        return;
    tlgpfs_vdisk_info_t* tmp = (tlgpfs_vdisk_info_t*)info;

    int x = (opType == UPDATE) ? colSize - pkSize : 0;   

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::Upsert SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rgNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, RG_NAME_SIZE, 0, tmp->rg_name, 0, &rgNameLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::Upsert SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, DA_NAME_SIZE, 0, tmp->da_name, 0, &daNameLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::Upsert SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN vdiskNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, VDISK_NAME_SIZE, 0, tmp->vdisk_name, 0, &vdiskNameLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::Upsert SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN vdiskRaidCodeLen = tmp->vdisk_raid_code ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, VDISK_RAID_CODE_SIZE, 0, tmp->vdisk_raid_code, 0, &vdiskRaidCodeLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::Upsert SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN vdiskStateLen = tmp->vdisk_state ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, VDISK_STATE_SIZE, 0, tmp->vdisk_state, 0, &vdiskStateLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::Upsert SQLBindParameter 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN vdiskRemarksLen = tmp->vdisk_remarks ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, VDISK_REMARKS_SIZE, 0, tmp->vdisk_remarks, 0, &vdiskRemarksLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::Upsert SQLBindParameter 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN vdiskBlockSizeLen = tmp->vdisk_block_size ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->vdisk_block_size, 0, &vdiskBlockSizeLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::Upsert SQLBindParameter 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN vdiskSizeLen = tmp->vdisk_size ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, tmp->vdisk_size, 0, &vdiskSizeLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::Upsert SQLBindParameter 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
   
    SQLLEN changeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::Upsert SQLBindParameter 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::Upsert SQLBindParameter 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);        

    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)upsertSql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbVdiskInfo::Upsert SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbVdiskInfo::bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init)
{
    SQLRETURN ret;
    int x = 1;
    tlgpfs_vdisk_info_t* tmp = (tlgpfs_vdisk_info_t*)info;

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::bindPrimaryKey SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rgNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, RG_NAME_SIZE, 0, tmp->rg_name, 0, &rgNameLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::bindPrimaryKey SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN daNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, DA_NAME_SIZE, 0, tmp->da_name, 0, &daNameLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::bindPrimaryKey SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN vdiskNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, VDISK_NAME_SIZE, 0, tmp->vdisk_name, 0, &vdiskNameLen);
    DbInterface::checkSqlRetcode("DbVdiskInfo::bindPrimaryKey SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    if( init )
    {
        int changeValue = 100;//init to 100
        int healthValue = 100;
        
        SQLLEN changeLen = SQL_NTS;    
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &changeValue, 0, &changeLen);
        DbInterface::checkSqlRetcode("DbVdiskInfo::bindPrimaryKey SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

        SQLLEN healthLen = SQL_NTS;        
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &healthValue, 0, &healthLen);
        DbInterface::checkSqlRetcode("DbVdiskInfo::bindPrimaryKey SQLBindParameter 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);    
    }
    
    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)sql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbVdiskInfo::bindPrimaryKey SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbVdiskInfo::updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst)
{
    vector<tlgpfs_vdisk_info_t*>* tempv = (vector<tlgpfs_vdisk_info_t*>*)temp;
    vector<tlgpfs_vdisk_info_t*>* lastv = (vector<tlgpfs_vdisk_info_t*>*)lst;
    tlgpfs_vdisk_info_t* last;

    tlgpfs_vdisk_info_t* tmp = tempv->front();
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
   
   anyChange |= strcmp(tmp->vdisk_raid_code, last->vdisk_raid_code);
   anyChange |= strcmp(tmp->vdisk_state, last->vdisk_state);
   anyChange |= strcmp(tmp->vdisk_remarks, last->vdisk_remarks);
   anyChange |= memcmp(tmp->vdisk_block_size, last->vdisk_block_size,sizeof( int));
   anyChange |= memcmp(tmp->vdisk_size, last->vdisk_size,sizeof(unsigned long long));

   *tmp->change = anyChange?CHANGE_MODIFIED:CHANGE_NONE;
   //"gpfsVdiskState": "ok", "critical", "offline","%d/%d-degraded"
   //only when "gpfsVdiskState" == "ok", it's healthy
   if(!strcmp(tmp->vdisk_state, "ok"))
       *tmp->health = HEALTHY;
   else
       *tmp->health = UNHEALTHY;
   updateTable(sqlStmt,table,tmp);

}
}

