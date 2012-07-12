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
package xCAT_schema::Teal_ib;

# This file contains the schema necessary to support the InfiniBand component in the TEAL framework

%tabspec = (
     x_IB_1_1 => {
        cols => [qw(rec_id severity category description comments disable)],
        keys => [qw(rec_id)],
        required => [qw(rec_id)],
        types => {
            rec_id => 'BIGINT',
            severity => 'VARCHAR(16)',
            category => 'VARCHAR(32)',
            description => 'VARCHAR(256)',
        },
        engine => 'InnoDB',
        tablespace =>'XCATTBS16K', 
        table_desc => 'TEAL Infiniband Event Extended Data',
        descriptions => {
            rec_id => 'Database record id of common event',
            severity => 'Severity of the event',
            category => 'Event category',
            description => 'Detailed description of the event',
            comments => 'Any user-written notes.',
            disable => q(Set to 'yes' or '1' to comment out this row.),
        },
    },
); # end of tabspec definition

1;    
 
