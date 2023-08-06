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

"""
This module contains classes to represent survey questions.

These can be constructed from YAML through the YamlConstructable abstract
class.
"""
# alias name to avoid clash with schema.Optional
import logging
from typing import Dict, List, Optional, Set

import schema
from pandas import Series

from hifis_surveyval.core.settings import Settings
from hifis_surveyval.models.answer_option import AnswerOption
from hifis_surveyval.models.answer_types import VALID_ANSWER_TYPES
from hifis_surveyval.models.mixins.mixins import HasLabel, HasText, HasID
from hifis_surveyval.models.mixins.yaml_constructable import (
    YamlConstructable, YamlDict)
from hifis_surveyval.models.translated import Translated


class Question(YamlConstructable, HasID, HasLabel, HasText):
    """
    Questions model concrete questions that could be answered in the survey.

    They can be constructed from YAML metadata via from_yaml_dictionary(). For
    this to be successful the YAML data has to adhere to Question.schema which
    describes the required fields and their data types.
    Answers then have to be added separately via add_answer().
    """

    token_ID = "id"
    token_ANSWER_OPTIONS = "answers"
    token_DATA_TYPE = "datatype"
    token_MANDATORY = "mandatory"

    schema = schema.Schema(
        {
            token_ID: str,
            HasLabel.YAML_TOKEN: str,
            HasText.YAML_TOKEN: dict,
            token_DATA_TYPE: lambda t: t in VALID_ANSWER_TYPES,
            token_MANDATORY: bool,
            schema.Optional(token_ANSWER_OPTIONS, default=[]): list,
            schema.Optional(str): object,  # Catchall for unsupported yaml data
        }
    )

    # TODO: log unsupported elements in YAML?

    def __init__(
        self,
        parent_id: str,
        question_id: str,
        text: Translated,
        label: str,
        answer_type: type,
        mandatory: bool,
        answer_options: List[AnswerOption],
        settings: Settings,
    ):
        """
        Initialize a question object with metadata.

        The answers have to be added separately via add_answer().

        Args:
            parent_id:
                The ID of the question collection this question is embedded in.
            question_id:
                An identifier assigned to the question. Must be unique within
                the question collection.
            text:
                A Translated object representing the text that describes the
                question.
            label:
                A short label that can be used in plotting to represent the
                question collection.
            answer_type:
                The data type of the answers. Must be one of the supported
                data types. See also
                hifis_surveyval.models.answer_types.VALID_ANSWER_TYPES
            mandatory:
                Whether there is an answer to this question expected from each
                participant in oder to consider the participant's answer data
                complete.
            answer_options:
                An optional list of predefined answers. If there are none
                given, the question can have any answer, otherwise the answer
                must be the short ID of the selected answer option.
            settings:
                An object reflecting the application settings.
        """
        super().__init__(
            object_id=question_id,
            parent_id=parent_id,
            label=label,
            translations=text,
            settings=settings
        )
        self._answer_type = answer_type
        self._mandatory = mandatory

        # Answer options are stored with their short ID as keys for easy
        # lookup when associating answers, since answers contain these as
        # values when selected.
        self._answer_options: Dict[str, AnswerOption] = {
            option.short_id: option for option in answer_options
        }

        # The actual answers are not part of the metadata but have to be read
        # from other sources in a separate step
        self._answers: Dict[str, Optional[answer_type]] = {}

    def add_answer(self, participant_id: str, value: str):
        """
        Store a given answer to this question.

        The answer value will be casted to the expected answer type.

        Args:
            participant_id:
                The ID of the participant who gave the answer
            value:
                The text-version of the answer as stored in the CSV.
                If the question is mandatory, the value must not be empty.
                If answer options are defined the value must match the short id
                of the selected answer option.
        Raises:
            ValueError:
                if the question was marked as mandatory but the given value was
                 an empty string
            KeyError:
                If answer options were present, but none of the answer options
                had an ID that matched the given value
        """
        # TODO this check should be performed when marking invalid answers,
        #  but must not prevent answers from being included in the first place
        # Mandatory questions must have an answer
        # if self._mandatory and not value:
        #     raise ValueError("No answer was given, but it was mandatory")

        if not value:
            # Convert empty strings to None to properly indicate that no
            # data was provided
            value = None
        elif self._answer_options:
            # If answer options are defined, the answer value is expected to
            # be the short id of the corresponding answer option
            # The label of the option then will be casted to the desired
            # data type
            option = self._answer_options[value]
            value = self._answer_type(option.label)
            # FIXME change: answer option values become a separate field,
            #  no longer derived from labels
        elif self._answer_type == bool:
            # When casting to boolean values, Python casts any non-empty string
            # to True and only empty strings to False. Consequently, values
            # are transformed according to a set of valid true and false
            # values to allow for different truth values.
            if value in self._settings.TRUE_VALUES:
                value = True
            elif value in self._settings.FALSE_VALUES:
                value = False
            else:
                logging.error(f"Boolean data is an invalid truth value "
                              f"in question {self.full_id}: {value}.")
                value = None
        else:
            # try to cast the answer value to the expected type
            value = self._answer_type(value)

        self._answers[participant_id] = value

    def remove_answers(self, participant_ids: Set[str]) -> None:
        """
        Remove the answers by the specified participants.

        Args:
            participant_ids:
                The IDs of the participants whose answers are to be removed.
                Invalid IDs are ignored.
        """
        for participant_id in participant_ids:
            if participant_id in self._answers:
                del self._answers[participant_id]

    @property
    def answers(self) -> Dict[str, Optional[object]]:  # NOTE (0) below
        """
        Obtain the given answers as read from the survey data.

        The answers are given as a mapping:
        participant ID -> participant answer

        The participant ID will be a string, while the answers may be
        assumed to be of the answer_type of the Question.
        If the Question is not mandatory, answers may also be None.

        Returns:
            The mapping from participant ID to the participant's answer for
            this question.
        """
        return self._answers

    # (0) Sadly I found no better way to narrow down the type since I could
    # not refer to self._answer_type when specifying the return type.
    # Suggestions for improvement are welcome.

    def as_series(self) -> Series:
        """
        Obtain the answers to this question as a pandas.Series.

        The series' index are the participant IDs, while data for the
        indices are the respective answers.

        The series will be named with the question's full ID.

        Returns:
            A pandas.Series representing the answers for each participant
        """
        series = Series(self._answers)
        series.name = self.full_id
        series.index.name = self._settings.ID_COLUMN_NAME
        return series

    @staticmethod
    def _from_yaml_dictionary(yaml: YamlDict, **kwargs) -> "Question":
        """
        Generate a new Question-instance from YAML data.

        Args:
            yaml:
                A YAML dictionary describing the Question

        Keyword Args:
            parent_id:
                (Required) The full ID of the QuestionCollection this Question
                belongs to.
            settings:
                (Required) An object reflecting the applications settings.

        Returns:
            A new Question containing the provided data
        """
        question_id = yaml[Question.token_ID]
        parent_id = kwargs["parent_id"]
        settings: Settings = kwargs["settings"]

        answer_type: type = VALID_ANSWER_TYPES[yaml[Question.token_DATA_TYPE]]

        answer_options = [
            AnswerOption.from_yaml_dictionary(
                yaml=answer_yaml,
                parent_id=question_id,
                settings=settings
            )
            for answer_yaml in yaml[Question.token_ANSWER_OPTIONS]
        ]

        return Question(
            question_id=question_id,
            parent_id=parent_id,
            label=yaml[HasLabel.YAML_TOKEN],
            text=Translated(yaml[HasText.YAML_TOKEN]),
            answer_type=answer_type,
            answer_options=answer_options,
            mandatory=yaml[Question.token_MANDATORY],
            settings=settings
        )
