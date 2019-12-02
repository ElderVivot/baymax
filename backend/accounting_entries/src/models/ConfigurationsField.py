class ConfigurationsField(object):
    def __init__(self, startPosition, endPosition=0, fieldFormat=''):
        self.__startPosition = startPosition
        self.__endPosition = endPosition
        self.__fieldFormat = fieldFormat

    @property
    def startPosition(self):
        return self.__startPosition

    @property
    def endPosition(self):
        return self.__endPosition

    @property
    def fieldFormat(self):
        return self.__fieldFormat
