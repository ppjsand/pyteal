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
#ifndef _GPFSDISKEVENTLOGGING_H_
#define _GPFSDISKEVENTLOGGING_H_
#include "tlgpfs_error.h"
#include "GPFSEvent.h"

class GPFSDiskEventLogging:public GPFSEventProcessor
{
public:
    GPFSDiskEventLogging();
    virtual ~GPFSDiskEventLogging();
    virtual TLGPFS_ERR_T action(GPFSEvent* event);
private:
};
#endif

