# Build status #

[![Build Status](https://travis-ci.org/xebialabs-community/xld-flyway-plugin.svg?branch=master)](https://travis-ci.org/xebialabs-community/xlr-flyway-plugin)

# Preface #

This document describes the functionality provided by the Flyway plugin.

See the **XL Deploy Reference Manual** for background information on XL Deploy and deployment concepts.

# Overview #

The Flyway plugin is a XL Deploy plugin that adds capability for migrating databases using Flyway.

See http://flywaydb.org/documentation/commandline/migrate.html for more information about the Flyway commands and configuration options used by this API.

# History #

* v1.0.0 - jdewinne - First version 
* v1.1.0 - gpaulissen - Added outOfOrder and validateOnMigrate flags. Removed startClean flag (from the UI).
* v1.2.0 - gpaulissen - Issue #4: The XL Deploy NOOP operation must act like CREATE or MODIFY. This ensures that running XL Deploy after a database backup restore will migrate the database so it will really resemble the XL Deploy administration.

# Requirements #

* **Requirements**
  * **XL Deploy** 5.0.0

# Build #

$ ./gradlew xlPlugin

or, if you are behind a proxy server:

$ ./gradlew -Dhttps.proxyHost=127.0.0.1 -Dhttps.proxyPort=3128 xlPlugin

And go to the build/distributions to find your plugin XLDP file.

# Installation #

Remove the previous plugin XLDP file from your `SERVER_HOME/plugins` directory.
Next, place the plugin XLDP file into your `SERVER_HOME/plugins` directory.
Finally, restart the server.

# Usage #

1. Go to `Repository - Infrastructure`, create a new `flyway.Runner`.
2. Create an environment under `Repository - Environments`
3. Create an application with `flyway.Scripts` as deployable.
4. Start migrating

# API #

* `flyway.Scripts`
    * username          - `string`          - The user to use to connect to the database.
    * password          - `string`          - The password to use to connect to the database.
    * schemas           - `set_of_string`   - Case-sensitive list of schemas managed by Flyway.
    * table             - `string`          - The name of Flyway's metadata table.
    * locations         - `set_of_string`   - List of locations to scan recursively for migrations.
    * encoding          - `string`          - The encoding of Sql migrations.
    * baselineOnMigrate - `boolean`         - Whether to automatically call baseline when migrate is executed against a non-empty schema with no metadata table.
                                              This is useful for initial Flyway production deployments on projects with an existing DB.
    * repair            - `boolean`         - Repairs the Flyway metadata table.
    * outOfOrder        - `boolean`         - Allows migrations to be run "out of order". 
                                              If you already have versions 1 and 3 applied, and now a version 2 is found, it will be applied too instead of being ignored.
    * validateOnMigrate - `boolean`         - Whether to automatically call validate or not when running migrate.
