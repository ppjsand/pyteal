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
#include "commandlistener.h"
#include "tlgpfs_command_api.h"
#include <errno.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <sys/stat.h>   
#include <fcntl.h>
#include <unistd.h>
#include <iostream>
using namespace std;
TLGPFS_ERR_T Commandapi::tlgpfs_command_open(int* fd)
{
    struct sockaddr_un un;
    if ((*fd = socket(AF_UNIX, SOCK_STREAM, 0)) < 0)
    {
        cerr<<"open socket failed!"<<endl;
        return TL_ERR_SOCKET_OPEN;
    }
    memset(&un, 0, sizeof(un));
    un.sun_family = AF_UNIX;
    strcpy(un.sun_path, GPFS_SOCK_FILE);
    memset(&un, 0, sizeof(un));
    un.sun_family = AF_UNIX;
    strcpy(un.sun_path, GPFS_SOCK_FILE);
    if (connect(*fd, (struct sockaddr *)&un, sizeof(un)) < 0) 
    {
        cerr<<"connect failed!"<<endl;
        close(*fd);
        return TL_ERR_SOCKET_CONNECT;
    }
    return TL_SUCCESS;
}

TLGPFS_ERR_T Commandapi::tlgpfs_command_close(int fd)
{
    if( fd < 0 )
    {
        cerr<<"invalid socket fd!"<<endl;
        return TL_ERR_INVALID_SOCKET;
    }
    if(close(fd) < 0)
    {
        cerr<<"close socket failed!"<<endl;
        return TL_ERR_SOCKET_CLOSE;
    }
    return TL_SUCCESS;
}

TLGPFS_ERR_T Commandapi::tlgpfs_command_refresh(int fd)
{
    int rc = TL_SUCCESS;
    TLGPFS_ERR_T buf  = TL_SUCCESS;
    tlgpfs_command_t command = REFRESH;
    rc = write(fd,&command,sizeof(tlgpfs_command_t));
    if(rc < 0)
    {
        cerr<<"send refresh command error!"<<endl;
        return TL_ERR_SOCKET_WRITE;
    }
    rc = read(fd, &buf, sizeof(buf));
    if(rc < 0)
    {
        cerr<<"get result failed!"<<endl;
        return TL_ERR_SOCKET_READ;
    }
    if(buf == TL_SUCCESS)
    {
        cout<<"TEAL GPFS configuration refresh succeeded!"<<endl;
        return buf;
    }
    else
    {
        cerr<<"TEAL GPFS configuration refresh failed with %d!"<<endl;
        return buf;
    }
}


