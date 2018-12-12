import re
import pprint

default_object_regex = re.compile("model: typeclasses.defaultobject")
default_account_regex = re.compile("model: typeclasses.defaultaccount")
default_script_regex = re.compile("model: typeclasses.[^\s]+script")
default_channel_regex = re.compile("model: typeclasses.defaultchannel")

obj_typeclasses = re.compile("model: typeclasses\.(?!defaultobject|defaultaccount|defaultchannel|defaultscript|tag|attribute)[^\s]+")

object_regex = "model: objects.ObjectDB"
account_regex = "model: accounts.AccountDB"
script_regex = "model: scripts.ScriptDB"
channel_regex = "model: comms.ChannelDB"

with open('dump.yaml', 'r') as dumpfile:
  data = dumpfile.read()

work_string = re.sub(re.compile("arg: --.*\n"), "", data)
work_string = re.sub(default_object_regex, object_regex, work_string)
work_string = re.sub(default_account_regex, account_regex, work_string)
work_string = re.sub(default_script_regex, script_regex, work_string)
work_string = re.sub(default_channel_regex, channel_regex, work_string)
work_string = re.sub(r"model: typeclasses.gametime", "model: scripts.ScriptDB", work_string)
work_string = re.sub(obj_typeclasses, object_regex, work_string)

with open("parsed_dump.raw_yaml", "w") as text_file:
    text_file.write(work_string)
