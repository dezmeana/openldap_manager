#!/bin/sh
#
# Dump LDAP database
/usr/sbin/ldbmcat -n /var/lib/ldap/stooges/id2entry.gdbm > /home/dbdumps/stooges-`date +%m%d%y`.ldif
sleep 10
#
# Convert ldif format to  csv
/bin/awk -F ': ' -f /opt/bin/ldif2csv-StoogesDumpAll.awk < /home/dbdumps/stooges-`date +%m%d%y`.ldif > /home/dbdumps/StoogesDatabaseAll-`date +%m%d%y`.csv
