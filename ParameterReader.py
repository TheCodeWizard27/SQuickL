
class ParameterDefinition:
    def __init__(
        self
        ,description = ""
        ,requires = []
        ,expectsValue = True
        ):
        self.description = description
        self.expectsValue = expectsValue
        self.requires = requires
        self.value = None

class ParameterReader:
    def __init__(self, usage, definedParams):
        self.usage = usage
        self._definedParams = definedParams
    
    def parse(self, argv):
        self._parseValues(argv)
        self._checkRequirements()

    def tryGetValue(self, key, default):
        # Return default if parameter doesn't exist or isn't set.
        if(key not in self._definedParams or not self._definedParams[key]): return default
        return self._definedParams[key].value

    def hasValue(self, key): return key in self._definedParams and self._definedParams[key]

    def printUsage(self):
        print(self.usage + "\n")

        for key, param in self._definedParams.items():
            print(key + "\t" + param.description)

    def _checkRequirements(self):
        for key, param in self._definedParams.items():
            if(not param.value): continue # Check Requirment only if value is set.

            for requirment in param.requires: self._checkRequirement(requirment)
                
    def _checkRequirement(self, requirment):
        if(requirment not in self._definedParams): raise Exception("Requirment [" + requirment + "] is not defined")
        if(not self._definedParams[requirment].value): raise Exception("Parameter [" + requirment + "] needs to be defined.")
    
    def _parseValues(self, argv):
        i = 1 # Skip the program name.
        while(i < len(argv)):
            arg = argv[i]

            if(arg in ("-h", "/h", "--Help")): 
                self.printUsage() 
                return

            if(arg not in self._definedParams): raise Exception("Parameter [" + arg + "] is not defined")
            
            argDefinition = self._definedParams[arg]
            
            if(argDefinition.expectsValue):
                i += 1 # Get next argument which is the value.
                
                # Check if arg is out of reach
                if(i >= len(argv)): raise Exception("Parameter [" + arg + "] expects a value")
                argDefinition.value = argv[i]
            else:
                argDefinition.value = True

            i += 1