#!/usr/bin/perl
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

$RES::Condition{'TealAnyNodeEventNotify_H'} = {
        Name => q(TealAnyNodeEventNotify_H),
        ResourceClass => q(IBM.Condition),
        EventExpression => q(LastEvent.Occurred==1 && LastEvent.ErrNum==0 && (LastEvent.EventFlags & 0x0233) == 0),
        RearmExpression => q(LastEvent.Occurred==1 && LastEvent.ErrNum==0 && (LastEvent.EventFlags & 3) ==1),   
        EventDescription => q(This condition collects all the TealAnyNodeEventNotify events from the service nodes. An event will be generated whenever there is output from running sensor related to any Teal Event Logged.),
        SelectionString => q(Name="TealAnyNodeEventNotify"),
        ManagementScope => q(4),
        Severity => q(0),
        NoToggleExprFlag => q(1),
};
1;
