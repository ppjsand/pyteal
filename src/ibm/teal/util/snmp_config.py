#!/usr/bin/env python

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

import re
import os

from ibm.teal import registry

class SNMPConnectorInstaller(object):
    ''' This class is responsible for installing and uninstalling the TEAL SNMP connector support
    '''

    CMD_RE = re.compile(r'cmds(\d+)')
    def _get_cmd_num(self, cmd_key):
        ''' Get the command number from the cmds monsetting entry

            If the cmds field is incorrectly formatted, 0 is returned
        '''
        m = self.CMD_RE.match(cmd_key)
        if m:
            return int(m.group(1))
        else:
            return 0

    def install(self, connector_info, connector_comment):
        ''' Install the SNMP connectors into the xCAT monsetting table
        '''
        # First clean up any remnants that still may exist
        self.uninstall(connector_comment)

        db = registry.get_service(registry.SERVICE_DB_INTERFACE)
        conn = db.get_connection()
        cursor = conn.cursor()

        # Get all the cmds entries to determine the starting number to use
        db.select(cursor, ['*'], 'monsetting',
                    where="$name = 'snmpmon' AND $key LIKE 'cmds%'",
                    where_fields=['name', 'key'])

        # Determine the max number for the new commands
        cmd_num = [self._get_cmd_num(row[1]) for row in cursor.fetchall()]
        if cmd_num:
            next_cmd_num = max(cmd_num) + 1
        else:
            next_cmd_num = 1

        root_dir = registry.get_service(registry.TEAL_ROOT_DIR)

        # Insert the entries for each of the SNMP connectors
        for connector in connector_info:
            cursor.executemany("INSERT INTO monsetting VALUES(?, ?, ?, ?, ?)",
                               [('snmpmon', 'cmds{0:02d}'.format(next_cmd_num), os.path.join(root_dir, connector[0]), connector_comment, None),
                                ('snmpmon', 'runcmd{0:02d}'.format(next_cmd_num), connector[1], connector_comment, None)])
            next_cmd_num += 1

        # Commit all the added entries to the monsetting table
        conn.commit()
        cursor.close()
        conn.close()

    def uninstall(self, connector_comment):
        ''' Remove all SNMP connector entries from the monsetting table
    
            All entries with the TEAL connector string in the comments field will be removed
        '''
        db = registry.get_service(registry.SERVICE_DB_INTERFACE)
        conn = db.get_connection()
        cursor = conn.cursor()

        db.delete(cursor,'monsetting', where="$comments = '{0}'".format(connector_comment), where_fields=['comments'])

        conn.commit()
        cursor.close()
        conn.close()

    def is_installed(self, connector_info, connector_comment):
        ''' Check whether the connector is installed or not by checking to see if the command is configured 
        in the monsetting table
        '''
        root_dir = registry.get_service(registry.TEAL_ROOT_DIR)

        db = registry.get_service(registry.SERVICE_DB_INTERFACE)
        conn = db.get_connection()
        cursor = conn.cursor()

        installed = False
        for cmd, snmp_filter in connector_info:
            db.select(cursor, ['*'], 'monsetting',
                      where="$name='snmpmon' AND $key LIKE 'cmd%' and $value = ?",
                      where_fields = ['name','key','value'],
                      parms=(os.path.join(root_dir, cmd),))

            row = cursor.fetchone()
            if row is None:
                installed = False
                break
            else:
                installed = True

        return installed
    