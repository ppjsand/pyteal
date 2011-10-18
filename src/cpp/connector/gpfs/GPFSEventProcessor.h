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
#ifndef _GPFSEVENTPROCESSOR_H
#define _GPFSEVENTPROCESSOR_H
#include "GPFSEvent.h"

const int IGNORE        = 1;
const int LOGGINGMISC   = 2;//logging events to misc event sub table
const int LOGGINGDISK   = 3;//logging events to disk event sub table
const int LOGGINGFS     = 4;//logging events to file system sub table
const int LOGGINGPS     = 5;//logging events to perseus sub table
const int REFRESHONLY   = 10; //if a behavior eqals 10+2, it should log disk and do a refresh.

class GPFSEvent;
class GPFSEventProcessor
{
public:
    virtual TLGPFS_ERR_T action(GPFSEvent*) = 0;
    GPFSEventProcessor();
    virtual ~GPFSEventProcessor();
private:
    
};
#endif
