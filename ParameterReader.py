
class ParameterDefinition:
    def __init__(
        self
        ,description = ""
        ,expectsValue = True
        ,optional = True
        ):
        self.description = description
        self.expectsValue = expectsValue
        self.optional = optional

class ParameterReader:
    def __init__(self, definedParams):
        self._definedParams = definedParams
    
    def parse(self, argv):
        print(argv)

    