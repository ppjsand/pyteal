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
/*  Includes                                                          */
/*--------------------------------------------------------------------*/

#include <RmcNotifier.h>
#include <TealException.h>
#include <sstream>
#include <cstdlib>
#include <cerrno>
#include <cstring>
#include <sys/wait.h>
#include <limits.h>
using namespace TEAL;

/*--------------------------------------------------------------------*/
/*  User Types                                                        */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Constants                                                         */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Macros                                                            */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Internal Function Prototypes                                      */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Global Variables                                                  */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/* >>> Function <<<                                                   */
/*--------------------------------------------------------------------*/

RmcNotifier::RmcNotifier(const char* sensorName) : Notifier(), ivCount(1)
{
	std::ostringstream cmd;
	cmd << "/usr/bin/refsensor " << sensorName << " Uint32=";
	ivCommand = cmd.str();
}

/*--------------------------------------------------------------------*/

RmcNotifier::~RmcNotifier()
{
}

/*--------------------------------------------------------------------*/

void RmcNotifier::post()
{
	std::ostringstream cmd;
	cmd << ivCommand << ivCount;

    ivCount = (ivCount == UINT_MAX ? 1 : ivCount + 1);

	int rc = std::system(cmd.str().c_str());
	if (rc == -1) {
		throw TealException(std::strerror(errno));
	} else {
		 int status = WEXITSTATUS(rc);

		 // Only report an error if the command failed because the
		 // sensor was not being monitored
		 if ((status != 0) && (status != 4)) {
				std::ostringstream msg;
				msg << "\"" << cmd << "\"" << " failed. rc = " << status;
				throw TealException(msg.str());
		 }
	}
}

