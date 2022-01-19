import sys

if __name__ == "__main__":
    _, pathToScript, className, methodName, jsonArguments = sys.argv

    sys.path.append(pathToScript)

    import main
    
    # Get the class itself and create an instance
    theclass = getattr(main, className)
    obj = theclass()
    
    # Get the method to be called
    thefunc = getattr(obj, methodName)
    
    # Result of the invoked method is printed to the stdout and caught by the PythonCaller class
    print(thefunc(jsonArguments))
