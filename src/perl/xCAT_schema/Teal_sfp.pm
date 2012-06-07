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
package xCAT_schema::Teal_sfp;

# This file contains the schema necessary to support the Service Focal Point component in the TEAL framework

%tabspec = (
     x_SFP_1_1 => {
        cols => [qw(rec_id prob_num description call_home fru_list sfp_raw_data comments disable)],
        keys => [qw(rec_id)],
        required => [qw(rec_id prob_num description)],
        types => {
            rec_id => 'BIGINT',
            prob_num => 'INTEGER',
            description => 'VARCHAR(256)',
            call_home => 'CHAR(1)',
            fru_list => 'VARCHAR(1536)',
            sfp_raw_data => 'VARCHAR(2048)',
        },
        engine => 'InnoDB',
        tablespace =>'XCATTBS32K', 
        table_desc => 'TEAL Loadleveler Event Extended Data',
        descriptions => {
            rec_id => 'Database record id of common event',
            prob_num => 'Problem number assigned by HMC',
            description => 'Description from serviceable event',
            call_home => 'Call home indicator from Event',
            fru_list => 'FRU information for each FRU listed in the serviceable event',
            sfp_raw_data => 'Additional event details for reference',
            comments => 'Any user-written notes.',
            disable => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
); # end of tabspec definition

1;    
