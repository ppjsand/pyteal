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
package xCAT_schema::Teal_ll;

# This file contains the schema necessary to support the Loadleveler component in the TEAL framework

%tabspec = (
     x_LL_1_1 => {
        cols => [qw(rec_id time_occurred time_logged msg_type message detail comments disable)],
        keys => [qw(rec_id)],
        required => [qw(rec_id time_occurred time_logged message detail)],
        types => {
            rec_id => 'BIGINT',
            time_occurred => 'BIGINT',
            time_logged => 'BIGINT',
            msg_type => 'CHAR(1)',
            message => 'VARCHAR(1024)',
            detail => 'VARCHAR(1024)',
        },
        tablespace =>'XCATTBS16K', 
        table_desc => 'TEAL Loadleveler Event Extended Data',
        descriptions => {
            rec_id => 'Database record id of common event',
            time_occurred => 'Time event occurred in Loadleveler - encoded value',
            time_logged => 'Time event was logged in Loadleveler RAS subsystem',
            msg_type => 'Message type (E)rror, (W)arning, (I)nfo, (T)race',
            message => 'Event message used in Alert',
            detail => 'Event details',
            comments => 'Any user-written notes.',
            disable => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
); # end of tabspec definition

1;    
 