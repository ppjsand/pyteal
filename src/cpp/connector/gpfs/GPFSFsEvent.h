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
#ifndef _GPFSFSEVENT_H
#define _GPFSFSEVENT_H
#include "GPFSEvent.h"
class GPFSFsEvent: public GPFSEvent
{
public:
    GPFSFsEvent(int evttype, int logtype, bool isRef);
    virtual ~GPFSFsEvent();
};

#endif

