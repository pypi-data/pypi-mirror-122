import os, pprint, uuid
from pathlib import Path
from ns.cleaner import Cleaner

class Sanitizer():
    
    def __init__(self, config):
        self.__config = config
        self.IS_FILE = 1
        self.IS_DIR = 2

    def start(self):
        if not self.__config.sanitizeOnlyDirectories() and not self.__config.sanitizeOnlyFiles():
            self.__cleanFileNames()
            self.__cleanFolderNames()
        else:
            if self.__config.sanitizeOnlyDirectories():
                self.__cleanFolderNames()
            if self.__config.sanitizeOnlyFiles():
                self.__cleanFileNames()
    
    def __cleanFolderNames(self):
        folders = self.__getFolders()
        folders = folders[::-1]
        for folder in folders:
            name = self.__processName(folder['name'], folder['path'], self.IS_DIR)
            output = "{}{}{}".format(folder['path'], os.path.sep, name)
            try:
                os.rename(folder['full_path'], output)
            except FileExistsError:
                name = self.__doUniqueName(name, folder['path'])
                output = "{}{}{}".format(folder['path'], os.path.sep, name)
                os.rename(folder['full_path'], output)

    def __getFolders(self):
        output = []
        for root, dirs, files in os.walk(self.__config.getRootPath()):
            for directory in dirs:
                path = "{}{}{}".format(root, os.path.sep, directory)
                output.append({'path': root, 'full_path': path, 'name': directory})
            if not self.__config.isRecursive():
                break
        return output

    def __cleanFileNames(self):
        files = self.__getFiles()
        for file in files:
            name = self.__processName(file['name'], file['path'], self.IS_FILE)
            output = "{}{}{}".format(file['path'], os.path.sep, name)
            try:
                os.rename(file['full_path'], output)
            except FileExistsError:
                name = self.__doUniqueName(name, file['path'])
                output = "{}{}{}".format(file['path'], os.path.sep, name)
                os.rename(file['full_path'], output)

    def __getFiles(self):
        output = []
        for root, dirs, files in os.walk(self.__config.getRootPath()):
            for file in files:
                if self.__config.hasSetSpecificExtensions():
                    if file.endswith(self.__config.getValidExtensions()):
                        path = "{}{}{}".format(root, os.path.sep, file)
                        output.append({'path': root, 'full_path': path, 'name': file})
                else:
                    path = "{}{}{}".format(root, os.path.sep, file)
                    output.append({'path': root, 'full_path': path, 'name': file})
            if not self.__config.isRecursive():
                break
        return output
    
    def __processName(self, name, path, element_type):
        name = Cleaner(name).get()
        if self.__config.isAnonymousName():
            name = self.__getAnonymousName(name, element_type)
        return name      

    def __getAnonymousName(self, name, element_type):
        new_name = uuid.uuid4().hex
        if element_type == self.IS_DIR:
            return new_name
        extensions = name.split(".")
        del extensions[0]
        for extension in extensions:
            new_name = "{}.{}".format(new_name, extension)
        return new_name

    def __doUniqueName(self, name, path):
        if not os.path.exists("{}{}{}".format(path, os.path.sep, name)):
            return name
        else:
            counter = 1
            while True: 
                temp_name = "{}_{}".format(counter, name)
                if not os.path.exists("{}{}{}".format(path, os.path.sep, temp_name)):
                    break
                else:
                    counter = counter + 1
            return "{}_{}".format(counter, name)
        
