#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from org.flywaydb.core import Flyway
from org.flywaydb.core.internal.info import MigrationInfoDumper
from org.flywaydb.core.api import FlywayException

import sys

flyway_runner = deployed.container
server_url = flyway_runner.getProperty("serverUrl")
username = flyway_runner.getProperty("username")
password = flyway_runner.getProperty("password")

# Override from deployed.username if set
if deployed.username:
    username = deployed.username

# Override from deployed.password if set
if deployed.password:
    password = deployed.password

print "*** Start of Flyway configuration ***"
print "username         : %s" % username
# do not print the password
print "schemas          : %s" % deployed.schemas
print "table            : %s" % deployed.table
print "locations        : %s" % deployed.locations
print "encoding         : %s" % deployed.encoding
print "baselineOnMigrate: %s" % deployed.baselineOnMigrate
print "repair           : %s" % deployed.repair
print "outOfOrder       : %s" % deployed.outOfOrder
print "validateOnMigrate: %s" % deployed.validateOnMigrate
print "*** End of Flyway configuration ***"
print ""
print "Connecting to flyway runner"

flyway = Flyway()

flyway.setDataSource(server_url,username,password)

flyway.setSchemas(list(deployed.schemas))

# a boolean is required
flyway.setBaselineOnMigrate(deployed.baselineOnMigrate)

if deployed.encoding:
    flyway.setEncoding(deployed.encoding)

if deployed.table:
    flyway.setTable(deployed.table)

# a boolean is required
flyway.setOutOfOrder(deployed.outOfOrder)

# a boolean is required
flyway.setValidateOnMigrate(deployed.validateOnMigrate)

# a boolean is required
flyway.setPlaceholderReplacement(deployed.placeholderReplacement)

if deployed.placeholderPrefix:
    flyway.setPlaceholderPrefix(deployed.placeholderPrefix)

if deployed.placeholderSuffix:
    flyway.setPlaceholderSuffix(deployed.placeholderSuffix)

folder_dir = deployed.file.path
locations = []
for location in deployed.locations:
    resolved_location = "filesystem:%s/%s" % (folder_dir, location.replace("filesystem:",""))
    print "Adding flyway location: [%s] for folder [%s]" % (resolved_location,deployed.file.name)
    locations.append(resolved_location)
flyway.setLocations(locations)

try:
    if deployed.startClean:
        print "Clean the Flyway schemas"
        flyway.clean()

    if deployed.repair:
        print "Repair the Flyway metadata table"
        flyway.repair()

    print "Start the Flyway migration"
    migrations = flyway.migrate()
    print "Number of migration scripts run: %s" % migrations
except FlywayException, err:
    print "Migration failed with error: ", err
    sys.exit(1)
finally:
    # Show flyway info details
    print "Flyway log results: ", MigrationInfoDumper.dumpToAsciiTable([flyway.info().current()])
