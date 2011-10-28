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
#ifndef _COMMANDAPI_H
#define _COMMANDAPI_H
#include "tlgpfs_error.h"
typedef enum {
    REFRESH = 10,
    STATUS_OVERALL,
    STATUS_CLUSTER,
    STATUS_NODE,
    STATUS_FS,
    STATUS_DISK,
} tlgpfs_command_t;

namespace Commandapi
{
    TLGPFS_ERR_T tlgpfs_command_open(int *fd);
    TLGPFS_ERR_T tlgpfs_command_close(int fd);
    TLGPFS_ERR_T tlgpfs_command_refresh(int fd);
    TLGPFS_ERR_T tlgpfs_command_status(int fd, tlgpfs_command_t level, bool is_detailed);

};
#endif
