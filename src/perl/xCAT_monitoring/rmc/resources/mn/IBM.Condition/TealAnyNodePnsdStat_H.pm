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

$RES::Condition{'TealAnyNodePnsdStat_H'} = {
    Name => q(TealAnyNodePnsdStat_H),
    ResourceClass => q(IBM.Condition),
    EventDescription => q(This condition collects all the TealAnyNodePnsdStat events from the service nodes.),
    EventExpression => q(LastEvent.Occurred==1 && LastEvent.ErrNum==0 && (LastEvent.EventFlags & 0x0233) == 0),
    RearmExpression => q(LastEvent.Occurred==1 && LastEvent.ErrNum==0 && (LastEvent.EventFlags & 3) == 1),
    SelectionString => q(Name="TealAnyNodePnsdStat"),
    ManagementScope => q(4),
    Severity => q(1),
    NoToggleExprFlag => q(1),
};
1;
