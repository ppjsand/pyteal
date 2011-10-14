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
Summary: Toolkit for Event Analysis and Logging base framework support
Name: teal-base		
Version: 1.1.0.2
Release: 2

License: EPL 1.0
Group: Applications/System
Source: pyteal-1.1.0.1.tar.gz 
Distribution: pyteal
URL: http://pyteal.sourceforge.net

Requires: xCAT >= 2.6.6, python >= 2.6, pyodbc >= 2.1.7, perl-Module-Load

%description
The Toolkit for Event Analysis and Logging (TEAL) is a pluggable processing pipeline that allows different components to use connectors
to log events, have analyzers evaluate the events to get closer to the root cause, report and log these as alerts.

# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%prep
%setup -n pyteal-code

%build
autoconf
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%pre
if  [ $1 -eq 1 ]; then
/sbin/service xcatd stop

site=`python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`
echo /opt"/teal" > $site"/teal.pth"

mkdir -p /var/log/teal/
else
/sbin/service teal stop
fi

%post 
if  [ $1 -eq 1 ]; then
/sbin/service xcatd start
/opt/xcat/sbin/runsqlcmd -d /opt/teal/data/ibm/teal/sql/install
ln -sf /opt/teal/ibm/teal/teal.py /opt/teal/bin/teal
fi

/sbin/service teal start

%preun
if  [ $1 -eq 0 ]; then
/sbin/service teal stop
rm /opt/teal/bin/teal
/opt/xcat/sbin/runsqlcmd -d /opt/teal/data/ibm/teal/sql/uninstall
/sbin/service xcatd stop
fi

%postun
if  [ $1 -eq 0 ]; then
/sbin/service xcatd start

find /opt/teal -name "*.pyc" -exec rm {} \;

site=`python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`
rm $site"/teal.pth"

rm -rf /var/log/teal/
fi

%files
%attr( 644, bin, bin ) /etc/teal/teal.conf
%attr( 755, bin, bin ) /etc/init.d/teal
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


