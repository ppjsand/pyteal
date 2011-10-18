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
#ifndef _COMMAND_LISTENER_H
#include "tlgpfs_error.h"

#define _COMMAND_LISTENER_H
#define GPFS_SOCK_FILE "/tmp/tlgpfsmon.socket"

namespace CommandListener
{
    TLGPFS_ERR_T init();
    TLGPFS_ERR_T AcceptConnection(int sockfd);
};
#endif
