#!/usr/bin/perl
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

$RES::Condition{'GPFSConnectorMonitor'} = {
        Name => q(GPFSConnectorMonitor),
        ResourceClass => q(IBM.Program),
        EventExpression => q(Processes.CurPidCount == 0),
        EventDescription => q(An event will be generated whenever there is no GPFS connector running on the collector node.),
        RearmExpression => q(Processes.CurPidCount != 0),
        RearmDescription => q(A rearm event will be generated when the GPFS connector on the node is brought up again),
        SelectionString => q(ProgramName=="tlgpfsmon"),
        ManagementScope => q(1),
        Severity => q(2),
};
1;
