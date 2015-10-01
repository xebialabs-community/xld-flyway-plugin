# Preface #

This document describes the functionality provided by the Flyway plugin.

See the **XL Deploy Reference Manual** for background information on XL Deploy and deployment concepts.

# Overview #

The Flyway plugin is a XL Deploy plugin that adds capability for migrating databases using Flyway.

# Requirements #

* **Requirements**
	* **XL Deploy** 5.0.0

# Installation #

Place the plugin JAR file into your `SERVER_HOME/plugins` directory.

# Usage #

1. Go to `Repository - Infrastructure`, create a new `flyway.Runner`.
2. Create an environment under `Repository - Environments`
3. Create an application with `flyway.Scripts` as deployable.
4. Start migrating

# API #

* `flyway.Scripts`
    * schemas - `set_of_string` - 
    * table - `string` -
    * locations - `set_of_string` - Location in archive containing scripts
    * encoding - `string` - 
    * baselineOnMigrate - `boolean` - Whether to automatically call baseline when migrate is executed against a non-empty schema with no metadata table.
    * username - `string` - 
    * password - `string` - 
    * startClean - `boolean` - Drops all objects (tables, views, procedures, triggers, ...) in the configured schemas. The schemas are cleaned in the order specified by the schemas property.
