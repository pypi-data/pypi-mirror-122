import re
class Cleaner:
    def __init__(self, name):
        self.__name = name
        self.__execute()

    def get(self):
        return self.__name

    def __execute(self):
        self.__name = self.__name.lower()
        self.__name = self.__name.strip()
        self.__cleanChars()
        self.__regexReplace('[^a-zA-Z0-9\.]+', '_')
        self.__regexReplace('[-\s_]+', '_')
        self.__regexReplace('(^_|_$)', '')

    def __regexReplace(self, regex_expression, replace_char):
        self.__name = re.sub(regex_expression, replace_char, self.__name)
        
        
    def __cleanChars(self):
        from_chars = "áéíóúýñàèìòùäëïöüÿ"
        to_chars = "aeiouynaeiouaeiouy"
        self.__name = self.__name.translate(str.maketrans(from_chars, to_chars))