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
#include "DbGpfsInfo.h"

namespace TEAL
{

DbGpfsInfo::DbGpfsInfo(DbInterface* dbi,string regulartable, string temptable,vector<string>* cols,vector<string>* pk,void* info)
{
    dbif = dbi;
    primary_key = pk;
    tableName = regulartable;
    tmptableName = temptable;
    polledInfo = info;
    fields = cols;
}

DbGpfsInfo::~DbGpfsInfo()
{
}

void DbGpfsInfo::removeRows(SQLHSTMT sqlStmt,string& table)
{
    SQLRETURN ret;
    string deleteSql = dbif->genDelete(*primary_key,table);
    bindPrimaryKey(sqlStmt,deleteSql,polledInfo,false);
 
    ret = DbInterface::dbModule.SQLFreeStmt(sqlStmt,SQL_RESET_PARAMS);
    DbInterface::checkSqlRetcode("DbGpfsInfo::removeRows SQLFreeStmt",ret,sqlStmt,SQL_HANDLE_STMT);  
}


void DbGpfsInfo::fillTable(SQLHSTMT sqlStmt,string& table)
{
    SQLRETURN ret;

    string insertSql = dbif->genInsert(*fields,table);
    Upsert(sqlStmt,insertSql,fields->size(),primary_key->size(),INSERT,polledInfo); //bind temp table columns

    ret = DbInterface::dbModule.SQLFreeStmt(sqlStmt,SQL_RESET_PARAMS); //reset bind parameters of statement handle
    DbInterface::checkSqlRetcode("DbGpfsInfo::fillTable SQLFreeStmt",ret,sqlStmt,SQL_HANDLE_STMT);
}

template <class T>
void DbGpfsInfo::queryTable(SQLHSTMT sqlStmt,string& table,T** holder)
{
    SQLRETURN ret;
    
    string querySql = dbif->genSelect(*primary_key,table);

    bindPrimaryKey(sqlStmt,querySql,polledInfo,false);
    
    ret = DbInterface::dbModule.SQLFreeStmt(sqlStmt,SQL_RESET_PARAMS);
    DbInterface::checkSqlRetcode("DbGpfsInfo::fillTempTable SQLFreeStmt",ret,sqlStmt,SQL_HANDLE_STMT);
    
    getResult(sqlStmt,holder);
    
    ret = DbInterface::dbModule.SQLFreeStmt(sqlStmt,SQL_CLOSE);
    DbInterface::checkSqlRetcode("DbGpfsInfo::queryTable SQLFreeStmt",ret,sqlStmt,SQL_HANDLE_STMT);


}

void DbGpfsInfo::updateTable(SQLHSTMT sqlStmt,string& table, void* tempInfo)
{
    SQLRETURN ret;
    vector<string> columns(fields->begin()+primary_key->size(),fields->end());//only update columns exclude primary key
    string updateSql = dbif->genUpdate(columns,*primary_key,table);
    Upsert(sqlStmt,updateSql,fields->size(),primary_key->size(),UPDATE,tempInfo); 
    
    ret = DbInterface::dbModule.SQLFreeStmt(sqlStmt,SQL_RESET_PARAMS); //reset bind parameters of statement handle
    DbInterface::checkSqlRetcode("DbGpfsInfo::fillTable SQLFreeStmt",ret,sqlStmt,SQL_HANDLE_STMT);

}

template <class T>
void DbGpfsInfo::queryTablebyCol(SQLHSTMT sqlStmt, string& table, const string& col, const string& value, T** holder)
{
    SQLRETURN ret;
    if(col != "*" && find(fields->begin(),fields->end(),col) == fields->end())
    {
        cerr<<"No column named "<<col<<endl;
        return;
    }
    vector<string> fields;
    fields.push_back(col);
    string querySql = dbif->genSelect(fields,table);//fields can be "*" to query all columns

    if(value != string(""))//null for all columns
    {
        SQLLEN valueLen = SQL_NTS;
        ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 128, 0, (void*)value.c_str(), 0, &valueLen);
        DbInterface::checkSqlRetcode("DbGpfsInfo::queryTablebyCol SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);
    }
    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)querySql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbGpfsInfo::queryTablebyCol SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);
    getResult(sqlStmt,holder);
    
    ret = DbInterface::dbModule.SQLFreeStmt(sqlStmt,SQL_CLOSE);
    DbInterface::checkSqlRetcode("DbGpfsInfo::queryTablebyCol SQLFreeStmt",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbGpfsInfo::updateTablebyCol(SQLHSTMT sqlStmt, string& table, const string& col, const string& colValue, const string& key, const string& keyValue)
{
    SQLRETURN ret;

    vector<string> fields;
    fields.push_back(col);//set col1, col2
    
    vector<string> keys;
    keys.push_back(key); // where key1, key2
    
    string updateSql = dbif->genUpdate(fields,keys,table);//fields can be "*" to update all columns

    SQLLEN colValueLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 128, 0, (void*)colValue.c_str(), 0, &colValueLen);
    DbInterface::checkSqlRetcode("DbGpfsInfo::updateTablebyCol SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN keyValueLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 128, 0, (void*)keyValue.c_str(), 0, &keyValueLen);
    DbInterface::checkSqlRetcode("DbGpfsInfo::updateTablebyCol SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)updateSql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbGpfsInfo::updateTablebyCol SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);
     
    ret = DbInterface::dbModule.SQLFreeStmt(sqlStmt,SQL_CLOSE);
    DbInterface::checkSqlRetcode("DbGpfsInfo::updateTablebyCol SQLFreeStmt",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbGpfsInfo::deleteTablebyCol(SQLHSTMT sqlStmt, string& table, const string& col, const string& colValue)
{
    SQLRETURN ret;
    vector<string> fields;
    fields.push_back(col);
    fields.push_back(string("health"));//hard coded
    string deleteSql = dbif->genDelete(fields,table);//fields can be "*" to delete all columns
    string keyValue  = "2";
    SQLLEN colValueLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 128, 0, (void*)colValue.c_str(), 0, &colValueLen);
    DbInterface::checkSqlRetcode("DbGpfsInfo::deleteTablebyCol SQLBindParameter 1 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    SQLLEN keyValueLen = SQL_NTS;
    ret = DbInterface::dbModule.SQLBindParameter(sqlStmt, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 128, 0, (void*)keyValue.c_str(), 0, &keyValueLen);
    DbInterface::checkSqlRetcode("DbGpfsInfo::deleteTablebyCol SQLBindParameter 2 STMT",ret,sqlStmt,SQL_HANDLE_STMT);

    ret = DbInterface::dbModule.SQLExecDirect(sqlStmt,(SQLCHAR*)deleteSql.c_str(), SQL_NTS);
    if(ret != SQL_NO_DATA)
        DbInterface::checkSqlRetcode("DbGpfsInfo::deleteTablebyCol SQLExecDirect",ret,sqlStmt,SQL_HANDLE_STMT);
     
    ret = DbInterface::dbModule.SQLFreeStmt(sqlStmt,SQL_CLOSE);
    DbInterface::checkSqlRetcode("DbGpfsInfo::deleteTablebyCol SQLFreeStmt",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbGpfsInfo::updateStatus(SQLHSTMT sqlStmt,const string& col, const string& colValue, const string& key, const string& keyValue)
{
    updateTablebyCol(sqlStmt,tableName,col,colValue,key,keyValue);
}

void DbGpfsInfo::deleteAll(SQLHSTMT sqlStmt,const string& col, const string& colValue)
{
    deleteTablebyCol(sqlStmt,tableName,col,colValue);
    deleteTablebyCol(sqlStmt,tmptableName,col,colValue); //delete tmp items as well
}

void DbGpfsInfo::initTable(SQLHSTMT sqlStmt,string& table)
{
    SQLRETURN ret;
    vector<string> fields(primary_key->begin(),primary_key->end());
    fields.push_back(string("change"));
    fields.push_back(string("health"));
    string insertSql = dbif->genInsert(fields, table);

    bindPrimaryKey(sqlStmt,insertSql,polledInfo,true);
    
    ret = DbInterface::dbModule.SQLFreeStmt(sqlStmt,SQL_RESET_PARAMS); //reset bind parameters of statement handle
    DbInterface::checkSqlRetcode("DbGpfsInfo::fillTable SQLFreeStmt",ret,sqlStmt,SQL_HANDLE_STMT);

}

void DbGpfsInfo::queryInfo(SQLHSTMT sqlStmt,const string& colName, const string& colValue,void** info)
{
    queryTablebyCol(sqlStmt,tableName,colName,colValue,info);
}

void DbGpfsInfo::upsertInfo(SQLHSTMT sqlStmt)
{
    removeRows(sqlStmt,tmptableName);     //clear all related temp tables at first
    fillTable(sqlStmt,tmptableName); //fill temp table
    
    queryTable(sqlStmt,tmptableName,&tempInfo);//query temp table
    queryTable(sqlStmt,tableName,&lastInfo); //query regular table

    updateRegularTable(sqlStmt,tableName, tempInfo, lastInfo); //update regular table
    
}

}

