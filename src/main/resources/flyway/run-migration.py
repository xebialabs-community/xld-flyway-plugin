#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from org.flywaydb.core import Flyway

flyway_runner = deployed.container
server_url = flyway_runner.getProperty("serverUrl")
username = flyway_runner.getProperty("username")
password = flyway_runner.getProperty("password")

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

folder_dir = deployed.file.file.getParentFile().getCanonicalFile().toPath()
locations = []
for location in deployed.locations:
    locations.extend("filesystem:%s/%s" % (folder_dir, location.lstrip("filesystem:")))
flyway.setLocations(locations)

print "Starting flyway migration"
migrations = flyway.migrate()
print "Ended with [%s] migrations" % migrations