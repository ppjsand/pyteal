/* begin_generated_IBM_copyright_prolog                             */
/*                                                                  */
/* This is an automatically generated copyright prolog.             */
/* After initializing,  DO NOT MODIFY OR MOVE                       */
/* ================================================================ */
/*                                                                  */
/* (C) Copyright IBM Corp.  2011                                    */
/* Eclipse Public License (EPL)                                     */
/*                                                                  */
/* ================================================================ */
/*                                                                  */
/* end_generated_IBM_copyright_prolog                               */
#ifndef DBGPFS_INFO_H_
#define DBGPFS_INFO_H_

#include <sql.h>
#include <string>
#include "DbInterface.h"
#include "DbModule.h"
#include <vector>
#include <map>
namespace TEAL {
    class DbInterface;
}
using namespace std;
namespace TEAL {
    const unsigned int CHANGE_NA        =  100;
    const unsigned int CHANGE_NONE      =  0;
    const unsigned int CHANGE_MODIFIED  =  1;
    const unsigned int CHANGE_ADDED     =  2;
    const unsigned int CHANGE_REMOVED   =  3;

    const int HEALTHY   = 0;
    const int UNHEALTHY = 1;
    const int UNKNOWN   = 2;
    
    const int INSERT = 0;
    const int UPDATE = 1;
class DbGpfsInfo
{
public:

    DbGpfsInfo(DbInterface* dbi = NULL,string regulartable = "", string temptable = "",vector<string>* cols = NULL,vector<string>* pk = NULL,void* polledinfo = NULL);
    virtual ~DbGpfsInfo();
    void upsertInfo(SQLHSTMT sqlStmt);    
    void queryInfo(SQLHSTMT sqlStmt,const std::string& colName, const std::string& colValue,void** info);
    void updateStatus(SQLHSTMT sqlStmt,const string& col, const string& colValue, const string& key, const string& keyValue);
    void deleteAll(SQLHSTMT sqlStmt,const string& col, const string& colValue);
protected:
    virtual void Upsert(SQLHSTMT sqlStmt, string& upsertSql,int colSize, int pkSize, int opType, void* info) = 0;
    virtual void getResult(SQLHSTMT sqlStmt,void** holder) = 0;
    virtual void updateRegularTable(SQLHSTMT sqlStmt,string& table,void* temp, void* lst) = 0;

    virtual void bindPrimaryKey(SQLHSTMT sqlStmt,string& sql, void* info,bool init) = 0;
    void initTable(SQLHSTMT sqlStmt,string& table);        
    void updateTable(SQLHSTMT sqlStmt,string& table, void* info);
        
private:
    void updateTablebyCol(SQLHSTMT sqlStmt, string& table, const string& col, const string& colValue, const string& key, const string& keyValue);
    void deleteTablebyCol(SQLHSTMT sqlStmt, string& table, const string& col, const string& colValue);
    template <class T>
    void queryTable(SQLHSTMT sqlStmt,string& table, T** holder);     
    void fillTable(SQLHSTMT sqlStmt,string& table);
    template <class T>
    void queryTablebyCol(SQLHSTMT sqlStmt, string& table, const string& col, const string& value, T** holder);    
    void removeRows(SQLHSTMT sqlStmt,string& table);
    DbInterface* dbif;
    vector<string>* fields; // all the columns
    vector<string>* primary_key; //primary key
    void* tempInfo; //query from temp table
    void* lastInfo;//query from regular table
    void* polledInfo;//polled from gpfs
    string tableName; //regular table
    string tmptableName;
};

}


#endif 

