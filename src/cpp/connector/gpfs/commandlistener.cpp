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
#include "GPFSConfigHandler.h"
#include <errno.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <sys/stat.h>   
#include <fcntl.h>
#include <strings.h>
#include <unistd.h>
#include "Log.h"

const int MAX_REQ = 256;

TLGPFS_ERR_T CommandListener::AcceptConnection(int sockfd)
{
    struct sockaddr_un  client_addr;
    socklen_t           client_len = sizeof(client_addr);
    int                 new_fd;
    int rc = 0;
    char buf[1024] = {0};
    TLGPFS_ERR_T ret = TL_SUCCESS;
    log_info("a new connection!");
    new_fd = accept(sockfd, (struct sockaddr *)&client_addr, &client_len);
    if(new_fd < 0)
    {
        log_error("accept failed!");
        close(new_fd);
        ret = TL_ERR_SOCKET_ACCPT;
        return ret;
    }
    tlgpfs_command_t command;
    rc = read(new_fd,&command,sizeof(tlgpfs_command_t));
    if(rc < 0)
    {
        log_error("read failed!");
        close(new_fd);
        ret = TL_ERR_SOCKET_READ;
        return ret;
    }
    //for refresh command
    if(command == REFRESH)
    {
        log_info("Got REFRESH command! Issue an on-demand refresh!");
        
        if(!GPFSConfigHandler::getConfigHandler()->getThread()->sendSignal())
        {
            log_error("send signal to polling thread failed!");
            close(new_fd);
            ret = TL_ERR_REFRESH_FAILED;
            return ret;
        }
        rc = write(new_fd,&ret,sizeof(ret));
        if(rc < 0)
        {
            log_error("read failed!");
            close(new_fd);
            ret = TL_ERR_SOCKET_READ;
            return ret;
        }

    }
    else
    {
        log_error("unsupported command!");
        close(new_fd);
        ret = TL_ERR_COMMAND_NOT_SUPPORT;
        return ret;
    }
    
    close(new_fd);
    return ret;
    
}

TLGPFS_ERR_T CommandListener::init()
{
    int rc = 0, sockfd, clifd;
    TLGPFS_ERR_T ret = TL_SUCCESS;
    struct sockaddr_un server_address;
    // Initialize the base socket
    sockfd = socket(AF_UNIX, SOCK_STREAM, 0);
    if(sockfd < 0 )
    {
        log_error("open socket failed!");
        ret = TL_ERR_SOCKET_OPEN;
        return ret;
    }
    unlink(GPFS_SOCK_FILE);
    bzero(&server_address, sizeof(server_address));
    server_address.sun_family = AF_UNIX;
    strcpy(server_address.sun_path, GPFS_SOCK_FILE);
    rc = bind(sockfd, (struct sockaddr *) &server_address, sizeof(server_address));
    if(rc < 0)
    {
        log_error("bind file failed!");
        close(sockfd);
        ret = TL_ERR_SOCKET_BIND;
        return ret;
    }
    rc = listen(sockfd, MAX_REQ); 
    if(rc < 0)
    {
        log_error("listen failed!");
        close(sockfd);
        ret = TL_ERR_SOCKET_LISTEN;
        return ret;
    }

    while(1)
    {
        fd_set  read_set;
        FD_ZERO(&read_set);
        FD_SET(sockfd, &read_set);
        rc = select(sockfd+1, &read_set, NULL, NULL, NULL);
        if( rc < 0 && errno == EINTR)
            continue;
        if(rc < 0)
        {
            log_error("select failed!");
            close(sockfd);
            ret = TL_ERR_SOCKET_SELECT;
            return ret;
        }
        if (FD_ISSET(sockfd, &read_set)) {
            if( (ret = AcceptConnection(sockfd))!= TL_SUCCESS)
            {
                log_error("accept connection failed!");
                return ret;
            }
        }
    }
    return ret;
}

