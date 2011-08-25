#!/usr/bin/perl
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
BEGIN
{
  $::XCATROOT = $ENV{'XCATROOT'} ? $ENV{'XCATROOT'} : '/opt/xcat';
}

$RES::Sensor{'TealSendAlert'} = {
    Name => q(TealSendAlert),
    Command => "/tmp/fake",
    UserName => q(root),
    RefreshInterval => q(0),
    ControlFlags => q(0), #change to 8 for rsct 2.5.3.0 and greater
    Description => q(This sensor is refreshed when an Alert is reported by the TEAL framework),
};
1;

