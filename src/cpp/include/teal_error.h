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
 * \file teal_error.h
 * \brief TEAL Error Values
 */

#ifndef _H_TEAL_ERROR_
#define _H_TEAL_ERROR_

#include <limits.h>

#ifdef __cplusplus
extern "C" {
#endif

  /**
   * \brief TEAL error values.
   *
   */

  typedef enum {
    TEAL_SUCCESS               = 0,     /**< Success                           */

    /* General TEAL errors. */
    TEAL_ERR_ARG               = -1,    /**< Invalid argument passed to API    */

    /* Operating system errors reflected by TEAL. */
    TEAL_ERR_SYS_GEN           = -1024, /**< A non-specific, non-recoverable
                                         *   error occurred.                   */
    TEAL_ERR_SYS_MEM           = -1025, /**< A non-recoverable memory  
                                         *   allocation error occurred.        */

    TEAL_ERR_SYS_FILE          = -1026, /**< A non-recoverable file error 
                                         *   occurred.                         */

    /* Connector errors.*/
    TEAL_ERR_CONN_HANDLE       = -2048, /**< Handle contents are invalid.      */
    TEAL_ERR_CONN_INIT         = -2049, /**< The connector failed to 
                                         *   initialize.                       */

    TEAL_ERR_CONN_GEN          = -2050, /**< A non-specific connector error.   */
    TEAL_ERR_CONN_WRITE        = -2051, /**< The connector failed to write 
                                         *   data.                             */

    TEAL_ERR_CONN_LOGGER_INIT  = -4092, /**< The connector logging subsystem 
                                         *   failed to initialize.             */
    TEAL_ERR_CONN_LOGGER_WRITE = -4093, /**< The connector logging subsystem
                                         *   failed to write data.             */



    TEAL_MAX_ERROR            = INT_MIN /**< Minimum error value.              */

  } TEAL_ERR_T;


#ifdef __cplusplus
} 
#endif  

#endif // _H_TEAL_ERROR_

