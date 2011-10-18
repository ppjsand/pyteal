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
#ifndef _GPFSEVENTPROCESSORFACTORY_H
#define _GPFSEVENTPROCESSORFACTORY_H

#include <string>
#include <list>

#include "GPFSEventProcessor.h"
class GPFSEventProcessor;
class GPFSEventProcessorFactory
{
public:
    static GPFSEventProcessor* getEventProcessor(int type, bool isRef);
};

#endif

