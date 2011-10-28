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
Summary: Toolkit for Event Analysis and Logging
Name: teal
Version: 1.1.0.2
Release: 2

License: EPL 1.0
Group: Applications/System
Source: pyteal-1.1.0.2.tar.gz 
Distribution: pyteal
URL: http://pyteal.sourceforge.net

%description
The Toolkit for Event Analysis and Logging (TEAL) is a pluggable processing pipeline that allows different components to use connectors
to log events, have analyzers evaluate the events to get closer to the root cause, report and log these as alerts.

# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

# define the default values
%define  with_isnm 1
%define  with_sfp 1
%define  with_ll 1
%define  with_pnsd 1
%define  with_gpfs 0
%define  with_test 1

# if --without switch is used
%{?_without_isnm: %{expand: %%global with_isnm 0}}
%{?_without_sfp: %{expand: %%global with_sfp 0}}
%{?_without_ll: %{expand: %%global with_ll 0}}
%{?_without_pnsd: %{expand: %%global with_pnsd 0}}
%{?_without_gpfs: %{expand: %%global with_gpfs 0}}
%{?_without_test: %{expand: %%global with_test 0}}

# if --with switch is used
%{?_with_isnm: %{expand: %%global with_isnm 1}}
%{?_with_sfp: %{expand: %%global with_sfp 1}}
%{?_with_ll: %{expand: %%global with_ll 1}}
%{?_with_pnsd: %{expand: %%global with_pnsd 1}}
%{?_with_gpfs: %{expand: %%global with_gpfs 1}}
%{?_with_test: %{expand: %%global with_test 1}}

%prep
%setup -n pyteal-code

%build
autoconf
%configure --enable-isnm=%{with_isnm} --enable-sfp=%{with_sfp} --enable-ll=%{with_ll} --enable-pnsd=%{with_pnsd} --enable-gpfs=%{with_gpfs} --enable-test=%{with_test}
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%package base
Summary: Toolkit for Event Analysis and Logging base framework support
Group: Applications/System
Requires: xCAT >= 2.6.6, python >= 2.6, pyodbc >= 2.1.7, perl-Module-Load

%description base
This package provides the base runtime support for event analysis

%pre base
if  [ $1 -eq 1 ]; then
/sbin/service xcatd stop

site=`python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`
echo /opt"/teal" > $site"/teal.pth"

else
/sbin/service teal stop
fi

%post base
if  [ $1 -eq 1 ]; then
/sbin/service xcatd start
/opt/xcat/sbin/runsqlcmd -d /opt/teal/data/ibm/teal/sql/install
ln -sf /opt/teal/ibm/teal/teal.py /opt/teal/bin/teal
fi

/sbin/service teal start

%preun base
if  [ $1 -eq 0 ]; then
/sbin/service teal stop
rm /opt/teal/bin/teal
/opt/xcat/sbin/runsqlcmd -d /opt/teal/data/ibm/teal/sql/uninstall
/sbin/service xcatd stop
fi

%postun base
if  [ $1 -eq 0 ]; then
/sbin/service xcatd start

find /opt/teal -name "*.pyc" -exec rm {} \;

site=`python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`
rm $site"/teal.pth"

fi

%files base
%attr( 644, bin, bin ) /opt/teal/data/ibm/teal/sql/install/Teal_db2.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/teal/sql/install/Teal_dba_db2.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/teal/sql/install/Teal_mysql.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/teal/sql/uninstall/Teal_dba_db2.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/teal/sql/uninstall/Teal_rm_db2.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/teal/sql/uninstall/Teal_rm_mysql.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/teal/xml/percs_location.xml
%ifarch ppc64 x86_64
%attr( 755, bin, bin ) /usr/lib64/libteal_common.so
%attr( 755, bin, bin ) /usr/lib64/libteal_common.so.1
%attr( 755, bin, bin ) /usr/lib64/libteal_common.so.1.0
%endif
%attr( 755, bin, bin ) /usr/lib/libteal_common.so
%attr( 755, bin, bin ) /usr/lib/libteal_common.so.1
%attr( 755, bin, bin ) /usr/lib/libteal_common.so.1.0
#%attr( 755, bin, bin ) /usr/lib64/libteal_common.so
%attr( 755, bin, bin ) /opt/teal/bin/tllsevent
%attr( 755, bin, bin ) /opt/teal/bin/tllsalert
%attr( 755, bin, bin ) /opt/teal/bin/tllsckpt
%attr( 755, bin, bin ) /opt/teal/bin/tlrmalert
%attr( 755, bin, bin ) /opt/teal/bin/tlchalert
%attr( 755, bin, bin ) /opt/teal/bin/tlrmevent
%attr( 755, bin, bin ) /opt/teal/bin/tlvfyrule
%attr( 755, bin, bin ) /opt/teal/sbin/tlnotify
%attr( 755, bin, bin ) /opt/teal/sbin/tltab
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/gear/__init__.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/gear/control.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/gear/error_handlers.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/gear/rule.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/gear/common.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/gear/engine.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/gear/engine_factory.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/gear/event_analyzer.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/gear/external_base_classes.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/gear/rule_action.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/gear/ruleset.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/gear/constants.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/gear/pool_control.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/gear/rule_condition.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/gear/rule_condition_data.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/gear/rule_value.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/gear/templates.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/gear/instance_helper.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/pool/__init__.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/pool/incident_pool.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/__init__.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/analysis_info.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/analyzer/analyzer.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/connector/__init__.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/database/__init__.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/database/db_interface.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/database/db_interface_pyodbc.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/filter/alert_filter.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/filter/__init__.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/filter/alert_filter_analyzer_name.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/filter/duplicate_alert_filter.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/filter/noise_alert_filter.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/listener/alert_listener.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/listener/file_alert_listener.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/listener/print_alert_listener.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/listener/__init__.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/listener/call_alert_listener.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/listener/logging_alert_listener.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/listener/rmc_alert_listener.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/listener/smtp_alert_listener.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/monitor/teal_semaphore.so
%attr( 755, bin, bin ) /opt/teal/ibm/teal/monitor/teal_condition.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/monitor/__init__.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/monitor/event_monitor.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/monitor/noop_monitor.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/monitor/historic_monitor.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/monitor/realtime_monitor.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/util/__init__.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/util/command.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/util/extendable_timer.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/util/listenable_queue.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/util/journal.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/util/msg_target.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/util/xml_file_reader.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/__init__.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/alert.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/alert_mgr.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/alert_delivery.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/checkpoint_mgr.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/constants.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/configuration.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/control_msg.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/event.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/extdata.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/incident.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/journalable.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/location.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/metadata.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/processable.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/registry.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/teal.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/teal_error.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/shutdown.py
%attr( 755, bin, bin ) /opt/teal/ibm/__init__.py
%attr( 644, bin, bin ) /opt/teal/xml/alertmeta.xsd
%attr( 644, bin, bin ) /opt/teal/xml/eventmeta.xsd
%attr( 644, bin, bin ) /opt/teal/xml/extension.xsd
%attr( 644, bin, bin ) /opt/teal/xml/location.xsd
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_schema/Teal_db2.pm
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_schema/Teal_mysql.pm
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.Sensor/TealSendAlert.pm
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.Condition/TealAnyNodeEventNotify.pm
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.EventResponse/TealNotifyEventLogged.pm
%attr( 644, bin, bin ) /opt/teal/locale/messages.pot
%attr( 644, bin, bin ) /opt/teal/locale/en_US/LC_MESSAGES/messages.po
%attr( 644, bin, bin ) /opt/teal/locale/en_US/LC_MESSAGES/messages.mo
%attr( 755, bin, bin ) /install/postscripts/rmcmon/resources/sn/IBM.Sensor/TealEventNotify.pm
%config(noreplace) /etc/teal/teal.conf
%attr( 755, bin, bin ) /etc/init.d/teal
%attr( 755, root, root ) /var/log/teal

%package isnm
Summary: Toolkit for Event Analysis and Logging ISNM Connector  	
Group: Applications/System
Requires: teal-base >= 1.1.0.0

%description isnm
This package provides the TEAL connector for ISNM. It also provides the additional plug-ins to 
support the additional user data, rules and TEAL framework configuration for reporting TEAL Alerts
to the HMC Service Focalpoint

%pre isnm
/sbin/service teal stop

if  [ $1 -eq 1 ]; then
/sbin/service xcatd stop
fi

%post isnm
if  [ $1 -eq 1 ]; then
/sbin/service xcatd start
/opt/xcat/sbin/runsqlcmd -d /opt/teal/data/ibm/isnm/sql/install
fi

/sbin/service teal start

%preun isnm
if  [ $1 -eq 0 ]; then
/sbin/service teal stop
/opt/xcat/sbin/runsqlcmd -d /opt/teal/data/ibm/isnm/sql/uninstall
/sbin/service xcatd stop
fi

%postun isnm
if  [ $1 -eq 0 ]; then
/sbin/service xcatd start
/sbin/service teal start
fi

%if %{with_isnm}
%files isnm
%attr( 755, bin, bin ) /opt/teal/ibm/isnm/__init__.py
%attr( 755, bin, bin ) /opt/teal/ibm/isnm/cnm_gear.py
%attr( 755, bin, bin ) /opt/teal/ibm/isnm/cnm_alert_listener.py
%attr( 755, bin, bin ) /opt/teal/ibm/isnm/sfp_message.py
%attr( 644, bin, bin ) /opt/teal/data/ibm/teal/xml/CNM_1.xml
%attr( 644, bin, bin ) /opt/teal/data/ibm/isnm/xml/CNM_GEAR_alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/data/ibm/isnm/xml/CNM_GEAR_event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/data/ibm/isnm/xml/CNM_GEAR_rule.xml
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_schema/Teal_isnm.pm
%attr( 644, bin, bin ) /opt/teal/data/ibm/isnm/sql/install/Teal_isnm_db2.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/isnm/sql/install/Teal_isnm_dba_db2.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/isnm/sql/install/Teal_isnm_mysql.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/isnm/sql/uninstall/Teal_isnm_dba_db2.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/isnm/sql/uninstall/Teal_isnm_rm_db2.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/isnm/sql/uninstall/Teal_isnm_rm_mysql.sql
%attr( 755, bin, bin ) /usr/lib/libteal_isnm.so
%attr( 755, bin, bin ) /usr/lib/libteal_isnm.so.1
%attr( 755, bin, bin ) /usr/lib/libteal_isnm.so.1.0
%ifarch ppc64 x86_64
%attr( 755, bin, bin ) /usr/lib64/libteal_isnm.so
%attr( 755, bin, bin ) /usr/lib64/libteal_isnm.so.1
%attr( 755, bin, bin ) /usr/lib64/libteal_isnm.so.1.0
%endif
%config(noreplace) /etc/teal/isnm.conf
%endif

%package ll
Summary: Toolkit for Event Analysis and Logging Loadleveler Connector  	
Group: Applications/System
Requires: teal-base >= 1.1.0.2, LoadL-scheduler-full-RH6-PPC64 >= 5.1.0.0

%description ll
This package provides the TEAL connector for Loadleveler. It also provides the additional plug-ins to 
support the additional user data, rules and TEAL framework configuration for reporting TEAL Alerts

%pre ll
/sbin/service teal stop

if  [ $1 -eq 1 ]; then
/sbin/service xcatd stop
else
/sbin/service teal_ll stop
fi

%post ll
if  [ $1 -eq 1 ]; then
/sbin/service xcatd start
/opt/xcat/sbin/runsqlcmd -d /opt/teal/data/ibm/ll/sql/install
fi

/sbin/service teal start
/sbin/service teal_ll start

%preun ll
if  [ $1 -eq 0 ]; then
/sbin/service teal_ll stop
/sbin/service teal stop
/opt/xcat/sbin/runsqlcmd -d /opt/teal/data/ibm/ll/sql/uninstall
/sbin/service xcatd stop
fi

%postun ll
if  [ $1 -eq 0 ]; then
/sbin/service xcatd start
/sbin/service teal start
fi

%if %{with_ll}
%files ll
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
%config(noreplace) /etc/teal/ll.conf
%endif

%package pnsd
Summary: Toolkit for Event Analysis and Logging Loadleveler Connector  	
Group: Applications/System
Requires: teal-base >= 1.1.0.2

%description pnsd
This package provides the TEAL connector for PNSD. It also provides the additional plug-ins to 
support the additional user data, rules and TEAL framework configuration for reporting TEAL Alerts

%pre pnsd
/sbin/service teal stop

%post pnsd
/sbin/service teal start

%preun pnsd
if  [ $1 -eq 0 ]; then
/sbin/service teal stop
fi

%postun pnsd
if  [ $1 -eq 0 ]; then
/sbin/service teal start
fi

%if %{with_pnsd}
%files pnsd
%attr( 755, bin, bin ) /install/postscripts/rmcmon/resources/node/IBM.Sensor/TealPnsdStat.pm
%attr( 755, bin, bin ) /install/postscripts/rmcmon/resources/sn/IBM.Condition/TealAnyNodePnsdStat.pm
%attr( 755, bin, bin ) /install/postscripts/rmcmon/scripts/tlpnsd_sensor
%attr( 755, bin, bin ) /opt/teal/ibm/teal/connector/pnsd.py
%attr( 644, bin, bin ) /opt/teal/data/ibm/pnsd/xml/PNSD_GEAR_rules.xml
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.Condition/TealAnyNodePnsdStat.pm
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.Condition/TealAnyNodePnsdStat_H.pm
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.EventResponse/TealLogPnsdEvent.pm 
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.EventResponse/TealLogPnsdEvent_H.pm 
%config(noreplace) /etc/teal/pnsd.conf
%endif

%package sfp
Summary: Toolkit for Event Analysis and Logging Service Focal Point Connector  	
Group: Applications/System
Requires: teal-base >= 1.1.0.2

%description sfp
This package provides the TEAL connector for the Service Focal Point. It also provides the additional plug-ins to 
support the additional user data, rules and TEAL framework configuration for reporting TEAL Alerts

%pre sfp
/sbin/service teal stop

if [ $1 -eq 1 ]; then
/sbin/service xcatd stop
fi

%post sfp
if  [ $1 -eq 1 ]; then
/sbin/service xcatd start
/opt/xcat/sbin/runsqlcmd -d /opt/teal/data/ibm/sfp/sql/install
fi

/sbin/service teal start

%preun sfp
if  [ $1 -eq 0 ]; then
/sbin/service teal stop
/opt/xcat/sbin/runsqlcmd -d /opt/teal/data/ibm/sfp/sql/uninstall
/sbin/service xcatd stop
fi

%postun sfp
if [ $1 -eq 0 ]; then
/sbin/service xcatd start
/sbin/service teal start
fi

%if %{with_sfp}
%files sfp
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
%config(noreplace) /etc/teal/sfp.conf
%endif

%package test
Summary: Toolkit for Event Analysis and Logging Testcases
Group: Applications/System
Requires: teal-base >= 1.1.0.2

%description test
This package provides the unit and functional verification test for TEAL

%if %{with_test}
%files test
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/__init__.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/teal_unittest.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/__init__.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/alert_analyzer_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/alert_test.py 
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/alert_delivery_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/alert_filter_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/alert_listener_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/all_unit_tests.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/checkpoint_mgr_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/checkpoint_shutdown_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/checkpoint_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/configuration_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_analyzer_test/inject_alerts01.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_analyzer_test/inject_events01.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_analyzer_test/test01.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_delivery_test/alert_metadata_01.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_delivery_test/analyzer_filter/alerts_out_all.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_delivery_test/analyzer_filter/alerts_out_analyzer1.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_delivery_test/analyzer_filter/alerts_out_analyzer2and3.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_delivery_test/analyzer_filter/alerts_out_not_analyzer1.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_delivery_test/analyzer_filter/alerts_out_not_analyzer1and2and3.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_delivery_test/analyzer_filter/alerts_out_not_analyzer2and3.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_delivery_test/analyzer_filter/inject_DQ_alerts.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_delivery_test/analyzer_filter/test.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_delivery_test/data_sample_inject_DQ.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_delivery_test/data_sample_out_ai_urgent.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_delivery_test/data_sample_out_alert_id.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_delivery_test/data_sample_out_all_alerts.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_delivery_test/test_local_filters.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_delivery_test/listener_failure/alerts_out_all.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_delivery_test/listener_failure/alerts_out_analyzer1.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_delivery_test/listener_failure/inject_DQ_alerts.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_delivery_test/listener_failure/test.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/alert_metadata_01.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/empty_alerts.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/full_alerts.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/ifname_alerts.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/ifnotname_alerts.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/inject_DQ_alerts.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/partial_alerts.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/test_01.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/test_02.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/test_03.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/test_04.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/test_05.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/test_06.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/test_07.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/test_08.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/test_09.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/test_10.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/test_11.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/test_common.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_filter_test/unfiltered_alerts.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_test/alert_metadata_01.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_test/inject_DQ_alerts.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_test/test.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_listener_test/alert_metadata_01.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/alert_listener_test/test_01.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/checkpoint_test/alert_metadata_demo_01.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/checkpoint_test/configurationtest_05_semaphore.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/checkpoint_test/data_sample_demo_NEW_001.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/checkpoint_test/eventsmetadatatest_06.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/checkpoint_test/noop_monitor.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/checkpoint_test/G1_base.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/checkpoint_test/G1_alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/checkpoint_test/G1_input_events_no_flush_001.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/checkpoint_test/G1_input_events_no_flush_002.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/checkpoint_test/G1_rule_001.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/checkpoint_test/G1_test_class.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/checkpoint_test/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/checkpoint_test/xcat/cfgloc
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/cnm/cnm.NMalertMetaData.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/common/configurationtest.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/common/dbinterfaceonly.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/common/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/common/xcat/cfgloc
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/common/teal/dbinterfaceonly.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/configuration_test/configurationtest_01.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/configuration_test/configurationtest_02.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/demo/GEAR_rule_example_001.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/demo/alert_metadata_demo_01.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/demo/configurationtest_05.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/demo/configurationtest_05_semaphore.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/demo/data_sample_demo_NEW_001.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/demo/eventsmetadatatest_06.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/event_analyzer_test/alert_metadata_01.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/event_analyzer_test/load_config_01.conf
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_alerts_001.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_analyze_001_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_analyze_002_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_constants_001.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_constants_002.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_constants_003.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_constants_004.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_constants_005.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_constants_006_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_constants_007_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_constants_008_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_constants_009_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_constants_010_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_constants_011_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_constants_012_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_constants_013_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_constants_014_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_constants_015_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_constants_016_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_constants_017_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_control_001.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_control_002.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_control_003.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_control_004.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_control_005.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_control_006.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_control_007_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_control_008_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_control_009_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_control_010_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_control_011_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_event_equals_001.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_events_001.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_events_002_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_events_003_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_events_004_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_events_005_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_events_006_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_events_007_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_events_008_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_pool_control_001.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_pool_control_002_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_pool_control_003_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_pool_control_004_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_pool_control_005_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_pool_control_006_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_001_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_002_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_003_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_004_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_005_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_006_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_007_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_008_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_009_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_010_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_011_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_012_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_013_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_014_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_015_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_016_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_017_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_018_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_019_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_020_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_021_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_022_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_023_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_024_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_025_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_026_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_027_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_028_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_029_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_030_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_031_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_032_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_033_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_034_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_035_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_036_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_037_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_038_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_039_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_040_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_041_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_042_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_043_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_044_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_045_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_046_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_047_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_048_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_049_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_050_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_051_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_052_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_rule_053_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_001_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_002_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_003_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_004_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_005_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_006_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_007_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_008_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_009_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_010_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_011_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_012_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_013_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_014_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_015_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_016_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_017_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_018_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_019_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_020_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_021_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_022_err.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/gear_ruleset_test.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/isnm/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/ll/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/pnsd/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d172183/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d172183/CNM_GEAR_alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d172183/CNM_GEAR_rule.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d172183/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d173776/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d173776/CNM_GEAR_alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d173776/CNM_GEAR_rule.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d173776/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d173863/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d173863/CNM_GEAR_alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d173863/CNM_GEAR_rule.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d173863/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d173874/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d173874/CNM_GEAR_alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d173874/CNM_GEAR_rule.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d173874/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d178935/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d178935/CNM_GEAR_alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d178935/CNM_GEAR_rule.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d178935/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/d178935/config2.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/x000001/alert_output_a.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/x000001/alert_output_b.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/x000001/alert_output_c.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/x000001/alert_output_d.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/x000001/CNM_GEAR_alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/x000001/CNM_GEAR_rule.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/bugs/x000001/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t001/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t001/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t001/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t001/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t001/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t001/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t001/percs_location.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t002/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t002/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t002/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t002/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t002/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t002/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t003/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t003/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t003/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t003/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t003/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t003/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t004/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t004/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t004/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t004/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t004/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t004/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t005/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t005/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t005/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t005/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t005/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t005/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t006/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t006/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t006/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t006/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t006/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t006/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t007/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t007/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t007/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t007/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t007/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t007/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t008/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t008/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t008/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t008/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t008/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t008/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t009/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t009/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t009/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t009/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t009/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t009/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t010/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t010/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t010/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t010/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t010/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t010/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t011/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t011/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t011/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t011/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t011/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t011/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t012/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t012/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t012/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t012/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t012/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t012/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t013/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t013/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t013/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t013/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t013/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t013/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t014/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t014/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t014/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t014/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t014/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t014/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t015/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t015/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t015/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t015/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t015/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t015/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t016/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t016/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t016/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t016/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t016/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t016/rule_to_test.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t017/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t017/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t017/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t017/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t017/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t017/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t017/rule_to_test.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t017/test_class.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t018/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t018/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t018/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t018/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t018/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t018/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t019/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t019/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t019/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t019/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t019/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t019/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t020/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t020/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t020/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t020/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t020/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t020/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t021/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t021/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t021/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t021/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t021/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t021/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t022/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t022/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t022/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t022/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t022/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t022/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t023/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t023/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t023/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t023/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t023/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t023/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t024/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t024/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t024/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t024/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t024/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t024/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t025/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t025/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t025/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t025/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t025/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t025/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t026/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t026/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t026/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t026/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t026/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t026/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t027/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t027/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t027/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t027/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t027/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t027/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t028/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t028/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t028/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t028/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t028/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t028/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t029/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t029/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t029/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t029/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t029/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t029/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t030/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t030/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t030/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t030/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t030/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t030/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t031/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t031/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t031/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t031/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t031/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t031/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t032/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t032/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t032/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t032/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t032/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t032/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t033/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t033/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t033/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t033/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t033/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t033/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t034/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t034/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t034/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t034/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t034/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t034/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t035/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t035/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t035/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t035/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t035/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t035/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t036/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t036/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t036/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t036/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t036/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t036/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t037/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t037/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t037/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t037/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t037/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t037/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t038/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t038/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t038/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t038/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t038/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t038/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t039/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t039/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t039/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t039/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t039/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t039/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t040/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t040/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t040/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t040/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t040/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t040/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t041/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t041/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t041/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t041/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t041/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t041/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t042/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t042/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t042/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t042/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t042/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t042/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t042/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t043/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t043/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t043/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t043/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t043/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t043/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t043/rule_to_test.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t044/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t044/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t044/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t044/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t044/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t044/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t044/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t044/rule_to_test.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t044/test_class.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t045/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t045/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t045/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t045/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t045/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t045/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t045/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t045/rule_to_test.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t045/test_class.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t046/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t046/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t046/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t046/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t046/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t046/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t046/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t046/rule_to_test.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t046/test_class.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t047/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t047/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t047/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t047/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t047/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t047/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t047/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t047/rule_to_test.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t047/test_class.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t048/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t048/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t048/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t048/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t048/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t048/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t048/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t048/rule_to_test.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t048/test_class.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t049/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t049/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t049/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t049/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t049/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t049/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t049/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t049/rule_to_test.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t049/test_class.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t050/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t050/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t050/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t050/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t050/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t050/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t050/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t050/rule_to_test.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t050/test_class.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t051/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t051/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t051/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t051/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t051/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t051/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t051/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t051/rule_to_test.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t051/test_class.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t052/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t052/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t052/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t052/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t052/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t052/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t052/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t052/rule_to_test.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t052/test_class.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t053/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t053/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t053/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t053/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t053/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t053/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t053/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t053/rule_to_test.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t053/test_class.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t054/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t054/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t054/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t054/alert_output2.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t054/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t054/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t054/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t054/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t054/rule_to_test1.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t054/rule_to_test2.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t054/test_class.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t055/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t055/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t055/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t055/alert_output2.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t055/alert_output3.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t055/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t055/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t055/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t055/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t055/rule_to_test1.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t055/rule_to_test2.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t055/rule_to_test3.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t055/test_class.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t056/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t056/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t056/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t056/alert_output2.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t056/alert_output3.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t056/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t056/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t056/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t056/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t056/rule_to_test1.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t056/rule_to_test2.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t056/rule_to_test3.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t056/test_class.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t057/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t057/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t057/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t057/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t057/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t057/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t057/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t057/rule_to_test1.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t058/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t058/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t058/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t058/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t058/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t058/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t058/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t058/rule_to_test1.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t059/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t059/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t059/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t059/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t059/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t059/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t059/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t059/rule_to_test1.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t060/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t060/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t060/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t060/alert_output2.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t060/alert_output3.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t060/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t060/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t060/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t060/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t060/rule_to_test1.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t060/rule_to_test2.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t060/rule_to_test3.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t060/test_class.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t061/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t061/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t061/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t061/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t061/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t061/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t061/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t061/rule_to_test1.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t062/__init__.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t062/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t062/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t062/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t062/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t062/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t062/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t062/rule_to_test1.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t062/test_class.py
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t063/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t063/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t063/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t063/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t063/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t063/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t063/rule_to_test1.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t064/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t064/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t064/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t064/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t064/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t064/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t064/rule_to_test1.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t065/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t065/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t065/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t065/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t065/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t065/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t065/rule_to_test1.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t066/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t066/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t066/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t066/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t066/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t066/locationtest.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t066/rule_to_test1.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t999/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t999/alert_output.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t999/cnm.NMalertMetaData.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t999/config.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t999/event_input.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t999/event_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t999/percs_location.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/gear_ruleset_test/t999/rule_to_test.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/ibm/teal/xml/CNM_1.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/ibm/teal/xml/TEST_0.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/journal_test/data_sample_001_NEW.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/journal_test/data_sample_001_NEW_AUTO_OUT.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/journal_test/data_sample_002_NEW.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/journal_test/data_sample_002_NEW_AUTO_OUT.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/journal_test/events_001.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/journal_test/events_002.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/journal_test/events_001.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/journal_test/events_002.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/journal_test/alerts_002.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/journal_test/alerts_003.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/journal_test/events_004.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/journal_test/alerts_005.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/journal_test/events_006_delta1.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/journal_test/events_006_nosec.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/journal_test/events_006_withsec.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/location_test/locationtest_01.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/location_test/locationtest_01.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/location_test/locationtest_02.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/location_test/locationtest_02.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/location_test/locationtest_03.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/location_test/locationtest_03.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/metadata_test/alert_metadata_01.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/metadata_test/alert_metadata_02.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/metadata_test/alert_metadata_03.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/metadata_test/alert_metadata_04a.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/metadata_test/alert_metadata_04b.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/metadata_test/alert_metadata_04c.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/metadata_test/event_metadata_01.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/metadata_test/event_metadata_02_error.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/metadata_test/event_metadata_03_error.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/metadata_test/event_metadata_04_error.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/metadata_test/event_metadata_05.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/metadata_test/event_metadata_06a.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/metadata_test/event_metadata_06b.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/metadata_test/load_config_01.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/metadata_test/load_config_02.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/metadata_test/load_config_03.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/restart_test/teal_nodelta_noanalyze.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/restart_test/three_events_one.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/restart_test/timed.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/restart_test/timed2.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/bad_01.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/bad_02.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/bad_hist_mon_01.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/bad_hist_mon_02.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/bad_hist_mon_03.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/bad_real_mon_01.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/bad_real_mon_02.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/bad_real_mon_03.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/rule_to_test1.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/rule_to_test2.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/configurationtest_05_auto.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/configurationtest_05_semaphore_auto.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/data_sample_demo_NEW_001_AAQ_Result.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/data_sample_demo_NEW_001_AAQ_Result_C.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/data_sample_demo_NEW_001_DQ_Result.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/data_sample_demo_NEW_001_DQ_Result_C.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/data_sample_demo_NEW_001_LIS_Result.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/data_sample_demo_NEW_001_LIS_Result_C.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/good_01.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/tealtest_01.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/tealtest_02.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/teal_test/tealtest_03.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/tllsalert_test/alerts_001.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/tllsalert_test/events_001.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/tllsalert_test/test.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/tlcommands_test/alerts_001.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/tlcommands_test/events_001.json
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/tlcommands_test/test.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/tlcommands_test/test_historic.conf
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/tlcommands_test/alert_metadata.xml
%attr( 644, bin, bin ) /opt/teal/ibm/teal/test/ut/data/tlcommands_test/tlcommands_rules.xml
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/event_analyzer_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/event_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/extdata_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/extendable_timer_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/gear_ruleset_basic_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/gear_ruleset_comp_check_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/gear_ruleset_execution_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/gear_ruleset_defect_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/gear_instance_helper_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/incident_pool_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/incident_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/journal_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/listenable_queue_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/location_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/makefile_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/metadata_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/pkgfiles_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/registry_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/restart_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/semaphore_init_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/teal_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/tllsalert_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/tlcommands_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/tlvfyrule_test.py
%attr( 755, bin, bin ) /opt/teal/ibm/teal/test/ut/xml_file_reader_test.py
%endif

%package gpfs
Summary: Toolkit for Event Analysis and Logging GPFS Connector  	
Group: Applications/System
Requires: teal-base >= 1.1.0.2

%description gpfs
This package provides the TEAL connector for GPFS. It also provides the additional plug-ins to 
support the additional user data, rules and TEAL framework configuration for reporting TEAL Alerts

%pre gpfs
/sbin/service teal stop

if  [ $1 -eq 1 ]; then
/sbin/service xcatd stop
fi

%post gpfs
if  [ $1 -eq 1 ]; then
/sbin/service xcatd start
/opt/xcat/sbin/runsqlcmd -d /opt/teal/data/ibm/gpfs/sql/install
fi

/sbin/service teal start

%preun gpfs
if  [ $1 -eq 0 ]; then
/sbin/service teal stop
/opt/xcat/sbin/runsqlcmd -d /opt/teal/data/ibm/gpfs/sql/uninstall
/sbin/service xcatd stop
fi

%postun gpfs
if  [ $1 -eq 0 ]; then
/sbin/service xcatd start
/sbin/service teal start
fi

%if %{with_gpfs}
%files gpfs
%attr( 644, bin, bin ) /opt/teal/data/ibm/gpfs/sql/install/Teal_gpfs_db2.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/gpfs/sql/install/Teal_gpfs_mysql.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/gpfs/sql/uninstall/Teal_gpfs_rm_db2.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/gpfs/sql/uninstall/Teal_gpfs_rm_mysql.sql
%attr( 644, bin, bin ) /opt/teal/data/ibm/teal/xml/GPFS_1.xml
%attr( 755, bin, bin ) /opt/teal/bin/tlgpfschnode
%attr( 755, bin, bin ) /opt/teal/bin/tlgpfserrhandler
%attr( 755, bin, bin ) /opt/teal/bin/tlgpfspurge
%attr( 755, bin, bin ) /opt/teal/bin/tlgpfsstatus
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.Condition/GPFSConnectorMonitor.pm
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_monitoring/rmc/resources/mn/IBM.EventResponse/GPFSConnectorFailed.pm
%attr( 755, bin, bin ) /opt/xcat/lib/perl/xCAT_schema/Teal_gpfs.pm
%attr( 755, bin, bin ) /usr/lib64/libteal_gpfs.so
%attr( 755, bin, bin ) /usr/lib64/libteal_gpfs.so.1
%attr( 755, bin, bin ) /usr/lib64/libteal_gpfs.so.1.0
%config(noreplace) /etc/teal/gpfs.conf
%endif

%package gpfs-sn
Version: 1.1.0.2
Summary: Toolkit for Event Analysis and Logging GPFS Connector (service node) 	
Group: Applications/System

Requires: gpfs.base >= 3.4.0-5 

%description gpfs-sn
This package provides the TEAL service node connector for GPFS. It will run on a service node selected as
a GPFS collector node for a cluster.

%pre gpfs-sn

%post gpfs-sn

%preun gpfs-sn

%postun gpfs-sn

%if %{with_gpfs}
%files gpfs-sn
%attr( 755, bin, bin ) /opt/teal/bin/tlgpfslauncher
%attr( 755, bin, bin ) /opt/teal/bin/tlgpfsmon
%attr( 755, bin, bin ) /opt/teal/bin/tlgpfsrefresh
%attr( 755, bin, bin ) /usr/lib64/libteal_common.so.1.0
%attr( 755, bin, bin ) /usr/lib64/libteal_common.so.1
%attr( 755, bin, bin ) /usr/lib64/libteal_common.so
%attr( 755, bin, bin ) /usr/lib64/libteal_gpfs.so
%attr( 755, bin, bin ) /usr/lib64/libteal_gpfs.so.1
%attr( 755, bin, bin ) /usr/lib64/libteal_gpfs.so.1.0
%attr( 644, bin, bin ) /opt/teal/data/ibm/gpfs/tlgpfsmon.conf.sample
%config(noreplace) /opt/teal/data/ibm/gpfs/tlgpfsmon.conf
%endif