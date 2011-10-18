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
#ifndef _UTILS_H_
#define _UTILS_H_
#include "tlgpfs_error.h"

#define MAXFD 128
#define PID_FILE         "/tmp/tlgpfsmon.pid"
#define GPFS_DAEMON_FILE "/var/mmfs/mmpmon/mmpmonSocket"

class Utils {
public:
    static TLGPFS_ERR_T init();//check and init when launch
    static TLGPFS_ERR_T checkGpfsMon();
    static void get_time_stamp(struct timeval* in,char* out);
    static void timeval_to_char(struct timeval* in,char* out);
    static char* int_to_char(char* out, int size, unsigned int* in);
private:
    static TLGPFS_ERR_T Daemonize();
    static void ProcessSig();
    static void sig_term(int);
    static TLGPFS_ERR_T checkMultiInstance();
    static TLGPFS_ERR_T checkRoot();
    static TLGPFS_ERR_T checkGpfsDaemon();
    
};
#endif 

