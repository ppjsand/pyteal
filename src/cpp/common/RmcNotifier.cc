// begin_generated_IBM_copyright_prolog
//
// This is an automatically generated copyright prolog.
// After initializing,  DO NOT MODIFY OR MOVE
// ================================================================
//
// (C) Copyright IBM Corp.  2011     
// Eclipse Public License (EPL)
//
// ================================================================
//
// end_generated_IBM_copyright_prolog

/*--------------------------------------------------------------------*/
/*  Includes                              */
/*--------------------------------------------------------------------*/

#include <RmcNotifier.h>
#include <TealException.h>
#include <Logging.h>
#include <sstream>
#include <cstdlib>
#include <cerrno>
#include <cstring>
#include <ctime>
#include <stdio.h>
#include <sys/wait.h>
#include <limits.h>
using namespace TEAL;

/*--------------------------------------------------------------------*/
/*  User Types                            */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Constants                             */
/*--------------------------------------------------------------------*/

const unsigned int MAX_RETRY = 3;

/*--------------------------------------------------------------------*/
/*  Macros                                */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Internal Function Prototypes                      */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Global Variables                          */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/* >>> Function <<<                           */
/*--------------------------------------------------------------------*/

RmcNotifier::RmcNotifier(const char* sensorName) : Notifier()
{
    sprintf(ivCommand,"/usr/bin/refsensor %s Uint32=",sensorName);
    std::srand(std::time(0));
    //Need to set this so calls to RMC will work correctly
    putenv("CT_MANAGEMENT_SCOPE=1");
}

/*--------------------------------------------------------------------*/

RmcNotifier::~RmcNotifier()
{
}

/*--------------------------------------------------------------------*/

void RmcNotifier::post()
{
    unsigned int retry = 0;

    while (1) {
        char cmd[128];
        sprintf(cmd,"%s%d",ivCommand,std::rand());

        int rc = 0;
        FILE* out = popen(cmd,"r");
        if (out) {
            char buf[1024];
            while (fgets(buf, sizeof(buf), out) != NULL)
                TEAL::getLog().Print(TEAL::TEAL_LOG_DEBUG, "RMC_NOTIF", buf, __FILE__, __LINE__);
            rc = pclose(out);
        } else {
            rc = -1;
        }

        if (rc == -1)
        {
            throw TealException(std::strerror(errno));
            return;
        }

        int status = WEXITSTATUS(rc);

        switch(status) {
            case 0: // The command has run successfully.
            case 4: // The sensor is not monitored and cannot be refreshed
                return;
            case 1: // An incorrect combination of flags and parameters has been entered
                if (retry < MAX_RETRY) {
                    ++retry;
                    break; // retry the operation
                } else {
                    // Fall through and report the error
                }
            default:
                std::ostringstream msg;
                msg << "\"" << cmd << "\"" << " failed. rc = " << status;
                throw TealException(msg.str());
        }
    }
}
