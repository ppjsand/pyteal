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
Summary: Toolkit for Event Analysis and Logging Loadleveler Connector  	
Name: teal-pnsd		
Version: 1.1.0.2
Release: 2

License: EPL 1.0
Group: Applications/System
Source: pyteal-1.1.0.1.tar.gz 
Distribution: pyteal
URL: http://pyteal.sourceforge.net

Requires: teal-base >= 1.1.0.2

%description
This package provides the TEAL connector for PNSD. It also provides the additional plug-ins to 
support the additional user data, rules and TEAL framework configuration for reporting TEAL Alerts

# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%prep
%setup -n pyteal-code

%build
autoconf
%configure --enable-connector=pnsd
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall


%pre
/sbin/service teal stop

%post
/sbin/service teal start

%preun
if  [ $1 -eq 0 ]; then
/sbin/service teal stop
fi

%postun
if  [ $1 -eq 0 ]; then
/sbin/service teal start
fi

%files
%attr( 755, bin, bin ) /install/postscripts/rmcmon/resources/node/IBM.Sensor/TealPnsdStat.pm
%attr( 755, bin, bin ) /install/postscripts/rmcmon/resources/sn/IBM.Condition/TealAnyNodePnsdStat.pm
%attr( 755, bin, bin ) /install/postscripts/rmcmon/scripts/tlpnsd_sensor
%attr( 755, bin, bin ) /opt/teal/ibm/teal/connector/pnsd.py
%attr( 644, bin, bin ) /opt/teal/data/ibm/pnsd/xml/PNSD_GEAR_rules.xml
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.Condition/TealAnyNodePnsdStat.pm
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.Condition/TealAnyNodePnsdStat_H.pm
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.EventResponse/TealLogPnsdEvent.pm 
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.EventResponse/TealLogPnsdEvent_H.pm 

%attr( 644, bin, bin ) /etc/teal/pnsd.conf

