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

$RES::Condition{'TealAnyNodeEventNotify'} = {
        Name => q(TealAnyNodeEventNotify),
        ResourceClass => q(IBM.Sensor),
        EventExpression => q(Uint32 != 0),
        EventDescription => q(An event will be generated whenever there is outpout from running sensor related to any serviceable events.),
        SelectionString => q(Name="TealEventNotify"),
        ManagementScope => q(4),
        Severity => q(0),
};
1;

