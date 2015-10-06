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

print "Connecting to flyway runner"

flyway = Flyway()
flyway.setDataSource(server_url,username,password)
flyway.setSchemas(list(deployed.schemas))
if deployed.baselineOnMigrate:
    flyway.setBaselineOnMigrate(deployed.baselineOnMigrate)
if deployed.encoding:
    flyway.setEncoding(deployed.encoding)
if deployed.table:
    flyway.setTable(deployed.table)

folder_dir = deployed.file.file.getCanonicalFile().toPath()
locations = []
for location in deployed.locations:
    resolved_location = "filesystem:%s/%s" % (folder_dir, location.replace("filesystem:",""))
    print "Adding flyway location: [%s] for folder [%s]" % (resolved_location,deployed.file.name)
    locations.append(resolved_location)
flyway.setLocations(locations)

try:
    if deployed.startClean:
        print "Start with clean Flyway"
        flyway.clean()

    if deployed.repair:
        print "Repair the Flyway metadata table."
        flyway.repair()

    print "Starting flyway migration"
    migrations = flyway.migrate()
    print "Ended with [%s] migrations" % migrations
except FlywayException, err:
    print "Migration failed with error: ", err
    sys.exit(1)
finally:
    # Show flyway info details
    print "Flyway log results: ", MigrationInfoDumper.dumpToAsciiTable([flyway.info().current()])