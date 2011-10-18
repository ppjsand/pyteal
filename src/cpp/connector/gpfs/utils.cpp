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
#include "utils.h"
#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include "tlgpfs_error.h"
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <iostream>
#include "Log.h"
#include "commandlistener.h"
#include "configuration.h"


void Utils::sig_term(int sig)
{
    log_info("Exiting....");
    if (sig == SIGTERM || sig == SIGKILL || sig == SIGINT) {
        unlink(PID_FILE);
        unlink(GPFS_SOCK_FILE);
        exit(TL_SUCCESS);
    }
    exit(TL_SUCCESS);
}

TLGPFS_ERR_T Utils::checkRoot()
{
    if (getuid() != 0) {
        log_error("Must running as root!");
        cerr<<"Must running as root!"<<endl;
        return TL_ERR_INVALID_USER;
    }
    return TL_SUCCESS;
}
TLGPFS_ERR_T Utils::checkGpfsDaemon()
{
    if(access(GPFS_DAEMON_FILE,0)!=0)
    {
        log_error("GPFS daemon maybe not running or not work well! Please restart that at first!");
        cerr<<"GPFS daemon maybe not running or not work well! Please restart that at first!"<<endl;
        return TL_ERR_GPFS_NOT_STARTED;
    }
    return TL_SUCCESS;

}

TLGPFS_ERR_T Utils::checkGpfsMon()
{
    if(access(PID_FILE,0)!=0)
    {
        log_error("tlgpfsmon daemon not running! Please start that at first!");
        cerr<<"tlgpfsmon daemon not running! Please start that at first!"<<endl;
        return TL_ERR_TLGPFS_NOT_STARTED;
    }
    return TL_SUCCESS;

}

TLGPFS_ERR_T Utils::checkMultiInstance() 
{
    int checkfile;
    char str[30] = {0};
    if(access(PID_FILE,0)==0)
    {
        log_error("Another instance is running or last launch not exit cleanly, remove /tmp/tlgpfsmon.pid to force the launch continue.");
        cerr<<"Another instance is running or last launch not exit cleanly, remove /tmp/tlgpfsmon.pid to force the launch continue."<<endl;
        return TL_ERR_MULTI_INSTANCE;
    }

    checkfile = open(PID_FILE,O_RDWR|O_CREAT,0640);
    if(checkfile < 0)
    {
        log_error("open tlgpfsmon check file failed!");
        cerr<<"open tlgpfsmon check file failed!"<<endl;
        return TL_ERR_FILE_CREATION;
    }
    sprintf(str,"%d\n",getpid());
    write(checkfile,str,strlen(str));
    close(checkfile);
    return TL_SUCCESS;
}

void Utils::ProcessSig()
{
    struct sigaction oldsa, sa;
    sigaction(SIGCHLD, NULL, &oldsa);
    
    sa.sa_handler = SIG_IGN;
    sa.sa_flags = 0;
    sigemptyset(&sa.sa_mask);
    sigaction(SIGHUP, &sa, NULL);
    sigaction(SIGPIPE, &sa, NULL);
    sigaction(SIGUSR1, &sa, NULL);
    sigaction(SIGUSR2, &sa, NULL);
    //sigaction(SIGCHLD, &sa, NULL);        
    sa.sa_handler = sig_term;
    sigaction(SIGTERM, &sa, NULL);
    sigaction(SIGKILL, &sa, NULL);
    sigaction(SIGINT, &sa, NULL);

}

TLGPFS_ERR_T Utils::Daemonize()
{
    int i;
    int pid;
    int status;
    ProcessSig();    
    pid = fork();
    if (pid > 0) {
        sleep(1); // sleep here to get child process status if it exits for some reason
        waitpid(-1,&status,WNOHANG);
        exit(status>>8); 
    } else if (pid < 0) {
        log_error("First fork failed");
        return TL_ERR_FORK_FAILED;
    }

    setsid();    
    if (signal(SIGHUP, SIG_IGN) == SIG_ERR) {
        log_error("Signal call to avoid control term failed");
        return TL_ERR_SIGNAL_FAILED;
    }
    umask(0);

    chdir("/");  
 //   for (i=0; i < MAXFD; i++) {
    for (i=0; i < 3; i++) {//reserve log fd.
        close(i);
    }
    open("/dev/null", O_RDONLY);
    open("/dev/null", O_RDWR);
    open("/dev/null", O_RDWR);
    
    return TL_SUCCESS;    
}

TLGPFS_ERR_T Utils::init()
{
    TLGPFS_ERR_T ret = TL_SUCCESS;

    if((ret = checkRoot()) != TL_SUCCESS)
        return ret;

    if((ret = checkGpfsDaemon()) != TL_SUCCESS)
        return ret;

    if(Configuration::getInstance().asDaemon())
    {
        if((ret = Daemonize()) != TL_SUCCESS)
            return ret;
    }
    else
    {
        ProcessSig();
    }
    ret = checkMultiInstance();
    
    return ret;
}

void Utils::get_time_stamp(struct timeval* in,char* out)
{
    if(out == NULL || in == NULL)
        return;
    struct tm * stm = NULL;
    stm = localtime(&in->tv_sec);
    sprintf(out,"%d-%d-%d %d:%02d:%02d",stm->tm_year+1900,stm->tm_mon+1,stm->tm_mday,stm->tm_hour,stm->tm_min,stm->tm_sec);
    return;

}

void Utils::timeval_to_char(struct timeval* in,char* out)
{
    if(out == NULL || in == NULL)
        return;
    struct tm * stm = NULL;
    stm = localtime(&in->tv_sec);
    sprintf(out,"%d.%d",in->tv_sec,in->tv_usec);
    return;

}

char* Utils::int_to_char(char* out, int size, unsigned int* in)
{
    if(out == NULL)
        return NULL;
    memset(out,0,size);
    sprintf(out,"%d",*in);
    return out;
}

