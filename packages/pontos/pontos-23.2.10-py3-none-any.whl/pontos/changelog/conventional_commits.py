# Copyright (C) 2021-2022 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import re
import subprocess
import sys
from argparse import ArgumentParser
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Union

import tomlkit

from pontos.changelog.errors import ChangelogBuilderError
from pontos.git import Git
from pontos.terminal import Terminal
from pontos.terminal.null import NullTerminal
from pontos.terminal.rich import RichTerminal

ADDRESS = "https://github.com/"

DEFAULT_CHANGELOG_CONFIG = """commit_types = [
    { message = "^add", group = "Added"},
    { message = "^remove", group = "Removed"},
    { message = "^change", group = "Changed"},
    { message = "^fix", group = "Bug Fixes"},
]
"""


class ChangelogBuilder:
    """
    Creates Changelog files from conventional commits using the git log,
    from the latest tag.
    """

    def __init__(
        self,
        *,
        terminal: Terminal,
        space: str,
        project: str,
        git_tag_prefix: Optional[str] = "v",
        config: Optional[Path] = None,
    ):
        self._terminal = terminal

        if config:
            if not config.exists():
                raise ChangelogBuilderError(
                    f"Changelog Config file '{config.absolute()}' does not "
                    "exist."
                )

            self.config = tomlkit.parse(config.read_text(encoding="utf-8"))
        else:
            self.config = tomlkit.parse(DEFAULT_CHANGELOG_CONFIG)

        self.project = project
        self.space = space

        self.git_tag_prefix = git_tag_prefix

    def create_changelog(
        self,
        *,
        last_version: Optional[str] = None,
        next_version: Optional[str] = None,
    ) -> str:
        """
        Create a changelog

        Args:
            last_version: Version of the last release. If None it is considered
                as the first release.
            next_version: Version of the to be created release the changelog
                corresponds to. If None a changelog for an unrelease version
                will be created.

        Returns:
            The created changelog content.
        """
        commit_list = self._get_git_log(last_version)
        commit_dict = self._sort_commits(commit_list)
        return self._build_changelog(last_version, next_version, commit_dict)

    def create_changelog_file(
        self,
        output: Union[str, Path],
        *,
        last_version: Optional[str] = None,
        next_version: Optional[str] = None,
    ) -> None:
        """
        Create a changelog and write the changelog to a file

        Args:
            output: A file path where to store the changelog
            last_version: Version of the last release. If None it is considered
                as the first release.
            next_version: Version of the to be created release the changelog
                corresponds to. If None a changelog for an unrelease version
                will be created.
        """
        changelog = self.create_changelog(
            last_version=last_version, next_version=next_version
        )
        self._write_changelog_file(changelog, output)

    def _get_first_commit(self) -> str:
        """
        Git the first commit ID for the current branch
        """
        git = Git()
        return git.rev_list("HEAD", max_parents=0, abbrev_commit=True)[0]

    def _get_git_log(self, last_version: Optional[str]) -> List[str]:
        """Getting the git log for the next version.

        Requires the fitting branch to be checked out

        Returns:
            A list of `git log` entries
        """
        git = Git()
        if not last_version:
            return git.log(oneline=True)

        git_version = f"{self.git_tag_prefix}{last_version}"
        return git.log(
            f"{git_version}..HEAD",
            oneline=True,
        )

    def _sort_commits(self, commits: List[str]) -> Dict[str, List[str]]:
        """Sort the commits by commit type and group them
        in a dict
        ```
        {
            'Added:': [
                'commit 1 [1234567](..)',
                'commit 2 [1234568](..)',
                '...',
            ],
            'Fixed:': [
                ...
            ],
        }
        ```

        Returns
            The dict containing the commit messages"""
        # get the commit types from the toml
        commit_types = self.config.get("commit_types")

        commit_link = f"{ADDRESS}{self.space}/{self.project}/commit/"

        commit_dict = {}
        if commits and len(commits) > 0:
            for commit in commits:
                commit = commit.split(" ", maxsplit=1)
                for commit_type in commit_types:
                    reg = re.compile(
                        rf'{commit_type["message"]}\s?[:|-]', flags=re.I
                    )
                    match = reg.match(commit[1])
                    if match:
                        if commit_type["group"] not in commit_dict:
                            commit_dict[commit_type["group"]] = []

                        # remove the commit tag from commit message
                        cleaned_msg = (
                            commit[1].replace(match.group(0), "").strip()
                        )
                        commit_dict[commit_type["group"]].append(
                            f"{cleaned_msg} [{commit[0]}]"
                            f"({commit_link}{commit[0]})"
                        )
                        self._terminal.info(f"{commit[0]}: {cleaned_msg}")

        return commit_dict

    def _build_changelog(
        self,
        last_version: Optional[str],
        next_version: Optional[str],
        commit_dict: Dict[str, List[str]],
    ) -> str:
        """
        Building the changelog from the passed commit information.

        Args:
            commit_dict: dict containing sorted commits

        Returns:
            The changelog content
        """

        # changelog header
        changelog = [
            "# Changelog\n",
            "All notable changes to this project "
            "will be documented in this file.\n",
        ]
        if next_version:
            changelog.append(
                f"## [{next_version}] - {date.today().isoformat()}"
            )
        else:
            changelog.append("## [Unreleased]")

        # changelog entries
        commit_types = self.config.get("commit_types")
        for commit_type in commit_types:
            if commit_type["group"] in commit_dict.keys():
                changelog.append(f"\n## {commit_type['group']}")
                for msg in commit_dict[commit_type["group"]]:
                    changelog.append(f"* {msg}")

        # comparison line (footer)
        pre = "\n[Unreleased]: "
        compare_link = f"{ADDRESS}{self.space}/{self.project}/compare/"
        if next_version and last_version:
            pre = f"\n[{next_version}]: "
            diff = (
                f"{self.git_tag_prefix}{last_version}..."
                f"{self.git_tag_prefix}{next_version}"
            )
        elif next_version:
            first_commit = self._get_first_commit()
            pre = f"\n[{next_version}]: "
            diff = f"{first_commit}...{self.git_tag_prefix}{next_version}"
        elif last_version:
            # unreleased version
            diff = f"{self.git_tag_prefix}{last_version}...HEAD"
        else:
            # unreleased version
            first_commit = self._get_first_commit()
            diff = f"{first_commit}...HEAD"

        changelog.append(f"{pre}{compare_link}{diff}")

        return "\n".join(changelog)

    def _write_changelog_file(
        self, changelog: str, output: Union[str, Path]
    ) -> None:
        """
        Write changelog to an output file

        Args:
            changelog: Changelog content to write to output file
            output: File name to write changelog into
        """

        changelog_file = Path(output)

        changelog_dir = changelog_file.parent
        changelog_dir.mkdir(parents=True, exist_ok=True)

        changelog_file.write_text(changelog, encoding="utf-8")


def parse_args(args: Iterable[str] = None) -> ArgumentParser:
    parser = ArgumentParser(
        description="Conventional commits utility.",
        prog="pontos-changelog",
    )

    parser.add_argument(
        "--config",
        "-C",
        default="changelog.toml",
        type=Path,
        help="Conventional commits config file (toml), including conventions.",
    )

    parser.add_argument(
        "--project",
        required=True,
        help="The github project",
    )

    parser.add_argument(
        "--space",
        default="greenbone",
        help="User/Team name in github",
    )

    parser.add_argument(
        "--current-version",
        default="greenbone",
        help="Current version before these changes",
    )

    parser.add_argument(
        "--next-version",
        help="The planned release version",
    )

    parser.add_argument(
        "--output",
        "-o",
        default="unreleased.md",
        help="The path to the output file (.md)",
    )

    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Don't print messages to the terminal",
    )

    parser.add_argument(
        "--log-file",
        dest="log_file",
        type=str,
        help="Activate logging using the given file path",
    )

    return parser.parse_args(args=args)


def main(
    args=None,
) -> None:
    parsed_args = parse_args(args)

    if parsed_args.quiet:
        term = NullTerminal()
    else:
        term = RichTerminal()

    term.bold_info("pontos-changelog")

    with term.indent():
        try:
            changelog_builder = ChangelogBuilder(
                terminal=term,
                config=parsed_args.config,
                project=args.project,
                space=args.space,
            )
            changelog_builder.create_changelog_file(
                args.output,
                last_version=args.current_version,
                next_version=args.next_version,
            )
        except ChangelogBuilderError as e:
            term.error(str(e))
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            term.error(f'Could not run command "{e.cmd}".')
            term.out(f"Error was: {e.stderr}")
            sys.exit(1)

    sys.exit(0)
