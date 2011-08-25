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
 * \file DbModule.h
 * \brief Wrapper to dynamically load and provide ODBC support.
 *
 */

#ifndef DBMODULE_H_
#define DBMODULE_H_

#include <stdexcept>
#include <sql.h>

namespace TEAL {
  typedef SQLRETURN SQL_API (*SQLDriverConnect_t)(SQLHDBC hdbc, SQLHWND hwnd,
                                                  SQLCHAR *szConnStrIn,
                                                  SQLSMALLINT cbConnStrIn,
                                                  SQLCHAR *szConnStrOut,
                                                  SQLSMALLINT cbConnStrOutMax,
                                                  SQLSMALLINT *pcbConnStrOut,
                                                  SQLUSMALLINT fDriverCompletion);

  typedef SQLRETURN SQL_API (*SQLDisconnect_t)(SQLHDBC ConnectionHandle);

  typedef SQLRETURN SQL_API (*SQLAllocHandle_t)(SQLSMALLINT HandleType,
                                                SQLHANDLE InputHandle,
                                                SQLHANDLE *OutputHandle);

  typedef SQLRETURN SQL_API (*SQLSetEnvAttr_t)(SQLHENV EnvironmentHandle,
                                               SQLINTEGER Attribute,
                                               SQLPOINTER Value,
                                               SQLINTEGER StringLength);

  typedef SQLRETURN SQL_API (*SQLBindParameter_t)(SQLHSTMT hstmt,
                                                  SQLUSMALLINT ipar,
                                                  SQLSMALLINT fParamType,
                                                  SQLSMALLINT fCType,
                                                  SQLSMALLINT fSqlType,
                                                  SQLULEN cbColDef,
                                                  SQLSMALLINT ibScale,
                                                  SQLPOINTER rgbValue,
                                                  SQLLEN cbValueMax,
                                                  SQLLEN *pcbValue);

  typedef SQLRETURN SQL_API (*SQLExecDirect_t)(SQLHSTMT StatementHandle,
                                               SQLCHAR *StatementText,
                                               SQLINTEGER TextLength);

  typedef SQLRETURN SQL_API (*SQLEndTran_t)(SQLSMALLINT HandleType,
                                            SQLHANDLE Handle,
                                            SQLSMALLINT CompletionType);

  typedef SQLRETURN SQL_API (*SQLFreeHandle_t)(SQLSMALLINT HandleType,
                                               SQLHANDLE Handle);

  typedef SQLRETURN SQL_API (*SQLFreeStmt_t)(SQLHSTMT StatementHandle,
                                               SQLUSMALLINT Option);

  typedef SQLRETURN SQL_API (*SQLGetDiagRec_t)(SQLSMALLINT HandleType,
                                               SQLHANDLE Handle,
                                               SQLSMALLINT RecNumber,
                                               SQLCHAR *Sqlstate,
                                               SQLINTEGER *NativeError,
                                               SQLCHAR *MessageText,
                                               SQLSMALLINT BufferLength,
                                               SQLSMALLINT *TextLength);

  typedef SQLRETURN SQL_API (*SQLBindCol_t)(SQLHSTMT StatementHandle,
                                            SQLUSMALLINT ColumnNumber,
                                            SQLSMALLINT TargetType,
                                            SQLPOINTER TargetValue,
                                            SQLLEN BufferLength,
                                            SQLLEN *StrLen_or_Ind);

  typedef SQLRETURN SQL_API (*SQLFetch_t)(SQLHSTMT StatementHandle);

  typedef SQLRETURN SQL_API (*SQLCloseCursor_t)(SQLHSTMT StatementHandle);

  typedef SQLRETURN SQL_API (*SQLSetConnectAttr_t)(SQLHDBC ConnectionHandle,
											       SQLINTEGER Attribute,
											       SQLPOINTER Value,
                                                   SQLINTEGER StringLength);

  /**
   * \brief Class which dynamically loads ODBC functionality.
   *
   * The class provides a wrapper around the unixODBC support. This
   * allows for the ODBC support to be dynamically loaded rather than
   * directly linked.
   */

  class DbModule {
   public:
    /**
     * \brief Construct a DbModule
     *
     * Dynamically load the unixODBC (or other) library and initialize
     * all data members to their correct function addresses.
     */
    DbModule();
    /**
     *
     * \brief Destroy a DbModule
     *
     * Close the dynamic library if still open.
     */
    virtual ~DbModule();

    SQLAllocHandle_t SQLAllocHandle;
    SQLBindCol_t SQLBindCol;
    SQLBindParameter_t SQLBindParameter;
    SQLCloseCursor_t SQLCloseCursor;
    SQLDisconnect_t SQLDisconnect;
    SQLDriverConnect_t SQLDriverConnect;
    SQLEndTran_t SQLEndTran;
    SQLExecDirect_t SQLExecDirect;
    SQLFetch_t SQLFetch;
    SQLFreeHandle_t SQLFreeHandle;
    SQLFreeStmt_t SQLFreeStmt;
    SQLGetDiagRec_t SQLGetDiagRec;
    SQLSetEnvAttr_t SQLSetEnvAttr;
    SQLSetConnectAttr_t SQLSetConnectAttr;

   private:
    void* ivSqlLib;
  };

} // namespace TEAL
#endif /* DBMODULE_H_ */
