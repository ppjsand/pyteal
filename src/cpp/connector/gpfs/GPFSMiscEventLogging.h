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
#ifndef _GPFSMISCEVENTLOGGING_H_
#define _GPFSMISCEVENTLOGGING_H_
#include "tlgpfs_error.h"
#include "GPFSEvent.h"

class GPFSMiscEventLogging:public GPFSEventProcessor
{
public:
    GPFSMiscEventLogging();
    virtual ~GPFSMiscEventLogging();
    virtual TLGPFS_ERR_T action(GPFSEvent* event);
private:
};
#endif

