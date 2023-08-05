# Copyright (C) 2020-2022 Greenbone Networks GmbH
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

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Type

from pontos.version.calculator import VersionCalculator


@dataclass
class VersionUpdate:
    previous: str
    new: str
    changed_files: list[Path] = field(default_factory=list)


class VersionCommand(ABC):
    """Generic class usable to implement the
    version commands for several programming languages"""

    project_file_name: str
    version_calculator_class: Type[VersionCalculator] = VersionCalculator

    def __init__(self) -> None:
        self.project_file_path = Path.cwd() / self.project_file_name

    @abstractmethod
    def get_current_version(self) -> str:
        """Get the current version of this project"""

    @abstractmethod
    def verify_version(self, version: str) -> None:
        """Verify the current version of this project"""

    @abstractmethod
    def update_version(
        self, new_version: str, *, develop: bool = False, force: bool = False
    ) -> VersionUpdate:
        """Update the current version of this project"""

    def project_found(self) -> bool:
        """
        Returns True if a command has detected a corresponding project
        """
        return self.project_file_path.exists()

    def get_version_calculator(self) -> VersionCalculator:
        return self.version_calculator_class()
