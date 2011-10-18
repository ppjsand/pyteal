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
#ifndef _CONFIGURATION_H_
#define _CONFIGURATION_H_
#include <iostream>
#include <string>
#include <stdlib.h>
#include <unistd.h>
using namespace std;
#define DEFAULT_POLL_INTERVAL 86400 //default polling interval is 1 day
#define DAEMON_NAME           "tlgpfsmon"
class Configuration
{
public:
    bool processCommandLineOptions(int argc, char *argv[]);
    bool init(int argc, char *argv[]);
    static Configuration& getInstance();
    bool asDaemon();
    bool isPoll();
    bool isEvent();
    string& getConfPath();
    int getInterval();
private:
    Configuration();
    bool enable_poll;
    bool as_daemon;
    bool enable_event;
    int poll_interval;
    void usage(const std::string &processName);
    static Configuration instance;
    string confPath;    
};

#endif
