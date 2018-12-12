import sys
from io import StringIO

from django.core.serializers.pyyaml import Serializer as YamlSerializer
from django.core.serializers.base import DeserializationError
from django.core.serializers.python import (
    Deserializer as PythonDeserializer
)
from evennia.utils import dbserialize

import yaml
from base64 import b64decode

from django.conf import settings
from pydoc import locate
from .strategy import SerializationStrategy

try:
    from yaml import CSafeLoader as SafeLoader
    from yaml import CSafeDumper as SafeDumper
except ImportError:
    from yaml import SafeLoader, SafeDumper


class Serializer(YamlSerializer):
    internal_use_only = False
    serialization_type = 'raw_yaml'

    def __init__(self):
        self.serializer = self.load_serializer()

    def load_serializer(self):
        serialization_strategy_path = settings.OBJECT_SERIALIZATION_STRATEGY[self.serialization_type]

        if not serialization_strategy_path:
            return SerializationStrategy()

        return locate(serialization_strategy_path)()

    def get_dump_object(self, obj):
        data = super(Serializer, self).get_dump_object(obj)

        return self.serializer.apply(data)

    def handle_field(self, obj, field):
        super(Serializer, self).handle_field(obj, field)


def Deserializer(stream_or_string, **options):
    if isinstance(stream_or_string, bytes):
        stream_or_string = stream_or_string.decode()
    if isinstance(stream_or_string, str):
        stream = StringIO(stream_or_string)
    else:
        stream = stream_or_string
    fixture = yaml.load(stream, Loader=SafeLoader)

    for record in fixture:
        if record["model"] == "typeclasses.attribute":
            db_val = record["fields"]["db_value"]
            if db_val and (isinstance(db_val, str) or isinstance(db_val, unicode)):
                record["fields"]["db_value"] = dbserialize.do_unpickle(b64decode(db_val))

    try:
        for obj in PythonDeserializer(fixture, **options):
            yield obj
    except GeneratorExit:
        raise
    except Exception as e:
        # Map to deserializer error
        six.reraise(DeserializationError, DeserializationError(e), sys.exc_info()[2])


