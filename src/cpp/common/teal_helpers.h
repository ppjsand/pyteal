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
 * \file teal_helpers.h
 * \brief TEAL Connector API, internal-only use functions.
 *
 *
 */

#ifndef _H_TEAL_HELPERS_
#define _H_TEAL_HELPERS_

// System Includes
#include <string>
#include <fstream>
#include <algorithm>

#include "teal_error.h"

// Short cuts for environment variables.

namespace TEAL {

  extern const char *tealDataDir;
  extern const char *tealConfDir;
  extern const char *tealLogDir;
  extern const char *tealRootDir;
  extern const char *tealEventLogTable;

  class Notifier;

  /**
   * \brief Process xCAT configuration file.
   *
   * Reads the xCAT configuratoin file, cfgloc, from the path
   * provided. Parses the file and returns a connection string usuable
   * by the unixODBC ODBC implementaiton.
   *
   * Currently supports xCAT cfgloc files formatted for MySQL and DB2.
   *
   * \param[in] path The path to the cfgloc file.
   * \param[in, out] connectionString A connection string usuable by ODBC.
   *
   * \retval A TEAL_ERR_T encoded return value.
   *
   */
  TEAL_ERR_T processxCATConfFile(const std::string &path,
                                 std::string &connectionString);

  /**
   * \brief Create a "PASCAL" encoded string in storage.
   *
   * Starting at the target pointer, write an unsigned character value
   * which represents the length of the data to follow, then write a
   * maximum of field_len characters following. Return a pointer
   * to the next valid location in target where data may be written.
   *
   * This function expects the target buffer to have been initialized
   * to null/space values.
   *
   * \param[in] target The starting address to which data should be written.
   * \param[in[ source The source of the data.
   * \param[in] field_len The maximum size allotted for data.
   *
   * \retval A pointer to the next valid location in target to begin writting
   *         data.
   */

  char * write_pstr(char *target, const char *source, int field_len);

  /**
   * Create the notifier for the process to be used when an event
   * is added to the event log
   */
  Notifier* create_notifier();

} // namespace TEAL
#endif // _H_TEAL_HELPERS_

