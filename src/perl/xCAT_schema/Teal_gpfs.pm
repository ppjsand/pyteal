# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2011     
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog
package xCAT_schema::Teal_gpfs;

# This file contains the schema necessary to support the GPFS component in the TEAL framework

%tabspec = (
    x_GPFS_1_1 => {
        cols => [
            qw(rec_id
              severity
              node_ip
              sgmgr_ip
              user_unba
              meta_unba
              user_ill_rep
              meta_ill_rep
              user_exposed
              meta_exposed
              pool_name
              pool_status
              pool_usage
              comments
              disable)
        ],
        keys     => [qw(rec_id)],
        required => [qw(rec_id severity)],
        types    => {
            rec_id       => 'BIGINT',
            severity     => 'VARCHAR(256)',
            node_ip      => 'VARCHAR(256)',
            sgmgr_ip     => 'VARCHAR(256)',
            user_unba    => 'VARCHAR(256)',
            meta_unba    => 'VARCHAR(256)',
            user_ill_rep => 'VARCHAR(256)',
            meta_ill_rep => 'VARCHAR(256)',
            user_exposed => 'VARCHAR(256)',
            meta_exposed => 'VARCHAR(256)',
            pool_name    => 'VARCHAR(256)',
            pool_status  => 'VARCHAR(256)',
            pool_usage   => 'INTEGER',
        },
        tablespace =>'XCATTBS32K', 
        table_desc   => 'TEAL GPFS Filesystem-related event data',
        descriptions => {
            rec_id       => 'Database record id of common event',
            severity     => 'Severity of the event',
            node_ip      => 'Reporting or failing node',
            sgmgr_ip     => 'Stripe group manager',
            user_unba    => 'User data unbalanced',
            meta_unba    => 'Metadata unbalanced',
            user_ill_rep => 'User data ill replicated',
            meta_ill_rep => 'Meata data ill replicated',
            user_exposed => 'User data exposed',
            meta_exposed => 'Metadata exposed',
            pool_name    => 'Storage pool name',
            pool_status  => 'Storage pool status',
            pool_usage   => 'Storage pool usage',
            comments     => 'Any user-written notes.',
            disable      => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
    x_GPFS_1_2 => {
        cols => [
            qw(rec_id
              severity
              fs_name
              node_name
              node_ip
              status
              availability
              fg_name
              meta
              data
              cmd
              my_role
              ck_reason
              other_node
              data_len
              err_cnt_client
              err_cnt_serv
              err_cnt_nsd
              rpt_interval
              io_length
              io_time
              start_sector
              comments
              disable
              )
        ],
        keys     => [qw(rec_id)],
        required => [qw(rec_id severity fs_name)],
        types    => {
            rec_id          => 'BIGINT',
            severity        => 'VARCHAR(256)',
            fs_name         => 'VARCHAR(256)',
            node_name       => 'VARCHAR(256)',
            node_ip         => 'VARCHAR(256)',
            status          => 'VARCHAR(256)',
            availability    => 'VARCHAR(256)',
            fg_name         => 'VARCHAR(256)',
            meta            => 'VARCHAR(256)',
            data            => 'VARCHAR(256)',
            cmd             => 'VARCHAR(256)',
            my_role         => 'VARCHAR(256)',
            ck_reason       => 'VARCHAR(256)',
            other_node      => 'VARCHAR(256)',
            data_len        => 'INTEGER',
            err_cnt_client  => 'INTEGER',
            err_cnt_serv    => 'INTEGER',
            err_cnt_nsd     => 'INTEGER',
            rpt_interval    => 'INTEGER',
            io_length       => 'INTEGER',
            io_time         => 'INTEGER',
            start_sector    => 'BIGINT',
        },
        tablespace =>'XCATTBS32K', 
        table_desc   => 'TEAL GPFS Disk-related event data',
        descriptions => {
            rec_id          => 'Database record id of common event',
            severity        => 'Severity of the event',
            fs_name         => 'Affected filesystem',
            node_name       => 'Affected node name',
            node_ip         => 'Affected node I/P address',
            status          => 'Status of the disk',
            availability    => 'Availability of the disk',
            fg_name         => 'Failure/recovery group name',
            meta            => 'Metadata information',
            data            => 'User data information',
            cmd             => 'Command, if timed out',
            my_role         => 'Reporting side of the event',
            ck_reason       => 'Reason for checksum error',
            other_node      => 'Address of the other side involved',
            data_len        => 'Data length of the failing transmission',
            err_cnt_client  => 'Cumulative number of errors for the involved client',
            err_cnt_serv    => 'Cumulative number of errors for the server',
            err_cnt_nsd     => 'Cumulative number of errors for the involved nsd',
            rpt_interval    => 'Value of the reporting interval',
            io_length       => 'Length of I/O operation being performed',
            io_time         => 'Elapsed time of I/O operation',
            start_sector    => 'Starting sector of the failing transmission',
            comments        => 'Any user-written notes.',
            disable         => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
    x_GPFS_1_3 => {
        cols => [
            qw(rec_id
              severity
              node_name
              location
              fru
              wwn
              state
              priority
              comments
              disable
              )
        ],
        keys     => [qw(rec_id)],
        required => [qw(rec_id severity node_name location fru wwn)],
        types    => {
            rec_id    => 'BIGINT',
            severity  => 'VARCHAR(256)',
            node_name => 'VARCHAR(256)',
            location  => 'VARCHAR(256)',
            fru       => 'VARCHAR(256)',
            wwn       => 'VARCHAR(256)',
            state     => 'VARCHAR(256)',
            priority  => 'INTEGER',
        },
        tablespace =>'XCATTBS32K', 
        table_desc   => 'TEAL GPFS Perseus-related event data',
        descriptions => {
            rec_id    => 'Database record id of common event',
            severity  => 'Severity of the event',
            node_name => 'Recovery Group sever',
            location  => 'Location of pdisk in enclosure',
            fru       => 'FRU information of pdisk',
            wwn       => 'Worldwide SCSI name of pdisk',
            state     => 'State of pdisk',
            priority  => 'Priority of pdisk replacement',
            comments  => 'Any user-written notes.',
            disable   => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
    x_GPFS_1_4 => {
        cols => [
            qw(rec_id
              severity
              msg_text
              diagnosis
              wait_time
              msg_level
              comments
              disable
              )
        ],
        keys     => [qw(rec_id)],
        required => [qw(rec_id severity)],
        types    => {
            rec_id    => 'BIGINT',
            severity  => 'VARCHAR(256)',
            msg_text  => 'VARCHAR(256)',
            diagnosis => 'VARCHAR(256)',
            wait_time => 'INTEGER',
            msg_level => 'INTEGER',
        },
        tablespace =>'XCATTBS32K', 
        table_desc   => 'TEAL GPFS miscellaneous event data',
        descriptions => {
            rec_id    => 'Database record id of common event',
            severity  => 'Severity of the event',
            msg_text  => 'Text displayed',
            diagnosis => 'Diagnosis of hung thread',
            wait_time => 'Duration of hang',
            comments  => 'Any user-written notes.',
            disable   => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
    x_clusterinfo => {
        cols => [
            qw(cluster_id
              cluster_name
              cluster_type
              min_rel_level
              uid_domain
              rsh_cmd
              rcp_cmd
              prim_server
              sec_server
              c_ref_time
              n_ref_time
              f_ref_time
              fp_ref_time
              sdr_fs_num
              num_nodes
              max_blk_size
              num_fs
              token_server
              fail_det_time
              tcp_port
              min_timeout
              max_timeout
              num_free_disk
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id)],
        required => [qw(cluster_id change health)],
        types    => {
            cluster_id    => 'VARCHAR(128)',
            cluster_name  => 'VARCHAR(128)',
            cluster_type  => 'VARCHAR(128)',
            min_rel_level => 'VARCHAR(128)',
            uid_domain    => 'VARCHAR(128)',
            rsh_cmd       => 'VARCHAR(128)',
            rcp_cmd       => 'VARCHAR(128)',
            prim_server   => 'VARCHAR(128)',
            sec_server    => 'VARCHAR(128)',
            c_ref_time    => 'VARCHAR(128)',
            n_ref_time    => 'VARCHAR(128)',
            f_ref_time    => 'VARCHAR(128)',
            fp_ref_time   => 'VARCHAR(128)',
            sdr_fs_num    => 'INTEGER',
            num_nodes     => 'INTEGER',
            max_blk_size  => 'INTEGER',
            num_fs        => 'INTEGER',
            token_server  => 'INTEGER',
            fail_det_time => 'INTEGER',
            tcp_port      => 'INTEGER',
            min_timeout   => 'INTEGER',
            max_timeout   => 'INTEGER',
            num_free_disk => 'INTEGER',
            change        => 'INTEGER',
            health        => 'INTEGER'
        },
        table_desc   => 'GPFS Cluster Configuration',
        descriptions => {
            cluster_id    => 'The cluster id assigned by GPFS',
            cluster_name  => 'Cluster name',
            cluster_type  => 'Type of cluster',
            min_rel_level => 'Minimum release level',
            uid_domain    => 'Domain',
            rsh_cmd       => 'Remote shell command',
            rcp_cmd       => 'Remote copy command',
            prim_server   => 'Primary cluster server',
            sec_server    => 'Secondary cluster server',
            c_ref_time    => 'Last cluster refresh time',
            n_ref_time    => 'Last node refresh time',
            f_ref_time    => 'Last filesystem refresh time',
            fp_ref_time   => 'Last filesystem performance refresh time',
            sdr_fs_num    => 'SDR filesystem generation number',
            num_nodes     => 'Number of nodes in the cluster',
            max_blk_size  => 'Maximum configured block size',
            num_fs        => 'Number of filesystems in the cluster',
            token_server  => 'Distributed token server name',
            fail_det_time => 'Failure detection time',
            tcp_port      => 'TCP port used',
            min_timeout   => 'Minimum missed ping time',
            max_timeout   => 'Maximum missed ping time',
            num_free_disk => 'Number of free disks in cluster',
            change        => 'Current change status',
            health        => 'Current aggregate health of cluster',
            comments      => 'Any user-written notes.',
            disable       => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
    x_clusterinfo_tmp => {
        cols => [
            qw(cluster_id
              cluster_name
              cluster_type
              min_rel_level
              uid_domain
              rsh_cmd
              rcp_cmd
              prim_server
              sec_server
              c_ref_time
              n_ref_time
              f_ref_time
              fp_ref_time
              sdr_fs_num
              num_nodes
              max_blk_size
              num_fs
              token_server
              fail_det_time
              tcp_port
              min_timeout
              max_timeout
              num_free_disk
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id)],
        required => [qw(cluster_id change health)],
        types    => {
            cluster_id    => 'VARCHAR(128)',
            cluster_name  => 'VARCHAR(128)',
            cluster_type  => 'VARCHAR(128)',
            min_rel_level => 'VARCHAR(128)',
            uid_domain    => 'VARCHAR(128)',
            rsh_cmd       => 'VARCHAR(128)',
            rcp_cmd       => 'VARCHAR(128)',
            prim_server   => 'VARCHAR(128)',
            sec_server    => 'VARCHAR(128)',
            c_ref_time    => 'VARCHAR(128)',
            n_ref_time    => 'VARCHAR(128)',
            f_ref_time    => 'VARCHAR(128)',
            fp_ref_time   => 'VARCHAR(128)',
            sdr_fs_num    => 'INTEGER',
            num_nodes     => 'INTEGER',
            max_blk_size  => 'INTEGER',
            num_fs        => 'INTEGER',
            token_server  => 'INTEGER',
            fail_det_time => 'INTEGER',
            tcp_port      => 'INTEGER',
            min_timeout   => 'INTEGER',
            max_timeout   => 'INTEGER',
            num_free_disk => 'INTEGER',
            change        => 'INTEGER',
            health        => 'INTEGER'
        },
        table_desc   => 'GPFS Cluster Configuration scratchpad',
        descriptions => {
            cluster_id    => 'The cluster id assigned by GPFS',
            cluster_name  => 'Cluster name',
            cluster_type  => 'Type of cluster',
            min_rel_level => 'Minimum release level',
            uid_domain    => 'Domain',
            rsh_cmd       => 'Remote shell command',
            rcp_cmd       => 'Remote copy command',
            prim_server   => 'Primary cluster server',
            sec_server    => 'Secondary cluster server',
            c_ref_time    => 'Last cluster refresh time',
            n_ref_time    => 'Last node refresh time',
            f_ref_time    => 'Last filesystem refresh time',
            fp_ref_time   => 'Last filesystem performance refresh time',
            sdr_fs_num    => 'SDR filesystem generation number',
            num_nodes     => 'Number of nodes in the cluster',
            max_blk_size  => 'Maximum configured block size',
            num_fs        => 'Number of filesystems in the cluster',
            token_server  => 'Distributed token server name',
            fail_det_time => 'Failure detection time',
            tcp_port      => 'TCP port used',
            min_timeout   => 'Minimum missed ping time',
            max_timeout   => 'Maximum missed ping time',
            num_free_disk => 'Number of free disks in cluster',
            change        => 'Current change status',
            health        => 'Current aggregate health of cluster',
            comments      => 'Any user-written notes.',
            disable       => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
    x_nodeinfo => {
        cols => [
            qw(cluster_id
              ip_addr
              node_name
              type
              endian
              os_name
              version
              platform
              admin
              status
              umnt_disk_fail
              healthy
              diag
              pg_pool_size
              failure_count
              thread_wait
              pre_threads
              max_MBPS
              max_file_cache
              max_stat_cache
              work1_threads
              dm_evt_timeout
              dm_mnt_timeout
              dm_ses_timeout
              nsd_win_mnt
              nsd_time_mnt
              num_disk_access
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id ip_addr)],
        required => [qw(cluster_id ip_addr change health)],
        types    => {
            cluster_id      => 'VARCHAR(128)',
            ip_addr         => 'VARCHAR(128)',
            node_name       => 'VARCHAR(128)',
            type            => 'VARCHAR(128)',
            endian          => 'VARCHAR(128)',
            os_name         => 'VARCHAR(128)',
            version         => 'VARCHAR(128)',
            platform        => 'VARCHAR(128)',
            admin           => 'VARCHAR(128)',
            status          => 'VARCHAR(128)',
            umnt_disk_fail  => 'VARCHAR(128)',
            healthy         => 'VARCHAR(128)',
            diag            => 'VARCHAR(128)',
            pg_pool_size    => 'BIGINT',
            failure_count   => 'INTEGER',
            thread_wait     => 'INTEGER',
            pre_threads     => 'INTEGER',
            max_MBPS        => 'INTEGER',
            max_file_cache  => 'INTEGER',
            max_stat_cache  => 'INTEGER',
            work1_threads   => 'INTEGER',
            dm_evt_timeout  => 'INTEGER',
            dm_mnt_timeout  => 'INTEGER',
            dm_ses_timeout  => 'INTEGER',
            nsd_win_mnt     => 'INTEGER',
            nsd_time_mnt    => 'INTEGER',
            num_disk_access => 'INTEGER',
            change          => 'INTEGER',
            health          => 'INTEGER',
        },
		tablespace =>'XCATTBS32K', 
        table_desc   => 'GPFS Node Configuration',
        descriptions => {
            cluster_id      => 'The cluster id assigned by GPFS',
            ip_addr         => 'Node I/P address',
            node_name       => 'Node name',
            type            => 'Type of GPFS node',
            endian          => 'Endian of node',
            os_name         => 'OS name on node',
            version         => 'GPFS version',
            platform        => 'OS platform',
            admin           => 'Admin indicator',
            status          => 'Current status',
            umnt_disk_fail  => 'Unmount on fail indicat',
            healthy         => 'Healthy indicator',
            diag            => 'Diagnosis information',
            pg_pool_size    => 'Page pool size',
            failure_count   => 'Failure counter',
            thread_wait     => 'Thread wait time',
            pre_threads     => 'Prefetch thread number',
            max_MBPS        => 'Maximum streaming rate',
            max_file_cache  => 'Maximum files to cache',
            max_stat_cache  => 'Maximum status to cache',
            work1_threads   => 'Number of worker threads',
            dm_evt_timeout  => 'Event timeout',
            dm_mnt_timeout  => 'Mount timeout',
            dm_ses_timeout  => 'Session failure timeout',
            nsd_win_mnt     => 'NSD server wait time window on mount',
            nsd_time_mnt    => 'NSD server wait time for mount',
            num_disk_access => 'Disk access items number',
            change          => 'Current change status',
            health          => 'Current aggregate health of node',
            comments        => 'Any user-written notes.',
            disable         => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
    x_nodeinfo_tmp => {
        cols => [
            qw(cluster_id
              ip_addr
              node_name
              type
              endian
              os_name
              version
              platform
              admin
              status
              umnt_disk_fail
              healthy
              diag
              pg_pool_size
              failure_count
              thread_wait
              pre_threads
              max_MBPS
              max_file_cache
              max_stat_cache
              work1_threads
              dm_evt_timeout
              dm_mnt_timeout
              dm_ses_timeout
              nsd_win_mnt
              nsd_time_mnt
              num_disk_access
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id ip_addr)],
        required => [qw(cluster_id ip_addr change health)],
        types    => {
            cluster_id      => 'VARCHAR(128)',
            ip_addr         => 'VARCHAR(128)',
            node_name       => 'VARCHAR(128)',
            type            => 'VARCHAR(128)',
            endian          => 'VARCHAR(128)',
            os_name         => 'VARCHAR(128)',
            version         => 'VARCHAR(128)',
            platform        => 'VARCHAR(128)',
            admin           => 'VARCHAR(128)',
            status          => 'VARCHAR(128)',
            umnt_disk_fail  => 'VARCHAR(128)',
            healthy         => 'VARCHAR(128)',
            diag            => 'VARCHAR(128)',
            pg_pool_size    => 'BIGINT',
            failure_count   => 'INTEGER',
            thread_wait     => 'INTEGER',
            pre_threads     => 'INTEGER',
            max_MBPS        => 'INTEGER',
            max_file_cache  => 'INTEGER',
            max_stat_cache  => 'INTEGER',
            work1_threads   => 'INTEGER',
            dm_evt_timeout  => 'INTEGER',
            dm_mnt_timeout  => 'INTEGER',
            dm_ses_timeout  => 'INTEGER',
            nsd_win_mnt     => 'INTEGER',
            nsd_time_mnt    => 'INTEGER',
            num_disk_access => 'INTEGER',
            change          => 'INTEGER',
            health          => 'INTEGER',
        },
        tablespace =>'XCATTBS32K', 
        table_desc   => 'GPFS Node Configuration scratchpad',
        descriptions => {
            cluster_id      => 'The cluster id assigned by GPFS',
            ip_addr         => 'Node I/P address',
            node_name       => 'Node name',
            type            => 'Type of GPFS node',
            endian          => 'Endian of node',
            os_name         => 'OS Name on node',
            version         => 'GPFS version',
            platform        => 'OS platform',
            admin           => 'Admin indicator',
            status          => 'Current status',
            umnt_disk_fail  => 'Unmount on fail indicat',
            healthy         => 'Healthy indicator',
            diag            => 'Diagnosis information',
            pg_pool_size    => 'Page pool size',
            failure_count   => 'Failure counter',
            thread_wait     => 'Thread wait time',
            pre_threads     => 'Prefetch thread number',
            max_MBPS        => 'Maximum streaming rate',
            max_file_cache  => 'Maximum files to cache',
            max_stat_cache  => 'Maximum status to cache',
            work1_threads   => 'Number of worker threads',
            dm_evt_timeout  => 'Event timeout',
            dm_mnt_timeout  => 'Mount timeout',
            dm_ses_timeout  => 'Session failure timeout',
            nsd_win_mnt     => 'NSD server wait time window on mount',
            nsd_time_mnt    => 'NSD server wait time for mount',
            num_disk_access => 'Disk access items number',
            change          => 'Current change status',
            health          => 'Current aggregate health of node',
            comments        => 'Any user-written notes.',
            disable         => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
    x_fsinfo => {
        cols => [
            qw(cluster_id
              fs_name
              manager
              status
              x_status
              pool_ref_time
              total_space
              total_inodes
              free_inodes
              free_space
              full_blk_space
              sub_blk_space
              stg_pool_num
              num_mgmt
              read_duration
              num_mnt_nodes
              num_policies
              write_duration
              was_updated
              num_mgr_chg
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id fs_name)],
        required => [qw(cluster_id fs_name change health)],
        types    => {
            cluster_id     => 'VARCHAR(128)',
            fs_name        => 'VARCHAR(128)',
            manager        => 'VARCHAR(128)',
            status         => 'VARCHAR(128)',
            x_status       => 'VARCHAR(128)',
            pool_ref_time  => 'VARCHAR(128)',
            total_space    => 'BIGINT',
            total_inodes   => 'BIGINT',
            free_inodes    => 'BIGINT',
            free_space     => 'BIGINT',
            full_blk_space => 'BIGINT',
            sub_blk_space  => 'BIGINT',
            stg_pool_num   => 'INTEGER',
            num_mgmt       => 'INTEGER',
            read_duration  => 'INTEGER',
            num_mnt_nodes  => 'INTEGER',
            num_policies   => 'INTEGER',
            write_duration => 'INTEGER',
            was_updated    => 'INTEGER',
            num_mgr_chg    => 'INTEGER',
            change         => 'INTEGER',
            health         => 'INTEGER',
        },
        table_desc   => 'GPFS Filesystem Configuration',
        descriptions => {
            cluster_id     => 'The cluster id assigned by GPFS',
            fs_name        => 'Filesystem name',
            manager        => 'Filesystem manager',
            status         => 'Current status of filesystem',
            x_status       => 'Extended status of filesystem',
            pool_ref_time  => 'Last storage pool data refresh time',
            total_space    => 'Total space in filesystem',
            total_inodes   => 'Total inodes in filesystem',
            free_inodes    => 'Total free inodes available',
            free_space     => 'Total free space availablbe',
            full_blk_space => 'Full block free space',
            sub_blk_space  => 'Subblock free space',
            stg_pool_num   => 'Total number of storage pools',
            num_mgmt       => 'Total number of management servers',
            read_duration  => 'Read duration of filesystem',
            num_mnt_nodes  => 'Number of nodes mounting the filesystem',
            num_policies   => 'Number of policies',
            write_duration => 'Write duration of filesystem',
            was_updated    => 'Filesystem update indicator',
            num_mgr_chg    => 'Total number of changed managers',
            change         => 'Current change status',
            health         => 'Current aggregate health of filesystem',
            comments       => 'Any user-written notes.',
            disable        => q(Set to 'yes 'or '1 'to comment out this row.),
        },
    },
    x_fsinfo_tmp => {
        cols => [
            qw(cluster_id
              fs_name
              manager
              status
              x_status              
              pool_ref_time
              total_space
              total_inodes
              free_inodes
              free_space
              full_blk_space
              sub_blk_space
              stg_pool_num
              num_mgmt
              read_duration
              num_mnt_nodes
              num_policies
              write_duration
              was_updated
              num_mgr_chg
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id fs_name)],
        required => [qw(cluster_id fs_name change health)],
        types    => {
            cluster_id     => 'VARCHAR(128)',
            fs_name        => 'VARCHAR(128)',
            manager        => 'VARCHAR(128)',
            status         => 'VARCHAR(128)',
            x_status       => 'VARCHAR(128)',
            pool_ref_time  => 'VARCHAR(128)',
            total_space    => 'BIGINT',
            total_inodes   => 'BIGINT',
            free_inodes    => 'BIGINT',
            free_space     => 'BIGINT',
            full_blk_space => 'BIGINT',
            sub_blk_space  => 'BIGINT',
            stg_pool_num   => 'INTEGER',
            num_mgmt       => 'INTEGER',
            read_duration  => 'INTEGER',
            num_mnt_nodes  => 'INTEGER',
            num_policies   => 'INTEGER',
            write_duration => 'INTEGER',
            was_updated    => 'INTEGER',
            num_mgr_chg    => 'INTEGER',
            change         => 'INTEGER',
            health         => 'INTEGER',
        },
        table_desc   => 'GPFS Filesystem Configuration scratchpad',
        descriptions => {
            cluster_id     => 'The cluster id assigned by GPFS',
            fs_name        => 'Filesystem name',
            manager        => 'Filesystem manager',
            status         => 'Current status of filesystem',
            x_status       => 'Extended status of filesystem',
            pool_ref_time  => 'Last storage pool data refresh time',
            total_space    => 'Total space in filesystem',
            total_inodes   => 'Total inodes in filesystem',
            free_inodes    => 'Total free inodes available',
            free_space     => 'Total free space availablbe',
            full_blk_space => 'Full block free space',
            sub_blk_space  => 'Subblock free space',
            stg_pool_num   => 'Total number of storage pools',
            num_mgmt       => 'Total number of management servers',
            read_duration  => 'Read duration of filesystem',
            num_mnt_nodes  => 'Number of nodes mounting the filesystem',
            num_policies   => 'Number of policies',
            write_duration => 'Write duration of filesystem',
            was_updated    => 'Filesystem update indicator',
            num_mgr_chg    => 'Total number of changed managers',
            change         => 'Current change status',
            health         => 'Current aggregate health of filesystem',
            comments       => 'Any user-written notes.',
            disable        => q(Set to 'yes 'or '1 'to comment out this row.),
        },
    },
    x_stgpoolinfo => {
        cols => [
            qw(cluster_id
              fs_name
              stg_name
              status
              refresh_time
              perf_ref_time
              total_space
              free_space
              parent_fs
              num_disks
              num_disk_items
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id fs_name stg_name)],
        required => [qw(cluster_id fs_name stg_name change health)],
        types    => {
            cluster_id     => 'VARCHAR(128)',
            fs_name        => 'VARCHAR(128)',
            stg_name       => 'VARCHAR(128)',
            status         => 'VARCHAR(128)',
            refresh_time   => 'VARCHAR(128)',
            perf_ref_time  => 'VARCHAR(128)',
            total_space    => 'BIGINT',
            free_space     => 'BIGINT',
            parent_fs      => 'INTEGER',
            num_disks      => 'INTEGER',
            num_disk_items => 'INTEGER',
            change         => 'INTEGER',
            health         => 'INTEGER',
        },
        table_desc   => 'GPFS Storage Pool Configuration',
        descriptions => {
            cluster_id     => 'The cluster id assigned by GPFS',
            fs_name        => 'Owning file system name',
            stg_name       => 'Storage pool name',
            status         => 'Storage pool status',
            refresh_time   => 'Last refresh time',
            perf_ref_time  => 'Last performance metrics refresh time',
            total_space    => 'Total space in storage pool',
            free_space     => 'Total free space in storage pool',
            parent_fs      => 'Owning filesystem',
            num_disks      => 'Number of disks in storage pool',
            num_disk_items => 'Number of disk items in storage pool',
            change         => 'Current change status',
            health         => 'Current aggregate health of storage pool',
            comments       => 'Any user-written notes.',
            disable        => q(Set to 'yes 'or '1 'to comment out this row.),
        },
    },
    x_stgpoolinfo_tmp => {
        cols => [
            qw(cluster_id
              fs_name
              stg_name
              status
              refresh_time
              perf_ref_time
              total_space
              free_space
              parent_fs
              num_disks
              num_disk_items
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id fs_name stg_name)],
        required => [qw(cluster_id fs_name stg_name change health)],
        types    => {
            cluster_id     => 'VARCHAR(128)',
            fs_name        => 'VARCHAR(128)',
            stg_name       => 'VARCHAR(128)',
            status         => 'VARCHAR(128)',
            refresh_time   => 'VARCHAR(128)',
            perf_ref_time  => 'VARCHAR(128)',
            total_space    => 'BIGINT',
            free_space     => 'BIGINT',
            parent_fs      => 'INTEGER',
            num_disks      => 'INTEGER',
            num_disk_items => 'INTEGER',
            change         => 'INTEGER',
            health         => 'INTEGER',
        },
        table_desc   => 'GPFS Storage Pool Configuration scratchpad',
        descriptions => {
            cluster_id     => 'The cluster id assigned by GPFS',
            fs_name        => 'Owning file system name',
            stg_name       => 'Storage pool name',
            status         => 'Storage pool status',
            refresh_time   => 'Last refresh time',
            perf_ref_time  => 'Last performance metrics refresh time',
            total_space    => 'Total space in storage pool',
            free_space     => 'Total free space in storage pool',
            parent_fs      => 'Owning filesystem',
            num_disks      => 'Number of disks in storage pool',
            num_disk_items => 'Number of disk items in storage pool',
            change         => 'Current change status',
            health         => 'Current aggregate health of storage pool',
            comments       => 'Any user-written notes.',
            disable        => q(Set to 'yes 'or '1 'to comment out this row.),
        },
    },
    x_diskinfo => {
        cols => [
            qw(cluster_id
              disk_name
              node_name
              status
              availability
              pool_name
              vol_id
              meta_data
              data
              disk_wait
              total_space
              full_blk_space
              sub_blk_space
              fail_group_id
              is_free
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id disk_name)],
        required => [qw(cluster_id disk_name change health)],
        types    => {
            cluster_id     => 'VARCHAR(128)',
            disk_name      => 'VARCHAR(128)',
            node_name      => 'VARCHAR(128)',
            status         => 'VARCHAR(128)',
            availability   => 'VARCHAR(128)',
            pool_name      => 'VARCHAR(128)',
            vol_id         => 'VARCHAR(128)',
            meta_data      => 'VARCHAR(128)',
            data           => 'VARCHAR(128)',
            disk_wait      => 'VARCHAR(128)',
            total_space    => 'BIGINT',
            full_blk_space => 'BIGINT',
            sub_blk_space  => 'BIGINT',
            fail_group_id  => 'INTEGER',
            is_free        => 'INTEGER',
            change         => 'INTEGER',
            health         => 'INTEGER',
        },
        tablespace =>'XCATTBS32K', 
        table_desc   => 'GPFS Disk Configuration',
        descriptions => {
            cluster_id     => 'The cluster id assigned by GPFS',
            disk_name      => 'Disk name',
            node_name      => 'Owning node',
            status         => 'Current status',
            availability   => 'Current availability',
            pool_name      => 'Associated storage pool',
            vol_id         => 'Volume ID',
            meta_data      => 'Contains metadata',
            data           => 'Contains user data',
            disk_wait      => '',
            total_space    => 'Total space on disk',
            full_blk_space => 'Total full block space',
            sub_blk_space  => 'Total subblock space',
            fail_group_id  => 'Failure group id',
            is_free        => 'Free indicator',
            change         => 'Current change status',
            health         => 'Current aggregate health of disk',
            comments       => 'Any user-written notes.',
            disable        => q(Set to 'yes 'or '1 'to comment out this row.),
        },
    },
    x_diskinfo_tmp => {
        cols => [
            qw(cluster_id
              disk_name
              node_name
              status
              availability
              pool_name
              vol_id
              meta_data
              data
              disk_wait
              total_space
              full_blk_space
              sub_blk_space
              fail_group_id
              is_free
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id disk_name)],
        required => [qw(cluster_id disk_name change health)],
        types    => {
            cluster_id     => 'VARCHAR(128)',
            disk_name      => 'VARCHAR(128)',
            node_name      => 'VARCHAR(128)',
            status         => 'VARCHAR(128)',
            availability   => 'VARCHAR(128)',
            pool_name      => 'VARCHAR(128)',
            vol_id         => 'VARCHAR(128)',
            meta_data      => 'VARCHAR(128)',
            data           => 'VARCHAR(128)',
            disk_wait      => 'VARCHAR(128)',
            total_space    => 'BIGINT',
            full_blk_space => 'BIGINT',
            sub_blk_space  => 'BIGINT',
            fail_group_id  => 'INTEGER',
            is_free        => 'INTEGER',
            change         => 'INTEGER',
            health         => 'INTEGER',
        },
        tablespace =>'XCATTBS32K', 
        table_desc   => 'GPFS Disk Configuration scratchpad',
        descriptions => {
            cluster_id     => 'The cluster id assigned by GPFS',
            disk_name      => 'Disk name',
            node_name      => 'Owning node',
            status         => 'Current status',
            availability   => 'Current availability',
            pool_name      => 'Associated storage pool',
            vol_id         => 'Volume ID',
            meta_data      => 'Contains metadata',
            data           => 'Contains user data',
            disk_wait      => '',
            total_space    => 'Total space on disk',
            full_blk_space => 'Total full block space',
            sub_blk_space  => 'Total subblock space',
            fail_group_id  => 'Failure group id',
            is_free        => 'Free indicator',
            change         => 'Current change status',
            health         => 'Current aggregate health of disk',
            comments       => 'Any user-written notes.',
            disable        => q(Set to 'yes 'or '1 'to comment out this row.),
        },
    },
    x_fsetinfo => {
        cols => [
            qw(cluster_id
              fs_name
              id
              fset_name
              root_inode
              parent_id
              comment
              status
              path
              created
              inodes
              data
              version
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id fs_name id)],
        required => [qw(cluster_id fs_name id change health)],
        types    => {
            cluster_id   => 'VARCHAR(128)',
            fs_name      => 'VARCHAR(128)',
            id           => 'VARCHAR(128)',
            fset_name    => 'VARCHAR(128)',
            root_inode   => 'VARCHAR(128)',
            parent_id    => 'VARCHAR(128)',
            comment      => 'VARCHAR(128)',
            status       => 'VARCHAR(128)',
            path         => 'VARCHAR(128)',
            created      => 'VARCHAR(128)',
            inodes       => 'BIGINT',
            data         => 'BIGINT',
            version      => 'INTEGER',
            change       => 'INTEGER',
            health       => 'INTEGER',
        },
        tablespace =>'XCATTBS16K', 
        table_desc   => 'GPFS Fileset configuration ',
        descriptions => {
            cluster_id   => 'The cluster id assigned by GPFS',
            fs_name      => 'Owning filesystem name',
            id           => 'Fileset id',
            fset_name    => 'Fileset name',
            root_inode   => 'Root inode',
            parent_id    => 'Parent fileset id',
            comment      => 'Fileset comment',
            status       => 'Status of fileset',
            path         => 'Path to fileset',
            created      => 'Fileset creator',
            inodes       => 'Number of inodes in fileset',
            data         => 'Size of data in fileset',
            version      => 'Fileset version',
            change       => 'Current change status',
            health       => 'Current aggregate health of fileset',
            comments     => 'Any user-written notes.',
            disable      => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
    x_fsetinfo_tmp => {
        cols => [
            qw(cluster_id
              fs_name
              id
              fset_name
              root_inode
              parent_id
              comment
              status
              path
              created
              inodes
              data
              version
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id fs_name id)],
        required => [qw(cluster_id fs_name id change health)],
        types    => {
            cluster_id   => 'VARCHAR(128)',
            fs_name      => 'VARCHAR(128)',
            id           => 'VARCHAR(128)',
            fset_name    => 'VARCHAR(128)',
            root_inode   => 'VARCHAR(128)',
            parent_id    => 'VARCHAR(128)',
            comment      => 'VARCHAR(128)',
            status       => 'VARCHAR(128)',
            path         => 'VARCHAR(128)',
            created      => 'VARCHAR(128)',
            inodes       => 'BIGINT',
            data         => 'BIGINT',
            version      => 'INTEGER',
            change       => 'INTEGER',
            health       => 'INTEGER',
        },
        tablespace =>'XCATTBS16K', 
        table_desc   => 'GPFS Fileset configuration scratchpad',
        descriptions => {
            cluster_id   => 'The cluster id assigned by GPFS',
            fs_name      => 'Owning filesystem name',
            id           => 'Fileset id',
            fset_name    => 'Fileset name',
            root_inode   => 'Root inode',
            parent_id    => 'Parent fileset id',
            comment      => 'Fileset comment',
            status       => 'Status of fileset',
            path         => 'Path to fileset',
            created      => 'Fileset creator',
            inodes       => 'Number of inodes in fileset',
            data         => 'Size of data in fileset',
            version      => 'Fileset version',
            change       => 'Current change status',
            health       => 'Current aggregate health of fileset',
            comments     => 'Any user-written notes.',
            disable      => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
    x_rginfo => {
        cols => [
            qw(cluster_id
              rg_name
              rg_act_svr
              rg_svrs
              rg_id
              rg_das
              rg_vdisks
              rg_pdisks
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id rg_name)],
        required => [qw(cluster_id rg_name change health)],
        types    => {
            cluster_id => 'VARCHAR(128)',
            rg_name    => 'VARCHAR(64)',
            rg_act_svr => 'VARCHAR(32)',
            rg_svrs    => 'VARCHAR(64)',
            rg_id      => 'VARCHAR(20)',
            rg_das     => 'INTEGER',
            rg_vdisks  => 'INTEGER',
            rg_pdisks  => 'INTEGER',
            change     => 'INTEGER',
            health     => 'INTEGER',
        },
        table_desc   => 'GPFS Recovery Group configuration',
        descriptions => {
            cluster_id => 'The cluster id assigned by GPFS',
            rg_name    => 'Recovery Group name',
            rg_act_svr => 'Recovery Group active server',
            rg_svrs    => 'Recovery Group servers',
            rg_id      => 'Recovery Group id',
            rg_das     => 'Number of declustered arrays',
            rg_vdisks  => 'Number of vdisks',
            rg_pdisks  => 'Number of pdisks',
            change     => 'Current change status',
            health     => 'Current aggregate health of recovery group',
            comments   => 'Any user-written notes.',
            disable    => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
    x_rginfo_tmp => {
        cols => [
            qw(cluster_id
              rg_name
              rg_act_svr
              rg_svrs
              rg_id
              rg_das
              rg_vdisks
              rg_pdisks
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id rg_name)],
        required => [qw(cluster_id rg_name change health)],
        types    => {
            cluster_id => 'VARCHAR(128)',
            rg_name    => 'VARCHAR(64)',
            rg_act_svr => 'VARCHAR(32)',
            rg_svrs    => 'VARCHAR(64)',
            rg_id      => 'VARCHAR(20)',
            rg_das     => 'INTEGER',
            rg_vdisks  => 'INTEGER',
            rg_pdisks  => 'INTEGER',
            change     => 'INTEGER',
            health     => 'INTEGER',
        },
        table_desc   => 'GPFS Recovery Group configuration scratchpad',
        descriptions => {
            cluster_id => 'The cluster id assigned by GPFS',
            rg_name    => 'Recovery Group name',
            rg_act_svr => 'Recovery Group active server',
            rg_svrs    => 'Recovery Group servers',
            rg_id      => 'Recovery Group id',
            rg_das     => 'Number of declustered arrays',
            rg_vdisks  => 'Number of vdisks',
            rg_pdisks  => 'Number of pdisks',
            change     => 'Current change status',
            health     => 'Current aggregate health of recovery group',
            comments   => 'Any user-written notes.',
            disable    => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
    x_dainfo => {
        cols => [
            qw(cluster_id
              rg_name
              da_name
              da_bg_task
              da_task_priority
              da_need_service  
              da_task_percent
              da_vdisks
              da_pdisks
              da_spares
              da_replace_thres
              da_free_space
              da_scrub_dura
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id rg_name da_name)],
        required => [qw(cluster_id rg_name da_name change health)],
        types    => {
            cluster_id       => 'VARCHAR(128)',
            rg_name          => 'VARCHAR(64)',
            da_name          => 'VARCHAR(64)',
            da_bg_task       => 'VARCHAR(32)',
            da_task_priority => 'VARCHAR(32)',
            da_need_service  => 'VARCHAR(8)',
            da_task_percent  => 'INTEGER',
            da_vdisks        => 'INTEGER',
            da_pdisks        => 'INTEGER',
            da_spares        => 'INTEGER',
            da_replace_thres => 'INTEGER',
            da_free_space    => 'BIGINT',
            da_scrub_dura    => 'INTEGER',
            change           => 'INTEGER',
            health           => 'INTEGER',
        },
        tablespace =>'XCATTBS16K', 
        table_desc   => 'GPFS Declustered Array configuration',
        descriptions => {
            cluster_id       => 'The cluster id assigned by GPFS',
            rg_name          => 'Recovery group name',
            da_name          => 'Declustered array name',
            da_bg_task       => 'Active background task',
            da_task_priority => 'Task priority',
            da_need_service  => 'If not healthy, need service',
            da_task_percent  => 'Task percent complete',
            da_vdisks        => 'Number of vdisks',
            da_pdisks        => 'Number of pdisks',
            da_spares        => 'Number of spare disks',
            da_replace_thres => 'Replacement threshold',
            da_free_space    => 'Free space',
            da_scrub_dura    => 'Scrub duration',
            change           => 'Current change status',
            health           => 'Current aggregate health of declustered array',
            comments         => 'Any user-written notes.',
            disable          => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
    x_dainfo_tmp => {
        cols => [
            qw(cluster_id
              rg_name
              da_name
              da_bg_task
              da_task_priority
              da_need_service
              da_task_percent
              da_vdisks
              da_pdisks
              da_spares
              da_replace_thres
              da_free_space
              da_scrub_dura
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id rg_name da_name)],
        required => [qw(cluster_id rg_name da_name change health)],
        types    => {
            cluster_id       => 'VARCHAR(128)',
            rg_name          => 'VARCHAR(64)',
            da_name          => 'VARCHAR(64)',
            da_bg_task       => 'VARCHAR(32)',
            da_task_priority => 'VARCHAR(32)',
            da_need_service  => 'VARCHAR(8)',
            da_task_percent  => 'INTEGER',
            da_vdisks        => 'INTEGER',
            da_pdisks        => 'INTEGER',
            da_spares        => 'INTEGER',
            da_replace_thres => 'INTEGER',
            da_free_space    => 'INTEGER',
            da_scrub_dura    => 'INTEGER',
            change           => 'INTEGER',
            health           => 'INTEGER',
        },
        tablespace =>'XCATTBS16K', 
        table_desc   => 'GPFS Declustered Array configuration scratchpad',
        descriptions => {
            cluster_id       => 'The cluster id assigned by GPFS',
            rg_name          => 'Recovery group name',
            da_name          => 'Declustered array name',
            da_bg_task       => 'Active background task',
            da_task_priority => 'Task priority',
            da_need_service  => 'If not healthy, need service',
            da_task_percent  => 'Task percent complete',
            da_vdisks        => 'Number of vdisks',
            da_pdisks        => 'Number of pdisks',
            da_spares        => 'Number of spare disks',
            da_replace_thres => 'Replacement threshold',
            da_free_space    => 'Free space',
            da_scrub_dura    => 'Scrub duration',
            change           => 'Current change status',
            health           => 'Current aggregate health of declustered array',
            comments         => 'Any user-written notes.',
            disable          => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
    x_vdiskinfo => {
        cols => [
            qw(cluster_id
              rg_name
              da_name
              vdisk_name
              vdisk_raid_code
              vdisk_state
              vdisk_remarks
              vdisk_block_size
              vdisk_size
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id rg_name da_name vdisk_name)],
        required => [qw(cluster_id rg_name da_name vdisk_name change health)],
        types    => {
            cluster_id       => 'VARCHAR(128)',
            rg_name          => 'VARCHAR(64)',
            da_name          => 'VARCHAR(64)',
            vdisk_name       => 'VARCHAR(64)',
            vdisk_raid_code  => 'VARCHAR(32)',
            vdisk_state      => 'VARCHAR(64)',
            vdisk_remarks    => 'VARCHAR(32)',
            vdisk_block_size => 'INTEGER',
            vdisk_size       => 'BIGINT',
            change           => 'INTEGER',
            health           => 'INTEGER',
        },
        tablespace =>'XCATTBS32K', 
        table_desc   => 'GPFS vdisk configuration',
        descriptions => {
            cluster_id       => 'The cluster id assigned by GPFS',
            rg_name          => 'Recovery group name',
            da_name          => 'Declustered array name',
            vdisk_name       => 'vdisk name',
            vdisk_raid_code  => 'vdisk',
            vdisk_state      => 'Current state of the vdisk',
            vdisk_remarks    => 'vdisk information',
            vdisk_block_size => 'vdisk block size',
            vdisk_size       => 'Total vdisk size',
            change           => 'Current change status',
            health           => 'Current aggregate health of vdisk',
            comments         => 'Any user-written notes.',
            disable          => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
    x_vdiskinfo_tmp => {
        cols => [
            qw(cluster_id
              rg_name
              da_name
              vdisk_name
              vdisk_raid_code
              vdisk_state
              vdisk_remarks
              vdisk_block_size
              vdisk_size
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id rg_name da_name vdisk_name)],
        required => [qw(cluster_id rg_name da_name vdisk_name change health)],
        types    => {
            cluster_id       => 'VARCHAR(128)',
            rg_name          => 'VARCHAR(64)',
            da_name          => 'VARCHAR(64)',
            vdisk_name       => 'VARCHAR(64)',
            vdisk_raid_code  => 'VARCHAR(32)',
            vdisk_state      => 'VARCHAR(64)',
            vdisk_remarks    => 'VARCHAR(32)',
            vdisk_block_size => 'INTEGER',
            vdisk_size       => 'BIGINT',
            change           => 'INTEGER',
            health           => 'INTEGER',
        },
        tablespace =>'XCATTBS32K', 
        table_desc   => 'GPFS vdisk configuration scratchpad',
        descriptions => {
            cluster_id       => 'The cluster id assigned by GPFS',
            rg_name          => 'Recovery group name',
            da_name          => 'Declustered array name',
            vdisk_name       => 'vdisk name',
            vdisk_raid_code  => 'vdisk',
            vdisk_state      => 'Current state of the vdisk',
            vdisk_remarks    => 'vdisk information',
            vdisk_block_size => 'vdisk block size',
            vdisk_size       => 'Total vdisk size',
            change           => 'Current change status',
            health           => 'Current aggregate health of vdisk',
            comments         => 'Any user-written notes.',
            disable          => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
    x_pdiskinfo => {
        cols => [
            qw(cluster_id
              rg_name
              da_name
              pdisk_name
              pdisk_dev_path
              pdisk_state
              pdisk_fru
              pdisk_location
              pdisk_repl_prior
              pdisk_free_space
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id rg_name da_name pdisk_name)],
        required => [qw(cluster_id rg_name da_name pdisk_name change health)],
        types    => {
            cluster_id       => 'VARCHAR(128)',
            rg_name          => 'VARCHAR(64)',
            da_name          => 'VARCHAR(64)',
            pdisk_name       => 'VARCHAR(64)',
            pdisk_dev_path   => 'VARCHAR(64)',
            pdisk_state      => 'VARCHAR(160)',
            pdisk_fru        => 'VARCHAR(32)',
            pdisk_location   => 'VARCHAR(32)',
            pdisk_repl_prior => 'INTEGER',
            pdisk_free_space => 'BIGINT',
            change           => 'INTEGER',
            health           => 'INTEGER',
        },
        tablespace =>'XCATTBS32K', 
        table_desc   => 'GPFS pdisk configuration',
        descriptions => {
            cluster_id       => 'The cluster id assigned by GPFS',
            rg_name          => 'Recovery group name',
            da_name          => 'Declustered array name',
            pdisk_name       => 'pdisk name',
            pdisk_dev_path   => 'pdisk device path',
            pdisk_state      => 'Current pdisk state',
            pdisk_fru        => 'pdisk FRU information',
            pdisk_location   => 'pdisk physical locatio',
            pdisk_repl_prior => 'pdisk replacement priority',
            pdisk_free_space => 'Total free space on pdisk',
            change           => 'Current change status',
            health           => 'Current aggregate health of pdisk',
            comments         => 'Any user-written notes.',
            disable          => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
    x_pdiskinfo_tmp => {
        cols => [
            qw(cluster_id
              rg_name
              da_name
              pdisk_name
              pdisk_dev_path
              pdisk_state
              pdisk_fru
              pdisk_location
              pdisk_repl_prior
              pdisk_free_space
              change
              health
              comments
              disable
              )
        ],
        keys     => [qw(cluster_id rg_name da_name pdisk_name)],
        required => [qw(cluster_id rg_name da_name pdisk_name change health)],
        types    => {
            cluster_id       => 'VARCHAR(128)',
            rg_name          => 'VARCHAR(64)',
            da_name          => 'VARCHAR(64)',
            pdisk_name       => 'VARCHAR(64)',
            pdisk_dev_path   => 'VARCHAR(64)',
            pdisk_state      => 'VARCHAR(160)',
            pdisk_fru        => 'VARCHAR(32)',
            pdisk_location   => 'VARCHAR(32)',
            pdisk_repl_prior => 'INTEGER',
            pdisk_free_space => 'BIGINT',
            change           => 'INTEGER',
            health           => 'INTEGER',
        },
        tablespace =>'XCATTBS32K', 
        table_desc   => 'GPFS pdisk configuration scratchpad',
        descriptions => {
            cluster_id       => 'The cluster id assigned by GPFS',
            rg_name          => 'Recovery group name',
            da_name          => 'Declustered array name',
            pdisk_name       => 'pdisk name',
            pdisk_dev_path   => 'pdisk device path',
            pdisk_state      => 'Current pdisk state',
            pdisk_fru        => 'pdisk FRU information',
            pdisk_location   => 'pdisk physical locatio',
            pdisk_repl_prior => 'pdisk replacement priority',
            pdisk_free_space => 'Total free space on pdisk',
            change           => 'Current change status',
            health           => 'Current aggregate health of pdisk',
            comments         => 'Any user-written notes.',
            disable          => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
);    # end of tabspec definition

1;
