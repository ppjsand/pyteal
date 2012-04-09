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
#include "teal_gpfs_connect.h"
#include "DbInterface.h"
#include "DbDiskEvent.h"
#include "DbCommonBaseEvent.h"
#include "Semaphore.h"
#include <stdexcept>
#include "DbFsEvent.h"
#include "DbPerseusEvent.h"
#include "DbMiscEvent.h"
#include "DbNodeInfo.h"
#include "DbFsInfo.h"
#include "DbStgPoolInfo.h"
#include "DbDiskInfo.h"
#include "DbFsetInfo.h"
#include "DbClusterInfo.h"
#include "DbDaInfo.h"
#include "DbRgInfo.h"
#include "DbPdiskInfo.h"
#include "DbVdiskInfo.h"

#ifdef __cpluplus
extern "C" {
#endif


  TEAL_ERR_T tlgpfs_write_disk_event(teal_connector_handle handle,
                                          teal_cbe_t *common_event,
                                          tlgpfs_disk_event_t *gpfs_disk_event)
  {
    TEAL_ERR_T ret = TEAL_SUCCESS;

    if(handle == NULL) {
      return TEAL_ERR_ARG;
    }
    
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;
    TEAL::Notifier *pNotifier = conn_handle->notifier;

    static unsigned long long fmtLL = 0;
    if(fmtLL == 0) {
      fmtLL |= (unsigned long long)(conn_handle->comp_id)[0] << 56;
      fmtLL |= (unsigned long long)(conn_handle->comp_id)[1] << 48;
      fmtLL |= (unsigned long long)(conn_handle->comp_id)[2] << 40;
      fmtLL |= (unsigned long long)(conn_handle->comp_id)[3] << 32;
      // DB table
      fmtLL |= 1ULL << 31;
      // Version is 01
      fmtLL |= 1ULL << 16;
      // Table is 2
      fmtLL |= 2ULL;
    }

    try {
        pDbInterface->connect();
        try {
            TEAL::DbCommonBaseEvent cbe(*pDbInterface, common_event, fmtLL, 0, NULL);
            TEAL::DbDiskEvent ie(*pDbInterface, gpfs_disk_event);    
            pDbInterface->insertRecord(cbe);
            pDbInterface->insertRecord(ie);
            pDbInterface->commit();
            pNotifier->post();
        } catch (TEAL::DbException& dbe) {
            pDbInterface->rollback();
            ret = TEAL_ERR_CONN_WRITE;
        } catch (std::invalid_argument& iae) {
            TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                    "tlgpfs_write_disk_event: ");
            TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                    iae.what());

            pDbInterface->rollback();
            ret = TEAL_ERR_ARG;
        }
        pDbInterface->disconnect();
    } catch (TEAL::DbException &dbe) {
        TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                "tlgpfs_write_disk_event: ");
        TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                dbe.what());
        ret = TEAL_ERR_CONN_GEN;
    } catch (TEAL::TealException &te) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_write_disk_event: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              te.what());
      ret = TEAL_ERR_CONN_GEN;
    } catch (...) {
        TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                "tlgpfs_write_disk_event: DB disconnect - unknown error");
        ret = TEAL_ERR_CONN_GEN;
    }

    return ret;
  }

TEAL_ERR_T tlgpfs_write_fs_event(teal_connector_handle handle,
                                        teal_cbe_t *common_event,
                                        tlgpfs_fs_event_t *gpfs_fs_event)
{
  TEAL_ERR_T ret = TEAL_SUCCESS;

  if(handle == NULL) {
    return TEAL_ERR_ARG;
  }
  
  TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
  TEAL::DbInterface *pDbInterface = conn_handle->dbi;
  TEAL::Notifier *pNotifier = conn_handle->notifier;

  static unsigned long long fmtLL = 0;
  if(fmtLL == 0) {
    fmtLL |= (unsigned long long)(conn_handle->comp_id)[0] << 56;
    fmtLL |= (unsigned long long)(conn_handle->comp_id)[1] << 48;
    fmtLL |= (unsigned long long)(conn_handle->comp_id)[2] << 40;
    fmtLL |= (unsigned long long)(conn_handle->comp_id)[3] << 32;
    // DB table
    fmtLL |= 1ULL << 31;
    // Version is 01
    fmtLL |= 1ULL << 16;
    // Table is 1
    fmtLL |= 1ULL;
  }

  try {
      pDbInterface->connect();
      try {
          TEAL::DbCommonBaseEvent cbe(*pDbInterface, common_event, fmtLL, 0, NULL);
          TEAL::DbFsEvent ie(*pDbInterface, gpfs_fs_event);   
          pDbInterface->insertRecord(cbe);
          pDbInterface->insertRecord(ie);
          pDbInterface->commit();
          pNotifier->post();
      } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_write_fs_event: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_write_fs_event: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_write_fs_event: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_write_fs_event: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}

TEAL_ERR_T tlgpfs_write_perseus_event(teal_connector_handle handle,
                                          teal_cbe_t *common_event,
                                          tlgpfs_perseus_event_t *gpfs_perseus_event)
{
  TEAL_ERR_T ret = TEAL_SUCCESS;

  if(handle == NULL) {
    return TEAL_ERR_ARG;
  }
  
  TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
  TEAL::DbInterface *pDbInterface = conn_handle->dbi;
  TEAL::Notifier *pNotifier = conn_handle->notifier;

  static unsigned long long fmtLL = 0;
  if(fmtLL == 0) {
    fmtLL |= (unsigned long long)(conn_handle->comp_id)[0] << 56;
    fmtLL |= (unsigned long long)(conn_handle->comp_id)[1] << 48;
    fmtLL |= (unsigned long long)(conn_handle->comp_id)[2] << 40;
    fmtLL |= (unsigned long long)(conn_handle->comp_id)[3] << 32;
    // DB table
    fmtLL |= 1ULL << 31;
    // Version is 01
    fmtLL |= 1ULL << 16;
    // Table is 3
    fmtLL |= 3ULL;
  }

  try {
      pDbInterface->connect();
      try {
          TEAL::DbCommonBaseEvent cbe(*pDbInterface, common_event, fmtLL, 0, NULL);
          TEAL::DbPerseusEvent ie(*pDbInterface, gpfs_perseus_event);   
          pDbInterface->insertRecord(cbe);
          pDbInterface->insertRecord(ie);
          pDbInterface->commit();
          pNotifier->post();
      } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_write_perseus_event: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_write_perseus_event: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_write_perseus_event: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_write_perseus_event: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}

TEAL_ERR_T tlgpfs_write_misc_event(teal_connector_handle handle,
                                          teal_cbe_t *common_event,
                                          tlgpfs_misc_event_t *gpfs_misc_event)
{
  TEAL_ERR_T ret = TEAL_SUCCESS;

  if(handle == NULL) {
    return TEAL_ERR_ARG;
  }
  
  TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
  TEAL::DbInterface *pDbInterface = conn_handle->dbi;
  TEAL::Notifier *pNotifier = conn_handle->notifier;

  static unsigned long long fmtLL = 0;
  if(fmtLL == 0) {
    fmtLL |= (unsigned long long)(conn_handle->comp_id)[0] << 56;
    fmtLL |= (unsigned long long)(conn_handle->comp_id)[1] << 48;
    fmtLL |= (unsigned long long)(conn_handle->comp_id)[2] << 40;
    fmtLL |= (unsigned long long)(conn_handle->comp_id)[3] << 32;
    // DB table
    fmtLL |= 1ULL << 31;
    // Version is 01
    fmtLL |= 1ULL << 16;
    // Table is 4
    fmtLL |= 4ULL;
  }

  try {
      pDbInterface->connect();
      try {
          TEAL::DbCommonBaseEvent cbe(*pDbInterface, common_event, fmtLL, 0, NULL);
          TEAL::DbMiscEvent ie(*pDbInterface, gpfs_misc_event);   
          pDbInterface->insertRecord(cbe);
          pDbInterface->insertRecord(ie);
          pDbInterface->commit();
          pNotifier->post();
      } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_write_misc_event: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_write_misc_event: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_write_misc_event: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_write_misc_event: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}

TEAL_ERR_T tlgpfs_update_cluster_info(teal_connector_handle handle,
                                          tlgpfs_cluster_info_t* cluster)

{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;

    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> primary_key;
            vector<string> columns;
            TEAL::DbClusterInfo clusterInfo(pDbInterface,&columns,&primary_key,cluster);
            pDbInterface->upsertConfiguration(clusterInfo);
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_update_cluster_info: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_cluster_info: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_update_cluster_info: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_cluster_info: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}
TEAL_ERR_T tlgpfs_update_node_info(teal_connector_handle handle,
                                          tlgpfs_node_info_t* node)

{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;
    
    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> primary_key;
            vector<string> columns;
            TEAL::DbNodeInfo nodeInfo(pDbInterface,&columns,&primary_key,node);
            pDbInterface->upsertConfiguration(nodeInfo);
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_update_node_info: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_node_info: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_update_node_info: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_node_info: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}

TEAL_ERR_T tlgpfs_update_fs_info(teal_connector_handle handle,
                                          tlgpfs_fs_info_t* fs)

{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;
    
    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> primary_key;
            vector<string> columns;
            TEAL::DbFsInfo fsInfo(pDbInterface,&columns,&primary_key,fs);
            pDbInterface->upsertConfiguration(fsInfo);
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_update_fs_info: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_fs_info: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_update_fs_info: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_fs_info: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}


TEAL_ERR_T tlgpfs_update_stg_info(teal_connector_handle handle,
                                          tlgpfs_stg_info_t* stg)

{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;
    
    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> primary_key;
            vector<string> columns;
            TEAL::DbStgPoolInfo stgInfo(pDbInterface,&columns,&primary_key,stg);
            pDbInterface->upsertConfiguration(stgInfo);
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_update_stg_info: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_stg_info: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_update_stg_info: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_stg_info: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}

TEAL_ERR_T tlgpfs_update_disk_info(teal_connector_handle handle,
                                          tlgpfs_disk_info_t* disk)

{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;
    
    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> primary_key;
            vector<string> columns;
            TEAL::DbDiskInfo diskInfo(pDbInterface,&columns,&primary_key,disk);
            pDbInterface->upsertConfiguration(diskInfo);
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_update_disk_info: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_disk_info: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_update_disk_info: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_disk_info: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}

TEAL_ERR_T tlgpfs_update_fset_info(teal_connector_handle handle,
                                          tlgpfs_fset_info_t* fset)

{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;

    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> primary_key;
            vector<string> columns;
            TEAL::DbFsetInfo fsetInfo(pDbInterface,&columns,&primary_key,fset);
            pDbInterface->upsertConfiguration(fsetInfo);
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_update_fset_info: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_fset_info: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_update_fset_info: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_fset_info: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}

TEAL_ERR_T tlgpfs_update_rg_info(teal_connector_handle handle,
                                          tlgpfs_rg_info_t* rg)

{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;

    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> primary_key;
            vector<string> columns;
            TEAL::DbRgInfo rgInfo(pDbInterface,&columns,&primary_key,rg);
            pDbInterface->upsertConfiguration(rgInfo);
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_update_rg_info: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_rg_info: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_update_rg_info: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_rg_info: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}

TEAL_ERR_T tlgpfs_update_da_info(teal_connector_handle handle,
                                          tlgpfs_da_info_t* da)

{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;

    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> primary_key;
            vector<string> columns;
            TEAL::DbDaInfo daInfo(pDbInterface,&columns,&primary_key,da);
            pDbInterface->upsertConfiguration(daInfo);
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_update_da_info: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_da_info: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_update_da_info: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_da_info: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}

TEAL_ERR_T tlgpfs_update_pdisk_info(teal_connector_handle handle,
                                          tlgpfs_pdisk_info_t* pdisk)

{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;

    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> primary_key;
            vector<string> columns;
            TEAL::DbPdiskInfo pdiskInfo(pDbInterface,&columns,&primary_key,pdisk);
            pDbInterface->upsertConfiguration(pdiskInfo);
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_update_pdisk_info: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_pdisk_info: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_update_pdisk_info: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_pdisk_info: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}

TEAL_ERR_T tlgpfs_update_vdisk_info(teal_connector_handle handle,
                                          tlgpfs_vdisk_info_t* vdisk)

{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;
    
    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> primary_key;
            vector<string> columns;
            TEAL::DbVdiskInfo vdiskInfo(pDbInterface,&columns,&primary_key,vdisk);
            pDbInterface->upsertConfiguration(vdiskInfo);
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_update_vdisk_info: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_vdisk_info: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_update_vdisk_info: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_update_vdisk_info: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}

TEAL_ERR_T tlgpfs_query_cluster_status(teal_connector_handle handle,
                                          vector<tlgpfs_cluster_info_t *>** gpfs_cluster_status,
                                          string& colName,
                                          string& colValue)


{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;

    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> col;
            TEAL::DbClusterInfo* tmpcluster = new TEAL::DbClusterInfo(pDbInterface,&col);
            pDbInterface->queryConfiguration(*tmpcluster,colName,colValue,(void**)gpfs_cluster_status);
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_query_cluster_status: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_cluster_status: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_query_cluster_status: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_cluster_status: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}
TEAL_ERR_T tlgpfs_query_node_status(teal_connector_handle handle,
                                          vector<tlgpfs_node_info_t *>** gpfs_node_status,
                                          string& colName,
                                          string& colValue)


{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;

    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> col;
            TEAL::DbNodeInfo* tmpnode = new TEAL::DbNodeInfo(pDbInterface,&col);
            pDbInterface->queryConfiguration(*tmpnode,colName,colValue,(void**)gpfs_node_status);          
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_query_node_status: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_node_status: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_query_node_status: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_node_status: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}

TEAL_ERR_T tlgpfs_query_fs_status(teal_connector_handle handle,
                                     vector<tlgpfs_fs_info_t *>** gpfs_fs_status,
                                     string& colName,
                                     string& colValue)
{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;

    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> cols;
            TEAL::DbFsInfo* tmpfs = new TEAL::DbFsInfo(pDbInterface,&cols);
            pDbInterface->queryConfiguration(*tmpfs,colName,colValue,(void**)gpfs_fs_status);
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_query_fs_status: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_fs_status: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_query_fs_status: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_fs_status: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}


TEAL_ERR_T tlgpfs_query_disk_status(teal_connector_handle handle,
                                     vector<tlgpfs_disk_info_t *>** gpfs_disk_status,
                                     string& colName,
                                     string& colValue)
{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;

    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> cols;
            TEAL::DbDiskInfo* tmpdisk = new TEAL::DbDiskInfo(pDbInterface,&cols);
            pDbInterface->queryConfiguration(*tmpdisk,colName,colValue,(void**)gpfs_disk_status);
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_query_disk_status: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_disk_status: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_query_disk_status: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_disk_status: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}


TEAL_ERR_T tlgpfs_query_stg_status(teal_connector_handle handle,
                                     vector<tlgpfs_stg_info_t *>** gpfs_stg_status,
                                     string& colName,
                                     string& colValue)
{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;
    
    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> cols;
            TEAL::DbStgPoolInfo* tmpstg = new TEAL::DbStgPoolInfo(pDbInterface,&cols);
            pDbInterface->queryConfiguration(*tmpstg,colName,colValue,(void**)gpfs_stg_status);
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_query_stg_status: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_stg_status: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_query_stg_status: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_stg_status: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}

TEAL_ERR_T tlgpfs_query_fset_status(teal_connector_handle handle,
                                     vector<tlgpfs_fset_info_t *>** gpfs_fset_status,
                                     string& colName,
                                     string& colValue)
{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;
    
    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> cols;
            TEAL::DbFsetInfo* tmpfset = new TEAL::DbFsetInfo(pDbInterface,&cols);
            pDbInterface->queryConfiguration(*tmpfset,colName,colValue,(void**)gpfs_fset_status);
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_query_fset_status: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_fset_status: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_query_fset_status: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_fset_status: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}

TEAL_ERR_T tlgpfs_query_rg_status(teal_connector_handle handle,
                                     vector<tlgpfs_rg_info_t *>** gpfs_rg_status,
                                     string& colName,
                                     string& colValue)
{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;
    
    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> cols;
            TEAL::DbRgInfo* tmprg = new TEAL::DbRgInfo(pDbInterface,&cols);
            pDbInterface->queryConfiguration(*tmprg,colName,colValue,(void**)gpfs_rg_status);
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_query_rg_status: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_rg_status: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_query_rg_status: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_rg_status: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}

TEAL_ERR_T tlgpfs_query_da_status(teal_connector_handle handle,
                                     vector<tlgpfs_da_info_t *>** gpfs_da_status,
                                     string& colName,
                                     string& colValue)
{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;

    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> cols;
            TEAL::DbDaInfo* tmpda = new TEAL::DbDaInfo(pDbInterface,&cols);
            pDbInterface->queryConfiguration(*tmpda,colName,colValue,(void**)gpfs_da_status);
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_query_da_status: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_da_status: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_query_da_status: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_da_status: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}

TEAL_ERR_T tlgpfs_query_pdisk_status(teal_connector_handle handle,
                                     vector<tlgpfs_pdisk_info_t *>** gpfs_pdisk_status,
                                     string& colName,
                                     string& colValue)
{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;

    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> cols;
            TEAL::DbPdiskInfo* tmppdisk = new TEAL::DbPdiskInfo(pDbInterface,&cols);
            pDbInterface->queryConfiguration(*tmppdisk,colName,colValue,(void**)gpfs_pdisk_status);
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_query_pdisk_status: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
  } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_pdisk_status: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
  } catch (TEAL::TealException &te) {
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            "tlgpfs_query_pdisk_status: ");
    TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
            te.what());
    ret = TEAL_ERR_CONN_GEN;
  } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_pdisk_status: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}

TEAL_ERR_T tlgpfs_query_vdisk_status(teal_connector_handle handle,
                                     vector<tlgpfs_vdisk_info_t *>** gpfs_vdisk_status,
                                     string& colName,
                                     string& colValue)
{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;

    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
            vector<string> cols;
            TEAL::DbVdiskInfo* tmpvdisk = new TEAL::DbVdiskInfo(pDbInterface,&cols);
            pDbInterface->queryConfiguration(*tmpvdisk,colName,colValue,(void**)gpfs_vdisk_status);
            pDbInterface->commit();
        } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_query_vdisk_status: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
    } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_vdisk_status: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
    } catch (TEAL::TealException &te) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_vdisk_status: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              te.what());
      ret = TEAL_ERR_CONN_GEN;
    } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_query_vdisk_status: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}

TEAL_ERR_T tlgpfs_update_overall_status(teal_connector_handle handle,
                                            std::string& colName, 
                                            std::string& colValue,
                                            std::string& keyName,
                                            std::string& keyValue)
{
      TEAL_ERR_T ret = TEAL_SUCCESS;
      
      // Validate the input
      if (handle == NULL) {
          return TEAL_ERR_ARG;
      }
      // Validate the input
      if (colName.empty() || colValue.empty() || keyName.empty()) {
          return TEAL_ERR_ARG;
      }
      // Pull the items out of our connection handle to do the work
      TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
      TEAL::DbInterface *pDbInterface = conn_handle->dbi;
    
      // Write the info to the database
      try {
          pDbInterface->connect();
          try {
              vector<string> nodecols;
              TEAL::DbNodeInfo* tmpnode = new TEAL::DbNodeInfo(pDbInterface,&nodecols);
              pDbInterface->updateStatusAll(*tmpnode,colName,colValue,keyName,keyValue);
              vector<string> clustercols;
              TEAL::DbClusterInfo* tmpcluster = new TEAL::DbClusterInfo(pDbInterface,&clustercols);
              pDbInterface->updateStatusAll(*tmpcluster,colName,colValue,keyName,keyValue);
              vector<string> diskcols;
              TEAL::DbDiskInfo* tmpdisk = new TEAL::DbDiskInfo(pDbInterface,&diskcols);
              pDbInterface->updateStatusAll(*tmpdisk,colName,colValue,keyName,keyValue);
              vector<string> fscols;
              TEAL::DbFsInfo* tmpfs = new TEAL::DbFsInfo(pDbInterface,&fscols);
              pDbInterface->updateStatusAll(*tmpfs,colName,colValue,keyName,keyValue);
              vector<string> fsetcols;
              TEAL::DbFsetInfo* tmpfset = new TEAL::DbFsetInfo(pDbInterface,&fsetcols);
              pDbInterface->updateStatusAll(*tmpfset,colName,colValue,keyName,keyValue);
              vector<string> pdiskcols;
              TEAL::DbPdiskInfo* tmppdisk = new TEAL::DbPdiskInfo(pDbInterface,&pdiskcols);
              pDbInterface->updateStatusAll(*tmppdisk,colName,colValue,keyName,keyValue);
              vector<string> vdiskcols;
              TEAL::DbVdiskInfo* tmpvdisk = new TEAL::DbVdiskInfo(pDbInterface,&vdiskcols);
              pDbInterface->updateStatusAll(*tmpvdisk,colName,colValue,keyName,keyValue);
              vector<string> rgcols;
              TEAL::DbRgInfo* tmprg = new TEAL::DbRgInfo(pDbInterface,&rgcols);
              pDbInterface->updateStatusAll(*tmprg,colName,colValue,keyName,keyValue);
              vector<string> dacols;
              TEAL::DbDaInfo* tmpda = new TEAL::DbDaInfo(pDbInterface,&dacols);
              pDbInterface->updateStatusAll(*tmpda,colName,colValue,keyName,keyValue);
              vector<string> stgcols;
              TEAL::DbStgPoolInfo* tmpstg = new TEAL::DbStgPoolInfo(pDbInterface,&stgcols);
              pDbInterface->updateStatusAll(*tmpstg,colName,colValue,keyName,keyValue);
              pDbInterface->commit();
          } catch (TEAL::DbException& dbe) {
            pDbInterface->rollback();
            ret = TEAL_ERR_CONN_WRITE;
        } catch (std::invalid_argument& iae) {
            TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                    "tlgpfs_update_overall_status: ");
            TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                    iae.what());
            pDbInterface->rollback();
            ret = TEAL_ERR_ARG;
        }
        pDbInterface->disconnect();
      } catch (TEAL::DbException &dbe) {
        TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                "tlgpfs_update_overall_status: ");
        TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                dbe.what());
        ret = TEAL_ERR_CONN_GEN;
      } catch (TEAL::TealException &te) {
        TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                "tlgpfs_update_overall_status: ");
        TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                te.what());
        ret = TEAL_ERR_CONN_GEN;
      } catch (...) {
        TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                "tlgpfs_update_overall_status: DB disconnect - unknown error");
        ret = TEAL_ERR_CONN_GEN;
    }
    
    return ret;

}

TEAL_ERR_T tlgpfs_purge_cluster(teal_connector_handle handle,
                                       std::string& cluster)
{
    TEAL_ERR_T ret = TEAL_SUCCESS;
    
    // Validate the input
    if (handle == NULL) {
        return TEAL_ERR_ARG;
    }
    
    // Pull the items out of our connection handle to do the work
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);
    TEAL::DbInterface *pDbInterface = conn_handle->dbi;

    // Write the info to the database
    try {
        pDbInterface->connect();
        try {
              vector<string> nodecols;
              TEAL::DbNodeInfo* tmpnode = new TEAL::DbNodeInfo(pDbInterface,&nodecols);
              pDbInterface->deleteUnknown(*tmpnode,"cluster_id",cluster);
              vector<string> clustercols;
              TEAL::DbClusterInfo* tmpcluster = new TEAL::DbClusterInfo(pDbInterface,&clustercols);
              pDbInterface->deleteUnknown(*tmpcluster,"cluster_id",cluster);
              vector<string> diskcols;
              TEAL::DbDiskInfo* tmpdisk = new TEAL::DbDiskInfo(pDbInterface,&diskcols);
              pDbInterface->deleteUnknown(*tmpdisk,"cluster_id",cluster);
              vector<string> fscols;
              TEAL::DbFsInfo* tmpfs = new TEAL::DbFsInfo(pDbInterface,&fscols);
              pDbInterface->deleteUnknown(*tmpfs,"cluster_id",cluster);
              vector<string> fsetcols;
              TEAL::DbFsetInfo* tmpfset = new TEAL::DbFsetInfo(pDbInterface,&fsetcols);
              pDbInterface->deleteUnknown(*tmpfset,"cluster_id",cluster);
              vector<string> pdiskcols;
              TEAL::DbPdiskInfo* tmppdisk = new TEAL::DbPdiskInfo(pDbInterface,&pdiskcols);
              pDbInterface->deleteUnknown(*tmppdisk,"cluster_id",cluster);
              vector<string> vdiskcols;
              TEAL::DbVdiskInfo* tmpvdisk = new TEAL::DbVdiskInfo(pDbInterface,&vdiskcols);
              pDbInterface->deleteUnknown(*tmpvdisk,"cluster_id",cluster);
              vector<string> rgcols;
              TEAL::DbRgInfo* tmprg = new TEAL::DbRgInfo(pDbInterface,&rgcols);
              pDbInterface->deleteUnknown(*tmprg,"cluster_id",cluster);
              vector<string> dacols;
              TEAL::DbDaInfo* tmpda = new TEAL::DbDaInfo(pDbInterface,&dacols);
              pDbInterface->deleteUnknown(*tmpda,"cluster_id",cluster);
              vector<string> stgcols;
              TEAL::DbStgPoolInfo* tmpstg = new TEAL::DbStgPoolInfo(pDbInterface,&stgcols);
              pDbInterface->deleteUnknown(*tmpstg,"cluster_id",cluster);
              pDbInterface->commit();
          } catch (TEAL::DbException& dbe) {
          pDbInterface->rollback();
          ret = TEAL_ERR_CONN_WRITE;
      } catch (std::invalid_argument& iae) {
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  "tlgpfs_purge_cluster: ");
          TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
                  iae.what());

          pDbInterface->rollback();
          ret = TEAL_ERR_ARG;
      }
      pDbInterface->disconnect();
    } catch (TEAL::DbException &dbe) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_purge_cluster: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              dbe.what());
      ret = TEAL_ERR_CONN_GEN;
    } catch (TEAL::TealException &te) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_purge_cluster: ");
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              te.what());
      ret = TEAL_ERR_CONN_GEN;
    } catch (...) {
      TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "GPFS_CONN",
              "tlgpfs_purge_cluster: DB disconnect - unknown error");
      ret = TEAL_ERR_CONN_GEN;
  }

  return ret;
}

#ifdef __cpluplus
}
#endif

