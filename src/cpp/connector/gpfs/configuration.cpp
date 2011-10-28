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
Configuration Configuration::instance;
bool Configuration::init(int argc, char *argv[])
{
    if (!processCommandLineOptions(argc, argv))
    {
        return false;
    }
    return true;
}

Configuration& Configuration::getInstance()
{
    return instance;
}
bool Configuration::asDaemon()
{
    return as_daemon;
}
Configuration::Configuration()
{

}
void Configuration::usage(const std::string &processName)
{
  std::cerr<<"Usage: "<< processName<<"[{options}]"                                                                    <<std::endl;
  std::cerr<<"  [options] can be any of"                                                                               <<std::endl;
  std::cerr<<"    -p              - enable polling"                                                                    <<std::endl;
  std::cerr<<"    -e              - enable events"                                                                     <<std::endl;
  std::cerr<<"    -d              - run as a daemon"                                                                   <<std::endl;
  std::cerr<<"    -i <interval>   - polling interval, 86400 seconds by default"                                        <<std::endl;
  std::cerr<<"    -c <conf path>  - path for configuration file, /opt/teal/data/ibm/gpfs/tlgpfsmon.conf by default"    <<std::endl;
  std::cerr<<"    -h              - print this message"                                                                <<std::endl;
}
bool Configuration::isPoll()
{
    return enable_poll;
}
bool Configuration::isEvent()
{
    return enable_event;
}
int Configuration::getInterval()
{
    return poll_interval;
}

string& Configuration::getConfPath()
{
    return confPath;
}

bool Configuration::processCommandLineOptions(int argc, char *argv[])
{
    int op;
    int interval = 0;
    poll_interval = DEFAULT_POLL_INTERVAL;    
    while ( (op = getopt(argc, argv, "pedhi:c:")) != -1 ) {
        switch (op) {
            case 'p':
                enable_poll = true;
                break;
                
            case 'e':
                enable_event = true;
                break;
                
            case 'd':
                as_daemon = true;
                break;
                
            case 'i':
                interval = strtol(optarg, NULL, 0);
                poll_interval = interval;
                break;

            case 'c':
                confPath = optarg;
                break;

            case 'h':
                usage(argv[0]);
                exit(0);

            default:
                usage(argv[0]);
                exit(1);
        }
    }
    if (enable_event == false && enable_poll == false)
    {
        std::cerr<<"You must specify at least -e or -p option"<<std::endl;
        usage(argv[0]);
        exit(1);
    }   
    if (interval == poll_interval && enable_poll == false)
    {
        std::cerr<<"You must use -i option together with -p option"<<std::endl;
        usage(argv[0]);
        exit(1);
    }   

    if(confPath.empty())
    {
        confPath = "/opt/teal/data/ibm/gpfs/tlgpfsmon.conf"; // use sample by default   
    }
    if(access(confPath.c_str(),0)!=0)
    {
        cerr<<confPath<<" doesn't exist, can't read default configuration!"<<endl;
        return false;
    }
    return true;   
}
