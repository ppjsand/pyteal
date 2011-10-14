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
Name: teal-ll		
Version: 1.1.0.2
Release: 2

License: EPL 1.0
Group: Applications/System
Source: pyteal-1.1.0.1.tar.gz
Distribution: pyteal
URL: http://pyteal.sourceforge.net

Requires: teal-base >= 1.1.0.2, LoadL-scheduler-full-RH6-PPC64 >= 5.1.0.0

%description
This package provides the TEAL connector for Loadleveler. It also provides the additional plug-ins to 
support the additional user data, rules and TEAL framework configuration for reporting TEAL Alerts

# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%prep
%setup -n pyteal-code

%build
autoconf
%configure --enable-connector=ll

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%pre
/sbin/service teal stop

if  [ $1 -eq 1 ]; then
/sbin/service xcatd stop
else
/sbin/service teal_ll stop
fi

%post
if  [ $1 -eq 1 ]; then
/sbin/service xcatd start
/opt/xcat/sbin/runsqlcmd -d /opt/teal/data/ibm/ll/sql/install
fi

/sbin/service teal start
/sbin/service teal_ll start

%preun
if  [ $1 -eq 0 ]; then
/sbin/service teal_ll stop
/sbin/service teal stop
/opt/xcat/sbin/runsqlcmd -d /opt/teal/data/ibm/ll/sql/uninstall
/sbin/service xcatd stop
fi

%postun
if  [ $1 -eq 0 ]; then
/sbin/service xcatd start
/sbin/service teal start
fi

%files
%attr( 755, bin, bin ) /opt/teal/ibm/teal/connector/loadleveler.py
%attr( 644, bin, bin ) /opt/teal/data/ibm/ll/sql/install/Teal_ll_db2.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/ll/sql/install/Teal_ll_dba_db2.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/ll/sql/install/Teal_ll_mysql.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/ll/sql/uninstall/Teal_ll_dba_db2.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/ll/sql/uninstall/Teal_ll_rm_db2.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/ll/sql/uninstall/Teal_ll_rm_mysql.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/ll/xml/LL_GEAR_rules.xml
%attr( 644, bin, bin ) /opt/teal/data/ibm/teal/xml/LL_1.xml
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_schema/Teal_ll.pm
%attr( 755, bin, bin ) /etc/init.d/teal_ll
%attr( 644, bin, bin ) /etc/teal/ll.conf

