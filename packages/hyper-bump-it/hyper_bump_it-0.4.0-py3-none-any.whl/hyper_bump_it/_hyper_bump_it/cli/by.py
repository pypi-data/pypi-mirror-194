"""
Bump version by part command.
"""
from pathlib import Path
from typing import Optional

import typer

from .. import core
from ..config import BumpByArgs, BumpPart, GitAction, config_for_bump_by
from . import common


def by_command(
    part_to_bump: BumpPart = typer.Argument(
        ..., help="Part of version to increment", show_default=False
    ),
    config_file: Optional[Path] = common.CONFIG_FILE,
    project_root: Path = common.PROJECT_ROOT,
    dry_run: bool = common.DRY_RUN,
    patch: bool = common.PATCH,
    skip_confirm_prompt: Optional[bool] = common.SKIP_CONFIRM_PROMPT,
    current_version: Optional[str] = common.CURRENT_VERSION,
    commit: Optional[GitAction] = common.commit(),
    branch: Optional[GitAction] = common.branch(),
    tag: Optional[GitAction] = common.tag(),
    remote: Optional[str] = common.remote(),
    commit_format_pattern: Optional[str] = common.commit_format_pattern(),
    branch_format_pattern: Optional[str] = common.branch_format_pattern(),
    tag_format_pattern: Optional[str] = common.tag_format_pattern(),
    allowed_init_branch: list[str] = common.allowed_init_branch(),
    allow_any_init_branch: Optional[bool] = common.allow_any_init_branch(),
) -> None:
    """
    Bump the version to the next value by a specific version part.
    """
    current_version_parsed = common.parse_version(current_version, "--current-version")

    with common.handle_bump_errors():
        app_config = config_for_bump_by(
            BumpByArgs(
                part_to_bump,
                config_file=common.resolve(config_file),
                project_root=common.resolve(project_root),
                dry_run=dry_run,
                patch=patch,
                skip_confirm_prompt=skip_confirm_prompt,
                current_version=current_version_parsed,
                commit=commit,
                branch=branch,
                tag=tag,
                remote=remote,
                commit_format_pattern=commit_format_pattern,
                branch_format_pattern=branch_format_pattern,
                tag_format_pattern=tag_format_pattern,
                allowed_initial_branches=common.allowed_init_branches(
                    allowed_init_branch, allow_any_init_branch
                ),
            )
        )

        core.do_bump(app_config)
