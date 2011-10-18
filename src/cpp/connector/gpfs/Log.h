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
#ifndef _LOG_H_
#define _LOG_H_

#include "Logging.h"
#define log_error(msg)  TEAL::getLog().Print(TEAL::TEAL_LOG_ERROR, "GPFS_CONN", msg, __FILE__, __LINE__)
#define log_warn(msg)   TEAL::getLog().Print(TEAL::TEAL_LOG_WARN, "GPFS_CONN", msg, __FILE__, __LINE__)
#define log_info(msg)   TEAL::getLog().Print(TEAL::TEAL_LOG_INFO, "GPFS_CONN",msg, __FILE__, __LINE__)
#define log_debug(msg)   TEAL::getLog().Print(TEAL::TEAL_LOG_DEBUG, "GPFS_CONN",msg, __FILE__, __LINE__)
#endif
