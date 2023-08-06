class Config():

    def __init__ (self, path, anonymize, recursive, only_dir, only_file, extensions):
        self.__path = path
        self.__anonymize = anonymize
        self.__recursive = recursive 
        self.__only_dir = only_dir 
        self.__only_file = only_file 
        self.__extensions = extensions
    
    def sanitizeOnlyFiles(self):
        return self.__only_file != None and self.__only_file

    def sanitizeOnlyDirectories(self):
        return self.__only_dir != None and self.__only_dir

    def isAnonymousName(self):
        return self.__anonymize != None and self.__anonymize

    def isRecursive(self):
        return self.__recursive != None and self.__recursive

    def hasSetSpecificExtensions(self):
        return self.__extensions != None

    def getValidExtensions(self):
        return tuple(self.__extensions.split(","))
    
    def getRootPath(self):
        return self.__path