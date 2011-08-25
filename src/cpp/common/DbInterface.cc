// begin_generated_IBM_copyright_prolog
//
// This is an automatically generated copyright prolog.
// After initializing,  DO NOT MODIFY OR MOVE
// ================================================================
//
// (C) Copyright IBM Corp.  2010,2011
// Eclipse Public License (EPL)
//
// ================================================================
//
// end_generated_IBM_copyright_prolog

/**
 * \file DbInterface.cc
 * \brief C++ wrapper over ODBC functionality.
 */

/*--------------------------------------------------------------------*/
/*  Includes                                                          */
/*--------------------------------------------------------------------*/

#include "DbInterface.h"
#include "DbEvent.h"
#include "DbGpfsInfo.h"

/*--------------------------------------------------------------------*/
/*  User Types                                                        */
/*--------------------------------------------------------------------*/

namespace TEAL {

class join
{
public:
    join(const std::vector<std::string>& fields,const std::string& jstr) : v(fields), j(jstr) { }
    std::ostream& operator()(std::ostream& os) const {
        bool first = true;
        for (std::vector<std::string>::const_iterator it = v.begin(); it != v.end(); ++it) {
            if (!first) {
                os << j;
            } else {
                first = false;
            }
            os << *it;
        }
        return os;
    }
private:
    const std::vector<std::string>& v;
    const std::string& j;
};

std::ostream& operator<<(std::ostream& os, const join& j)
{
    return j(os);
}

/*--------------------------------------------------------------------*/

class upper
{
public:
    upper (const std::string& str) : s(str) { }
    std::ostream &operator()(std::ostream& os) const
    {
        for(std::string::const_iterator it = s.begin(); it != s.end(); ++it) {
            os << (unsigned char)toupper(*it);
        }
        return os;
    }
private:
    const std::string& s;
};

std::ostream& operator<<(std::ostream& os, const upper& u)
{
    return u(os);
}

/*--------------------------------------------------------------------*/

class repeat
{
public:
    repeat(const std::string& str, unsigned cnt) : count(cnt), s(str) { }
    std::ostream& operator()(std::ostream& os) const
    {
        for (unsigned i = 0; i < count; ++i) {
            os << s;
        }
        return os;
    }
private:
    unsigned count;
    const std::string& s;
};

std::ostream& operator<<(std::ostream& os, const repeat& r)
{
    return r(os);
}

/*--------------------------------------------------------------------*/

class SqlGenerator {
    public:
        SqlGenerator() { }
        virtual ~SqlGenerator() { }

        virtual std::string genInsert(std::vector<std::string>, std::string& tableName) = 0;
        virtual std::string genSubtableInsert(std::vector<std::string>, std::string& tableName) = 0;
        virtual std::string genUpdate(std::vector<std::string>& fields,std::vector<std::string>& keys, std::string& tableName) = 0;
        virtual std::string genDelete(std::vector<std::string>& keys, std::string& tableName) = 0;
        virtual std::string genSelect(std::vector<std::string>& fields, std::string& tableName) = 0;
};

/*--------------------------------------------------------------------*/

class MySqlGenerator : public SqlGenerator {
    public:
        MySqlGenerator() { }
        virtual ~MySqlGenerator() { }

        virtual std::string genInsert(std::vector<std::string> fields, std::string& tableName) {
            std::ostringstream oss;
            oss << "INSERT INTO " << tableName << "(" << join(fields,",") << ") VALUES(" << repeat("?,",fields.size()-1) << "?)";
            return oss.str();
        }

        virtual std::string genSubtableInsert(std::vector<std::string> fields, std::string& tableName) {
            std::ostringstream oss;
            unsigned repeatCount = fields.size() < 2 ? 0 : fields.size()-2;
            oss << "INSERT INTO " << tableName << "(" << join(fields,",") << ") VALUES(LAST_INSERT_ID()" << repeat(",?",repeatCount) << ",?)";
            return oss.str();
        }

        virtual std::string genUpdate(std::vector<std::string>& fields,std::vector<std::string>& keys, std::string& tableName) {
            std::ostringstream oss;
            oss << "UPDATE " << tableName << " SET " << join(fields,"=?,") << "=? WHERE " << join(keys,"=? AND ") << "=?";
            return oss.str();
        }

        virtual std::string genDelete(std::vector<std::string>& fields, std::string& tableName) {
            std::ostringstream oss;
            oss << "DELETE FROM " << tableName;

            if((fields.size() == 1 && fields.front() == "*") || fields.size() == 0)
                  return oss.str();

            oss << " WHERE " << join(fields,"=? AND ") << "=?";
            return oss.str();
        }

        virtual std::string genSelect(std::vector<std::string>& fields, std::string& tableName) {
            std::ostringstream oss;
            oss << "SELECT DISTINCT * FROM " << tableName;

            if((fields.size() == 1 && fields.front() == "*") || fields.size() == 0)
                  return oss.str();

            oss << " WHERE " << join(fields,"=? AND ") << "=?";
            return oss.str();
        }

};

/*--------------------------------------------------------------------*/

class Db2Generator : public SqlGenerator {
    public:
        Db2Generator() { }
        virtual ~Db2Generator() { }

        virtual std::string genInsert(std::vector<std::string> fields, std::string& tableName) {
            std::ostringstream oss;
            oss << "INSERT INTO " << upper(tableName) << "(\"" << join(fields,"\",\"") << "\") VALUES(" << repeat("?,",fields.size()-1) << "?)";
            return oss.str();
        }

        virtual std::string genSubtableInsert(std::vector<std::string> fields, std::string& tableName) {
            std::ostringstream oss;
            unsigned repeatCount = fields.size() < 2 ? 0 : fields.size()-2;
            oss << "INSERT INTO " << upper(tableName) << "(\"" << join(fields,"\",\"") << "\") VALUES(IDENTITY_VAL_LOCAL()" << repeat(",?",repeatCount) << ",?)";
            return oss.str();
        }

        virtual std::string genUpdate(std::vector<std::string>& fields,std::vector<std::string>& keys, std::string& tableName) {
            std::ostringstream oss;
            oss << "UPDATE " << upper(tableName) << " SET " << "\"" << join(fields,"\"=?,\"") << "\"=? WHERE \"" << join(keys,"\"=? AND \"") << "\"=?";
            return oss.str();
        }

        virtual std::string genDelete(std::vector<std::string>& fields, std::string& tableName) {
            std::ostringstream oss;

            oss << "DELETE FROM " << upper(tableName);
            if((fields.size() == 1 && fields.front() == "*") || fields.size() == 0)
                  return oss.str();

            oss<< " WHERE \"" << join(fields,"\"=? AND \"") << "\"=?";
            return oss.str();
        }

        virtual std::string genSelect(std::vector<std::string>& fields, std::string& tableName) {
            std::ostringstream oss;

            oss << "SELECT DISTINCT * FROM " << upper(tableName);
            if((fields.size() == 1 && fields.front() == "*") || fields.size() == 0)
                  return oss.str();

            oss << " WHERE \"" << join(fields,"\"=? AND \"") << "\"=?";
            return oss.str();
        }

};

}

/*--------------------------------------------------------------------*/
/*  Constants                                                         */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Macros                                                            */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Internal Function Prototypes                                      */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Global Variables                                                  */
/*--------------------------------------------------------------------*/

TEAL::DbModule TEAL::DbInterface::dbModule;

/*--------------------------------------------------------------------*/
/* >>> Function <<<                                                   */
/*--------------------------------------------------------------------*/


namespace TEAL {

  // The constructor body is wrapped in a try block to handle
  // an exceptions thrown by the DbModule member initialization.
  DbInterface::DbInterface(const std::string &connectionString) try


    : ivConnectStr(connectionString),ivAPIVersion("1.0")
        {
          SQLRETURN ret;

          std::ostringstream strm;

          // Set information on what database is in use. This is needed to handle
          // SQL differences within other API calls.
          if(connectionString.find("MySQL") != std::string::npos) {
            ivDbType = "MySQL";
            ivSqlGenerator = new MySqlGenerator();
          } else if(connectionString.find("DB2") != std::string::npos) {
            ivDbType = "DB2";
            ivSqlGenerator = new Db2Generator();
          } else {
            ivDbType = "UNKNOWN";
            ivSqlGenerator = new MySqlGenerator();
          }

          ret = dbModule.SQLAllocHandle(SQL_HANDLE_ENV,SQL_NULL_HANDLE, &ivSqlEnv);
          checkSqlRetcode("SQLAllocHandle ENV",ret,ivSqlEnv,SQL_HANDLE_ENV);

          ret = dbModule.SQLSetEnvAttr(ivSqlEnv,SQL_ATTR_ODBC_VERSION,(void *)SQL_OV_ODBC3,0);
          checkSqlRetcode("SQLSetEnvAttr",ret,ivSqlEnv,SQL_HANDLE_ENV);

          ret = dbModule.SQLAllocHandle(SQL_HANDLE_DBC,ivSqlEnv,&ivSqlDbc);
          checkSqlRetcode("SQLAllocHandle DBC",ret,ivSqlDbc,SQL_HANDLE_DBC);


        }

  catch(std::runtime_error &rE) {
    std::string error(rE.what());
    throw TEAL::TealException(error);
  }
  catch(...) {
    throw TEAL::TealException("Unknown failure in DbInterface initialization.");
  }



  DbInterface::~DbInterface() {
    dbModule.SQLFreeHandle(SQL_HANDLE_DBC,ivSqlDbc);
    dbModule.SQLFreeHandle(SQL_HANDLE_ENV,ivSqlEnv);
    delete ivSqlGenerator;
  }

  void DbInterface::connect() {
    SQLRETURN ret;

    ret = dbModule.SQLDriverConnect(ivSqlDbc,
									NULL,
									toSqlStr(ivConnectStr),
                                    SQL_NTS,
                                    NULL,
                                    0,
                                    NULL,
                                    SQL_DRIVER_NOPROMPT);
    // checkSqlRetcode will throw if there is an error.
    checkSqlRetcode("SQLDriverConnect",ret,ivSqlDbc,SQL_HANDLE_DBC);

    try {
  	  ret = dbModule.SQLSetConnectAttr(ivSqlDbc, SQL_ATTR_AUTOCOMMIT, SQL_AUTOCOMMIT_OFF, 0);
  	  checkSqlRetcode("SQLSetConnectAttr",ret,ivSqlDbc,SQL_HANDLE_DBC);
    } catch(const DbException& dbe) {
  	  try {
  		  disconnect();
  	  } catch(DbException& tmp_dbe) {
  		  // Do nothing
  	  }
  	  throw dbe;
    }
    return;
  }

  void DbInterface::insertRecord(DbEvent& eventData) {
        SQLHSTMT sqlStmt;
        SQLRETURN ret;

        ret = DbInterface::dbModule.SQLAllocHandle(SQL_HANDLE_STMT, ivSqlDbc, &sqlStmt);
        DbInterface::checkSqlRetcode("DbObject::insertRecord SQLAllocHandle",ret,sqlStmt,SQL_HANDLE_STMT);

        eventData.insert(sqlStmt);

        ret = DbInterface::dbModule.SQLFreeHandle(SQL_HANDLE_STMT,sqlStmt);
        DbInterface::checkSqlRetcode("DbObject::insertRecord SQLFreeHandle",ret,sqlStmt,SQL_HANDLE_STMT);
  }

  void DbInterface::upsertConfiguration(DbGpfsInfo& configData) {
        SQLHSTMT sqlStmt;
        SQLRETURN ret;

        ret = DbInterface::dbModule.SQLAllocHandle(SQL_HANDLE_STMT, ivSqlDbc, &sqlStmt);
        DbInterface::checkSqlRetcode("DbObject::upsertConfiguration SQLAllocHandle",ret,sqlStmt,SQL_HANDLE_STMT);

        configData.upsertInfo(sqlStmt);

        ret = DbInterface::dbModule.SQLFreeHandle(SQL_HANDLE_STMT,sqlStmt);
        DbInterface::checkSqlRetcode("DbObject::upsertConfiguration SQLFreeHandle",ret,sqlStmt,SQL_HANDLE_STMT);
  }

  void DbInterface::queryConfiguration(DbGpfsInfo& configData, const std::string& colName, const std::string& colValue,void** info) {
        SQLHSTMT sqlStmt;
        SQLRETURN ret;

        ret = DbInterface::dbModule.SQLAllocHandle(SQL_HANDLE_STMT, ivSqlDbc, &sqlStmt);
        DbInterface::checkSqlRetcode("DbObject::queryConfiguration SQLAllocHandle",ret,sqlStmt,SQL_HANDLE_STMT);

        configData.queryInfo(sqlStmt,colName,colValue,info);

        ret = DbInterface::dbModule.SQLFreeHandle(SQL_HANDLE_STMT,sqlStmt);
        DbInterface::checkSqlRetcode("DbObject::queryConfiguration SQLFreeHandle",ret,sqlStmt,SQL_HANDLE_STMT);
  }

  void DbInterface::updateStatusAll(DbGpfsInfo& configData,
                                    const std::string& colName,
                                    const std::string& colValue,
                                    const std::string& keyName,
                                    const std::string& keyValue){
        SQLHSTMT sqlStmt;
        SQLRETURN ret;

        ret = DbInterface::dbModule.SQLAllocHandle(SQL_HANDLE_STMT, ivSqlDbc, &sqlStmt);
        DbInterface::checkSqlRetcode("DbObject::updateStatusAll SQLAllocHandle",ret,sqlStmt,SQL_HANDLE_STMT);

        configData.updateStatus(sqlStmt, colName, colValue, keyName, keyValue);

        ret = DbInterface::dbModule.SQLFreeHandle(SQL_HANDLE_STMT,sqlStmt);
        DbInterface::checkSqlRetcode("DbObject::updateStatusAll SQLFreeHandle",ret,sqlStmt,SQL_HANDLE_STMT);
  }
  void DbInterface::deleteUnknown(DbGpfsInfo& configData,
                         const std::string& colName,
                         const std::string& colValue){
        SQLHSTMT sqlStmt;
        SQLRETURN ret;

        ret = DbInterface::dbModule.SQLAllocHandle(SQL_HANDLE_STMT, ivSqlDbc, &sqlStmt);
        DbInterface::checkSqlRetcode("DbObject::deleteUnknown SQLAllocHandle",ret,sqlStmt,SQL_HANDLE_STMT);

        configData.deleteAll(sqlStmt, colName, colValue);

        ret = DbInterface::dbModule.SQLFreeHandle(SQL_HANDLE_STMT,sqlStmt);
        DbInterface::checkSqlRetcode("DbObject::deleteUnknown SQLFreeHandle",ret,sqlStmt,SQL_HANDLE_STMT);
  }

  // Private functions.
  DbInterface::DbInterface(const DbInterface&) {}

  void DbInterface::checkSqlRetcode(const std::string &funcName,
                                    SQLRETURN retCode,
                                    SQLHANDLE handle,
                                    SQLSMALLINT type) {

    if(!SQL_SUCCEEDED(retCode)) {

      // Retrieve some error information.
      SQLINTEGER i = 0;
      SQLINTEGER native;
      SQLCHAR state[7];
      SQLCHAR text[256];
      SQLSMALLINT len;
      SQLRETURN ret;

      ret = dbModule.SQLGetDiagRec(type,handle,++i,state, &native,text,sizeof(text),&len);
      if(SQL_SUCCEEDED(ret)) {

        std::ostringstream s;
        s << "SQL Failure: " << funcName << " ("
          << reinterpret_cast<char *>(state) << ") "
          << reinterpret_cast<char *>(text);
        TEAL::getLog().printForced(TEAL::TEAL_LOG_DEBUG,"TEAL_DBINTERFACE",
                                    s.str().c_str());
        throw DbException(retCode,reinterpret_cast<char *>(text),
                          reinterpret_cast<char *>(state),native);
      } else {
        std::ostringstream s;
        s << "SQL Failure: " << funcName << " :SQLRETURN=" <<  retCode;
        TEAL::getLog().printForced(TEAL::TEAL_LOG_DEBUG,"TEAL_DBINTERFACE",
                                    s.str().c_str());
        throw DbException(retCode);
      }

    }
  }

  std::string DbInterface::genInsert(std::vector<std::string>& fields, std::string& table)
  {
      return ivSqlGenerator->genInsert(fields, table);
  }

  std::string DbInterface::genSubtableInsert(std::vector<std::string>& fields, std::string& table)
  {
        return ivSqlGenerator->genSubtableInsert(fields, table);
  }

  std::string DbInterface::genDelete(std::vector<std::string>& keys, std::string& table)
  {
      return ivSqlGenerator->genDelete(keys, table);
  }

  std::string DbInterface::genSelect(std::vector<std::string>& fields, std::string& table)
  {
      return ivSqlGenerator->genSelect(fields, table);
  }

  std::string DbInterface::genUpdate(std::vector<std::string>& fields,std::vector<std::string>& keys, std::string& table)
  {
      return ivSqlGenerator->genUpdate(fields, keys, table);
  }

} // namespace TEAL
