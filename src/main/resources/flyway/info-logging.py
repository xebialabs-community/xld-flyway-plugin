from flyway.FlywayUtil import FlywayUtil

flyway = FlywayUtil.create_flyway_client(thisCi.serverUrl, thisCi.username, thisCi.password)
flyway.log_results(thisCi.infoMode)
