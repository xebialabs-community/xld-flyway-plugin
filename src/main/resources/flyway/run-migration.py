#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from flyway.FlywayUtil import FlywayUtil
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

flyway = FlywayUtil.create_flyway_client(server_url, username, password)
flyway.set_schemas(deployed.schemas)
flyway.set_baseline_on_migrate(deployed.baselineOnMigrate)
flyway.set_encoding(deployed.encoding)
flyway.set_table(deployed.table)
flyway.set_out_of_order(deployed.outOfOrder)
flyway.set_validate_on_migrate(deployed.validateOnMigrate)
flyway.set_placeholder_replacement(deployed.placeholderReplacement)
flyway.set_placeholder_prefix(deployed.placeholderPrefix)
flyway.set_placeholder_suffix(deployed.placeholderSuffix)
flyway.set_target_as_string(deployed.targetVersion)

flyway.set_locations(deployed.file.path, deployed.file.name, deployed.locations)

try:
    flyway.run_clean(deployed.startClean)
    flyway.run_repair(deployed.repair)
    flyway.migrate()
except FlywayException, err:
    print "Migration failed with error: ", err
    sys.exit(1)
finally:
    flyway.log_results(deployed.container.infoMode)
