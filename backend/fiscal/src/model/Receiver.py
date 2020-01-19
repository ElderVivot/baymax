class Receiver(object):
    def __init__(self, obj):
        self._obj = obj
        self._cnpj = self._obj["cnpjReceiver"]
        self._name = self._obj["nameReceiver"]

    @property
    def cnpj(self):
        return self._cnpj

    @property
    def name(self):
        return self._name
