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
#ifndef _ERROR_H
#define _ERROR_H
typedef enum {

    TL_SUCCESS = 0,
    TL_ERR_CONFIGRATION_FAILED = 300,
    TL_ERR_FORK_FAILED,
    TL_ERR_SIGNAL_FAILED,
    TL_ERR_FILE_CREATION,
    TL_ERR_MULTI_INSTANCE,
    TL_ERR_INVALID_USER,
    TL_ERR_SOCKET_READ,
    TL_ERR_SOCKET_WRITE,
    TL_ERR_SOCKET_OPEN,
    TL_ERR_INVALID_SOCKET,
    TL_ERR_SOCKET_CLOSE,
    TL_ERR_SOCKET_BIND,
    TL_ERR_SOCKET_ACCPT,
    TL_ERR_SOCKET_CONNECT,
    TL_ERR_SOCKET_LISTEN,
    TL_ERR_SOCKET_SELECT,
    TL_ERR_GPFS_NOT_STARTED,
    TL_ERR_INVALID_ARG,
    TL_ERR_TLGPFS_NOT_STARTED,
    TL_ERR_POLL_INIT_FAILED,
    TL_ERR_EVENT_INIT_FAILED,
    TL_ERR_THREAD_CREATE_FAILED,
    TL_ERR_THREAD_JOIN_FAILED,
    TL_ERR_REFRESH_FAILED,
    TL_ERR_EVENT_NOT_SUPPORT,
    TL_ERR_COMMAND_NOT_SUPPORT
}TLGPFS_ERR_T;
#endif
