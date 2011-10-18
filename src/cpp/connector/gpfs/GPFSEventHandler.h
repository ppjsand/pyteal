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
#ifndef _GPFS_EVENT_HANDLER_H
#define _GPFS_EVENT_HANDLER_H

#include "GPFSEvent.h"
#include "GPFSHandler.h"
#include "teal_connect_api.h"
#include <map>

class GPFSEventHandler:public GPFSHandler
{
    public:
        static GPFSEventHandler* getEventHandler();
        static string getEventName(int type);
        static int getEventBehavior(int type);
        static int getEventType(string name);
    private:
        static GPFSEventHandler* instance;
        GPFSEventHandler();
        virtual ~GPFSEventHandler();
        static int getLogType(int evttype);
        void registerEvent();
        static void initEventMap(); //persist all supported events
        virtual void action(GPFSHandler* handler);
        static map<int,string>* events;
        static map<int,int>* behaviors;//key = event number, value = behavior
        static TEAL_ERR_T processGPFSConfFile(const std::string& path);
        static TEAL_ERR_T initBehaviorMap(const std::string& name,const std::string& bahavior);

};

#endif

