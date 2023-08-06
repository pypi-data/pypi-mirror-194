from __future__ import annotations  # Added for type hints

import functools
import itertools
import logging
import os
import struct

from abc import ABC, abstractmethod
from collections import defaultdict
from pathlib import Path
from typing import Any, DefaultDict, Optional, Union, Iterable

from fittie.utils.datastream import DataStream, Streamable
from fittie.utils.exceptions import DecodeException
from fittie.fitfile.data_message import DataMessage
from fittie.fitfile.definition_message import DefinitionMessage
from fittie.fitfile.field_description import FieldDescription
from fittie.fitfile.header import Header, decode_header
from fittie.fitfile.profile.fit_types import FIT_TYPES
from fittie.fitfile.profile.mesg_nums import MESG_NUMS
from fittie.fitfile.records import read_record_header, read_record
from fittie.fitfile.util import datetime_from_timestamp

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=LOGLEVEL)
logger = logging.getLogger("fittie")


class _IterableMixin(ABC):
    @property
    @abstractmethod
    def _iter_collection(self):
        """
        Defines which collection of data the __next__ method should use.

        Make sure to decorate this with @cached_property if it is an expensive
        calculation.

        Also make sure to add __dict__ to  __slots__ if slots are used and the
        property is cached, because  __dict__ has to be mutable.
        """
        ...

    def __next__(self) -> dict:
        if self._iter_index >= len(self._iter_collection):
            # Remove _iter_collection value from cache, if it exists.
            # If _iter_collection is cached, then it should exist and be cleared
            # as soon as the collection has been fully iterated.
            if "_iter_collection" in self.__dict__:
                del self.__dict__["_iter_collection"]

            # Remove _iter_file from dict, because it is only used in iterations
            if "_iter_filter" in self.__dict__:
                del self.__dict__["_iter_filter"]

            raise StopIteration

        value = self._iter_collection[self._iter_index]
        self._iter_index += 1

        if hasattr(self, "_iter_filter") and (fields := self._iter_filter["fields"]):
            return {field: value.fields[field] for field in fields}

        return value.fields

    def __iter__(self):
        self._iter_index = 0
        return self


class FitFile(_IterableMixin):

    header: Header
    data_messages: dict[str, list[DataMessage]]
    local_message_definitions: dict[int, DefinitionMessage] = {}
    developer_data: dict[int, dict[str, Any]] = {}  # TODO: add typing

    def __init__(
        self,
        header: Header,
        data_messages: dict[str, list[DataMessage]],
        local_message_definitions: dict[int, DefinitionMessage],
        developer_data: dict[int, dict[str, Any]],
    ):
        self.header = header
        self.data_messages = data_messages
        self.local_message_definitions = local_message_definitions
        self.developer_data = developer_data

    @functools.cached_property
    def _iter_collection(self) -> Iterable[DataMessage]:
        if hasattr(self, "_iter_filter"):
            # Entered through __call__, filter messages
            message_type = self._iter_filter["message_type"]
            return self.data_messages.get(message_type, [])

        return list(itertools.chain(*self.data_messages.values()))

    def __call__(self, *, message_type: str, fields: Optional[list[str]] = None):
        """
        Makes the instance callable and adds filter options for a specific message
        type and keywords of field values to return while iterating
        """
        self._iter_filter = {
            "fields": fields or [],
            "message_type": message_type,
        }

        return self

    @property
    def file_id(self) -> Optional[dict[str, Any]]:
        """
        Get file id information.

        Raw values from the FIT file will be filled with information from the Garmin
        FIT SDK Fit Types
        """
        if not (file_id_messages := self.data_messages.get("file_id")):
            raise ValueError(
                "no file_id message detected, FIT file is possible incorrect"
            )

        file_id = {}

        # Should be just one file_id, but to be sure use latest from list
        for key, value in file_id_messages[-1].fields.items():
            if key == "time_created":
                file_id[key] = datetime_from_timestamp(value)
            elif key == "type":
                file_id[key] = FIT_TYPES["file"]["values"][value]["value_name"]
            elif key == "manufacturer":
                file_id[key] = FIT_TYPES["manufacturer"]["values"][value]["value_name"]
            else:
                file_id[key] = value

        return file_id

    @property
    def file_type(self) -> str:
        """
        Returns the file type of the FIT File. The file type is retrieved from the
        file_id message, which is always present in a FIT file.
        """
        return self.file_id["type"]

    @property
    def available_message_types(self) -> list[str]:
        """Returns a list of all message types that this FIT file contains"""
        return list(self.data_messages.keys())

    def get_messages_by_type(self, message_type: str) -> list[DataMessage]:
        """
        Returns all messages of the provided type, if the FIT file contains these
        messages. If not, it will return an empty list.

        If the provided message type is unknown, a ValueError will be raised.
        """
        if message_type not in MESG_NUMS.values():
            raise ValueError(f"unknown message type '{message_type}' received")

        return self.data_messages.get(message_type, [])


def decode(
    source: Union[str, Path, Streamable], calculate_crc: Optional[bool] = True
) -> FitFile:
    """
    Decode a fit file
    """
    with DataStream(source) as data:
        if not calculate_crc:
            # Don't calculate checksum
            data.should_calculate_crc = False

        header = decode_header(data)

        logger.debug(header)

        local_message_definitions: dict[int, DefinitionMessage] = {}
        developer_data: dict[int, dict[str, Any]] = {}
        messages: DefaultDict[str, list[DataMessage]] = defaultdict(list)

        while data.tell() < header.length + header.data_size:
            # Read record header
            record_header = read_record_header(data)

            # Read message
            message = read_record(
                record_header,
                local_message_definitions.get(record_header.local_message_type),
                developer_data,
                data,
            )
            logger.debug(message)

            # Assign message to correct collection
            if record_header.is_compressed_timestamp_message:
                # TODO:
                ...
            elif record_header.is_developer_data or record_header.is_definition_message:
                # TODO: check if this can be merged with is_definition_message
                local_message_definitions[record_header.local_message_type] = message
            else:
                if (
                    global_message_type := local_message_definitions.get(
                        record_header.local_message_type
                    ).global_message_type
                ) == 207:
                    # Add developer data index
                    index = message.fields["developer_data_index"]
                    developer_data[index] = message.fields
                    developer_data[index].update({"fields": {}})
                elif global_message_type == 206:
                    # Add field descriptions
                    index = message.fields["developer_data_index"]
                    field = FieldDescription(**message.fields)
                    developer_data[index]["fields"][
                        field.field_definition_number
                    ] = field

                messages[MESG_NUMS[global_message_type]].append(message)

        calculated_crc = data.calculated_crc
        (crc,) = struct.unpack("H", data.read(2))

        if calculate_crc and crc != calculated_crc:
            raise DecodeException(
                detail=(
                    "the calculated crc does not match the crc at the end of the file"
                ),
                position=data.tell(),
            )

    fitfile = FitFile(
        header=header,
        data_messages=messages,
        local_message_definitions=local_message_definitions,
        developer_data=developer_data,
    )

    return fitfile
