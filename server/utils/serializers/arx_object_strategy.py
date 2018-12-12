from .strategy import SerializationStrategy

import re


class ObjectSerializationStrategy(SerializationStrategy):
    obj_typeclasses = re.compile("typeclasses\.(?!defaultobject|defaultaccount|defaultchannel|defaultscript|tag|attribute)[^\s]+")
    script_typeclasses = "typeclasses.[^\s]+script"

    def apply(self, payload):
        self.convert_model_name(payload)

        return payload

    def convert_model_name(self, payload):
        if payload['model'] == u"typeclasses.defaultobject":
            payload['model'] = "objects.ObjectDB"
        elif payload['model'] == u"typeclasses.defaultaccount":
            payload['model'] = "accounts.AccountDB"
        elif payload['model'] == u"typeclasses.defaultchannel":
            payload['model'] = "comms.ChannelDB"
        elif payload['model'] == u"typeclasses.gametime":
            payload['model'] = "scripts.ScriptDB"
        elif re.match(self.script_typeclasses, payload['model']):
            payload['model'] = "scripts.ScriptDB"
        elif re.match(self.obj_typeclasses, payload['model']):
            payload['model'] = "objects.ObjectDB"
        return payload
