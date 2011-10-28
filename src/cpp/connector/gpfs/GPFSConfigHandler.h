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
#ifndef _GPFS_CONFIG_HANDLER_H
#define _GPFS_CONFIG_HANDLER_H
#include "GPFSHandler.h"
#include "DbInterface.h"
class GPFSConfigHandler:public GPFSHandler
{
public:
    static GPFSConfigHandler* getConfigHandler();
    
private:
    static GPFSConfigHandler* instance;
    GPFSConfigHandler();
    virtual ~GPFSConfigHandler();
    virtual void action(GPFSHandler* handle);
    static TEAL_ERR_T refreshNode(NodeInfo* nodeInfo, string& clusterId);
    static TEAL_ERR_T refreshStgPool(StoragePoolInfo* stgInfo, string& clusterId, string& fsName);
    static TEAL_ERR_T refreshFS(FilesystemInfo* fsInfo, string& clusterId);
    static TEAL_ERR_T refreshDisk(DiskInfo* diskInfo, string& clusterId);
    static TEAL_ERR_T refreshRg(gpfsRecoveryGroup* rgInfo, string& clusterId, bool allDAOK);
    static TEAL_ERR_T refreshDa(gpfsRecoveryGroupDeclusteredArray* daInfo, string& clusterId, string& rgName);
    static TEAL_ERR_T refreshPdisk(gpfsDeclusteredArrayPdisk* pdiskInfo, string& clusterId, string& rgName, string& daName);
    static TEAL_ERR_T refreshVdisk(gpfsDeclusteredArrayVdisk* vdiskInfo, string& clusterId, string& rgName, string& daName);
    static TEAL_ERR_T refreshFset(FileSet* fsetInfo, string& clusterId);
    static void task();
    static TEAL_ERR_T refreshCluster(ClusterInfo* clusterInfo, ClusterStatus* clusterStatus);
    TEAL::DbInterface* conn;
};

#endif
