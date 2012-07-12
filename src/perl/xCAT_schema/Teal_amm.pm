# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2012
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog
package xCAT_schema::Teal_amm;

# This file contains the schema necessary to support the AMM component in the TEAL framework

%tabspec = (
     x_AMM_1_1 => {
        cols => [qw(rec_id 
        			app_id 
        			sp_txt_id 
        			sys_uuid 
        			sys_sern 
        			app_type 
        			priority 
        			msg_text 
        			host_contact 
        			host_location
        			blade_name
        			blade_sern 
        			blade_uuid 
        			evt_name 
        			source_id
					call_home_flag 
					sys_ip_address 
					sys_machine_model 
					blade_machine_model
					comments 
					disable)],
        keys => [qw(rec_id)],
        required => [qw(rec_id msg_txt priority)],
        types => {
            rec_id => 'BIGINT',
            app_id => 'VARCHAR(255)',
            sp_txt_id => 'VARCHAR(255)',
            sys_uuid => 'VARCHAR(255)',
            sys_sern => 'VARCHAR(255)',
            app_type => 'INTEGER',
            priority => 'INTEGER',
            msg_text => 'VARCHAR(255)',
            host_contact => 'VARCHAR(255)',
            host_location => 'VARCHAR(255)',
            blade_name => 'VARCHAR(255)',
            blade_sern => 'VARCHAR(255)',
            blade_uuid => 'VARCHAR(255)',
            evt_name => 'INTEGER',
            source_id => 'VARCHAR(255)',
            call_home_flag => 'INTEGER',
            sys_ip_address => 'VARCHAR(255)',
            sys_machine_model => 'VARCHAR(255)',
            blade_machine_model => 'VARCHAR(255)'
        },
        engine => 'InnoDB',  
        tablespace =>'XCATTBS16K', 
        table_desc => 'TEAL AMM Event Extended Data',
        descriptions => {
            rec_id => 'Database record id of common event',
            app_id => 'Application ID.',
            sp_txt_id => 'SP System Identification - Text Identification.',
            sys_uuid => 'Host System UUID(Universal Unique ID).',
            sys_sern => 'Host System Serial Number.',
            app_type => 'Application Alert Type - Event Number ID.',
            priority => 'Alert Severity Value: Critical Alert(0), Major(1), Non-Critical Alert(2), System Alert(4), Recovery Alert(8), Informational Only Alert(255)',
            msg_text => 'Alert Message Text.)',
            host_contact => 'Host Contact',
            host_location => 'Host Location',
            blade_name => 'Blade Name',
            blade_sern => 'Blade Serial Number.',
            blade_uuid => 'Blade UUID(Universal Unique ID).',
            evt_name => 'The 32 bit event name associated with the event that caused the trap.',
            source_id => 'The source identifier associated with the event that caused the trap.',
            call_home_flag => 'The call home flag associated with the event that caused the trap.',
            sys_ip_address => 'The AMM IP Address',
            sys_machine_model => 'Chassis Machine Type/Module',
            blade_machine_model => 'Blade Machine Type/Module',
            comments => 'Any user-written notes.',
            disable => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
); # end of tabspec definition

1;    

