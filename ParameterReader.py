
class ParameterException(Exception): pass

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
        self._parse_values(argv)
        self._check_requirements()

    def try_get_value(self, key, default):
        # Return default if parameter doesn't exist or isn't set.
        if(key not in self._definedParams or not self._definedParams[key].value): return default
        return self._definedParams[key].value

    def has_value(self, *args):
        for param in args:
            if(self._definedParams[param].value): return True

        return False

    # Print full usage and generates text for each defined parameter.
    def print_usage(self):
        print(self.usage + "\n")

        for key, param in self._definedParams.items():
            print(key + "\t" + param.description)

    def _check_requirements(self):
        for key, param in self._definedParams.items():
            if(not param.value): continue # Check Requirment only if value is set.

            for requirment in param.requires: self._check_requirement(requirment)
                
    def _check_requirement(self, requirment):
        if(requirment not in self._definedParams): raise ParameterException("Requirment [" + requirment + "] is not defined")
        if(not self._definedParams[requirment].value): raise ParameterException("Parameter [" + requirment + "] needs to be defined.")
    
    def _parse_values(self, argv):
        i = 1 # Skip the program name.
        while(i < len(argv)):
            arg = argv[i]

            # End program right away to display help text.
            if(arg in ("-h", "/h", "--Help")): 
                raise ParameterException("Help")
                return

            if(arg not in self._definedParams): raise ParameterException("Parameter [" + arg + "] is not defined")
            
            argDefinition = self._definedParams[arg]
            
            if(argDefinition.expectsValue):
                i += 1 # Get next argument which is the value.
                
                # Check if arg is out of reach
                if(i >= len(argv)): raise ParameterException("Parameter [" + arg + "] expects a value")
                argDefinition.value = argv[i]
            else:
                argDefinition.value = True

            i += 1