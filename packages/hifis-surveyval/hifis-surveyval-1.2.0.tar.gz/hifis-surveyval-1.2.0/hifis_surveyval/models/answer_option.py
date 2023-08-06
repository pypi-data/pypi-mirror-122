# hifis-surveyval
# Framework to help developing analysis scripts for the HIFIS Software survey.
#
# SPDX-FileCopyrightText: 2021 HIFIS Software <support@hifis.net>
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
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""This module contains a class to represent survey answers."""

from schema import Schema

from hifis_surveyval.core.settings import Settings
from hifis_surveyval.models.mixins.mixins import HasLabel, HasText, HasID
from hifis_surveyval.models.mixins.yaml_constructable import (
    YamlConstructable,
    YamlDict,
)
from hifis_surveyval.models.translated import Translated


class AnswerOption(YamlConstructable, HasID, HasLabel, HasText):
    """The AnswerOption models allowed answers for a specific Question."""

    token_ID = "id"

    schema = Schema(
        {token_ID: str, HasLabel.YAML_TOKEN: str, HasText.YAML_TOKEN: dict}
    )

    def __init__(
            self,
            parent_id: str,
            option_id: str,
            text: Translated,
            label: str,
            settings: Settings
    ) -> None:
        """
        Create an answer option from the metadata.

        Args:
            parent_id:
                The full ID of the question this answer option belongs to.
            option_id (str):
                A unique string identifying the answer.
            text:
                A Translated object containing the texts that represent the
                answer option across various languages.
            label:
                A short string used to represent the answer option in plotting.
            settings:
                An object reflecting the application settings.
        """
        super().__init__(
            object_id=option_id,
            parent_id=parent_id,
            label=label,
            translations=text,
            settings=settings
        )

    def __str__(self) -> str:
        """
        Generate a string representation of the answer option.

        Returns:
                String representation of the answer.
        """
        return f"{self.full_id}: {self._label}"

    @staticmethod
    def _from_yaml_dictionary(yaml: YamlDict, **kwargs) -> "AnswerOption":
        """
        Generate a new AnswerOption-instance from YAML data.

        Args:
            yaml:
                A YAML dictionary describing the AnswerOption
            **kwargs:
                Must contain the ID of the Question-instance to which the newly
                generated AnswerOption belongs as the parameter "parent_id".
        Returns:
            A new AnswerOption containing the provided data
        """
        parent_id = kwargs["parent_id"]
        settings: Settings = kwargs["settings"]

        return AnswerOption(
            parent_id=parent_id,
            option_id=yaml[AnswerOption.token_ID],
            label=yaml[HasLabel.YAML_TOKEN],
            text=Translated.from_yaml_dictionary(
                yaml[HasText.YAML_TOKEN]
            ),
            settings=settings
        )
