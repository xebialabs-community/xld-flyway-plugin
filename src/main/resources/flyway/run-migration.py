#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from flyway.FlywayUtil import FlywayUtil
from java.io import File
from org.flywaydb.core.api import FlywayException

import sys
import os

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
flyway.set_placeholders(deployed.flywayPlaceholders)
flyway.set_target_as_string(deployed.targetVersion)

flyway.set_classloader(File("%s/%s/db.jar" % (os.getcwd(),deployed.file.path)).toURI().toURL())
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
