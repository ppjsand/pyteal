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
#ifndef _GPFSDISKEVENT_H
#define _GPFSDISKEVENT_H
#include "GPFSEvent.h"
class GPFSDiskEvent: public GPFSEvent
{
public:
    GPFSDiskEvent(int evttype, int logtype, bool isRef);
    virtual ~GPFSDiskEvent();
};

#endif

