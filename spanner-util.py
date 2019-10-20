import copy
from collections import namedtuple
from decimal import Decimal
from datetime import date, datetime
from enum import Enum
import json
import os
from retrying import retry

from google.cloud import spanner
from google.api_core.exceptions import NotFound

import namutil
from app import util



instance_id = os.getenv('SPANNER_INSTANCE_ID')
database_id = os.getenv('SPANNER_DATABASE_ID')
project_name = os.getenv('SPANNER_PROJECT_NAME')

_Type = namedtuple('_Type', ['type', 'default', 'null'])

def list_of_int(val):
    # this type will be called as function for type casting.
    return list(map(int, filter(bool, map(str.strip, str(val or '').split(',')))))

def datetime_str(string):
    return datetime.strptime(string, "%Y-%m-%dT%H:%MZ")

spanner_client = spanner.Client(project_name)
instance = spanner_client.instance(instance_id)
database = instance.database(database_id)

class SpannerDB(Enum):

    @classmethod
    def get_fields(cls):
        for attr in cls.__members__.keys():
            yield attr

    @classmethod
    def get_values(cls, values_list):
        for values in values_list:
            row = []
            for attr, _type in cls.__members__.items():
                val = values.get(attr)
                try:
                    val = _type.value.type(val) if val is not None else _type.value.null
                except Exception as e:
                    logger.warn("catalog-index SpannerDB type error {0} {1} {2} {3}".format(
                        cls, e, attr, val))
                    val = _type.value.default
                row.append(val)
            yield row

    @classmethod
    def upsert(cls, table_name, values_list):
        with database.batch() as batch:
            batch.replace(
                table=table_name,
                columns=cls.get_fields(),
                values=cls.get_values(values_list)
            )


class Detail(SpannerDB):
    key_config = _Type(str, '', '')
    key_en = _Type(json.dumps, None, None)
    key_ar = _Type(json.dumps, None, None)
    updated_at = _Type(date, spanner.COMMIT_TIMESTAMP, spanner.COMMIT_TIMESTAMP)


