/* begin_generated_IBM_copyright_prolog                             */
/*                                                                  */
/* This is an automatically generated copyright prolog.             */
/* After initializing,  DO NOT MODIFY OR MOVE                       */
/* ================================================================ */
/*                                                                  */
/* (C) Copyright IBM Corp.  2010,2011                               */
/* Eclipse Public License (EPL)                                     */
/*                                                                  */
/* ================================================================ */
/*                                                                  */
/* end_generated_IBM_copyright_prolog                               */
/**
 * \file DbInterface.h
 * \brief C++ wrapper over ODBC functionality.
 */

#ifndef _H_DBINTERFACE_
#define _H_DBINTERFACE_

#include <stdexcept>
#include <string>
#include <sstream>
#include <algorithm>
#include <iterator>
#include <vector>

#include <sql.h>
#include <sqlext.h>

#include "teal_error.h"
#include "DbModule.h"
#include "Logging.h"


namespace TEAL {

class DbEvent;
class DbGpfsInfo;
class SqlGenerator;


  /**
   * \brief A class to represent ODBC errors as exceptions.
   */

  class DbException : public std::exception {

   public:
    DbException(SQLRETURN errorcode = SQL_ERROR) :
      ivSqlErrorCode(errorcode), ivSqlErrorText(""),
      ivSqlState(""),ivSqlNativeErrorValue(0)
    {
    }

    DbException(SQLRETURN errorcode, char *str,
                char *state, int nativeVal) :
      ivSqlErrorCode(errorcode), ivSqlErrorText(str),
      ivSqlState(state),ivSqlNativeErrorValue(nativeVal)
    {
        std::ostringstream retValue;

        retValue << "DbException:" << std::endl;
        retValue << "SQL Error:" << ivSqlErrorCode << std::endl;;
        retValue << "ODBC SQLSTATE:" << ivSqlState << std::endl;;
        retValue << "ODBC Native Error: " << ivSqlNativeErrorValue << std::endl;
        retValue << "Error Text: " << ivSqlErrorText << std::endl;
        ivWhat.assign(retValue.str());
    }

    ~DbException()  throw()
    {
    }

    virtual const char *what() throw()
    {
        return ivWhat.c_str();
    }

   private:

    SQLRETURN ivSqlErrorCode;
    std::string ivSqlErrorText;
    std::string ivSqlState;
    SQLINTEGER ivSqlNativeErrorValue;
    std::string ivWhat;
  };


  /**
   * \brief A class to wrap the ODBC interface.
   */

  class DbInterface {
   public:

    /**
     * \brief Setup the basic ODBC information for accessing the database.
     *
     * The DbInterface() constructor performs the following steps
     *
     * -# Retrieve the needed information to create the db connection string.
     * -# Allocate an ODBC ENV handle.
     * -# Set the ODBC version attribute to ODBC3.
     * -# Allocate an ODBC DBC handle.
     *
     * Any errors in these processes will cause an exception to be thrown.
     *
     * \parm connStr The database connection string for ODBC.
     *
     *
     * \exception DbException
     */

    DbInterface(const std::string &connStr);

    /*
     * \brief Cleanup the basic ODBC structures allocated by constructor.
     */
    ~DbInterface();


    /**
     * \brief Connect to the underlying db via ODBC.
     *
     * \exception DbException
     */

    void connect();

    /**
     * \brief Disconnect from the underlying db via ODBC.
     *
     * \exception DbException
     */

    void disconnect()
    {
      SQLRETURN ret;
      ret = dbModule.SQLEndTran(SQL_HANDLE_DBC,ivSqlDbc,SQL_COMMIT);
      checkSqlRetcode("SQLEndTran",ret,ivSqlDbc,SQL_HANDLE_DBC);
      ret = dbModule.SQLDisconnect(ivSqlDbc);
      checkSqlRetcode("SQLDisconnect",ret,ivSqlDbc,SQL_HANDLE_DBC);
      return;
    }

    /**
     * \brief Commit any pending operations to the underlying db via ODBC.
     *
     * \exception DbException
     */

    void commit()
    {
      SQLRETURN ret;
      ret = dbModule.SQLEndTran(SQL_HANDLE_DBC,ivSqlDbc,SQL_COMMIT);
      checkSqlRetcode("SQLEndTran",ret,ivSqlDbc,SQL_HANDLE_DBC);
      return;
    }

    /**
     * \brief Rollback any pending operations to the underlying db via ODBC.
     *
     * \exception DbException
     */

    void rollback()
    {
      SQLRETURN ret;
      ret = dbModule.SQLEndTran(SQL_HANDLE_DBC,ivSqlDbc,SQL_ROLLBACK);
      checkSqlRetcode("SQLEndTran",ret,ivSqlDbc,SQL_HANDLE_DBC);
      return;
    }

    /**
     * Insert information into a database using ODBC.
     *
     * @param eventData the event objecxt to insert
     */
    void insertRecord(DbEvent& eventData);

    /**
     * Upsert configuration information in a database using ODBC.
     *
     * @param configData the cofiguration object to be upserted
     */
    void upsertConfiguration(DbGpfsInfo& configData);

    /**
     * Query configuration information in a database using ODBC.
     *
     * @param configData the cofiguration object to be queried
     * @param colName column name to query, "*" for all columns
     * @param colValue column value should be equaled, "" for all value when colName is "*"
     * @param info the configuration container to hold the result
     */
    void queryConfiguration(DbGpfsInfo& configData, const std::string& colName, const std::string& colValue,void** info);

    /**
     *Update configuration information in a database using ODBC.
     *
     * @param configData the cofiguration object to be updated
     * @param colName column name to update
     * @param colValue column value should be equaled
     * @param keyName column name to search column
     * @param keyValue column value should be equaled by keyName specified column
     */
    void updateStatusAll(DbGpfsInfo& configData,
                           const std::string& colName,
                           const std::string& colValue,
                           const std::string& keyName,
                           const std::string& keyValue);

    /**
     *Delete unkown configuration information in a database using ODBC.
     *
     * @param configData the cofiguration object to be deleted
     * @param colName column name to refer to
     * @param colValue column value should be equaled
     */
    void deleteUnknown(DbGpfsInfo& configData,
                           const std::string& colName,
                           const std::string& colValue);

    /**
     * \brief Process an ODBC return code to create and throw an exception.
     *
     * \exception DbException
     */
    static void checkSqlRetcode(const std::string &funcName,
                                SQLRETURN retCode,
                                SQLHANDLE handle, SQLSMALLINT type);


    /**
     * This method will create an insert string formatted for the configured database
     *
     * @param fields the database columns to insert
     * @param the table name to insert to
     *
     * @return the formatted insert string
     */
    std::string genInsert(std::vector<std::string>& fields, std::string& table);

    /**
     * This method will create an insert string formatted for the configured database. It assumes
     * that the first column is the record id and will substitute the appropriate method on
     * the database to get the last identity value created. This means that the prior insert
     * must be in the primary table with no intervening insert.
     *
     * @param fields the database columns to insert
     * @param the table name to insert to
     *
     * @return the formatted insert string
     */
    std::string genSubtableInsert(std::vector<std::string>& fields, std::string& table);


    /**
     * This method will create a update string formatted for the configured database according to the keys specified by argument.
     *
     * @param fields the database columns to update
     * @param the keys to locate the rows of the table
     * @param the table name to update
     *
     * @return the formatted update string
     */

    std::string genUpdate(std::vector<std::string>& fields,std::vector<std::string>& keys, std::string& table);

    /**
     * This method will create a delete string formatted for the configured database according to the keys specified by argument.
     *
     * @param the keys to locate the rows of the table
     * @param the table name to delete
     *
     * @return the formatted delete string
     */

    std::string genDelete(std::vector<std::string>& keys, std::string& table);

    /**
     * This method will create a select string formatted for the configured database according to the fields specified by argument.
     *
     * @param the fileds columns of the table
     * @param the table name to delete
     *
     * @return the formatted select string
     */

    std::string genSelect(std::vector<std::string>& fields, std::string& table);


    /**
     * Return the table name of the event log. Different implementations may use
     * other names.
     */
    const char* getEventLogTableName() const { return "x_tealeventlog"; }

    /**
     * Return the database table prefix. This is for tables that have a constucted
     * name, such as for extended data, but still need to follow a naming convention
     * for the product
     */
    const char* getTablePrefix() const { return "x_"; }

   public:
        /**
         * \brief The associated ODBC wrapper module.
         */
        static TEAL::DbModule dbModule;


   private:
    DbInterface(const DbInterface&);

    /**
     * \brief Do the necessary work to get a pointer usable by ODBC
     * interfaces from a std::string.
     */

    unsigned char *toSqlStr(const std::string& s)
    {
      return reinterpret_cast<unsigned char *>(const_cast<char *>(s.c_str()));
    }

    /**
     * \brief The ODBC environment handle.
     */
    SQLHENV ivSqlEnv;

    /**
     * \brief The ODBC database handle.
     */
    SQLHDBC ivSqlDbc;

    /**
     * \brief The ODBC statement handle.
     */
    SQLHSTMT ivSqlStmt;

    /**
     * \brief The ODBC connection string.
     */
    std::string ivConnectStr;

    /**
     * \brief A string representing the type of database.
     */
    std::string ivDbType;

    /**
     * The SQL Generator for the configured database
     */
    SqlGenerator* ivSqlGenerator;

    /**
     * \brief A string representing the DbInterface API version.
     */
    std::string ivAPIVersion;
  };

}
#endif // _H_DBINTERFACE_

