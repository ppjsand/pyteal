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
package xCAT_schema::Teal_mysql;

# This file contains the schema necessary to support the TEAL framework

%tabspec = (
    x_tealeventlog => { 
        cols => [qw(rec_id event_id time_logged time_occurred src_comp src_loc_type src_loc rpt_comp rpt_loc_type rpt_loc event_cnt elapsed_time raw_data_fmt raw_data comments disable)],
        keys => [qw(rec_id)],
        required => [qw(event_id time_logged time_occurred src_loc_type src_comp src_loc raw_data_fmt)],
        types => {
           rec_id => 'BIGINT AUTO_INCREMENT',
           event_id => 'CHAR(8)',
           time_logged => 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
           time_occurred => 'TIMESTAMP',
           src_comp => 'VARCHAR(128)',
           src_loc_type => 'VARCHAR(2)',
           src_loc => 'VARCHAR(255)',
           rpt_comp => 'VARCHAR(128)',
           rpt_loc_type => 'VARCHAR(2)',
           rpt_loc => 'VARCHAR(255)',
           event_cnt => 'INTEGER',
           elapsed_time => 'BIGINT UNSIGNED',
           raw_data_fmt => 'BIGINT UNSIGNED',
           raw_data => 'VARCHAR(1024)'
        },
        table_desc => 'TEAL Event Log',
        descriptions => {
           rec_id => 'Unique id assigned by DB for each item. It will be auto incremented on insertion.',
           event_id => 'A unique id within the Source Component for events that occur. This is defined by the component.',
           time_occurred => 'Time that event occurred in the cluster. This should be the local time value on the hardware that created the event.',
           time_logged => 'Time that event was inserted into the event log.',
           src_comp => 'The component that is detecting the event. This is a freeform user defined string.',
           src_loc_type => 'Type of location code. (H) - Hardware, (S) - Software, (D) - Device, (J) - Job.',
           src_loc => 'Component location that created the event',
           rpt_comp => 'Component reporting on behalf of source component. Set only if different from source.',
           rpt_loc_type => 'Type of location code.',
           rpt_loc => 'Component location that reported the event.',
           event_cnt => 'In certain high-volume error conditions on the system, the EA framework may collapse like events into one event. This count will indicate how many of this event are compressed into this one event.',
           elapsed_time => 'When the event count is non-zero, this field will indicate the amount of time between the first and last event.',
           raw_data_fmt => 'Format information for raw_data field.',
           raw_data => 'Component specific event information.',
           comments => 'Any user-written notes.',
           disable => q(Set to 'yes' or '1' to comment out this row.)
        },
    },
    
    x_tealalertlog => { 
        cols => [qw(rec_id alert_id creation_time severity urgency event_loc_type event_loc fru_loc recommendation reason src_name state raw_data comments disable)],
        keys => [qw(rec_id)],
        required => [qw(alert_id severity urgency event_loc_type event_loc recommendation reason src_name state)],
        types => {
           rec_id => 'BIGINT AUTO_INCREMENT',
           alert_id => 'CHAR(8)',
           creation_time => 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
           severity => 'CHAR(1)',
           urgency => 'CHAR(1)',
           event_loc_type => 'VARCHAR(2)',
           event_loc => 'VARCHAR(255)',
           fru_loc => 'VARCHAR(512)',
           recommendation => 'VARCHAR(2048)',
           reason => 'VARCHAR(512)',
           src_name => 'VARCHAR(64)',
           state => 'TINYINT',
           raw_data => 'VARCHAR(2048)'
        },
        table_desc => 'TEAL Alert Log',
        descriptions => {
           rec_id => 'Unique id assigned by DB for each item. It will be auto incremented on insertion.',
           alert_id => 'A unique id within the entire system for alerts that occur. This is defined by the component.',
           creation_time => 'Time that alert was created in the DB. This will be automatically generated on insertion',
           severity => '(F)atal - Unrecoverable system error has occurred, (E)rror - Unrecoverable error. Loss of function but system can still run, (W)arning - Non-critical failure or impending failure, (I)nfo - Informational message only. No action required.',
           urgency => '(I)mmediate - must take corrective action now, (S)chedule - schedule corrective action as soon as possible, (N)ormal - schedule corrective action during normal working hours, (D)efer - corrective action can wait until the next maintenance window, (O)ptional - corrective action can be taken at any time that is most convenient to the client.',
           event_loc_type => 'Type of location code. (H) - Hardware, (S) - Software, (D) - Device, (J) - Job.',
           event_loc => 'Logical location of failing/reporting component.',
           fru_loc => 'pSeries FRU location code.',
           recommendation => 'Recommended action to take.',
           reason => 'Reason for failure.',
           src_name => 'Reporting analyzer.',
           state => 'Current state of event.',
           raw_data => 'Additional alert data.',
           comments => 'Any user-written notes.',
           disable => q(Set to 'yes' or '1' to comment out this row.)
        },
    },
    
    x_tealalert2alert => {
          cols => [qw(assoc_id alert_recid assoc_type t_alert_recid comments disable)], 
        keys => [qw(assoc_id)],
        required => [qw(alert_recid assoc_type)],
        types => { 
           assoc_id => 'BIGINT AUTO_INCREMENT',
           alert_recid => 'BIGINT',
           assoc_type => 'CHAR(1)',
           t_alert_recid => 'BIGINT'
        },
        table_desc => 'TEAL Alert 2 Alert Table. Lists what Alerts are associated with a particular Alert',
        descriptions => {
            assoc_id => 'Database record id of association.',
            alert_recid => 'The Alert record id reported in the Alert Log.',
            assoc_type => 'Indicates type of association. (S)uppresses, (D)uplicate, or (C)ondition.',
            t_alert_recid => 'The record id of the alert that is the target of the association.',
            comments => 'Any user-written notes.',
            disable => q(Set to 'yes' or '1' to comment out this row.)
        },
    },
    
    x_tealalert2event => {
          cols => [qw(assoc_id alert_recid assoc_type t_event_recid comments disable)], 
        keys => [qw(assoc_id)],
        required => [qw(alert_recid assoc_type)],
        types => { 
           assoc_id => 'BIGINT AUTO_INCREMENT',
           alert_recid => 'BIGINT',
           assoc_type => 'CHAR(1)',
           t_event_recid => 'BIGINT'
        },
        table_desc => 'TEAL Alert 2 Event Table. Lists what Events are associated with a particular Alert',
        descriptions => {
            assoc_id => 'Database record id of association.',
            alert_recid => 'The Alert record id reported in the Alert Log.',
            assoc_type => 'Indicates type of association. (S)uppresses or (C)ondition.',
            t_event_recid => 'The record id of the event that is the target of the association.',
            comments => 'Any user-written notes.',
            disable => q(Set to 'yes' or '1' to comment out this row.)
        },
    },
    
    x_tealcheckpoint => {
        cols => [qw(chkpt_id name status event_recid data comments disable)],
        keys => [qw(chkpt_id)],
        types => {
            chkpt_id => 'BIGINT AUTO_INCREMENT',
            name => 'VARCHAR(128)', 
            status => 'CHAR(1)',
            event_recid => 'BIGINT',
            data => 'VARCHAR(1024)'
        },
        table_desc => 'TEAL Event Processing Checkpoint Table.',
        descriptions => {
            chkpt_id => 'Database record id of checkpoint',
            status => 'Indicates the last status checkpointed',
            event_recid => 'Record id of last event processed',
            data => 'Data specific to this checkpoint',
            comments => 'Any user-written notes.',
            disable => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
); # end of tabspec definition

1;    
