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
Summary: Toolkit for Event Analysis and Logging Service Focal Point Connector  	
Name: teal-sfp		
Version: 1.1.0.2
Release: 2

License: EPL 1.0
Group: Applications/System
Source: pyteal-1.1.0.1.tar.gz
Distribution: pyteal
URL: http://pyteal.sourceforge.net

Requires: teal-base >= 1.1.0.2

%description
This package provides the TEAL connector for the Service Focal Point. It also provides the additional plug-ins to 
support the additional user data, rules and TEAL framework configuration for reporting TEAL Alerts

# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%prep
%setup -n pyteal-code

%build
autoconf
%configure --enable-connector=sfp

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%pre
/sbin/service teal stop

if [ $1 -eq 1 ]; then
/sbin/service xcatd stop
fi

%post
if  [ $1 -eq 1 ]; then
/sbin/service xcatd start
/opt/xcat/sbin/runsqlcmd -d /opt/teal/data/ibm/sfp/sql/install
fi

/sbin/service teal start

%preun
if  [ $1 -eq 0 ]; then
/sbin/service teal stop
/opt/xcat/sbin/runsqlcmd -d /opt/teal/data/ibm/sfp/sql/uninstall
/sbin/service xcatd stop
fi

%postun
if [ $1 -eq 0 ]; then
/sbin/service xcatd start
/sbin/service teal start
fi

%files
%attr( 755, bin, bin ) /opt/teal/ibm/sfp/__init__.py
%attr( 755, bin, bin ) /opt/teal/ibm/sfp/sfp_analyzer.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/connector/sfp.py
%attr( 644, bin, bin ) /opt/teal/data/ibm/sfp/sql/install/Teal_sfp_db2.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/sfp/sql/install/Teal_sfp_dba_db2.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/sfp/sql/install/Teal_sfp_mysql.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/sfp/sql/uninstall/Teal_sfp_dba_db2.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/sfp/sql/uninstall/Teal_sfp_rm_db2.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/sfp/sql/uninstall/Teal_sfp_rm_mysql.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/teal/xml/SFP_1.xml
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.EventResponse/TealLogSfpEvent.pm
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.EventResponse/TealLogSfpEvent_HB.pm
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_schema/Teal_sfp.pm
%attr( 644, bin, bin ) /etc/teal/sfp.conf

