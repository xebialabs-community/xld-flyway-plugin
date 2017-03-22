#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from java.net import URLClassLoader
from org.flywaydb.core import Flyway
from org.flywaydb.core.internal.info import MigrationInfoDumper

class FlywayClient(object):
    def __init__(self, server_url, username, password):
        self.flyway = Flyway()
        self.flyway.setDataSource(server_url,username,password)

    @staticmethod
    def create_client(server_url, username=None, password=None):
        return FlywayClient(server_url, username, password)

    def set_schemas(self, schemas):
        self.flyway.setSchemas(list(schemas))

    # a boolean is required
    def set_baseline_on_migrate(self, baseline_on_migrate):
        self.flyway.setBaselineOnMigrate(baseline_on_migrate)

    def set_encoding(self, encoding):
        if encoding:
            self.flyway.setEncoding(encoding)

    def set_table(self, table):
        if table:
            self.flyway.setTable(table)

    # a boolean is required
    def set_out_of_order(self, out_of_order):
        self.flyway.setOutOfOrder(out_of_order)

    # a boolean is required
    def set_validate_on_migrate(self, validate_on_migrate):
        self.flyway.setValidateOnMigrate(validate_on_migrate)

    # a boolean is required
    def set_placeholder_replacement(self, placeholder_replacement):
        self.flyway.setPlaceholderReplacement(placeholder_replacement)

    def set_placeholder_prefix(self, placeholder_prefix):
        if placeholder_prefix:
            self.flyway.setPlaceholderPrefix(placeholder_prefix)

    def set_placeholder_suffix(self, placeholder_suffix):
            if placeholder_suffix:
                self.flyway.setPlaceholderSuffix(placeholder_suffix)

    def set_placeholders(self, placeholders):
        if placeholders:
            self.flyway.setPlaceholders(placeholders)

    def set_target_as_string(self, target_as_string):
        if target_as_string:
            self.flyway.setTargetAsString(target_as_string)

    def set_classloader(self, path):
        prev_cl = self.flyway.getClassLoader()
        url_cl = URLClassLoader.newInstance([path], prev_cl)
        print "New classloader: [%s]" % url_cl.getURLs()
        self.flyway.setClassLoader(url_cl)

    def set_locations(self, path, name, locations):
        locs = []
        for location in locations:
            if location.startswith("filesystem:"):
                resolved_location = "filesystem:%s/%s" % (path, location.replace("filesystem:",""))
            elif location.startswith("classpath:"):
                resolved_location = location
            else:
                resolved_location = location
            print "Adding flyway location: [%s] for folder [%s]" % (resolved_location,name)
            locs.append(resolved_location)
        self.flyway.setLocations(locs)

    def run_clean(self, clean):
        if clean:
            print "Clean the Flyway schemas"
            self.flyway.clean()

    def run_repair(self, repair):
        if repair:
            print "Repair the Flyway metadata table"
            self.flyway.repair()

    def migrate(self):
        print "Start the Flyway migration"
        migrations = self.flyway.migrate()
        print "Number of migration scripts run: %s" % migrations
        return migrations

    # Show flyway info details
    def log_results(self, info_mode):
        if info_mode == "Current":
            print "Flyway log results: ", MigrationInfoDumper.dumpToAsciiTable([self.flyway.info().current()])
        if info_mode == "All":
            print "Flyway log results: ", MigrationInfoDumper.dumpToAsciiTable(self.flyway.info().all())
        if info_mode == "Applied":
            print "Flyway log results: ", MigrationInfoDumper.dumpToAsciiTable(self.flyway.info().applied())
        if info_mode == "Pending":
            print "Flyway log results: ", MigrationInfoDumper.dumpToAsciiTable(self.flyway.info().pending())
