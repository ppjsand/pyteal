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
 * \file teal_connect_api.h
 * \brief TEAL Connector API
 *
 */

#ifndef _H_TEAL_CONNECT_API_
#define _H_TEAL_CONNECT_API_

// System Includes

// Local Includes
#include "teal_event.h"
#include "teal_error.h"

#ifdef __cplusplus
extern "C" {
#endif

  typedef void* teal_connector_handle;

  /**
   * \brief Initialize the connector API.
   *
   * Initializes the connector interface to the TEAL event
   * log. Returns a pointer to an opaque teal_connect_handle_t object
   * which is then passed to other API calls.
   *
   * The storage for the handle is managed by the API; clients should
   * not free the handle.
   *
   * \param[in,out] conn_handle A point to storage for the connector handle
   * \param[in] comp_name A null-terminated string representing the
   *            component using the connector.
   * \param[in] log_dir A null-terminated string representing a location
   *            in the file system to write the connector's log file.
   *            If NULL, connector uses TEAL_LOG_DIR.
   *
   */

  TEAL_ERR_T teal_open_connector(teal_connector_handle *conn_handle,
                                 const char * comp_name,
                                 const char * log_dir);

  /**
   * \brief Close the connector interface.
   *
   * Closes the connector interface to the TEAL event log.
   * Deallocates storage associated with the handle.
   *
   * \param[in] conn_handle The connector handle.
   *
   */
  TEAL_ERR_T teal_close_connector(teal_connector_handle conn_handle);

  /**
   * Write an event to the event log
   *
   * This will write the specified event and then notify the framework
   * that a new event is available for processing
   *
   * @param conn_handle the connector handle
   * @param event - the event to write
   * @param raw_data_len - amount of additional data to write
   * @param raw_data - the additional user-defined data
   *
   * @return status of the operation
   */
  TEAL_ERR_T teal_write_event(teal_connector_handle conn_handle,
					          teal_cbe_t* event,
					          unsigned raw_data_len,
					          void* raw_data);

#ifdef __cplusplus
}
#endif

#endif // _H_TEAL_CONNECT_API_

