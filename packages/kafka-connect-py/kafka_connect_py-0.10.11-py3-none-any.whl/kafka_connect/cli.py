from .kafka_connect import KafkaConnect

import click
import json
import os
import logging
import requests
import traceback
import urllib3


class CatchAllExceptions(click.Group):
    """A click group that catches all exceptions and displays them as a message.
    This class extends the functionality of the `click.Group` class by adding
    a try-except block around the call to `main()`. Any exceptions that are
    raised during the call to `main()` are caught and displayed as a message
    to the user.
    """

    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except (
            requests.exceptions.RequestException,
            urllib3.exceptions.HTTPError,
        ) as e:
            click.echo(e)
        except Exception as e:
            if os.environ.get("KAFKA_CONNECT_ENABLE_TRACEBACK", "false").lower() == "true":
                click.echo(traceback.print_exc())
            else:
                click.echo(
                    "\n".join(
                        [
                            f"Oops! An unknown error has occurred: {e}",
                            "",
                            "Setting KAFKA_CONNECT_ENABLE_TRACEBACK=true will provide more information in the event of a python error.",
                            "Please see consider opening an issue: https://github.com/aidanmelen/kafka-connect-py/issues",
                        ]
                    )
                )


def get_logger(log_level="NOTSET"):
    """Get a logger configured to write to the console.

    Args:
        log_level (str): The logging level to use for the logger and console
            handler. Defaults to "INFO".

    Returns:
        A logger configured to write log messages with a level equal to or higher
        than `log_level` to the console.
    """
    # create logger
    logger = logging.getLogger("kafka-connect")
    log_level_number = logging.getLevelName(log_level.upper())
    logger.setLevel(log_level_number)

    # create console handler and set log level
    ch = logging.StreamHandler()
    ch.setLevel(log_level.upper())

    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger


@click.group(cls=CatchAllExceptions)
@click.version_option(package_name="kafka-connect-py", prog_name="kc|kafka-connect")
@click.option("--url", "-u", default="http://localhost:8083", metavar="URL", envvar="KAFKA_CONNECT_URL", show_envvar=True, help="The base URL for the Kafka Connect REST API.")
@click.option("--auth", "-a", metavar="USERNAME:PASSWORD", envvar="KAFKA_CONNECT_BASIC_AUTH", show_envvar=True, help="A colon-delimited string of `username` and `password` to use for authenticating with the Kafka Connect REST API.")
@click.option("--ssl-verify/--no-ssl-verify", "-s", default=True, is_flag=True, envvar="KAFKA_CONNECT_SSL_VERIFY", show_envvar=True, help="Whether to verify the SSL certificate when making requests to the Kafka Connect REST API.")
@click.option("--log-level", "-l", type=click.Choice( ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"], case_sensitive=False, ), default="NOTSET", metavar="LEVEL", envvar="KAFKA_CONNECT_LOG_LEVEL", show_envvar=True, help="The logging level to use for the logger and console handler.")
@click.pass_context
def cli(ctx, url, auth, ssl_verify, log_level):
    """A command-line client for the Confluent Platform Kafka Connect REST API."""
    logger = get_logger(log_level)
    kafka_connect = KafkaConnect(url, auth, ssl_verify, logger)
    ctx.obj = kafka_connect


@cli.command()
@click.pass_obj
def info(kafka_connect):
    """Get the version and other details of the Kafka Connect cluster."""
    cluster = kafka_connect.get_cluster_info()
    click.echo(json.dumps(cluster))


@cli.command()
@click.option("-e", "--expand", type=click.Choice(["status", "info"]), show_envvar=True, help="Whether to retrieve additional information about the connectors.")
@click.option("-p", "--pattern", default=None, metavar="REGEX", show_envvar=True, help="The regex pattern that will list only the connectors that match.")
@click.option("-s", "--state", type=click.Choice(["RUNNING", "PAUSED", "UNASSIGNED", "FAILED"], case_sensitive=False), default=None, metavar="STATE", show_envvar=True, help="The state that will list only the connectors that match.")
@click.pass_obj
def list(kafka_connect, expand, pattern, state):
    """Get a list of active connectors."""
    response = kafka_connect.list_connectors(expand=expand, pattern=pattern, state=state)
    click.echo(json.dumps(response))


@cli.command()
@click.option("--config-file", "-f", type=click.File("r"), help="Path to the configuration file")
@click.option("--config-data", "-d", help="Inline configuration data in JSON format")
@click.pass_obj
def create(kafka_connect, config_file, config_data):
    """Create a new connector, returning the current connector info if successful. Return 409 (Conflict) if rebalance is in process, or if the connector already exists."""
    try:
        if config_file:
            config_data = json.loads(config_file.read())
        elif config_data:
            config_data = json.loads(config_data)
        else:
            raise click.UsageError("One of --config-file or --config-data is required")
    except json.JSONDecodeError as e:
        click.echo(f"Error decoding JSON: {e}")
        return None
    
    response = kafka_connect.create_connector(config_data)
    click.echo(json.dumps(response))


@cli.command()
@click.argument("connector")
@click.option("--config-file", "-f", type=click.File("r"), help="Path to the configuration file")
@click.option("--config-data", "-d", help="Inline configuration data in JSON format")
@click.pass_obj
def update(kafka_connect, connector, config_file, config_data):
    """Create a new connector using the given configuration, or update the configuration for an existing connector. Returns information about the connector after the change has been made. Return 409 (Conflict) if rebalance is in process."""
    try:
        if config_file:
            config_data = json.loads(config_file.read())
        elif config_data:
            config_data = json.loads(config_data)
        else:
            raise click.UsageError("One of --config-file or --config-data is required")
    except json.JSONDecodeError as e:
        click.echo(f"Error decoding JSON: {e}")
        return None
    
    response = kafka_connect.update_connector(connector, config_data)
    click.echo(json.dumps(response))


@cli.command()
@click.argument("connector")
@click.pass_obj
def get(kafka_connect, connector):
    """Gets the details of a connector or all connectors matching a certain pattern."""
    response = kafka_connect.get_connector(connector)
    click.echo(json.dumps(response))


@cli.command()
@click.argument("connector")
@click.pass_obj
def config(kafka_connect, connector):
    """Gets the config of a connector."""
    response = kafka_connect.get_connector_config(connector)
    click.echo(json.dumps(response))


@cli.command()
@click.argument("connector")
@click.pass_obj
def status(kafka_connect, connector):
    """Gets the status of a connector."""
    response = kafka_connect.get_connector_status(connector)
    click.echo(json.dumps(response))


@cli.command()
@click.argument("connector", required=False)
@click.option("-i", "--include-tasks", is_flag=True, default=False, show_envvar=True, help="Whether to include the Task objects in the restart operation.")
@click.option("-o", "--only-failed", is_flag=True, default=False, show_envvar=True, help="Whether to restart only failed Task objects.")
@click.option("-a", "--all", is_flag=True, default=False, show_envvar=True, help="Whether to restart all connectors.")
@click.option("-p", "--pattern", default=None, metavar="REGEX", show_envvar=True, help="The regex pattern that will restart only the connectors that match when the --all option is set.")
@click.option("-s", "--state", type=click.Choice(["RUNNING", "PAUSED", "UNASSIGNED", "FAILED"], case_sensitive=False), default=None, metavar="STATE", show_envvar=True, help="The state that will list only the connectors that match.")
@click.pass_obj
def restart(kafka_connect, connector, include_tasks, only_failed, all, pattern, state):
    """Restart a connector or all connectors matching a certain pattern."""
    if all:
        response = kafka_connect.restart_all_connectors(
            include_tasks=include_tasks, only_failed=only_failed, pattern=pattern
        )
        click.echo(
            json.dumps(kafka_connect.list_connectors(expand="status", pattern=pattern, state=state))
        )
    elif connector:
        response = kafka_connect.restart_connector(
            connector, include_tasks=include_tasks, only_failed=only_failed
        )
        click.echo(json.dumps(kafka_connect.get_connector_status(connector)))
    else:
        raise click.UsageError("One of connector or --all is required")


@cli.command()
@click.argument("connector", required=False)
@click.option("-a", "--all", is_flag=True, default=False, show_envvar=True, help="Whether to pause all connectors.")
@click.option("-p", "--pattern", default=None, metavar="REGEX", show_envvar=True, help="The regex pattern that will pause only the connectors that match when the --all option is set.")
@click.option("-s", "--state", type=click.Choice(["RUNNING", "PAUSED", "UNASSIGNED", "FAILED"], case_sensitive=False), default=None, metavar="STATE", show_envvar=True, help="The state that will list only the connectors that match.")
@click.pass_obj
def pause(kafka_connect, connector, all, pattern, state):
    """Pauses a connector or all connectors that match a certain pattern."""
    if all:
        response = kafka_connect.pause_all_connectors(pattern=pattern, state=state)
    elif connector:
        response = kafka_connect.pause_connector(connector)
    else:
        raise click.UsageError("One of connector or --all is required")


@cli.command()
@click.argument("connector", required=False)
@click.option("-a", "--all", is_flag=True, default=False, show_envvar=True, help="Whether to resume all connectors.")
@click.option("-p", "--pattern", default=None, metavar="REGEX", show_envvar=True, help="The regex pattern that will resume only the connectors that match when the --all option is set.")
@click.option("-s", "--state", type=click.Choice(["RUNNING", "PAUSED", "UNASSIGNED", "FAILED"], case_sensitive=False), default=None, metavar="STATE", show_envvar=True, help="The state that will list only the connectors that match.")
@click.pass_obj
def resume(kafka_connect, connector, all, pattern, state):
    """Resumes a connector or all connectors that match a certain pattern."""
    if all:
        response = kafka_connect.resume_all_connectors(pattern=pattern, state=state)
    elif connector:
        response = kafka_connect.resume_connector(connector)
    else:
        raise click.UsageError("One of connector or --all is required")


@cli.command()
@click.argument("connector", required=False)
@click.option("-a","--all",is_flag=True,default=False,show_envvar=True,help="Whether to delete all connectors.")
@click.option("-p","--pattern",default=None,metavar="REGEX",show_envvar=True,help="The regex pattern that will delete only the connectors that match when the --all option is set.")
@click.option("-s","--state",type=click.Choice(["RUNNING", "PAUSED", "UNASSIGNED", "FAILED"], case_sensitive=False),default=None,metavar="STATE",show_envvar=True,help="The state that will list only the connectors that match.")
@click.pass_obj
def delete(kafka_connect, connector, all, pattern, state):
    """Deletes a connector or all connectors that match a certain pattern."""
    if all:
        response = kafka_connect.delete_all_connectors(pattern=pattern, state=state)
    elif connector:
        response = kafka_connect.delete_connector(connector)
    else:
        raise click.UsageError("One of connector or --all is required")


@cli.command()
@click.argument("connector")
@click.pass_obj
def list_tasks(kafka_connect, connector):
    """Gets the list of tasks associated with a connector."""
    response = kafka_connect.list_connector_tasks(connector)
    click.echo(json.dumps(response))


@cli.command()
@click.argument("connector")
@click.argument("task_id")
@click.pass_obj
def task_status(kafka_connect, connector, task_id):
    """Gets the status of a task associated with a connector."""
    response = kafka_connect.get_connector_task_status(connector, task_id)
    click.echo(json.dumps(response))


@cli.command()
@click.argument("connector")
@click.argument("task_id")
@click.pass_obj
def restart_task(kafka_connect, connector, task_id):
    """Restart a specific task of a connector."""
    response = kafka_connect.restart_connector_task(connector, task_id)
    click.echo(json.dumps(response))


@cli.command()
@click.argument("connector")
@click.pass_obj
def list_topics(kafka_connect, connector):
    """Get the list of topics for a connector."""
    response = kafka_connect.list_connector_topics(connector)
    click.echo(json.dumps(response))


@cli.command()
@click.argument("connector")
@click.pass_obj
def reset_topics(kafka_connect, connector):
    """Reset the list of topics for a connector."""
    response = kafka_connect.reset_connector_topics(connector)
    click.echo(json.dumps(response))


@cli.command()
@click.pass_obj
def list_plugins(kafka_connect):
    """Get the list of connector plugins."""
    response = kafka_connect.list_connector_plugins()
    click.echo(json.dumps(response))


@cli.command()
@click.argument("plugin")
@click.option("--config-file", "-f", type=click.File("r"), help="Path to the configuration file")
@click.option("--config-data", "-d", help="Inline configuration data in JSON format")
@click.pass_obj
def validate_config(kafka_connect, plugin, config_file, config_data):
    """Validate the configuration for a specific connector plugin."""
    if config_file:
        config_data = config_file.read()
    elif config_data:
        config_data = config_data
    else:
        raise click.UsageError("One of --config-file or --config-data is required")
    config = json.loads(config_data)
    response = kafka_connect.validate_connector_config(plugin, config_data)
    click.echo(json.dumps(response))
