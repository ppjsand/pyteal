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
#include "tlgpfs_command_api.h"
#include <stdio.h>
int main()
{
    int fd=0;
    TLGPFS_ERR_T rc;
    rc = Commandapi::tlgpfs_command_open(&fd);
    printf("open return %d\n",rc);
    rc = Commandapi::tlgpfs_command_refresh(fd);
    printf("echo return %d\n",rc);
    rc = Commandapi::tlgpfs_command_close(fd);
    printf("close return %d\n",rc);
}

