# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2010,2011
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog
package xCAT_schema::Teal_isnm;

# This file contains the schema necessary to support the ISNM component in the TEAL framework
  
%tabspec = (
     x_CNM_1_2 => {
        cols => [qw(rec_id 
        			eed_loc_info 
        			encl_mtms 
        			pwr_ctrl_mtms 
        			neighbor_loc_type 
        			neighbor_loc 
        			recovery_file_path 
        			isnm_raw_data 
        			local_port 
        			local_torrent 
        			local_planar 
        			local_om1
                    local_om2
        			nbr_port
        			nbr_torrent
        			nbr_planar
        			nbr_om1
                    nbr_om2
                    global_counter
                    comments
                    disable
        			)],
        keys => [qw(rec_id)],
        required => [qw(rec_id eed_loc_info encl_mtms pwr_ctrl_mtms recovery_file_path)],
        types => {
            rec_id => 'BIGINT',
            eed_loc_info => 'VARCHAR(64)',
            encl_mtms => 'VARCHAR(20)',
            pwr_ctrl_mtms => 'VARCHAR(20)',
            neighbor_loc_type => 'VARCHAR(2)',
            neighbor_loc => 'VARCHAR(256)',
            recovery_file_path => 'VARCHAR(32)',
            isnm_raw_data => 'VARCHAR(1024)',
   			local_port => 'VARCHAR(256)', 
   			local_torrent => 'VARCHAR(256)',
   			local_planar => 'VARCHAR(256)',
   			local_om1 => 'VARCHAR(256)',
            local_om2 => 'VARCHAR(256)',
   			nbr_port => 'VARCHAR(256)',
   			nbr_torrent => 'VARCHAR(256)',
   			nbr_planar => 'VARCHAR(256)',
            nbr_om1 => 'VARCHAR(256)',
   			nbr_om2 => 'VARCHAR(256)',
   			global_counter => 'BIGINT',
        },
        engine => 'InnoDB',
        tablespace =>'XCATTBS32K',        
        table_desc => 'TEAL ISNM Event Extended Data',
        descriptions => {
            rec_id => 'Database record id of common event',
            eed_loc_info => 'Location of extended error data saved by CNM',
            encl_mtms => 'The enclosure machine type/model number/serial number',
            pwr_ctrl_mtms => 'The power enclosure machine type/model number/serial number',
            neighbor_loc_type => 'Neighbor location type',
            neighbor_loc_ => 'Neighbor location to the source event location',
            recovery_file_path => 'Recover file path',
            isnm_raw_data => 'Additional miscellaneous error information',
   			local_port => 'The local port service location', 
   			local_torrent => 'The location and VPD information for the local hub module',
   			local_planar => 'The location and VPD information for the local planar',
            local_om1 => 'The location information for the local optical module 1',
            local_om2 => 'The location information for the local optical module 2',
   			nbr_port => 'The neighbor port service location',
   			nbr_torrent => 'The location and VPD information for the neighbor hub module',
   			nbr_planar => 'The location and VPD information for the neighbor planar',
            nbr_om1 => 'The location information for the neighbor optical module 1',
   			nbr_om2 => 'The location information for the neighbor optical module 2',
   			global_counter => 'Global counter for network',
            comments => 'Any user-written notes.',
            disable => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
); # end of tabspec definition

1;    
 