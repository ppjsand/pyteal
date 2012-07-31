CREATE DATABASE IF NOT EXISTS tealdb0;

-- Use the created database
USE tealdb0;

DROP TABLE IF EXISTS x_CNM_1_2;
DROP TABLE IF EXISTS x_GPFS_1_1;
DROP TABLE IF EXISTS x_GPFS_1_2;
DROP TABLE IF EXISTS x_GPFS_1_3;
DROP TABLE IF EXISTS x_GPFS_1_4;

DROP TABLE IF EXISTS x_clusterinfo;
DROP TABLE IF EXISTS x_clusterinfo_tmp;
DROP TABLE IF EXISTS x_nodeinfo;
DROP TABLE IF EXISTS x_nodeinfo_tmp;
DROP TABLE IF EXISTS x_fsinfo;
DROP TABLE IF EXISTS x_fsinfo_tmp;
DROP TABLE IF EXISTS x_stgpoolinfo;
DROP TABLE IF EXISTS x_stgpoolinfo_tmp;
DROP TABLE IF EXISTS x_diskinfo;
DROP TABLE IF EXISTS x_diskinfo_tmp;
DROP TABLE IF EXISTS x_fsetinfo;
DROP TABLE IF EXISTS x_fsetinfo_tmp;
DROP TABLE IF EXISTS x_rginfo;
DROP TABLE IF EXISTS x_rginfo_tmp;
DROP TABLE IF EXISTS x_dainfo;
DROP TABLE IF EXISTS x_dainfo_tmp;
DROP TABLE IF EXISTS x_vdiskinfo;
DROP TABLE IF EXISTS x_vdiskinfo_tmp;
DROP TABLE IF EXISTS x_pdiskinfo;
DROP TABLE IF EXISTS x_pdiskinfo_tmp;

DROP TABLE IF EXISTS x_LL_1_1;
DROP TABLE IF EXISTS x_SFP_1_1;
DROP TABLE IF EXISTS site;

DROP TABLE IF EXISTS x_AMM_1_1;
DROP TABLE IF EXISTS x_IPMI_1_1;
DROP TABLE IF EXISTS `x_IB_1_1`;

DROP TABLE IF EXISTS x_tealalert2alert;
DROP TABLE IF EXISTS x_tealalert2event;
DROP TABLE IF EXISTS x_tealcheckpoint;
DROP TABLE IF EXISTS x_tealalertlog;
DROP TABLE IF EXISTS x_tealeventlog;


CREATE TABLE x_tealalert2alert (
  assoc_id bigint(20) NOT NULL auto_increment,
  alert_recid bigint(20) NOT NULL,
  assoc_type char(1) NOT NULL,
  t_alert_recid bigint(20) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY  (assoc_id)
) ENGINE=InnoDB;

CREATE TABLE x_tealalert2event (
  assoc_id bigint(20) NOT NULL auto_increment,
  alert_recid bigint(20) NOT NULL,
  assoc_type char(1) NOT NULL,
  t_event_recid bigint(20) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY  (assoc_id)
) ENGINE=InnoDB;

CREATE TABLE x_tealcheckpoint (
  chkpt_id bigint(20) NOT NULL auto_increment,
  name varchar(128),
  status char(1) default NULL,
  event_recid bigint(20) default NULL,
  data varchar(1024) default NULL,
  comments text,
  disable text,
  PRIMARY KEY  (chkpt_id)
) ENGINE=InnoDB;

CREATE TABLE x_tealalertlog (
  rec_id bigint(20) NOT NULL auto_increment,
  alert_id char(8) NOT NULL,
  creation_time timestamp NOT NULL default CURRENT_TIMESTAMP,
  severity char(1) NOT NULL,
  urgency char(1) NOT NULL,
  event_loc_type varchar(2) NOT NULL,
  event_loc varchar(255) NOT NULL,
  fru_loc varchar(512) default NULL,
  recommendation varchar(2048) NOT NULL,
  reason varchar(512) NOT NULL,
  src_name varchar(64) NOT NULL,
  state tinyint(4) NOT NULL,
  raw_data varchar(2048) default NULL,
  comments text,
  disable text,
  PRIMARY KEY  (rec_id)
) ENGINE=InnoDB;

CREATE TABLE x_tealeventlog (
  rec_id bigint(20) NOT NULL auto_increment,
  event_id char(8) NOT NULL,
  time_logged timestamp NOT NULL default CURRENT_TIMESTAMP,
  time_occurred timestamp NOT NULL,
  src_comp varchar(128) NOT NULL,
  src_loc_type varchar(2) NOT NULL,
  src_loc varchar(255) NOT NULL,
  rpt_comp varchar(128) default NULL,
  rpt_loc_type varchar(2) default NULL,
  rpt_loc varchar(255) default NULL,
  event_cnt int(11) default NULL,
  elapsed_time bigint(20) unsigned default NULL,
  raw_data_fmt bigint(20) unsigned default NULL,
  raw_data varchar(1024) default NULL,
  ext_key  char(36) default NULL,   
  comments text,
  disable text,
  PRIMARY KEY  (rec_id)
) ENGINE=InnoDB;

CREATE TABLE x_CNM_1_2 (
  rec_id bigint(20) NOT NULL,
  eed_loc_info varchar(64) NOT NULL,
  encl_mtms varchar(20) NOT NULL,
  pwr_ctrl_mtms varchar(20) NOT NULL,
  neighbor_loc_type varchar(2) DEFAULT NULL,
  neighbor_loc varchar(256) DEFAULT NULL,
  recovery_file_path varchar(32) NOT NULL,
  isnm_raw_data varchar(1024) DEFAULT NULL,
  local_port varchar(256) DEFAULT NULL,
  local_torrent varchar(256) DEFAULT NULL,
  local_planar varchar(256) DEFAULT NULL,
  local_om1 varchar(256) DEFAULT NULL,
  local_om2 varchar(256) DEFAULT NULL,
  nbr_port varchar(256) DEFAULT NULL,
  nbr_torrent varchar(256) DEFAULT NULL,
  nbr_planar varchar(256) DEFAULT NULL,
  nbr_om1 varchar(256) DEFAULT NULL,
  nbr_om2 varchar(256) DEFAULT NULL,
  global_counter bigint(20) DEFAULT NULL,
  comments text,
  disable text,
  PRIMARY KEY  (rec_id)
) ENGINE=InnoDB;

CREATE TABLE x_GPFS_1_1 (
  rec_id bigint(20) NOT NULL,
  severity varchar(256) NOT NULL,
  node_ip varchar(256) DEFAULT NULL,
  sgmgr_ip varchar(256) DEFAULT NULL,
  user_unba varchar(256) DEFAULT NULL,
  meta_unba varchar(256) DEFAULT NULL,
  user_ill_rep varchar(256) DEFAULT NULL,
  meta_ill_rep varchar(256) DEFAULT NULL,
  user_exposed varchar(256) DEFAULT NULL,
  meta_exposed varchar(256) DEFAULT NULL,
  pool_name varchar(256) DEFAULT NULL,
  pool_status varchar(256) DEFAULT NULL,
  pool_usage int(11) DEFAULT NULL,
  comments text,
  disable text,
  PRIMARY KEY (rec_id)
) ENGINE=InnoDB;

CREATE TABLE x_GPFS_1_2 (
  rec_id bigint(20) NOT NULL,
  severity varchar(256) NOT NULL,
  fs_name varchar(256) NOT NULL,
  node_name varchar(256) DEFAULT NULL,
  node_ip varchar(256) DEFAULT NULL,
  status varchar(256) DEFAULT NULL,
  availability varchar(256) DEFAULT NULL,
  fg_name varchar(256) DEFAULT NULL,
  meta varchar(256) DEFAULT NULL,
  data varchar(256) DEFAULT NULL,
  cmd varchar(256) DEFAULT NULL,
  my_role varchar(256) DEFAULT NULL,
  ck_reason varchar(256) DEFAULT NULL,
  other_node varchar(256) DEFAULT NULL,
  data_len int(11) DEFAULT NULL,
  err_cnt_client int(11) DEFAULT NULL,
  err_cnt_serv int(11) DEFAULT NULL,
  err_cnt_nsd int(11) DEFAULT NULL,
  rpt_interval int(11) DEFAULT NULL,
  io_length int(11) DEFAULT NULL,
  io_time int(11) DEFAULT NULL,
  start_sector bigint(20) DEFAULT NULL,
  comments text,
  disable text,
  PRIMARY KEY (rec_id)
) ENGINE=InnoDB;

CREATE TABLE x_GPFS_1_3 (
  rec_id bigint(20) NOT NULL,
  severity varchar(256) NOT NULL,
  node_name varchar(256) NOT NULL,
  location varchar(256) DEFAULT NULL,
  fru varchar(256) DEFAULT NULL,
  wwn varchar(256) DEFAULT NULL,
  state varchar(256) DEFAULT NULL,
  reason varchar(256) DEFAULT NULL,
  dev_name varchar(256) DEFAULT NULL,
  priority int(11) DEFAULT NULL,
  rem_redund int(11) DEFAULT NULL,
  err int(11) DEFAULT NULL,
  comments text,
  disable text,
  PRIMARY KEY (rec_id)
) ENGINE=InnoDB;

CREATE TABLE x_GPFS_1_4 (
  rec_id bigint(20) NOT NULL,
  severity varchar(256) NOT NULL,
  msg_text varchar(256) DEFAULT NULL,
  diagnosis varchar(256) DEFAULT NULL,
  wait_time int(11) DEFAULT NULL,
  msg_level int(11) DEFAULT NULL,
  comments text,
  disable text,
  PRIMARY KEY (rec_id)
) ENGINE=InnoDB;

CREATE TABLE x_clusterinfo (
  cluster_id varchar(128) NOT NULL,
  cluster_name varchar(128) DEFAULT NULL,
  cluster_type varchar(128) DEFAULT NULL,
  min_rel_level varchar(128) DEFAULT NULL,
  uid_domain varchar(128) DEFAULT NULL,
  rsh_cmd varchar(128) DEFAULT NULL,
  rcp_cmd varchar(128) DEFAULT NULL,
  prim_server varchar(128) DEFAULT NULL,
  sec_server varchar(128) DEFAULT NULL,
  c_ref_time varchar(128) DEFAULT NULL,
  n_ref_time varchar(128) DEFAULT NULL,
  f_ref_time varchar(128) DEFAULT NULL,
  fp_ref_time varchar(128) DEFAULT NULL,
  sdr_fs_num int(11) DEFAULT NULL,
  num_nodes int(11) DEFAULT NULL,
  max_blk_size int(11) DEFAULT NULL,
  num_fs int(11) DEFAULT NULL,
  token_server int(11) DEFAULT NULL,
  fail_det_time int(11) DEFAULT NULL,
  tcp_port int(11) DEFAULT NULL,
  min_timeout int(11) DEFAULT NULL,
  max_timeout int(11) DEFAULT NULL,
  num_free_disk int(11) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id)
) ENGINE=InnoDB;

CREATE TABLE x_clusterinfo_tmp (
  cluster_id varchar(128) NOT NULL,
  cluster_name varchar(128) DEFAULT NULL,
  cluster_type varchar(128) DEFAULT NULL,
  min_rel_level varchar(128) DEFAULT NULL,
  uid_domain varchar(128) DEFAULT NULL,
  rsh_cmd varchar(128) DEFAULT NULL,
  rcp_cmd varchar(128) DEFAULT NULL,
  prim_server varchar(128) DEFAULT NULL,
  sec_server varchar(128) DEFAULT NULL,
  c_ref_time varchar(128) DEFAULT NULL,
  n_ref_time varchar(128) DEFAULT NULL,
  f_ref_time varchar(128) DEFAULT NULL,
  fp_ref_time varchar(128) DEFAULT NULL,
  sdr_fs_num int(11) DEFAULT NULL,
  num_nodes int(11) DEFAULT NULL,
  max_blk_size int(11) DEFAULT NULL,
  num_fs int(11) DEFAULT NULL,
  token_server int(11) DEFAULT NULL,
  fail_det_time int(11) DEFAULT NULL,
  tcp_port int(11) DEFAULT NULL,
  min_timeout int(11) DEFAULT NULL,
  max_timeout int(11) DEFAULT NULL,
  num_free_disk int(11) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id)
) ENGINE=InnoDB;

CREATE TABLE x_nodeinfo (
  cluster_id varchar(128) NOT NULL,
  ip_addr varchar(128) NOT NULL,
  node_name varchar(128) DEFAULT NULL,
  type varchar(128) DEFAULT NULL,
  endian varchar(128) DEFAULT NULL,
  os_name varchar(128) DEFAULT NULL,
  version varchar(128) DEFAULT NULL,
  platform varchar(128) DEFAULT NULL,
  admin varchar(128) DEFAULT NULL,
  status varchar(128) DEFAULT NULL,
  umnt_disk_fail varchar(128) DEFAULT NULL,
  healthy varchar(128) DEFAULT NULL,
  diag varchar(128) DEFAULT NULL,
  pg_pool_size bigint(20) DEFAULT NULL,
  failure_count int(11) DEFAULT NULL,
  thread_wait int(11) DEFAULT NULL,
  pre_threads int(11) DEFAULT NULL,
  max_MBPS int(11) DEFAULT NULL,
  max_file_cache int(11) DEFAULT NULL,
  max_stat_cache int(11) DEFAULT NULL,
  work1_threads int(11) DEFAULT NULL,
  dm_evt_timeout int(11) DEFAULT NULL,
  dm_mnt_timeout int(11) DEFAULT NULL,
  dm_ses_timeout int(11) DEFAULT NULL,
  nsd_win_mnt int(11) DEFAULT NULL,
  nsd_time_mnt int(11) DEFAULT NULL,
  num_disk_access int(11) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id,ip_addr)
) ENGINE=InnoDB;

CREATE TABLE x_nodeinfo_tmp (
  cluster_id varchar(128) NOT NULL,
  ip_addr varchar(128) NOT NULL,
  node_name varchar(128) DEFAULT NULL,
  type varchar(128) DEFAULT NULL,
  endian varchar(128) DEFAULT NULL,
  os_name varchar(128) DEFAULT NULL,
  version varchar(128) DEFAULT NULL,
  platform varchar(128) DEFAULT NULL,
  admin varchar(128) DEFAULT NULL,
  status varchar(128) DEFAULT NULL,
  umnt_disk_fail varchar(128) DEFAULT NULL,
  healthy varchar(128) DEFAULT NULL,
  diag varchar(128) DEFAULT NULL,
  pg_pool_size bigint(20) DEFAULT NULL,
  failure_count int(11) DEFAULT NULL,
  thread_wait int(11) DEFAULT NULL,
  pre_threads int(11) DEFAULT NULL,
  max_MBPS int(11) DEFAULT NULL,
  max_file_cache int(11) DEFAULT NULL,
  max_stat_cache int(11) DEFAULT NULL,
  work1_threads int(11) DEFAULT NULL,
  dm_evt_timeout int(11) DEFAULT NULL,
  dm_mnt_timeout int(11) DEFAULT NULL,
  dm_ses_timeout int(11) DEFAULT NULL,
  nsd_win_mnt int(11) DEFAULT NULL,
  nsd_time_mnt int(11) DEFAULT NULL,
  num_disk_access int(11) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id,ip_addr)
) ENGINE=InnoDB;

CREATE TABLE x_fsinfo (
  cluster_id varchar(128) NOT NULL,
  fs_name varchar(128) NOT NULL,
  manager varchar(128) DEFAULT NULL,
  status varchar(128) DEFAULT NULL,
  x_status varchar(128) DEFAULT NULL,
  pool_ref_time varchar(128) DEFAULT NULL,
  total_space bigint(20) DEFAULT NULL,
  total_inodes bigint(20) DEFAULT NULL,
  free_inodes bigint(20) DEFAULT NULL,
  free_space bigint(20) DEFAULT NULL,
  full_blk_space bigint(20) DEFAULT NULL,
  sub_blk_space bigint(20) DEFAULT NULL,
  stg_pool_num int(11) DEFAULT NULL,
  num_mgmt int(11) DEFAULT NULL,
  read_duration int(11) DEFAULT NULL,
  num_mnt_nodes int(11) DEFAULT NULL,
  num_policies int(11) DEFAULT NULL,
  write_duration int(11) DEFAULT NULL,
  was_updated int(11) DEFAULT NULL,
  num_mgr_chg int(11) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id,fs_name)
) ENGINE=InnoDB;

CREATE TABLE x_fsinfo_tmp (
  cluster_id varchar(128) NOT NULL,
  fs_name varchar(128) NOT NULL,
  manager varchar(128) DEFAULT NULL,
  status varchar(128) DEFAULT NULL,
  x_status varchar(128) DEFAULT NULL,
  pool_ref_time varchar(128) DEFAULT NULL,
  total_space bigint(20) DEFAULT NULL,
  total_inodes bigint(20) DEFAULT NULL,
  free_inodes bigint(20) DEFAULT NULL,
  free_space bigint(20) DEFAULT NULL,
  full_blk_space bigint(20) DEFAULT NULL,
  sub_blk_space bigint(20) DEFAULT NULL,
  stg_pool_num int(11) DEFAULT NULL,
  num_mgmt int(11) DEFAULT NULL,
  read_duration int(11) DEFAULT NULL,
  num_mnt_nodes int(11) DEFAULT NULL,
  num_policies int(11) DEFAULT NULL,
  write_duration int(11) DEFAULT NULL,
  was_updated int(11) DEFAULT NULL,
  num_mgr_chg int(11) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id,fs_name)
) ENGINE=InnoDB;

CREATE TABLE x_stgpoolinfo (
  cluster_id varchar(128) NOT NULL,
  fs_name varchar(128) NOT NULL,
  stg_name varchar(128) NOT NULL,
  status varchar(128) DEFAULT NULL,
  refresh_time varchar(128) DEFAULT NULL,
  perf_ref_time varchar(128) DEFAULT NULL,
  total_space bigint(20) DEFAULT NULL,
  free_space bigint(20) DEFAULT NULL,
  parent_fs int(11) DEFAULT NULL,
  num_disks int(11) DEFAULT NULL,
  num_disk_items int(11) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id,fs_name,stg_name)
) ENGINE=InnoDB;

CREATE TABLE x_stgpoolinfo_tmp (
  cluster_id varchar(128) NOT NULL,
  fs_name varchar(128) NOT NULL,
  stg_name varchar(128) NOT NULL,
  status varchar(128) DEFAULT NULL,
  refresh_time varchar(128) DEFAULT NULL,
  perf_ref_time varchar(128) DEFAULT NULL,
  total_space bigint(20) DEFAULT NULL,
  free_space bigint(20) DEFAULT NULL,
  parent_fs int(11) DEFAULT NULL,
  num_disks int(11) DEFAULT NULL,
  num_disk_items int(11) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id,fs_name,stg_name)
) ENGINE=InnoDB;

CREATE TABLE x_diskinfo (
  cluster_id varchar(128) NOT NULL,
  disk_name varchar(128) NOT NULL,
  node_name varchar(128) DEFAULT NULL,
  status varchar(128) DEFAULT NULL,
  availability varchar(128) DEFAULT NULL,
  pool_name varchar(128) DEFAULT NULL,
  vol_id varchar(128) DEFAULT NULL,
  meta_data varchar(128) DEFAULT NULL,
  data varchar(128) DEFAULT NULL,
  disk_wait varchar(128) DEFAULT NULL,
  total_space bigint(20) DEFAULT NULL,
  full_blk_space bigint(20) DEFAULT NULL,
  sub_blk_space bigint(20) DEFAULT NULL,
  fail_group_id int(11) DEFAULT NULL,
  is_free int(11) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id,disk_name)
) ENGINE=InnoDB;

CREATE TABLE x_diskinfo_tmp (
  cluster_id varchar(128) NOT NULL,
  disk_name varchar(128) NOT NULL,
  node_name varchar(128) DEFAULT NULL,
  status varchar(128) DEFAULT NULL,
  availability varchar(128) DEFAULT NULL,
  pool_name varchar(128) DEFAULT NULL,
  vol_id varchar(128) DEFAULT NULL,
  meta_data varchar(128) DEFAULT NULL,
  data varchar(128) DEFAULT NULL,
  disk_wait varchar(128) DEFAULT NULL,
  total_space bigint(20) DEFAULT NULL,
  full_blk_space bigint(20) DEFAULT NULL,
  sub_blk_space bigint(20) DEFAULT NULL,
  fail_group_id int(11) DEFAULT NULL,
  is_free int(11) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id,disk_name)
) ENGINE=InnoDB;

CREATE TABLE x_fsetinfo (
  cluster_id varchar(128) NOT NULL,
  fs_name varchar(128) NOT NULL,
  id varchar(128) NOT NULL,
  fset_name varchar(128) DEFAULT NULL,
  root_inode varchar(128) DEFAULT NULL,
  parent_id varchar(128) DEFAULT NULL,
  comment varchar(128) DEFAULT NULL,
  status varchar(128) DEFAULT NULL,
  path varchar(128) DEFAULT NULL,
  created varchar(128) DEFAULT NULL,
  inodes bigint(20) DEFAULT NULL,
  data bigint(20) DEFAULT NULL,
  version int(11) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id,fs_name,id)
) ENGINE=InnoDB;

CREATE TABLE x_fsetinfo_tmp (
  cluster_id varchar(128) NOT NULL,
  fs_name varchar(128) NOT NULL,
  id varchar(128) NOT NULL,
  fset_name varchar(128) DEFAULT NULL,
  root_inode varchar(128) DEFAULT NULL,
  parent_id varchar(128) DEFAULT NULL,
  comment varchar(128) DEFAULT NULL,
  status varchar(128) DEFAULT NULL,
  path varchar(128) DEFAULT NULL,
  created varchar(128) DEFAULT NULL,
  inodes bigint(20) DEFAULT NULL,
  data bigint(20) DEFAULT NULL,
  version int(11) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id,fs_name,id)
) ENGINE=InnoDB;

CREATE TABLE x_rginfo (
  cluster_id varchar(128) NOT NULL,
  rg_name varchar(64) NOT NULL,
  rg_act_svr varchar(64) DEFAULT NULL,
  rg_svrs varchar(128) DEFAULT NULL,
  rg_id varchar(20) DEFAULT NULL,
  rg_das int(11) DEFAULT NULL,
  rg_vdisks int(11) DEFAULT NULL,
  rg_pdisks int(11) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id,rg_name)
) ENGINE=InnoDB;

CREATE TABLE x_rginfo_tmp (
  cluster_id varchar(128) NOT NULL,
  rg_name varchar(64) NOT NULL,
  rg_act_svr varchar(64) DEFAULT NULL,
  rg_svrs varchar(128) DEFAULT NULL,
  rg_id varchar(20) DEFAULT NULL,
  rg_das int(11) DEFAULT NULL,
  rg_vdisks int(11) DEFAULT NULL,
  rg_pdisks int(11) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id,rg_name)
) ENGINE=InnoDB;

CREATE TABLE x_dainfo (
  cluster_id varchar(128) NOT NULL,
  rg_name varchar(64) NOT NULL,
  da_name varchar(64) NOT NULL,
  da_bg_task varchar(32) DEFAULT NULL,
  da_task_priority varchar(32) DEFAULT NULL,
  da_need_service varchar(8) DEFAULT NULL,
  da_task_percent int(11) DEFAULT NULL,
  da_vdisks int(11) DEFAULT NULL,
  da_pdisks int(11) DEFAULT NULL,
  da_spares int(11) DEFAULT NULL,
  da_replace_thres int(11) DEFAULT NULL,
  da_free_space bigint(20) DEFAULT NULL,
  da_scrub_dura int(11) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id,rg_name,da_name)
) ENGINE=InnoDB;

CREATE TABLE x_dainfo_tmp (
  cluster_id varchar(128) NOT NULL,
  rg_name varchar(64) NOT NULL,
  da_name varchar(64) NOT NULL,
  da_bg_task varchar(32) DEFAULT NULL,
  da_task_priority varchar(32) DEFAULT NULL,
  da_need_service varchar(8) DEFAULT NULL,
  da_task_percent int(11) DEFAULT NULL,
  da_vdisks int(11) DEFAULT NULL,
  da_pdisks int(11) DEFAULT NULL,
  da_spares int(11) DEFAULT NULL,
  da_replace_thres int(11) DEFAULT NULL,
  da_free_space bigint(20) DEFAULT NULL,
  da_scrub_dura int(11) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id,rg_name,da_name)
) ENGINE=InnoDB;

CREATE TABLE x_vdiskinfo (
  cluster_id varchar(128) NOT NULL,
  rg_name varchar(64) NOT NULL,
  da_name varchar(64) NOT NULL,
  vdisk_name varchar(64) NOT NULL,
  vdisk_raid_code varchar(32) DEFAULT NULL,
  vdisk_state varchar(64) DEFAULT NULL,
  vdisk_remarks varchar(32) DEFAULT NULL,
  vdisk_block_size int(11) DEFAULT NULL,
  vdisk_size bigint(20) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id,rg_name,da_name,vdisk_name)
) ENGINE=InnoDB;

CREATE TABLE x_vdiskinfo_tmp (
  cluster_id varchar(128) NOT NULL,
  rg_name varchar(64) NOT NULL,
  da_name varchar(64) NOT NULL,
  vdisk_name varchar(64) NOT NULL,
  vdisk_raid_code varchar(32) DEFAULT NULL,
  vdisk_state varchar(64) DEFAULT NULL,
  vdisk_remarks varchar(32) DEFAULT NULL,
  vdisk_block_size int(11) DEFAULT NULL,
  vdisk_size bigint(20) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id,rg_name,da_name,vdisk_name)
) ENGINE=InnoDB;

CREATE TABLE x_pdiskinfo (
  cluster_id varchar(128) NOT NULL,
  rg_name varchar(64) NOT NULL,
  da_name varchar(64) NOT NULL,
  pdisk_name varchar(64) NOT NULL,
  pdisk_dev_path varchar(64) DEFAULT NULL,
  pdisk_state varchar(160) DEFAULT NULL,
  pdisk_fru varchar(32) DEFAULT NULL,
  pdisk_location varchar(32) DEFAULT NULL,
  pdisk_repl_prior int(11) DEFAULT NULL,
  pdisk_free_space bigint(20) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id,rg_name,da_name,pdisk_name)
) ENGINE=InnoDB;

CREATE TABLE x_pdiskinfo_tmp (
  cluster_id varchar(128) NOT NULL,
  rg_name varchar(64) NOT NULL,
  da_name varchar(64) NOT NULL,
  pdisk_name varchar(64) NOT NULL,
  pdisk_dev_path varchar(64) DEFAULT NULL,
  pdisk_state varchar(160) DEFAULT NULL,
  pdisk_fru varchar(32) DEFAULT NULL,
  pdisk_location varchar(32) DEFAULT NULL,
  pdisk_repl_prior int(11) DEFAULT NULL,
  pdisk_free_space bigint(20) DEFAULT NULL,
  `change` int(11) NOT NULL,
  health int(11) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (cluster_id,rg_name,da_name,pdisk_name)
) ENGINE=InnoDB;

CREATE TABLE x_LL_1_1 (
  rec_id bigint(20) NOT NULL,
  time_occurred bigint(20) NOT NULL,
  time_logged bigint(20) NOT NULL,
  msg_type char(1) DEFAULT NULL,
  message varchar(1024) NOT NULL,
  detail varchar(1024) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (rec_id)
) ENGINE=InnoDB;

CREATE TABLE x_SFP_1_1 (
  rec_id bigint(20) NOT NULL,
  prob_num int(11) NOT NULL,
  description varchar(256) NOT NULL,
  call_home char(1) DEFAULT NULL,
  fru_list varchar(1536) DEFAULT NULL,
  sfp_raw_data varchar(2048) DEFAULT NULL,
  comments text,
  disable text,
  PRIMARY KEY (rec_id)
) ENGINE=InnoDB;

CREATE TABLE site (
    `key` VARCHAR(128) NOT NULL DEFAULT '',
    value TEXT,
    comments TEXT,
    disable TEXT,
    PRIMARY KEY  (`key`)
) ENGINE=InnoDB;


CREATE TABLE x_AMM_1_1 (
  rec_id bigint(20) NOT NULL,
  app_id varchar(255) DEFAULT NULL,
  sp_txt_id varchar(255) DEFAULT NULL,
  sys_uuid varchar(255) DEFAULT NULL,
  sys_sern varchar(255) DEFAULT NULL,
  app_type int(11) DEFAULT NULL,
  priority int(11) NOT NULL,
  msg_text varchar(255) DEFAULT NULL,
  host_contact varchar(255) DEFAULT NULL,
  host_location varchar(255) DEFAULT NULL,
  blade_name varchar(255) DEFAULT NULL,
  blade_sern varchar(255) DEFAULT NULL,
  blade_uuid varchar(255) DEFAULT NULL,
  evt_name int(11) DEFAULT NULL,
  source_id varchar(255) DEFAULT NULL,
  call_home_flag int(11) DEFAULT NULL,
  sys_ip_address varchar(255) DEFAULT NULL,
  sys_machine_model varchar(255) DEFAULT NULL,
  blade_machine_model varchar(255) DEFAULT NULL,
  comments text,
  disable text,
  PRIMARY KEY (rec_id)
) ENGINE=InnoDB;

CREATE TABLE x_IPMI_1_1 (
  rec_id bigint(20) NOT NULL,
  guid char(32) DEFAULT NULL,
  sequence smallint(6) DEFAULT NULL,
  time_occurred int(11) DEFAULT NULL,
  utc_offset smallint(6) DEFAULT NULL,
  trap_src smallint(6) DEFAULT NULL,
  event_src smallint(6) DEFAULT NULL,
  severity smallint(6) DEFAULT NULL,
  sensor_dev smallint(6) DEFAULT NULL,
  sensor_num smallint(6) DEFAULT NULL,
  entity smallint(6) DEFAULT NULL,
  entity_inst smallint(6) DEFAULT NULL,
  event_data1 smallint(6) DEFAULT NULL,
  event_data2 smallint(6) DEFAULT NULL,
  event_data3 smallint(6) DEFAULT NULL,
  event_data4 smallint(6) DEFAULT NULL,
  event_data5 smallint(6) DEFAULT NULL,
  event_data6 smallint(6) DEFAULT NULL,
  event_data7 smallint(6) DEFAULT NULL,
  event_data8 smallint(6) DEFAULT NULL,
  lang_code smallint(6) DEFAULT NULL,
  mfg_id smallint(6) DEFAULT NULL,
  sys_id smallint(6) DEFAULT NULL,
  message varchar(256) NOT NULL,
  comments text,
  disable text,
  PRIMARY KEY (rec_id)
) ENGINE=InnoDB;

CREATE TABLE `x_IB_1_1` (
  `rec_id` BIGINT NOT NULL,
  `severity` varchar(16) DEFAULT NULL,
  `category` varchar(32) DEFAULT NULL,
  `description` varchar(256) DEFAULT NULL,
  `comments` text,
  `disable` text,
  PRIMARY KEY (`rec_id`)
) ENGINE=InnoDB;


ALTER TABLE x_tealalert2alert ADD CONSTRAINT teal_fk_arec FOREIGN KEY (alert_recid) REFERENCES x_tealalertlog (rec_id) ON DELETE CASCADE;
ALTER TABLE x_tealalert2alert ADD CONSTRAINT teal_fk_t_arec FOREIGN KEY (t_alert_recid) REFERENCES x_tealalertlog (rec_id) ON DELETE RESTRICT;
ALTER TABLE x_tealalert2alert ADD CONSTRAINT teal_a2a_assoc_check CHECK(assoc_type IN ('C','S','D'));

ALTER TABLE x_tealalert2event ADD CONSTRAINT teal_fk_erec FOREIGN KEY (alert_recid) REFERENCES x_tealalertlog (rec_id) ON DELETE CASCADE;
ALTER TABLE x_tealalert2event ADD CONSTRAINT teal_fk_t_erec FOREIGN KEY (t_event_recid) REFERENCES x_tealeventlog (rec_id) ON DELETE RESTRICT;
ALTER TABLE x_tealalert2event ADD CONSTRAINT teal_a2e_assoc_check CHECK(assoc_type IN ('C','S'));

ALTER TABLE x_tealcheckpoint ADD CONSTRAINT teal_fk_chkrec FOREIGN KEY (event_recid) REFERENCES x_tealeventlog (rec_id) ON DELETE RESTRICT;

ALTER TABLE x_tealalertlog ADD CONSTRAINT teal_alert_state_check CHECK (state IN (1,2));

ALTER TABLE x_CNM_1_2 ADD CONSTRAINT teal_isnm_fk FOREIGN KEY (rec_id) REFERENCES x_tealeventlog (rec_id) ON DELETE CASCADE;

ALTER TABLE x_GPFS_1_1 ADD CONSTRAINT teal_gpfs_fs_fk  FOREIGN KEY (rec_id) REFERENCES x_tealeventlog (rec_id) ON DELETE CASCADE;
ALTER TABLE x_GPFS_1_2 ADD CONSTRAINT teal_gpfs_dsk_fk FOREIGN KEY (rec_id) REFERENCES x_tealeventlog (rec_id) ON DELETE CASCADE;
ALTER TABLE x_GPFS_1_3 ADD CONSTRAINT teal_gpfs_per_fk FOREIGN KEY (rec_id) REFERENCES x_tealeventlog (rec_id) ON DELETE CASCADE;
ALTER TABLE x_GPFS_1_4 ADD CONSTRAINT teal_gpfs_msc_fk FOREIGN KEY (rec_id) REFERENCES x_tealeventlog (rec_id) ON DELETE CASCADE;

ALTER TABLE x_LL_1_1 ADD CONSTRAINT teal_ll_fk FOREIGN KEY (rec_id) REFERENCES x_tealeventlog (rec_id) ON DELETE CASCADE;

ALTER TABLE x_SFP_1_1 ADD CONSTRAINT teal_sfp_fk FOREIGN KEY (rec_id) REFERENCES x_tealeventlog (rec_id) ON DELETE CASCADE;

ALTER TABLE x_IPMI_1_1 ADD CONSTRAINT teal_ipmi_fk FOREIGN KEY (rec_id) REFERENCES x_tealeventlog (rec_id) ON DELETE CASCADE;
ALTER TABLE x_AMM_1_1  ADD CONSTRAINT teal_amm_fk  FOREIGN KEY (rec_id) REFERENCES x_tealeventlog (rec_id) ON DELETE CASCADE;
ALTER TABLE x_IB_1_1 ADD CONSTRAINT teal_ib_fk FOREIGN KEY (rec_id) REFERENCES x_tealeventlog (rec_id) ON DELETE CASCADE;
