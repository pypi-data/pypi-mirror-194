"""Definition of the top-level Click group for the Meltano CLI."""

from __future__ import annotations

import logging
import os
import sys
import typing as t
from pathlib import Path

import click

import meltano
from meltano.cli.utils import InstrumentedGroup
from meltano.core.behavior.versioned import IncompatibleVersionError
from meltano.core.error import EmptyMeltanoFileException, ProjectNotFound
from meltano.core.logging import LEVELS, setup_logging
from meltano.core.project import PROJECT_ENVIRONMENT_ENV, Project
from meltano.core.project_settings_service import ProjectSettingsService
from meltano.core.tracking import Tracker
from meltano.core.tracking.contexts import CliContext
from meltano.core.utils import get_no_color_flag

logger = logging.getLogger(__name__)


class NoWindowsGlobbingGroup(InstrumentedGroup):
    """A instrumented Click group that does not perform glob expansion on Windows.

    This restores the behaviour of Click's globbing to how it was before v8.
    Click (as of version 8.1.3) ignores quotes around an asterisk, which makes
    it behave differently than most shells that support globbing, and make some
    typical Meltano commands fail, e.g. `meltano select tap-gitlab tags "*"`.
    """

    def main(self, *args, **kwargs) -> t.NoReturn:
        """Invoke the Click CLI with Windows globbing disabled.

        Args:
            args: Positional arguments for the Click group.
            kwargs: Keyword arguments for the Click group.
        """
        return super().main(*args, windows_expand_args=False, **kwargs)


@click.group(
    cls=NoWindowsGlobbingGroup, invoke_without_command=True, no_args_is_help=True
)
@click.option("--log-level", type=click.Choice(LEVELS.keys()))
@click.option(
    "--log-config", type=str, help="Path to a python logging yaml config file."
)
@click.option("-v", "--verbose", count=True, help="Not used.")
@click.option("--environment", help="Meltano environment name.")
@click.option(
    "--no-environment", is_flag=True, default=False, help="Don't use any environment."
)
@click.option(
    "--cwd",
    type=click.Path(exists=True, file_okay=False, resolve_path=True, path_type=Path),
    help="Run Meltano as if it had been started in the specified directory.",
)
@click.version_option(version=meltano.__version__, prog_name="meltano")
@click.pass_context
def cli(  # noqa: C901,WPS231
    ctx: click.Context,
    log_level: str,
    log_config: str,
    verbose: int,
    environment: str,
    no_environment: bool,
    cwd: Path | None,
):  # noqa: WPS231
    """
    Your CLI for ELT+

    \b\nRead more at https://docs.meltano.com/reference/command-line-interface
    """  # noqa: D400
    ctx.ensure_object(dict)

    if log_level:
        ProjectSettingsService.config_override["cli.log_level"] = log_level

    if log_config:
        ProjectSettingsService.config_override["cli.log_config"] = log_config

    ctx.obj["verbosity"] = verbose
    ctx.obj["explicit_no_environment"] = no_environment

    no_color = get_no_color_flag()
    if no_color:
        ctx.color = False

    if cwd:
        try:
            os.chdir(cwd)
        except OSError as ex:
            raise Exception(f"Unable to run Meltano from {cwd!r}") from ex

    try:  # noqa: WPS229
        project = Project.find()
        setup_logging(project)
        if project.readonly:
            logger.debug("Project is read-only.")

        (
            ctx.obj["selected_environment"],
            ctx.obj["is_default_environment"],
        ) = detect_selected_environment(
            cli_environment=environment,
            cli_no_environment=no_environment,
            project=project,
        )
        ctx.obj["project"] = project
        ctx.obj["tracker"] = Tracker(project)
        ctx.obj["tracker"].add_contexts(CliContext.from_click_context(ctx))
    except ProjectNotFound:
        ctx.obj["project"] = None
    except EmptyMeltanoFileException:
        if ctx.invoked_subcommand != "init":
            raise
        ctx.obj["project"] = None
    except IncompatibleVersionError:
        click.secho(
            "This Meltano project is incompatible with this version of `meltano`.",
            fg="yellow",
        )
        click.echo(
            "For more details, visit https://docs.meltano.com/guide/installation#upgrading-meltano-version"
        )
        sys.exit(3)


def detect_selected_environment(
    *,
    cli_environment: str | None,
    cli_no_environment: bool,
    project: Project,
) -> tuple[str | None, bool]:
    """Detect the Meltano environment selected (but not yet activated).

    Precedence is:
    1. The `--environment` CLI option
    2. Env var from the shell
    3. Env var from `.env`
    4. Default environment from `meltano.yml`
    5. `None`

    Args:
        cli_environment: The `--environment` option value from the CLI.
        no_environment: The `--no-environment` option value from the CLI.
        project: The Meltano project.
        project_setting_service: A project settings service for the project.

    Returns:
        The selected environment, and whether it is the default environment.
    """
    environment = cli_environment or os.environ.get(
        PROJECT_ENVIRONMENT_ENV,
        project.dotenv_env.get(PROJECT_ENVIRONMENT_ENV, None),
    )
    if cli_no_environment or (environment and environment.lower() == "null"):
        logger.info("No Meltano environment was selected")
    elif environment:
        return environment, False
    elif project.settings.get("default_environment"):
        return project.settings.get("default_environment"), True
    return None, False
