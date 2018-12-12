from django.utils.encoding import force_text


class SerializationStrategy:
    def __init__(self):
        pass

    def apply(self, payload):
        return payload
