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
#include "GPFSConfigHandler.h"
#include "configuration.h"
#include "Log.h"
#include "teal_gpfs_connect.h"
#include "utils.h"
#include "DbClusterInfo.h"
#include "DbNodeInfo.h"
#include "DbFsInfo.h"
#include "DbStgPoolInfo.h"
#include "DbDiskInfo.h"
#include "DbFsetInfo.h"
#include "DbDaInfo.h"
#include "DbRgInfo.h"
#include "DbPdiskInfo.h"
#include "DbVdiskInfo.h"

GPFSConfigHandler* GPFSConfigHandler::instance = NULL;

GPFSConfigHandler::GPFSConfigHandler():GPFSHandler()
{
    conn = NULL;
}

GPFSConfigHandler* GPFSConfigHandler::getConfigHandler()
{
    if(instance == NULL)
    {
        GPFSHandler::init(MGMT_SNMP,1,Configuration::getInstance().getInterval());
        instance = new GPFSConfigHandler();
    }
    return instance;
}


TEAL_ERR_T GPFSConfigHandler::refreshCluster(ClusterInfo* clusterInfo, ClusterStatus* clusterStatus)
{
    teal_connector_handle conn_handle = NULL;
    string msg;
    char rc[10];
    TEAL_ERR_T ret = TEAL_SUCCESS;
    if(clusterInfo == NULL)
    {
        log_error("Null cluster info, return!");
        ret = TEAL_ERR_ARG;
        return ret;
    }
    if(clusterStatus == NULL)
    {
        log_error("Null cluster status, return!");
        ret = TEAL_ERR_ARG;
        return ret;  
    }
    ret = teal_open_connector(&conn_handle,"GPFS","/tmp");
    if(ret != TEAL_SUCCESS)
    {
        msg = "open gpfs connector failed with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg); 
        return ret;
    }
    tlgpfs_cluster_info_t* cluster = TEAL::DbClusterInfo::extract(clusterInfo);
    if(cluster == NULL)
    {
        log_error("Null cluster extracted, return!");
        ret = TEAL_ERR_ARG;
        return ret;    
    }
    *cluster->health = clusterStatus->getQuorumAchieved(); //identify cluster status here, 0 for unhealthy, 1 for healthy
    ret = tlgpfs_update_cluster_info(conn_handle,cluster);
    if(ret != TEAL_SUCCESS)
    {
        msg = "update cluster info error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        teal_close_connector(conn_handle);
        return ret;
    }
    ret = teal_close_connector(conn_handle);
    if(ret != TEAL_SUCCESS)
    {
        msg = "close gpfs connector error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
    }

    return ret;

}
TEAL_ERR_T GPFSConfigHandler::refreshNode(NodeInfo* nodeInfo, string& clusterId)
{
    teal_connector_handle conn_handle = NULL;
    TEAL_ERR_T ret = TEAL_SUCCESS;
    string msg;
    char rc[10];
    if(nodeInfo == NULL)
    {
        log_error("Null node info, return!");
        ret = TEAL_ERR_ARG;
        return ret;
    }
    ret = teal_open_connector(&conn_handle,"GPFS","/tmp");
    if(ret != TEAL_SUCCESS)
    {
        msg = "open gpfs connector failed with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        return ret;
    }
    tlgpfs_node_info_t* node = TEAL::DbNodeInfo::extract(nodeInfo, clusterId);
    if(node == NULL)
    {
        log_error("Null node extracted, return!");
        ret = TEAL_ERR_ARG;
        return ret;    
    }
    ret = tlgpfs_update_node_info(conn_handle,node);
    if(ret != TEAL_SUCCESS)
    {
        msg = "update node info error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        teal_close_connector(conn_handle);
        return ret;
    }
    ret = teal_close_connector(conn_handle);
    if(ret != TEAL_SUCCESS)
    {
        msg = "close gpfs connector error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
    }
    return ret;

}


TEAL_ERR_T GPFSConfigHandler::refreshFS(FilesystemInfo* fsInfo, string& clusterId)
{
    teal_connector_handle conn_handle = NULL;
    TEAL_ERR_T ret = TEAL_SUCCESS;
    string msg;
    char rc[10];
    if(fsInfo == NULL)
    {
        log_error("Null fs info, return!");
        ret = TEAL_ERR_ARG;
        return ret;
    }

    ret = teal_open_connector(&conn_handle,"GPFS","/tmp");
    if(ret != TEAL_SUCCESS)
    {
        msg = "open gpfs connector failed with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        return ret;
    }
    tlgpfs_fs_info_t* fs = TEAL::DbFsInfo::extract(fsInfo, clusterId);
    if(fs == NULL)
    {
        log_error("Null fs extracted, return!");
        ret = TEAL_ERR_ARG;
        return ret;    
    }

    ret = tlgpfs_update_fs_info(conn_handle,fs);
    if(ret != TEAL_SUCCESS)
    {
        msg = "update fs info error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        teal_close_connector(conn_handle);
        return ret;
    }
    ret = teal_close_connector(conn_handle);
    if(ret != TEAL_SUCCESS)
    {
        msg = "close gpfs connector error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
    }

    return ret;
}

TEAL_ERR_T GPFSConfigHandler::refreshDisk(DiskInfo* diskInfo, string& clusterId)
{
    teal_connector_handle conn_handle = NULL;
    TEAL_ERR_T ret = TEAL_SUCCESS;
    string msg;
    char rc[10];
    if(diskInfo == NULL)
    {
        log_error("Null disk info, return!");
        ret = TEAL_ERR_ARG;
        return ret;
    }

    ret = teal_open_connector(&conn_handle,"GPFS","/tmp");
    if(ret != TEAL_SUCCESS)
    {
        msg = "open gpfs connector failed with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        return ret;
    }
    tlgpfs_disk_info_t* disk = TEAL::DbDiskInfo::extract(diskInfo, clusterId);
    if(disk == NULL)
    {
        log_error("Null disk extracted, return!");
        ret = TEAL_ERR_ARG;
        return ret;    
    }

    ret = tlgpfs_update_disk_info(conn_handle,disk);
    if(ret != TEAL_SUCCESS)
    {
        msg = "update disk info error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        teal_close_connector(conn_handle);
        return ret;
    }
    ret = teal_close_connector(conn_handle);
    if(ret != TEAL_SUCCESS)
    {
        msg = "close gpfs connector error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
    }
    return ret;
}

TEAL_ERR_T GPFSConfigHandler::refreshStgPool(StoragePoolInfo* stgInfo, string& clusterId, string& fsName)
{
    teal_connector_handle conn_handle = NULL;
    TEAL_ERR_T ret = TEAL_SUCCESS;
    string msg;
    char rc[10];
    if(stgInfo == NULL)
    {
        log_error("Null storage pool info, return!");
        ret = TEAL_ERR_ARG;
        return ret;
    }

    ret = teal_open_connector(&conn_handle,"GPFS","/tmp");
    if(ret != TEAL_SUCCESS)
    {
        msg = "open gpfs connector failed with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        return ret;
    }
    tlgpfs_stg_info_t* stg = TEAL::DbStgPoolInfo::extract(stgInfo, clusterId, fsName);
    if(stg == NULL)
    {
        log_error("Null stg pool extracted, return!");
        ret = TEAL_ERR_ARG;
        return ret;    
    }

    ret = tlgpfs_update_stg_info(conn_handle,stg);
    if(ret != TEAL_SUCCESS)
    {
        msg = "update storage pool info error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);

        teal_close_connector(conn_handle);
        return ret;
    }
    ret = teal_close_connector(conn_handle);
    if(ret != TEAL_SUCCESS)
    {
        msg = "close gpfs connector error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
    }
    return ret;

}

TEAL_ERR_T GPFSConfigHandler::refreshFset(FileSet* fsetInfo, string& clusterId)
{
    teal_connector_handle conn_handle = NULL;
    TEAL_ERR_T ret = TEAL_SUCCESS;
    string msg;
    char rc[10];
    if(fsetInfo == NULL)
    {
        log_error("Null file set info, return!");
        ret = TEAL_ERR_ARG;
        return ret;
    }

    ret = teal_open_connector(&conn_handle,"GPFS","/tmp");
    if(ret != TEAL_SUCCESS)
    {
        msg = "open gpfs connector failed with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        return ret;
    }
    tlgpfs_fset_info_t* fset = TEAL::DbFsetInfo::extract(fsetInfo, clusterId);
    if(fset == NULL)
    {
        log_error("Null fset extracted, return!");
        ret = TEAL_ERR_ARG;
        return ret;    
    }

    ret = tlgpfs_update_fset_info(conn_handle,fset);
    if(ret != TEAL_SUCCESS)
    {
        msg = "update file set info error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        teal_close_connector(conn_handle);
        return ret;
    }
    ret = teal_close_connector(conn_handle);
    if(ret != TEAL_SUCCESS)
    {
        msg = "close gpfs connector error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
    }

    return ret;

}

TEAL_ERR_T GPFSConfigHandler::refreshRg(gpfsRecoveryGroup* rgInfo, string& clusterId, bool allDAOK)
{
    teal_connector_handle conn_handle = NULL;
    TEAL_ERR_T ret = TEAL_SUCCESS;
    string msg;
    char rc[10];
    if(rgInfo == NULL)
    {
        log_error("Null recovery group info, return!");
        ret = TEAL_ERR_ARG;
        return ret;
    }

    ret = teal_open_connector(&conn_handle,"GPFS","/tmp");
    if(ret != TEAL_SUCCESS)
    {
        msg = "open gpfs connector failed with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        return ret;
    }
    tlgpfs_rg_info_t* rg = TEAL::DbRgInfo::extract(rgInfo, clusterId);
    if(rg == NULL)
    {
        log_error("Null rg extracted, return!");
        ret = TEAL_ERR_ARG;
        return ret;    
    }
    //update rg status here due to convenience
    //if rg has an active server AND all of its member declustered arrays are healthy, it's healthy
    if((rg->rg_act_svr && strlen(rg->rg_act_svr)) && allDAOK)
        *rg->health = 0;
    else
        *rg->health = 1;

    ret = tlgpfs_update_rg_info(conn_handle,rg);
    if(ret != TEAL_SUCCESS)
    {
        msg = "update recovery group info error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        teal_close_connector(conn_handle);
        return ret;
    }
    ret = teal_close_connector(conn_handle);
    if(ret != TEAL_SUCCESS)
    {
        msg = "close gpfs connector error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
    }
    return ret;

}

TEAL_ERR_T GPFSConfigHandler::refreshDa(gpfsRecoveryGroupDeclusteredArray* daInfo, string& clusterId, string& rgName)
{
    teal_connector_handle conn_handle = NULL;
    TEAL_ERR_T ret = TEAL_SUCCESS;
    string msg;
    char rc[10];
    if(daInfo == NULL)
    {
        log_error("Null declustered array info, return!");
        ret = TEAL_ERR_ARG;
        return ret;
    }

    ret = teal_open_connector(&conn_handle,"GPFS","/tmp");
    if(ret != TEAL_SUCCESS)
    {
        msg = "open gpfs connector failed with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        return ret;
    }
    tlgpfs_da_info_t* da = TEAL::DbDaInfo::extract(daInfo, clusterId, rgName);
    if(da == NULL)
    {
        log_error("Null da extracted, return!");
        ret = TEAL_ERR_ARG;
        return ret;    
    }

    ret = tlgpfs_update_da_info(conn_handle,da);
    if(ret != TEAL_SUCCESS)
    {
        msg = "update declustered array info error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        teal_close_connector(conn_handle);
        return ret;
    }
    ret = teal_close_connector(conn_handle);
    if(ret != TEAL_SUCCESS)
    {
        msg = "close gpfs connector error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
    }

    return ret;

}

TEAL_ERR_T GPFSConfigHandler::refreshPdisk(gpfsDeclusteredArrayPdisk* pdiskInfo, string& clusterId, string& rgName, string& daName)
{
    teal_connector_handle conn_handle = NULL;
    TEAL_ERR_T ret = TEAL_SUCCESS;
    string msg;
    char rc[10];
    if(pdiskInfo == NULL)
    {
        log_error("Null pdisk info, return!");
        ret = TEAL_ERR_ARG;
        return ret;
    }

    ret = teal_open_connector(&conn_handle,"GPFS","/tmp");
    if(ret != TEAL_SUCCESS)
    {
        msg = "open gpfs connector failed with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        return ret;
    }
    tlgpfs_pdisk_info_t* pdisk = TEAL::DbPdiskInfo::extract(pdiskInfo, clusterId, rgName, daName);
    if(pdisk == NULL)
    {
        log_error("Null pdisk extracted, return!");
        ret = TEAL_ERR_ARG;
        return ret;    
    }

    ret = tlgpfs_update_pdisk_info(conn_handle,pdisk);
    if(ret != TEAL_SUCCESS)
    {
        msg = "update pdisk info error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        teal_close_connector(conn_handle);
        return ret;
    }
    ret = teal_close_connector(conn_handle);
    if(ret != TEAL_SUCCESS)
    {
        msg = "close gpfs connector error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
    }
    return ret;

}

TEAL_ERR_T GPFSConfigHandler::refreshVdisk(gpfsDeclusteredArrayVdisk* vdiskInfo, string& clusterId, string& rgName, string& daName)
{
    teal_connector_handle conn_handle = NULL;
    TEAL_ERR_T ret = TEAL_SUCCESS;
    string msg;
    char rc[10];
    if(vdiskInfo == NULL)
    {
        log_error("Null vdisk info, return!");
        ret = TEAL_ERR_ARG;
        return ret;
    }

    ret = teal_open_connector(&conn_handle,"GPFS","/tmp");
    if(ret != TEAL_SUCCESS)
    {
        msg = "open gpfs connector failed with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        return ret;
    }
    tlgpfs_vdisk_info_t* vdisk = TEAL::DbVdiskInfo::extract(vdiskInfo, clusterId, rgName, daName);
    if(vdisk == NULL)
    {
        log_error("Null vdisk extracted, return!");
        ret = TEAL_ERR_ARG;
        return ret;    
    }

    ret = tlgpfs_update_vdisk_info(conn_handle,vdisk);
    if(ret != TEAL_SUCCESS)
    {
        msg = "update vdisk info error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
        teal_close_connector(conn_handle);
        return ret;
    }
    ret = teal_close_connector(conn_handle);
    if(ret != TEAL_SUCCESS)
    {
        msg = "close gpfs connector error with ";
        msg += Utils::int_to_char(rc,10,(unsigned int*)&ret);
        log_error(msg);
    }

    return ret;

}

void GPFSConfigHandler::task()
{
    int nFSs   = 0;
    int nPools = 0;
    int nDisks = 0;
    int nFsets = 0;
    int nNodes = 0;

    TEAL_ERR_T ret;
    string msg;
    char tmp[10];
    string fsName;
    string stgName;
    string diskName;
    string fsetName;
    string nodeName;
    string clusterName;

    FilesystemInfo* fsInfo       = NULL;
    StoragePoolInfo* stgInfo     = NULL;
    DiskInfo* diskInfo           = NULL;
    FileSet* fsetInfo            = NULL;
    FileSet* fileSetList         = NULL;
	
    MErrno err = M_OK;
    log_info("########################Launch GPFSConfigHandler#########################################");    
    err = GPFSHandler::getPollHandler()->getDaemonState();
    if(err != M_OK)
    {
        msg = "daemon is down on local node ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
        log_error(msg);
        return;
    }

    err = GPFSHandler::getPollHandler()->refreshClusterRecipe();
    if(err != M_OK)
    {
        msg = "refresh cluster failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
        log_error(msg);
        return;
    }
    ClusterInfo* clusterInfo = new ClusterInfo(&err);
    //update cluster info
    err = GPFSHandler::getPollHandler()->updateClusterInfo(clusterInfo);
    if(err != M_OK)
    {
        msg = "update cluster info failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
        log_error(msg);
        return;
    } 
    
    //update all nodes info
    err = GPFSHandler::getPollHandler()->updateNodeInfo(clusterInfo);
    if(err != M_OK)
    {
        msg = "update node failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
        log_error(msg);
        return;
    }        
    err = GPFSHandler::getPollHandler()->getClusterInfo(clusterInfo); //this maybe not needed
    if(err != M_OK)
    {
        msg = "get cluster info failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
        log_error(msg);
        return;
    }     
    err = GPFSHandler::getPollHandler()->updateDiskSDRInfo();
    if(err != M_OK)
    {
        msg = "update disk SDR info failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
        log_error(msg);
        return;
    }
    err = GPFSHandler::getPollHandler()->updateFilesystemInfo(clusterInfo, 1);// to get perfermance statics even if not used.
    if(err != M_OK)
    {
        msg = "update file system failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
        log_error(msg);
        return;
    }    

    err = GPFSHandler::getPollHandler()->updateMountedNodeInfo(clusterInfo); // to get mounted node info
    if(err != M_OK)
    {
        msg = "update mounted node info failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
        log_error(msg);
        return;
    } 
    err = GPFSHandler::getPollHandler()->updateVfsStatsInfo(clusterInfo); // to get vfs info
    if(err != M_OK)
    {
        msg = "update vfs info failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
        log_error(msg);
        return;
    } 
    err = GPFSHandler::getPollHandler()->updateThreadUtilInfo(clusterInfo); // to get thread util info
    if(err != M_OK)
    {
        msg = "update thread util info failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
        log_error(msg);
        return;
    }      
    err = GPFSHandler::getPollHandler()->updateIocStatsInfo(clusterInfo); // to get ioc statics info
    if(err != M_OK)
    {
        msg = "update ioc statics info failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
        log_error(msg);
        return;
    }      
    err = GPFSHandler::getPollHandler()->updateCacheStatsInfo(clusterInfo); // to get cache statics info
    if(err != M_OK)
    {
        msg = "update cache statics info failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
        log_error(msg);
        return;
    }  
     err = GPFSHandler::getPollHandler()->updatePCacheStatsInfo(clusterInfo); // to get pcache statics info
    if(err != M_OK)
    {
        msg = "update pcache statics info failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
        log_error(msg);
        return;
    } 
    err = GPFSHandler::getPollHandler()->updateFilesystemManagerInfo(clusterInfo);// update fs manager
    if(err != M_OK)
    {
        msg = "update file system manager failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
        log_error(msg);
        return;
    }    
    err = GPFSHandler::getPollHandler()->updatePolicyInfo(clusterInfo); // to get policy info
    if(err != M_OK)
    {
        msg = "update policy info failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
        log_error(msg);
        return;
    } 
    err = GPFSHandler::getPollHandler()->updateFilesystemConfigInfo(clusterInfo);// update fs config
    if(err != M_OK)
    {
        msg = "update file system config failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
        log_error(msg);
        return;
    }   
   
    ClusterStatus* clusterStatus = new ClusterStatus();
    err = GPFSHandler::getPollHandler()->getClusterStatus(clusterStatus); 
    if(err != M_OK)
    {
        msg = "get cluster status failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
        log_error(msg);
    } 
    
    clusterName = clusterInfo->getName();
    msg = "Refresh cluster: ";
    msg += clusterName;
    log_info(msg);

    ret = refreshCluster(clusterInfo,clusterStatus);
    if(ret != TEAL_SUCCESS)
    {
        msg = "Refresh cluster failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
        log_error(msg);
    }
    int i = 0;
    string clusterid = clusterInfo->getId();
    nFSs = clusterInfo->getNumFilesystems();
    //log fs one by one
    for( i = 0 ; i < nFSs; i++)
    {
        fsInfo = clusterInfo->getFilesystem(i);
           
        if (fsInfo == NULL)
        {
            msg = "NULL filesystem ";
            msg += Utils::int_to_char(tmp,10,(unsigned int*)&i);
            log_error(msg);
            continue;
        }
        fsName = fsInfo->getName(); 
        err = GPFSHandler::getPollHandler()->updateStoragePoolInfo(clusterInfo, (char*)fsName.c_str());
        if(err != M_OK)
        {
            msg  = "update storage pool info for file system: ";
            msg += fsName;
            msg += " failed with ";
            msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
            log_error(msg);
            continue;
        }  
        msg = "Refresh file system: ";
        msg += fsName;
        log_info(msg);
        ret = refreshFS(fsInfo, clusterid);
        if(ret != TEAL_SUCCESS)
        {
            msg  = "Refresh file system: ";
            msg += fsName;
            msg += " failed with ";
            msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
            log_error(msg);
        }  
          
        nPools = fsInfo->getNumStoragePools();
        int j = 0;   
        //log stg one by one
        for(; j < nPools; j++ )
        {         
            stgInfo = fsInfo->getStoragePool(j);
            if(stgInfo == NULL)
            {
                msg  = "ERR stgInfo for storage pool: ";
                msg += Utils::int_to_char(tmp,10,(unsigned int*)&i);
                msg += " in (fs: ";
                msg += fsName;
                msg += ") is NULL";
                log_error(msg);
                continue;
            }
            stgName = stgInfo->getName();
            err = GPFSHandler::getPollHandler()->updateDiskInfo(clusterInfo, (char*)fsName.c_str(), (char*)stgName.c_str(),1);
            if(err != M_OK)
            {
                msg  = "update disk info in (file system: ";
                msg += fsName;
                msg += ", storage pool: ";
                msg += stgName;
                msg += ") failed with ";
                msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
                log_error(msg);
                continue;
            }  
            msg  = "Refresh storage pool: ";
            msg += stgName;
            msg += " in (fs: ";
            msg += fsName;
            msg += ")";
            log_info(msg); 
            ret = refreshStgPool(stgInfo, clusterid, fsName);
            if(ret != TEAL_SUCCESS)
            {
                msg  = "Refresh storage pool: ";
                msg += stgName;
                msg += " in (fs: ";
                msg += fsName;
                msg += ") failed with ";
                msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
                log_error(msg);
            }  

            int k = 0;
            nDisks = stgInfo->getNumDisks();
            //log disk one by one        
            for(; k < nDisks ; k++ )
            {
                diskInfo = stgInfo->getDisk(k);
                if(diskInfo == NULL)
                {
                    msg  = "diskInfo for disk: ";
                    msg += Utils::int_to_char(tmp,10,(unsigned int*)&i);
                    msg += " in (storage pool: ";
                    msg += stgName;
                    msg += ", fs: ";
                    msg += fsName;
                    msg += ") is NULL";
                    log_error(msg);
                    continue;
                }
                diskName = diskInfo->getName();
                msg  = "Refresh disk: ";
                msg += diskName;
                msg += " in (storage pool: ";
                msg += stgName;
                msg += ", fs: ";
                msg += fsName;
                msg += ")";
                log_info(msg);
                ret = refreshDisk(diskInfo, clusterid);
                if(ret != TEAL_SUCCESS)
                {
                    msg  = "Refresh disk: ";
                    msg += diskName;
                    msg += " in (storage pool: ";
                    msg += stgName;
                    msg += ", fs: ";
                    msg += fsName;
                    msg += ") failed with ";
                    msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
                    log_error(msg);
                }   
            }
        }
        
        //err = GPFSHandler::getPollHandler()->getFileSets((char*)fsName.c_str(), &fileSetList); //core dump in GPFS 3.4, only effective in 3.5
        err = GPFSHandler::getPollHandler()->getFileSets1((char*)fsName.c_str(), fileSetList, &nFsets);
/*
              if(err != M_OK)
              {
                  msg  = "update fileset info in (fs: ";
                  msg += fsName;
                  msg += ") failed with ";
                  msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
                  log_error(msg);
                  nFsets = 0;
                  fileSetList = NULL;
                  continue;  
              } //at first time to get nFsets but will not return M_OK
       */
        if(nFsets <= 0)
        {
            msg  = "no fileset found in (fs: ";
            msg += fsName;
            msg += ")";
            log_error(msg);
            nFsets = 0;
            fileSetList = NULL;
            continue;  
        }
        fileSetList = new FileSet[nFsets];

        err = GPFSHandler::getPollHandler()->getFileSets1((char*)fsName.c_str(), fileSetList, &nFsets);
  	    if(err != M_OK)
  	    {
  		    msg  = "update fileset info in (fs: ";
  		    msg += fsName;
  		    msg += ") failed with ";
  		    msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
  		    log_error(msg);
                    nFsets = 0;
                    fileSetList = NULL;
  		    continue;  
  	    } 

        int l = 0;
        
        //log fileset one by one
        for(; l < nFsets; l++ )
        {         
            fsetInfo = &fileSetList[l];
            if(fsetInfo == NULL)
            {
                msg  = "fsetInfo for fset: ";
                msg += Utils::int_to_char(tmp,10,(unsigned int*)&i);
                msg += " in (fs: ";
                msg += fsName;
                msg += ") is NULL";
                log_error(msg);
                continue;
            }
            fsetName = fsetInfo->getName();
            msg  = "Refresh fileset: ";
            msg += fsetName;
            msg += " in (fs: ";
            msg += fsName;
            msg += ")";
            log_info(msg);
            ret = refreshFset(fsetInfo, clusterid);
            if(ret != TEAL_SUCCESS)
            {
                msg  = "Refresh file set: ";
                msg += fsetName;
                msg += " in (fs: ";
                msg += fsName;
                msg += ") failed with";
                msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
                log_error(msg);
            }  
        }
		if(fileSetList) 
		{
			delete []fileSetList;
			fileSetList = NULL;
			nFsets = 0;
			fsetInfo = NULL;
		}  
    }    
    
    nNodes = clusterInfo->getNumNodes();
    // to get disk access info, place this here to update num_access_disk in nodeinfo and need to invoke updateStoragePool() prior to this API
    err = GPFSHandler::getPollHandler()->updateDiskAccessInfo(clusterInfo); 
    if(err != M_OK)
    {
        msg = "update disk access info failed with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&err);
        log_error(msg);
        return;
    }

    NodeInfo* nodeInfo = NULL;
    //log node one by one
    for( i = 0 ; i < nNodes; i++)
    {        
        nodeInfo = clusterInfo->getNode(i);
            
        if (nodeInfo == NULL)
        {
            msg = "nodeInfo for node ";
            msg += Utils::int_to_char(tmp,10,(unsigned int*)&i);
            msg += "is NULL";
            log_error(msg);
            continue;
        }
        nodeName = nodeInfo->getName();
        msg = "Refresh node: ";
        msg += nodeName;
        log_info(msg);
        ret = refreshNode(nodeInfo, clusterid);
        if(ret != TEAL_SUCCESS)
        {
            msg = "Refresh node: ";
            msg += nodeName;
            msg += " failed with ";
            msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
            log_error(msg);
            continue;
        }         
    }

    log_info("##################Start to refresh perseus configuration###################");

    int nRgAllocated = 1; /* number of rg slots allocated in the buffer */
    char *bufP       = NULL;
    int bufLen       = 0;
    int rc           = 0;
    int nPdisk       = 0;
    int nVdisk       = 0;
    int nRg          = 0;
    int nDa          = 0;
    string pdiskName;
    string vdiskName;
    string rgName;
    string daName;
    
    gpfsRecoveryGroupSdrInfo *rgSdrTableP  = NULL;
    gpfsRecoveryGroupSdrInfo *rgSdrP       = NULL;    
    gpfsRecoveryGroup *rgTableP            = NULL;
    gpfsRecoveryGroup *rgP                 = NULL;
    gpfsRecoveryGroupDeclusteredArray* daP = NULL;        
    gpfsDeclusteredArrayPdisk* pdiskP      = NULL;
    gpfsDeclusteredArrayVdisk* vdiskP      = NULL;
    
    rgSdrTableP = new gpfsRecoveryGroupSdrInfo[nRgAllocated];
    nRg = nRgAllocated;

    /* get initial info from SDR (all RG names) */
    rc = getNsdRAIDSdrInfo(rgSdrTableP, &nRg);
    if (rc == 0)
    {
        if (nRg >= 1)
        {
            rgTableP = new gpfsRecoveryGroup[nRg];
        
            if (rgTableP == NULL)
            {
                msg = "Initial RG table failed with ";
                msg += Utils::int_to_char(tmp,10,(unsigned int*)&rc);
                log_error(msg);
                return;
            }
            for (i = 0, rgSdrP = rgSdrTableP; i < nRg && i < nRgAllocated; i++, rgSdrP++)
            {
                rgP = rgTableP + i;
                
                rgP->updateRgSdrInfo(rgSdrP->getRecoveryGroupName(),rgSdrP->getRecoveryGroupServerList(),rgSdrP->getRecoveryGroupId());
        
                rc = getRecoveryGroupSummary(rgP);  //refresh rg info
                if (rc == 0)
                { 
                    rgName = rgP->getRecoveryGroupName();
                    
                    rc = getRecoveryGroupDeclusteredArrays(rgP); // refresh da info
                    if (rc == 0)
                    {                        
                        int l = 0;
                        int nDa = rgP->getRecoveryGroupDeclusterArrays();
                        bool allDaOK = true; // is all DA ok?
                        for(; l < nDa; l++)
                        {
                            daP = rgP->getDeclusteredArrayP(l);
                            if(daP == NULL)
                            {
                                msg = "da: ";
                                msg += Utils::int_to_char(tmp,10,(unsigned int*)&i);
                                msg +=  "in (rg: ";
                                msg += rgName;
                                msg += ") is NULL";
                                log_error(msg);
                                continue;
                            }
                            daName = daP->getDeclusteredArrayName();
                            msg = "Refresh da: ";
                            msg += daName;
                            msg += " in rg: ";
                            msg += rgName;
                            log_info(msg);
                            ret = refreshDa(daP, clusterid, rgName);
                            if(ret != TEAL_SUCCESS)
                            {
                                msg = "Refresh declustered array: ";
                                msg += daName;
                                msg += " in (rg: ";
                                msg += rgName;
                                msg += ") failed with ";
                                msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
                                log_error(msg);
                            } 
                            int j = 0;
                            int k = 0;
                            nPdisk = daP->getDeclusteredArrayPdisks();
                            nVdisk = daP->getDeclusteredArrayVdisks();
                            for(; j < nPdisk; j++)
                            {
                                pdiskP = daP->getDeclusteredArrayPdiskP(j);
                                if(pdiskP == NULL)
                                {
                                    msg = "pdisk: ";
                                    msg += Utils::int_to_char(tmp,10,(unsigned int*)&i);
                                    msg += " in (rg: ";
                                    msg += rgName;
                                    msg += ", da: ";
                                    msg += daName;
                                    msg += ") is NULL";
                                    log_error(msg);
                                    continue;
                                }
                                pdiskName = pdiskP->getPdiskName();                                 
                                msg = "Refresh pdisk: ";
                                msg += pdiskName;
                                msg += " in (rg: ";
                                msg += rgName;
                                msg += ", da: ";
                                msg += daName;
                                msg += ")";
                                log_info(msg);
                                ret = refreshPdisk(pdiskP,clusterid,rgName,daName);
                                if(ret != TEAL_SUCCESS)
                                {
                                    msg = "Refresh pdisk: ";
                                    msg += pdiskName;
                                    msg += " in (rg: ";
                                    msg += rgName;
                                    msg += ", da: ";
                                    msg += daName;
                                    msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
                                    log_error(msg);
                                }
                            }
                            for(; k < nVdisk; k++)
                            {
                                vdiskP = daP->getDeclusteredArrayVdiskP(k);
                                if(vdiskP == NULL)
                                {
                                    msg = "vdisk: ";
                                    msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
                                    msg += " in (rg: ";
                                    msg += rgName;
                                    msg += ", da: ";
                                    msg += daName;
                                    msg += ") is NULL";
                                    log_error(msg);
                                    continue;
                                }
                                vdiskName = vdiskP->getVdiskName();
                                msg = "Refresh vdisk: ";
                                msg += vdiskName;
                                msg += " in (rg: ";
                                msg += rgName;
                                msg += ", da: ";
                                msg += daName;
                                log_info(msg);
                                ret = refreshVdisk(vdiskP,clusterid,rgName,daName);
                                if(ret != TEAL_SUCCESS)
                                {
                                    msg = "Refresh vdisk: ";
                                    msg += vdiskName;
                                    msg += " in (rg: ";
                                    msg += rgName;
                                    msg += ", da: ";
                                    msg += daName;
                                    msg += ") failed with ";
                                    msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
                                    log_error(msg);
                                }
                            }
                            allDaOK &= strcmp(daP->getDeclusteredNeedsService(),"yes"); // check all DA's status
                        }
                        msg = "Refresh rg: ";
                        msg += rgName;
                        log_info(msg);  
                        ret = refreshRg(rgP, clusterid,allDaOK);
                        if(ret != TEAL_SUCCESS)
                        {
                            msg = "Refresh recovery group: ";
                            msg += rgName;
                            msg += " failed with ";
                            msg += Utils::int_to_char(tmp,10,(unsigned int*)&ret);
                            log_error(msg);
                        }  
                    }
                    else
                    {
                        msg = "get DA to refresh DA in RG: ";
                        msg += rgName;
                        msg += " failed with ";
                        msg += Utils::int_to_char(tmp,10,(unsigned int*)&rc);
                        log_error(msg);
                        continue;
                    }
                }
                else
                {
                    msg = "get RG summary to refresh RG: ";
                    msg += Utils::int_to_char(tmp,10,(unsigned int*)&i);
                    msg += " failed with ";
                    msg += Utils::int_to_char(tmp,10,(unsigned int*)&rc);
                    log_error(msg);
                    continue;
                }
             }
          }
        else
        {
            log_error("No recovery group found!");
        }

    }
    else
    {
        msg = "Failed to getNsdRAIDSdrInfo with ";
        msg += Utils::int_to_char(tmp,10,(unsigned int*)&rc);
        log_error(msg);
    }
    log_info("########################End of GPFSConfigHandler#########################################");
    return;
    
}
void GPFSConfigHandler::action(GPFSHandler* handler)
{
    
    handler->getThread()->schedule(task,getInterv());
    
    return;
}

GPFSConfigHandler::~GPFSConfigHandler()
{
    if(conn)
        delete conn;
    if(instance)
        delete instance;
}


