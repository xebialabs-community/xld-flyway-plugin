# Preface #

This document describes the functionality provided by the Flyway plugin.

See the [XL Deploy Documentation](https://docs.xebialabs.com/xl-deploy/) for background information on XL Deploy and deployment concepts.

# CI status #

[![Build Status][xld-flyway-plugin-travis-image]][xld-flyway-plugin-travis-url]
[![Codacy Badge][xld-flyway-plugin-codacy-image] ][xld-flyway-plugin-codacy-url]
[![Code Climate][xld-flyway-plugin-code-climate-image] ][xld-flyway-plugin-code-climate-url]
[![License: MIT][xld-flyway-plugin-license-image] ][xld-flyway-plugin-license-url]
[![Downloads][xld-flyway-plugin-downloads-image] ][xld-flyway-plugin-downloads-url]

[xld-flyway-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xld-flyway-plugin.svg?branch=master
[xld-flyway-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xld-flyway-plugin
[xld-flyway-plugin-codacy-image]: https://api.codacy.com/project/badge/Grade/64a366db9c814c81807b0ad87b5830a6
[xld-flyway-plugin-codacy-url]: https://www.codacy.com/app/joris-dewinne/xld-flyway-plugin
[xld-flyway-plugin-code-climate-image]: https://codeclimate.com/github/xebialabs-community/xld-flyway-plugin/badges/gpa.svg
[xld-flyway-plugin-code-climate-url]: https://codeclimate.com/github/xebialabs-community/xld-flyway-plugin
[xld-flyway-plugin-license-image]: https://img.shields.io/badge/license-MIT-yellow.svg
[xld-flyway-plugin-license-url]: https://opensource.org/licenses/MIT
[xld-flyway-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xld-flyway-plugin/total.svg
[xld-flyway-plugin-downloads-url]: https://github.com/xebialabs-community/xld-flyway-plugin/releases


# Overview #

The Flyway plugin is a XL Deploy plugin that adds capability for migrating databases using Flyway.

See http://flywaydb.org/documentation/commandline/migrate.html for more information about the Flyway commands and configuration options used by this API.

# Requirements #

* **Requirements**
  * plugin versions <= v2.3.1 require **XL Deploy** 5.1.0+
  * plugin versions >= v3.0.0 require **XL Deploy** 8.5.0+

# Build #

$ ./gradlew xlPlugin

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
    * username          - `string`        - The user to use to connect to the database.
    * password          - `string` 				- The password to use to connect to the database.
    * schemas           - `set_of_string` - Case-sensitive list of schemas managed by Flyway.
		* table             - `string` 				- The name of Flyway's metadata table.
		* locations         - `set_of_string` - List of locations to scan recursively for migrations.
		* encoding          - `string` 				- The encoding of Sql migrations.
		* baselineOnMigrate - `boolean` 			- Whether to automatically call baseline when migrate is executed against a non-empty schema with no metadata table.
																					  This is useful for initial Flyway production deployments on projects with an existing DB.
		* repair            - `boolean` 		  - Repairs the Flyway metadata table.
    * outOfOrder        - `boolean` 			- Allows migrations to be run "out of order". 
																						If you already have versions 1 and 3 applied, and now a version 2 is found, it will be applied too instead of being ignored.
    * validateOnMigrate - `boolean` 			- Whether to automatically call validate or not when running migrate.
    * When using Java based migrations, the java classes need to be in a jar with name `db.jar` and under the folder artifact.
