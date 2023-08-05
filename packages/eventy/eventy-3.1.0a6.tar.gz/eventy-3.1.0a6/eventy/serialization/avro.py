# Copyright (c) Qotto, 2021
import json
import logging
import os
from datetime import datetime, timezone
from io import BytesIO
from typing import Union, Dict, Any, Optional, Iterator

import avro.schema
import semver
import yaml
from avro.datafile import DataFileWriter, DataFileReader
from avro.io import DatumWriter, AvroTypeException, DatumReader
from avro.schema import RecordSchema
from semver import VersionInfo

from eventy.record import Record, Event, Request, Response
from eventy.serialization import RecordSerializer
from eventy.serialization.errors import SerializationError, UnknownRecordTypeError

__all__ = [
    'AvroSerializer',
]

logger = logging.getLogger(__name__)


class AvroSerializer(RecordSerializer):
    """
    Avro serializer, encode and decode records in avro format.
    """

    def __init__(
        self,
    ):
        """
        Instantiate a serializer.
        """
        self.avro_schemas = {}

    def load_schemas_folder(self, schemas_folder: str, schemas_ext='.evsc.yaml', recursive=True) -> None:
        for schema_data in _load_schema_files(schemas_folder, schemas_ext, recursive):
            self.register_schema(schema_data)

    def register_schema(self, schema_data: dict) -> None:
        try:
            protocol_version = VersionInfo.parse(schema_data.pop('protocol_version'))
        except Exception:
            raise ValueError(f'Malformed schema_data, cannot parse protocol_version: {schema_data}.')

        try:
            schema = schema_data.get('schema')
        except Exception:
            raise ValueError(f'Field schema is missing: {schema_data}.')
        if schema in self.avro_schemas:
            raise ValueError(f'Schema {schema} already registered.')

        if protocol_version.match('>=2.0.0') and protocol_version.match('<3.0.0'):
            avro_schema = _gen_avro_schema_v2(**schema_data)
        else:
            raise ValueError(f'Cannot parse schema {schema}, cannot handle protocol_version {protocol_version}.')

        self.avro_schemas[schema] = avro_schema

    def encode(self, record: Record) -> bytes:
        record_schema_urn = record.schema
        avro_schema = self.avro_schemas.get(record_schema_urn)
        if not avro_schema:
            raise SerializationError(f"Could not find avro schema for record {record_schema_urn}.")

        record_dict: Dict[str, Any] = {
            'type': record.type,
            'protocol_version': record.protocol_version,
            'version': record.version,
            'source': record.source,
            'uuid': record.uuid,
            'correlation_id': record.correlation_id,
            'partition_key': record.partition_key,
            'date_timestamp': int(record.date.timestamp() * 1000),
            'date_iso8601': record.date.isoformat(),
        }
        if isinstance(record, Response):
            record_dict.update(
                {
                    'destination': record.destination,
                    'request_uuid': record.request_uuid,
                    'ok': record.ok,
                    'error_code': record.error_code,
                    'error_message': record.error_message,
                }
            )
        record_dict.update(
            {
                'context': record.context,
                'data': record.data
            }
        )

        try:
            bytes_io = BytesIO()
            with DataFileWriter(bytes_io, DatumWriter(), avro_schema) as writer:
                writer.append(record_dict)
                writer.flush()
                output_bytes = bytes_io.getvalue()
            return output_bytes
        except AvroTypeException as avro_exception:
            raise SerializationError(avro_exception)

    def decode(self, encoded: bytes) -> Union[Event, Request, Response]:
        try:
            reader = DataFileReader(BytesIO(encoded), DatumReader())
            avro_schema_data = json.loads(reader.meta.get('avro.schema').decode('utf-8'))
            avro_record_data = next(reader)
        except Exception as e:
            raise SerializationError from e

        try:
            protocol_version = VersionInfo.parse(avro_record_data.get('protocol_version'))
        except Exception:
            logger.warning(f"There was no protocol_version in record data, assuming 1.0.0")
            protocol_version = semver.VersionInfo(1)

        if protocol_version.match('<2.0.0'):
            return _decode_avro_record_v1(avro_schema_data, avro_record_data)
        elif protocol_version.match('<3.0.0'):
            return _decode_avro_record_v2(avro_schema_data, avro_record_data)
        else:
            raise ValueError(f"Cannot handle protocol_version {protocol_version}.")


def _decode_avro_record_v1(avro_schema_data: dict, avro_record_data: dict) -> Union[Event, Request, Response]:
    # build a record_data with correct format
    record_data = dict()

    # get record type
    record_type = avro_record_data.pop('type', 'EVENT')

    # get mandatory data
    record_data['protocol_version'] = avro_record_data.pop('protocol_version', '1.0.0')
    record_data['schema'] = avro_record_data.pop(
        'schema',
        _namespace_name_to_schema_urn(avro_schema_data['namespace'], avro_schema_data['name'])
    )
    record_data['version'] = avro_record_data.pop('version', '1.0.0')
    record_data['source'] = avro_record_data.pop('source', 'urn:unknown')

    # get optional data
    for meta_key in [
        'uuid', 'correlation_id', 'partition_key', 'context',
    ]:
        if meta_key in avro_record_data:
            record_data[meta_key] = avro_record_data.pop(meta_key)

    # get date from timestamp
    for timestamp_key in [
        'timestamp', 'timestamp_ms',
        'date_timestamp', 'date_timestamp_ms',
        'event_timestamp', 'event_timestamp_ms',
    ]:
        if timestamp_key in avro_record_data:
            timestamp = avro_record_data.pop(timestamp_key)
            if 'date' not in record_data:
                record_data['date'] = datetime.fromtimestamp(timestamp / 1000, timezone.utc)

    # get date from iso string
    for date_iso_key in [
        'date_iso', 'date_iso8601',
    ]:
        if date_iso_key in avro_record_data:
            date_iso = avro_record_data.pop(date_iso_key)
            if 'date' not in record_data:
                record_data['date'] = datetime.fromisoformat(date_iso)

    # add data fields
    record_data['data'] = dict()
    record_data['data'].update(avro_record_data.pop('data', {}))
    record_data['data'].update(avro_record_data)

    if record_type == 'EVENT':
        return Event(**record_data)
    elif record_type == 'REQUEST':
        return Request(**record_data)
    elif record_type == 'RESPONSE':
        return Response(**record_data)
    else:
        raise UnknownRecordTypeError(record_type)


def _decode_avro_record_v2(avro_schema_data: dict, avro_record_data: dict) -> Union[Event, Request, Response]:
    name = avro_schema_data['name']
    namespace = avro_schema_data['namespace']
    schema = _namespace_name_to_schema_urn(namespace, name)
    record_type = avro_record_data.pop('type')

    date = datetime.fromisoformat(avro_record_data.pop('date_iso8601'))
    avro_record_data.pop('date_timestamp')

    avro_record_data['date'] = date
    avro_record_data['schema'] = schema

    if record_type == 'EVENT':
        return Event(**avro_record_data)
    elif record_type == 'REQUEST':
        return Request(**avro_record_data)
    elif record_type == 'RESPONSE':
        return Response(**avro_record_data)
    else:
        raise UnknownRecordTypeError(record_type)


def _gen_avro_schema_v2(
    schema: str,
    type: str,
    doc: Optional[str] = None,
    data_fields: Optional[list] = None,
) -> RecordSchema:
    name = schema.split(':')[-1]
    namespace = '.'.join(schema.split(':')[1:-1])
    if type not in ['EVENT', 'REQUEST', 'RESPONSE']:
        raise ValueError(f'Cannot parse eventy schema {schema}, type must be EVENT, REQUEST, or RESPONSE.')

    fields = [
        {
            'name': 'type',
            'type': {
                'name': 'RecordType',
                'type': 'enum',
                'symbols': [type]
            },
            'doc': 'Type of of record: one of EVENT, REQUEST or RESPONSE',
        },
        {
            'name': 'protocol_version',
            'type': 'string',
            'doc': 'Version of the Eventy protocol used for encoding this message (semver format: X.Y.Z)',
        },
        {
            'name': 'version',
            'type': 'string',
            'doc': 'Version of the schema used for encoding this message (semver format: X.Y.Z)',
        },
        {
            'name': 'source', 'type': 'string',
            'doc': 'Source of the record (URN of the producing service)',
        },
        {
            'name': 'uuid', 'type': 'string', 'logicalType': 'uuid',
            'doc': 'UUID for this record',
        },
        {
            'name': 'correlation_id', 'type': 'string',
            'doc': 'Identifier propagated across the system and to link associated records together',
        },
        {
            'name': 'partition_key', 'type': ['string', 'null'],
            'doc': 'A string determining to which partition your record will be assigned',
        },
        {
            'name': 'date_timestamp', 'type': 'long', 'logicalType': 'timestamp-millis',
            'doc': 'UNIX timestamp in milliseconds',
        },
        {
            'name': 'date_iso8601', 'type': 'string',
            'doc': 'ISO 8601 date with timezone',
        },
    ]
    if type == 'RESPONSE':
        fields += [
            {
                'name': 'destination', 'type': 'string',
                'doc': 'URN of the destination service',
            },
            {
                'name': 'request_uuid', 'type': 'string',
                'doc': 'UUID of the associated request',
            },
            {
                'name': 'ok', 'type': 'boolean',
                'doc': 'Status: True if there was no error, false otherwise',
            },
            {
                'name': 'error_code', 'type': ['null', 'int'],
                'doc': 'Numeric code for the error, if ok is False, null otherwise',
            },
            {
                'name': 'error_message', 'type': ['null', 'string'],
                'doc': 'Description for the error, if ok is False, null otherwise',
            },
        ]
    fields += [
        {
            'name': 'context', 'type':
            {
                'type': 'map', 'values':
                {
                    'type': 'map',
                    'values': ['string', 'double', 'float', 'long', 'int', 'boolean', 'null']
                }
            },
            'doc': 'Context data, always propagated'
        },
        {
            'name': 'data', 'type':
            {
                'type': 'record', 'name': f'{name}_data', 'namespace': namespace, 'fields':
                data_fields or []
            },
            'doc': 'Record payload',
        }
    ]
    schema_dict = {
        'name': name,
        'namespace': namespace,
        'doc': doc or f'{name} {type} Record',
        'type': 'record',
        'fields': fields,
    }
    return avro.schema.parse(json.dumps(schema_dict))


def _load_schema_files(
    schemas_folder: str,
    schemas_ext: str,
    recursive: bool,
) -> Iterator[dict]:
    with os.scandir(schemas_folder) as entries:
        entry: os.DirEntry
        for entry in entries:

            # load in sub folder if recursive option set
            if entry.is_dir():
                if recursive:
                    yield from _load_schema_files(entry.path, schemas_ext, recursive)
                else:
                    continue

            # ignores everything that is not a file
            if not entry.is_file():
                continue  # pragma: nocover

            # ignores hidden files
            if entry.name.startswith("."):
                continue  # pragma: nocover

            # ignores everything files with wrong extension
            if not entry.name.endswith(schemas_ext):
                continue  # pragma: nocover

            with open(entry.path) as avro_yml:
                yaml_data = yaml.load(avro_yml.read(), Loader=yaml.SafeLoader)
                yield yaml_data


def _schema_urn_to_avro_namespace(schema_urn: str) -> str:
    if schema_urn.startswith('urn:'):
        schema_urn = schema_urn[4:]
    return '.'.join(schema_urn.split(':')[0:-1])


def _schema_urn_to_avro_name(schema_urn: str) -> str:
    return schema_urn.split(':')[-1]


def _namespace_name_to_schema_urn(namespace: str, name: str) -> str:
    return f'urn:{namespace.replace(".", ":")}:{name}'
