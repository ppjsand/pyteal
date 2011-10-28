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
#include "configuration.h"
#include "Log.h"
#include "utils.h"
#include "tlgpfs_error.h"
#include "teal_error.h"
#include "commandlistener.h"
#include "GPFSConfigHandler.h"
#include "GPFSEventHandler.h"

using namespace std;
int main(int argc, char *argv[])
{
    TLGPFS_ERR_T ret = TL_SUCCESS;
    TEAL_ERR_T rc = TEAL_SUCCESS;
    if(argc == 1)
    {
        cerr<< "You should specify at least one option!" <<endl;
    }
    if(!Configuration::getInstance().init(argc, argv))
    {
        cerr<< "Failed to initialize configuration!" <<endl;
        return TL_ERR_CONFIGRATION_FAILED;
    }
    
    if((ret = Utils::init())!= TL_SUCCESS)
    {
        log_error("Failed to initialize!");
        return ret;
    }
    
    log_info("Start to initialize server!");

    if(Configuration::getInstance().isPoll())
    {
        if((ret = GPFSConfigHandler::getConfigHandler()->start()) != TL_SUCCESS )
        {
            char rc[10]; 
            string msg = "GPFSConfigHandler start failed with ";
            msg += Utils::int_to_char(rc,10,(unsigned int*)&ret); 
            log_error(msg);
            return ret;
        }
    }
    if(Configuration::getInstance().isEvent())
    {
        if((ret = GPFSEventHandler::getEventHandler()->start()) != TL_SUCCESS )
        {
            char rc[10];
            string msg = "GPFSEventHandler start failed with "; 
            msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
            log_error(msg);
            return ret;
        }
    }
    if((ret = CommandListener::init()) != TL_SUCCESS)
    {
        char rc[10];
        string msg = "CommandListener init failed with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        return ret;
    }
    if(Configuration::getInstance().isPoll())
    {
        if((ret = GPFSConfigHandler::getConfigHandler()->join()) != TL_SUCCESS)
        {
            char rc[10];
            string msg = "GPFSConfigHandler::join failed with  ";
            msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
            log_error(msg);
            return ret;
        }
    }
    if(Configuration::getInstance().isEvent())
    {
        if((ret = GPFSEventHandler::getEventHandler()->join()) != TL_SUCCESS)
        {
            char rc[10];
            string msg = "GPFSEventHandler::join failed with  ";
            msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
            log_error(msg);
            return ret;
        }
    }
    return 0;
}

