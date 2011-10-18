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
#include "DbFsetInfo.h"
#include <iomanip>

namespace TEAL
{
DbFsetInfo::DbFsetInfo(DbInterface* dbi, vector<string>* cols, vector<string>* pk, tlgpfs_fset_info_t* fset):DbGpfsInfo(dbi,REGULAR_FSET_TABLE,TMP_FSET_TABLE,cols,pk,fset)
{
    if (fset)
    {
        if (!fset->cluster_id) throw std::invalid_argument("Cluster id is NULL");
        if (!fset->fs_name) throw std::invalid_argument("FS name is NULL");
        if (!fset->id) throw std::invalid_argument("Fset id is NULL");
        if (!fset->change) throw std::invalid_argument("Change is NULL");
        if (!fset->health) throw std::invalid_argument("health is NULL");
    }
    if(cols)
    {
        cols->push_back("cluster_id");
        cols->push_back("fs_name");
        cols->push_back("id");
        cols->push_back("fset_name");
        cols->push_back("root_inode");
        cols->push_back("parent_id");
        cols->push_back("comment");
        cols->push_back("status");    
        cols->push_back("path");    
        cols->push_back("created");
        cols->push_back("inodes");
        cols->push_back("data");
        cols->push_back("version");
        cols->push_back("change");
        cols->push_back("health");
    }
    if(pk)
    {
        pk->push_back("cluster_id");
        pk->push_back("fs_name");
        pk->push_back("id");
    }
}

DbFsetInfo::~DbFsetInfo()
{
}

void DbFsetInfo::printStatus(tlgpfs_fset_info_t* fset, bool detailed)
{
    if(fset == NULL)
        cerr<<"Can't print a null structure of status!"<<endl;

    cout<<setiosflags(ios::left)<<setw(20)<<"cluster_id"     <<setiosflags(ios::left)<<setw(40)<<"(cluster id)"                            <<": "<<  fset->cluster_id         <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"fs_name"        <<setiosflags(ios::left)<<setw(40)<<"(file system name)"                      <<": "<<  fset->fs_name            <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"id"             <<setiosflags(ios::left)<<setw(40)<<"(file set id)"                           <<": "<<  fset->id                 <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"health"         <<setiosflags(ios::left)<<setw(40)<<"(health status)"                         <<": "<<string((*fset->health == HEALTHY)?"healthy":((*fset->health == UNHEALTHY)?"unhealthy":"unknown"))<<endl;   
    if(!detailed)
        return;
    cout<<setiosflags(ios::left)<<setw(20)<<"fset_name"      <<setiosflags(ios::left)<<setw(40)<<"(file set name)"                         <<": "<<  fset->fset_name          <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"root_inode"     <<setiosflags(ios::left)<<setw(40)<<"(root inode)"                            <<": "<<  fset->root_inode         <<endl; 
    cout<<setiosflags(ios::left)<<setw(20)<<"parent_id"      <<setiosflags(ios::left)<<setw(40)<<"(parent file set id)"                    <<": "<<  fset->parent_id          <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"comment"        <<setiosflags(ios::left)<<setw(40)<<"(file set comment)"                      <<": "<<  fset->comment            <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"status"         <<setiosflags(ios::left)<<setw(40)<<"(file set status)"                       <<": "<<  fset->status             <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"path"           <<setiosflags(ios::left)<<setw(40)<<"(file set path)"                         <<": "<<  fset->path               <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"created"        <<setiosflags(ios::left)<<setw(40)<<"(file set created)"                      <<": "<<  fset->created            <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"inodes"         <<setiosflags(ios::left)<<setw(40)<<"(file set inodes)"                       <<": "<< *fset->inodes             <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"data"           <<setiosflags(ios::left)<<setw(40)<<"(file set data in KB)"                   <<": "<< *fset->data               <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"version"        <<setiosflags(ios::left)<<setw(40)<<"(file set version)"                      <<": "<< *fset->version            <<endl;
    cout<<setiosflags(ios::left)<<setw(20)<<"change"         <<setiosflags(ios::left)<<setw(40)<<"(change value)"                          <<": "<< *fset->change             <<endl;

}

void DbFsetInfo::getResult(SQLHSTMT sqlStmt,void** holder)
{
    SQLRETURN ret;
    *holder = new vector<tlgpfs_fset_info_t*>;
    vector<tlgpfs_fset_info_t*>* status = (vector<tlgpfs_fset_info_t*>*)* holder;
    tlgpfs_fset_info_t* tmp = allocateMemory();

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 1, SQL_C_CHAR, tmp->cluster_id, CLUSTER_ID_SIZE, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::getResult SQLBindCol 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN fsNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 2, SQL_C_CHAR, tmp->fs_name, FS_NAME_SIZE, &fsNameLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::getResult SQLBindCol 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN idLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 3, SQL_C_CHAR, tmp->id, ID_SIZE, &idLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::getResult SQLBindCol 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN fsetNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 4, SQL_C_CHAR, tmp->fset_name, FSET_NAME_SIZE, &fsetNameLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::getResult SQLBindCol 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rootInodeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 5, SQL_C_CHAR, tmp->root_inode, ROOT_INODE_SIZE, &rootInodeLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::getResult SQLBindCol 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN parentIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 6, SQL_C_CHAR, tmp->parent_id, PARENT_ID_SIZE, &parentIdLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::getResult SQLBindCol 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN commentLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 7, SQL_C_CHAR, tmp->comment, COMMENT_SIZE, &commentLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::getResult SQLBindCol 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN statusLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 8, SQL_C_CHAR, tmp->status, STATUS_SIZE, &statusLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::getResult SQLBindCol 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN pathLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 9, SQL_C_CHAR, tmp->path, PATH_SIZE, &pathLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::getResult SQLBindCol 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN createdLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 10, SQL_C_CHAR, tmp->created, CREATED_SIZE, &createdLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::getResult SQLBindCol 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN inodeSizeLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 11, SQL_C_UBIGINT, tmp->inodes, 0, &inodeSizeLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::getResult SQLBindCol 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN dataLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 12, SQL_C_UBIGINT, tmp->data, 0, &dataLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::getResult SQLBindCol 12 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN versionLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 13, SQL_C_SLONG, tmp->version, 0, &versionLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::getResult SQLBindCol 13 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN changeLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 14, SQL_C_SLONG, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::getResult SQLBindCol 14 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = 0;
    ret = DbInterface::dbModule.SQLBindCol(sqlStmt, 15, SQL_C_SLONG, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::getResult SQLBindCol 15 STMT",ret,sqlStmt,SQL_HANDLE_STMT);    
    
    ret = DbInterface::dbModule.SQLFetch(sqlStmt);
    if(ret != SQL_NO_DATA)//don't roll back even if empty row.
        DbInterface::checkSqlRetcode("DbFsetInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    
    while((ret == SQL_SUCCESS || ret == SQL_SUCCESS_WITH_INFO))
    {        
        tlgpfs_fset_info_t* temp = allocateMemory();
        copyInfo(temp,tmp);
        status->push_back(temp);
        resetMemory(tmp);
        ret = DbInterface::dbModule.SQLFetch(sqlStmt);
        if(ret != SQL_NO_DATA)//don't roll back even if empty row.
            DbInterface::checkSqlRetcode("DbFsetInfo::getResult SQLFetch",ret,sqlStmt,SQL_HANDLE_STMT);
    }

}

tlgpfs_fset_info_t* DbFsetInfo::extract(FileSet* fsetInfo, string& clusterId)
{
    if(fsetInfo == NULL)
        return NULL;
    tlgpfs_fset_info* tmpFsetInfo = allocateMemory();
    
    strcpy(tmpFsetInfo->cluster_id, clusterId.c_str());
    strcpy(tmpFsetInfo->fs_name, fsetInfo->getFSName());
    strcpy(tmpFsetInfo->id, fsetInfo->getId());
    strcpy(tmpFsetInfo->fset_name, fsetInfo->getName());
    strcpy(tmpFsetInfo->root_inode, fsetInfo->getRootINode());
    strcpy(tmpFsetInfo->parent_id, fsetInfo->getParentId());
    strcpy(tmpFsetInfo->comment, fsetInfo->getComment());    
    strcpy(tmpFsetInfo->status, fsetInfo->getStatus());
    strcpy(tmpFsetInfo->path, fsetInfo->getPath());
    strcpy(tmpFsetInfo->created, fsetInfo->getCreated());
    *tmpFsetInfo->inodes        = fsetInfo->getINodes();
    *tmpFsetInfo->data          = fsetInfo->getData();
    *tmpFsetInfo->version       = fsetInfo->getVersion();
    return tmpFsetInfo;

}

tlgpfs_fset_info_t* DbFsetInfo::allocateMemory()
{
    tlgpfs_fset_info* tmpFsetInfo = new tlgpfs_fset_info();
    
    tmpFsetInfo->cluster_id        = new char[CLUSTER_ID_SIZE];
    memset(tmpFsetInfo->cluster_id, 0, CLUSTER_ID_SIZE);

    tmpFsetInfo->fs_name           = new char[FS_NAME_SIZE];
    memset(tmpFsetInfo->fs_name, 0, FS_NAME_SIZE);

    tmpFsetInfo->id                = new char[ID_SIZE];
    memset(tmpFsetInfo->id, 0, ID_SIZE);
        
    tmpFsetInfo->fset_name         = new char[FSET_NAME_SIZE];
    memset(tmpFsetInfo->fset_name, 0, FSET_NAME_SIZE);
    
    tmpFsetInfo->root_inode        = new char[ROOT_INODE_SIZE];
    memset(tmpFsetInfo->root_inode, 0, ROOT_INODE_SIZE);
    
    tmpFsetInfo->parent_id         = new char[PARENT_ID_SIZE];
    memset(tmpFsetInfo->parent_id, 0, PARENT_ID_SIZE);
    
    tmpFsetInfo->comment           = new char[COMMENT_SIZE];
    memset(tmpFsetInfo->comment, 0, COMMENT_SIZE);
    
    tmpFsetInfo->status            = new char[STATUS_SIZE];
    memset(tmpFsetInfo->status, 0, STATUS_SIZE);
    
    tmpFsetInfo->path              = new char[PATH_SIZE];
    memset(tmpFsetInfo->path, 0, PATH_SIZE);
    
    tmpFsetInfo->created           = new char[CREATED_SIZE];
    memset(tmpFsetInfo->created, 0, CREATED_SIZE);
    
    tmpFsetInfo->inodes            = new unsigned long long;
    memset(tmpFsetInfo->inodes, 0, sizeof( unsigned long long));
    
    tmpFsetInfo->data              = new unsigned long long;
    memset(tmpFsetInfo->data, 0, sizeof( unsigned long long));

    tmpFsetInfo->version           = new  int;
    memset(tmpFsetInfo->version, 0, sizeof( int));
    
    tmpFsetInfo->change            = new  int;
    memset(tmpFsetInfo->change, 0, sizeof( int));

    tmpFsetInfo->health            = new  int;
    memset(tmpFsetInfo->health, 0, sizeof( int));        
    
    return tmpFsetInfo;
    
}


void DbFsetInfo::Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info)
{
    SQLRETURN ret;
    
    if(opType != UPDATE && opType != INSERT)
        return;
    tlgpfs_fset_info_t* tmp = (tlgpfs_fset_info_t*)info;

    int x = (opType == UPDATE) ? colSize - pkSize : 0;   

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::Upsert SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN fsNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, FS_NAME_SIZE, 0, tmp->fs_name, 0, &fsNameLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::Upsert SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN idLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, ID_SIZE, 0, tmp->id, 0, &idLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::Upsert SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN fsetNameLen = tmp->fset_name ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, FSET_NAME_SIZE, 0, tmp->fset_name, 0, &fsetNameLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::Upsert SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN rootInodeLen = tmp->root_inode ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, ROOT_INODE_SIZE, 0, tmp->root_inode, 0, &rootInodeLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::Upsert SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN parentIdLen = tmp->parent_id ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, PARENT_ID_SIZE, 0, tmp->parent_id, 0, &parentIdLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::Upsert SQLBindParameter 6 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN commentLen = tmp->comment ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, COMMENT_SIZE, 0, tmp->comment, 0, &commentLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::Upsert SQLBindParameter 7 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN statusLen = tmp->status ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, STATUS_SIZE, 0, tmp->status, 0, &statusLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::Upsert SQLBindParameter 8 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN pathLen = tmp->path ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, PATH_SIZE, 0, tmp->path, 0, &pathLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::Upsert SQLBindParameter 9 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN createdLen = tmp->created ? SQL_NTS : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CREATED_SIZE, 0, tmp->created, 0, &createdLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::Upsert SQLBindParameter 10 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN inodesLen = tmp->inodes ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, tmp->inodes, 0, &inodesLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::Upsert SQLBindParameter 11 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    
    SQLLEN dataLen = tmp->data ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_UBIGINT, SQL_BIGINT, 0, 0, tmp->data, 0, &dataLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::Upsert SQLBindParameter 12 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN versionLen = tmp->version ? 0 : SQL_NULL_DATA;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->version, 0, &versionLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::Upsert SQLBindParameter 13 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN changeLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->change, 0, &changeLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::Upsert SQLBindParameter 14 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN healthLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, (x = (++x < colSize+1 ? x : 1)), SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, tmp->health, 0, &healthLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::Upsert SQLBindParameter 15 STMT",ret,sqlStmt,SQL_HANDLE_STMT);                

    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)upsertSql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbFsetInfo::Upsert SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbFsetInfo::copyInfo(tlgpfs_fset_info_t* dst, tlgpfs_fset_info_t* src)
{
    strcpy(dst->cluster_id, src->cluster_id);
    strcpy(dst->fs_name, src->fs_name);
    strcpy(dst->id, src->id);
    strcpy(dst->fset_name, src->fset_name);
    strcpy(dst->root_inode, src->root_inode);
    strcpy(dst->parent_id, src->parent_id);
    strcpy(dst->comment, src->comment);
    strcpy(dst->status, src->status);
    strcpy(dst->path, src->path);
    strcpy(dst->created, src->created);
    *dst->inodes    = *src->inodes;
    *dst->data      = *src->data;
    *dst->version   = *src->version;
    *dst->change    = *src->change;
    *dst->health    = *src->health;

}
void DbFsetInfo::resetMemory(tlgpfs_fset_info* tmpFsetInfo)
{
    if( tmpFsetInfo == NULL )
        return;
    
    memset(tmpFsetInfo->cluster_id, 0, CLUSTER_ID_SIZE);

    memset(tmpFsetInfo->fs_name, 0, FS_NAME_SIZE);

    memset(tmpFsetInfo->id, 0, ID_SIZE);
    
    memset(tmpFsetInfo->fset_name, 0, FSET_NAME_SIZE);
    
    memset(tmpFsetInfo->root_inode, 0, ROOT_INODE_SIZE);
    
    memset(tmpFsetInfo->parent_id, 0, PARENT_ID_SIZE);
    
    memset(tmpFsetInfo->comment, 0, COMMENT_SIZE);
    
    memset(tmpFsetInfo->status, 0, STATUS_SIZE);
    
    memset(tmpFsetInfo->path, 0, PATH_SIZE);
    
    memset(tmpFsetInfo->created, 0, CREATED_SIZE);
    
    memset(tmpFsetInfo->inodes, 0, sizeof( unsigned long long));
    
    memset(tmpFsetInfo->data, 0, sizeof( unsigned long long));

    memset(tmpFsetInfo->version, 0, sizeof( int)); 

    memset(tmpFsetInfo->change, 0, sizeof( int));

    memset(tmpFsetInfo->health, 0, sizeof( int));        


}

void DbFsetInfo::bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info, bool init)
{
    SQLRETURN ret;
    int x = 1;
    tlgpfs_fset_info_t* tmp = (tlgpfs_fset_info_t*)info;

    SQLLEN clusterIdLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, CLUSTER_ID_SIZE, 0, tmp->cluster_id, 0, &clusterIdLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::bindPrimaryKey SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN fsNameLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, FS_NAME_SIZE, 0, tmp->fs_name, 0, &fsNameLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::bindPrimaryKey SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN idLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, ID_SIZE, 0, tmp->id, 0, &idLen);
    DbInterface::checkSqlRetcode("DbFsetInfo::bindPrimaryKey SQLBindParameter 3 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    if( init )
    {
        int changeValue = 100;//init to 100
        int healthValue = 100;
        
        SQLLEN changeLen = SQL_NTS;    
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &changeValue, 0, &changeLen);
        DbInterface::checkSqlRetcode("DbFsetInfo::bindPrimaryKey SQLBindParameter 4 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

        SQLLEN healthLen = SQL_NTS;        
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, x++, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &healthValue, 0, &healthLen);
        DbInterface::checkSqlRetcode("DbFsetInfo::bindPrimaryKey SQLBindParameter 5 STMT",ret,sqlStmt,SQL_HANDLE_STMT);    
    }
    
    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)sql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbFsetInfo::bindPrimaryKey SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbFsetInfo::updateRegularTable(SQLHSTMT sqlStmt,string& table, void* temp, void* lst)
{
    vector<tlgpfs_fset_info_t*>* tempv = (vector<tlgpfs_fset_info_t*>*)temp;
    vector<tlgpfs_fset_info_t*>* lastv = (vector<tlgpfs_fset_info_t*>*)lst;
    tlgpfs_fset_info_t* last;
    tlgpfs_fset_info_t* tmp = tempv->front();
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
   
   anyChange |= strcmp(tmp->fset_name, last->fset_name);
   anyChange |= strcmp(tmp->root_inode, last->root_inode);
   anyChange |= strcmp(tmp->parent_id, last->parent_id);
   anyChange |= strcmp(tmp->comment, last->comment);
   anyChange |= strcmp(tmp->status, last->status);
   anyChange |= strcmp(tmp->path, last->path);
   anyChange |= strcmp(tmp->created, last->created);
   anyChange |= memcmp(tmp->inodes, last->inodes, sizeof( long long));
   anyChange |= memcmp(tmp->data, last->data, sizeof( long long));
   anyChange |= memcmp(tmp->version, last->version, sizeof( int));

   *tmp->change = anyChange?CHANGE_MODIFIED:CHANGE_NONE;
   //"status": "Unused" "Creating" "Linked" "Deleting" "Linking" "Unlinking" "Deleted" "Unlinked" "Invalid"
   //only when "status" == "Invalid", it's unhealthy
   *tmp->health = strcmp(tmp->status, "Invalid")?HEALTHY:UNHEALTHY;
   updateTable(sqlStmt,table,tmp);

}
}

