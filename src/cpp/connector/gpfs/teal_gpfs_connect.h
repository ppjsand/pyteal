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
#ifndef _H_TEAL_GPFS_CONNECT_
#define _H_TEAL_GPFS_CONNECT_

#include <limits.h>
#include <time.h>
#include <inttypes.h>

#include "teal_error.h"
#include "teal_connect_internal.h"
#include "teal_helpers.h"
#include "DbInterface.h"
#include "teal_connect_api.h"
#include <vector>
#ifdef __cplusplus
extern "C" {
#endif

  typedef struct tlgpfs_fs_event {
      char*        severity; 
      char*        node_ip;
      char*        sgmgr_ip;
      char*        user_unbalanced;           
      char*        meta_unbalanced;        
      char*        user_ill_rep;   
      char*        meta_ill_rep;   
      char*        user_exposed;
      char*        meta_exposed;      
      char*        pool_name;   
      char*        pool_status;
       int*        pool_usage;    

  } tlgpfs_fs_event_t;

  typedef struct tlgpfs_disk_event {
      char*               severity;
      char*               fs_name;         
      char*               node_name;   
      char*               node_ip; 
      char*               status;  
      char*               availability;  
      char*               fg_name;     
      char*               meta;   
      char*               data;
      char*               cmd;
      char*               my_role;
      char*               ck_reason;
      char*               other_node;
      unsigned int*       data_len;
      unsigned int*       err_cnt_client;
      unsigned int*       err_cnt_serv;
      unsigned int*       err_cnt_nsd;
      unsigned int*       rpt_interval;
      int*                io_length;
      long*               io_time;
      unsigned long long* start_sector;

  } tlgpfs_disk_event_t;
  
  typedef struct tlgpfs_perseus_event {
      char*        severity;        
      char*        node_name; 
      char*        location;  
      char*        fru;  
      char*        wwn;     
      char*        state;   
      char*        reason;
      char*        dev_name;
       int*        priority;
       int*        rem_redund;
       int*        err;

  } tlgpfs_perseus_event_t;

  typedef struct tlgpfs_misc_event {
      char*        severity;        
      char*        msg_text; 
      char*        diagnosis; 
      long*        wait_time; 
       int*        msg_level;    

  } tlgpfs_misc_event_t;

  typedef struct tlgpfs_cluster_info {

      char*            cluster_id;     
      char*            cluster_name;        
      char*            cluster_type;   
      char*            min_rel_level;   
      char*            uid_domain;
      char*            rsh_cmd;      
      char*            rcp_cmd;    
      char*            prim_server;   
      char*            sec_server;   
      char*            c_ref_time;      
      char*            n_ref_time;   
      char*            f_ref_time;
      char*            fp_ref_time;        
       int*            sdr_fs_num;    
       int*            num_nodes;
       int*            max_blk_size;
       int*            num_fs;    
       int*            token_server;   
       int*            fail_det_time;   
       int*            tcp_port;
       int*            min_timeout;   
       int*            max_timeout;
       int*            num_free_disk;   
       int*            change;
       int*            health;

  } tlgpfs_cluster_info_t;

 typedef struct tlgpfs_node_info {
 
     char*                  cluster_id;      
     char*                  ip_addr;        
     char*                  name;   
     char*                  type;   
     char*                  endian;
     char*                  os_name;        
     char*                  version;      
     char*                  platform;     
     char*                  admin;    
     char*                  status;       
     char*                  umnt_disk_fail;    
     char*                  healthy;
     char*                  diag;         
     unsigned long long*  pg_pool_size;
     int*                  failure_count;     
     int*                  thread_wait;
     int*                  pre_threads;
     int*                  max_MBPS;     
     int*                  max_file_cache;   
     int*                  max_stat_cache;   
     int*                  work1_threads;
     int*                  dm_evt_timeout;     
     int*                  dm_mnt_timeout;
     int*                  dm_ses_timeout;   
      int*                  nsd_win_mnt;     
     int*                  nsd_time_mnt;
     int*                  num_disk_access;   
     int*                  change;
     int*                  health;

     
 } tlgpfs_node_info_t;

 typedef struct tlgpfs_fs_info {
 
     char*                  cluster_id;      
     char*                  fs_name;        
     char*                  manager;   
     char*                  status;   
     char*                  x_status;
     char*                  util_status;        
     char*                  pool_ref_time;      
     unsigned long long*  total_space;     
     unsigned long long*  total_inodes;    
     unsigned long long*  free_inodes;       
     unsigned long long*  free_space;    
     unsigned long long*  full_blk_space;
     unsigned long long*  sub_blk_space;         
     int*                 stg_pool_num;
     int*                  num_mgmt;     
     int*                  read_duration;
     int*                  num_mnt_nodes;
     int*                  num_policies;     
     int*                  write_duration;   
     int*                  was_updated;   
     int*                  num_mgr_chg;  
     int*                  change;
     int*                  health;

     
 } tlgpfs_fs_info_t;

 typedef struct tlgpfs_stg_info {
 
     char*                  cluster_id;      
     char*                  fs_name;        
     char*                  stg_name;   
     char*                  status;   
     char*                  refresh_time;
     char*                  perf_ref_time;              
     unsigned long long*  total_space;       
     unsigned long long*  free_space;         
     int*                 parent_fs;
     int*                  num_disks;     
     int*                  num_disk_items;
     int*                  change;
     int*                  health;

     
 } tlgpfs_stg_info_t;

 typedef struct tlgpfs_disk_info {
 
     char*                  cluster_id;      
     char*                  disk_name;        
     char*                  node_name;   
     char*                  status;   
     char*                  availability;
     char*                  pool_name;        
     char*                  vol_id;    
     char*                  meta_data;   
     char*                  data;   
     char*                  disk_wait; 
     unsigned long long*    total_space;    
     unsigned long long*    full_blk_space;
     unsigned long long*    sub_blk_space;
     int*                   fail_group_id;   
     int*                   is_free;  
     int*                   change;
     int*                   health;

     
 } tlgpfs_disk_info_t;

  typedef struct tlgpfs_fset_info {
 
     char*                  cluster_id;      
     char*                  fs_name;        
     char*                  id;     
     char*                  fset_name;
     char*                  root_inode;        
     char*                  parent_id;    
     char*                  comment;    
     char*                  status; 
     char*                  path;    
     char*                  created;  
     unsigned long long*    inodes;    
     unsigned long long*    data;
     int*                   version;   
     int*                   change;
     int*                   health;
     
 } tlgpfs_fset_info_t;
  
  typedef struct tlgpfs_rg_info {
  
      char*                cluster_id;       
      char*                rg_name;     
      char*                rg_act_svr;   
      char*                rg_svrs;   
      char*                rg_id;
       int*                rg_das;     
       int*                rg_vdisks;    
       int*                rg_pdisks;  
       int*                change;
       int*                health;      
  } tlgpfs_rg_info_t;
  
  typedef struct tlgpfs_da_info {
  
      char*                cluster_id;       
      char*                rg_name;     
      char*                da_name;   
      char*                da_bg_task;   
      char*                da_task_priority;
      char*                da_need_service;
       int*                da_task_percent;     
       int*                da_vdisks;    
       int*                da_pdisks;
       int*                da_spares;    
       int*                da_replace_thres;
      unsigned long long*  da_free_space;
       int*                da_scrub_dura;
       int*                change;
       int*                health;      
  } tlgpfs_da_info_t;
  
  typedef struct tlgpfs_vdisk_info {
  
      char*                cluster_id;       
      char*                rg_name;     
      char*                da_name;   
      char*                vdisk_name;   
      char*                vdisk_raid_code;
      char*                vdisk_state;     
      char*                vdisk_remarks;    
       int*                vdisk_block_size;
      unsigned long long*  vdisk_size;    
       int*                change;
       int*                health;      
  } tlgpfs_vdisk_info_t;

 typedef struct tlgpfs_pdisk_info {
 
     char *                  cluster_id;      
     char *                  rg_name;       
     char *                  da_name;     
     char *                  pdisk_name;    
     char *                  pdisk_dev_path;
     char *                  pdisk_state;    
     char *                  pdisk_fru;     
     char *                  pdisk_location;
      int *                  pdisk_repl_prior;     
     unsigned long long *    pdisk_free_space;
      int *                  change;
      int *                  health;     
 } tlgpfs_pdisk_info_t;
  
  TEAL_ERR_T tlgpfs_update_cluster_info(teal_connector_handle conn_handle,
                                             tlgpfs_cluster_info_t *gpfs_cluster_info);
  
  TEAL_ERR_T tlgpfs_update_node_info(teal_connector_handle conn_handle,
                                           tlgpfs_node_info_t *gpfs_node_info);

  TEAL_ERR_T tlgpfs_update_fs_info(teal_connector_handle conn_handle,
                                        tlgpfs_fs_info_t *gpfs_fs_info);
  
  TEAL_ERR_T tlgpfs_update_stg_info(teal_connector_handle conn_handle,
                                         tlgpfs_stg_info_t *gpfs_stg_info);

  TEAL_ERR_T tlgpfs_update_disk_info(teal_connector_handle conn_handle,
                                          tlgpfs_disk_info_t *gpfs_disk_info);
  
  TEAL_ERR_T tlgpfs_update_fset_info(teal_connector_handle conn_handle,
                                          tlgpfs_fset_info_t *gpfs_fset_info);

  TEAL_ERR_T tlgpfs_update_rg_info(teal_connector_handle conn_handle,
                                          tlgpfs_rg_info_t *gpfs_rg_info);

  TEAL_ERR_T tlgpfs_update_da_info(teal_connector_handle conn_handle,
                                          tlgpfs_da_info_t *gpfs_da_info);
  
  TEAL_ERR_T tlgpfs_update_vdisk_info(teal_connector_handle conn_handle,
                                          tlgpfs_vdisk_info_t *gpfs_vdisk_info);
  
  TEAL_ERR_T tlgpfs_update_pdisk_info(teal_connector_handle conn_handle,
                                          tlgpfs_pdisk_info_t *gpfs_pdisk_info);
 
  TEAL_ERR_T tlgpfs_write_fs_event(teal_connector_handle handle,
                                     teal_cbe_t *common_event,
                                     tlgpfs_fs_event_t *gpfs_fs_event);

                                          
  TEAL_ERR_T tlgpfs_write_disk_event(teal_connector_handle handle,
                                        teal_cbe_t *common_event,
                                        tlgpfs_disk_event_t *gpfs_disk_event);   
  
  TEAL_ERR_T tlgpfs_write_perseus_event(teal_connector_handle handle,
                                        teal_cbe_t *common_event,
                                        tlgpfs_perseus_event_t *gpfs_perseus_event);   
  
  TEAL_ERR_T tlgpfs_write_misc_event(teal_connector_handle handle,
                                        teal_cbe_t *common_event,
                                        tlgpfs_misc_event_t *gpfs_misc_event);   

  TEAL_ERR_T tlgpfs_query_cluster_status(teal_connector_handle conn_handle,
                                              std::vector<tlgpfs_cluster_info_t *>** gpfs_cluster_status, 
                                              std::string& colName,
                                              std::string& colValue);//* for all
 
  TEAL_ERR_T tlgpfs_query_node_status(teal_connector_handle conn_handle,
                                             std::vector<tlgpfs_node_info_t *>** gpfs_node_status, 
                                             std::string& colName,
                                             std::string& colValue);//* for all 
                                             
  TEAL_ERR_T tlgpfs_query_fs_status(teal_connector_handle conn_handle,
                                         std::vector<tlgpfs_fs_info_t *>** gpfs_fs_status, 
                                         std::string& colName, 
                                         std::string& colValue);//* for all 
                                         
  TEAL_ERR_T tlgpfs_query_disk_status(teal_connector_handle conn_handle,
                                         std::vector<tlgpfs_disk_info_t *>** gpfs_disk_status, 
                                         std::string& colName, 
                                         std::string& colValue);//* for all 
                                         
  TEAL_ERR_T tlgpfs_query_stg_status(teal_connector_handle conn_handle,
                                         std::vector<tlgpfs_stg_info_t *>** gpfs_stg_status, 
                                         std::string& colName, 
                                         std::string& colValue);//* for all 

  TEAL_ERR_T tlgpfs_query_fset_status(teal_connector_handle conn_handle,
                                         std::vector<tlgpfs_fset_info_t *>** gpfs_fset_status, 
                                         std::string& colName, 
                                         std::string& colValue);//* for all 

  TEAL_ERR_T tlgpfs_query_rg_status(teal_connector_handle conn_handle,
                                         std::vector<tlgpfs_rg_info_t *>** gpfs_rg_status, 
                                         std::string& colName, 
                                         std::string& colValue);//* for all 

  TEAL_ERR_T tlgpfs_query_da_status(teal_connector_handle conn_handle,
                                         std::vector<tlgpfs_da_info_t *>** gpfs_da_status, 
                                         std::string& colName, 
                                         std::string& colValue);//* for all   

  TEAL_ERR_T tlgpfs_query_pdisk_status(teal_connector_handle conn_handle,
                                         std::vector<tlgpfs_pdisk_info_t *>** gpfs_pdisk_status, 
                                         std::string& colName, 
                                         std::string& colValue);//* for all 

  TEAL_ERR_T tlgpfs_query_vdisk_status(teal_connector_handle conn_handle,
                                         std::vector<tlgpfs_vdisk_info_t *>** gpfs_vdisk_status, 
                                         std::string& colName, 
                                         std::string& colValue);//* for all         
                                         
  TEAL_ERR_T tlgpfs_update_overall_status(teal_connector_handle handle,
                                            std::string& colName, 
                                            std::string& colValue,
                                            std::string& keyName,
                                            std::string& keyValue);//update all enetities's status
                                            
  TEAL_ERR_T tlgpfs_purge_cluster(teal_connector_handle conn_handle,
                                         std::string& cluster);

#ifdef __cplusplus
}
#endif

#endif
