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
#ifndef _GPFSEVENTFACTORY_H
#define _GPFSEVENTFACTORY_H

#include <string>
#include <list>

#include "GPFSEvent.h"
#include "teal_error.h"
class GPFSEventFactory
{
public:
    static GPFSEvent* getEvent(int type, bool isRef, int logtype);

};

#endif

