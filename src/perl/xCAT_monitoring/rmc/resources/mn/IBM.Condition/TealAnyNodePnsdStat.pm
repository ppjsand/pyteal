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

$RES::Condition{'TealAnyNodePnsdStat'} = {
    Name => q(TealAnyNodePnsdStat),
    ResourceClass => q(IBM.Sensor),
    EventExpression => q(Float64 >= 0.01),
    EventDescription => q(An event will be generated when the pnsd_stat reports a retransmit exceeds the configured value),
    RearmExpression => q(Float64 < 0.01),
    RearmDescription => q(A rearm event will be generated when the pnsd_stat reports a retransmit rate less than the configured value),
    SelectionString => q(Name="TealPnsdStat"),
    ManagementScope => q(4),
    Severity => q(1),
};
1;
