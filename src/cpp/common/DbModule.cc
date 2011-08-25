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
 * \file DbModule.cc
 *
 */

#include <DbModule.h>
#include <dlfcn.h>
#include <stdexcept>

#define DBMODULE_SQLLIB "libodbc.so"
#define DBMODULE_LOAD_FUNC(funcName)                    \
  funcName = (funcName ## _t)dlsym(ivSqlLib,#funcName); \
  if (!funcName) throw std::runtime_error(dlerror())

namespace TEAL {

  DbModule::DbModule() {
    ivSqlLib = dlopen(DBMODULE_SQLLIB,RTLD_NOW);
    if (ivSqlLib) {
      DBMODULE_LOAD_FUNC(SQLAllocHandle);
      DBMODULE_LOAD_FUNC(SQLBindCol);
      DBMODULE_LOAD_FUNC(SQLBindParameter);
      DBMODULE_LOAD_FUNC(SQLCloseCursor);
      DBMODULE_LOAD_FUNC(SQLDisconnect);
      DBMODULE_LOAD_FUNC(SQLDriverConnect);
      DBMODULE_LOAD_FUNC(SQLEndTran);
      DBMODULE_LOAD_FUNC(SQLExecDirect);
      DBMODULE_LOAD_FUNC(SQLFetch);
      DBMODULE_LOAD_FUNC(SQLFreeHandle);
      DBMODULE_LOAD_FUNC(SQLFreeStmt);
      DBMODULE_LOAD_FUNC(SQLGetDiagRec);
      DBMODULE_LOAD_FUNC(SQLSetEnvAttr);
      DBMODULE_LOAD_FUNC(SQLSetConnectAttr);

    } else {
      throw std::runtime_error(dlerror());
    }
  }

  DbModule::~DbModule() {
    if (ivSqlLib) {
      dlclose(ivSqlLib);
    }
  }

} // namespace TEAL
