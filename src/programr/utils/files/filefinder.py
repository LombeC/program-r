from programr.utils.logging.ylogger import YLogger
import os

from abc import ABCMeta, abstractmethod

class FileFinder(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def load_file_contents(self, id, filename, userid="*"):
        """
        Never Implemented
        """

    def find_files(self, path, subdir=False, extension=None):
        found_files = []
        try:
            if subdir is False:
                paths = os.listdir(path)
                for filename in paths:
                    if filename.endswith(extension):
                        found_files.append((filename, os.path.join(path, filename)))
            else:
                for dirpath, _, filenames in os.walk(path):
                    for filename in [f for f in filenames if f.endswith(extension)]:
                        found_files.append((filename, os.path.join(dirpath, filename)))
        except FileNotFoundError:
            YLogger.error(self, "No directory found [%s]", path)

        return sorted(found_files, key=lambda element: (element[1], element[0]))

    def load_dir_contents(self, paths, subdir=False, extension=".txt", filename_as_userid=False):
        # print("Paths: {}".format(paths))
        # print("Subdir: {}".format(subdir))
        files = self.find_files(paths, subdir, extension)
        # print("Files: {}".format(files))

        collection = {}
        file_maps = {}
        for file in files:
            just_filename = self.get_just_filename_from_filepath(file[0])
            try:
                if filename_as_userid is True:
                    userid = just_filename
                else:
                    userid = "*"
                collection[just_filename.upper()] = self.load_file_contents(just_filename, file[1], userid=userid)
                file_maps[just_filename.upper()] = file[1]
            except Exception as excep:
                print(excep)
                YLogger.exception(self, "Failed to load file contents for file [%s]"% file[1], excep)

        return collection, file_maps

    def load_single_file_contents(self, filename):
        just_filename = self.get_just_filename_from_filepath(filename)

        collection = {}
        try:
            collection[just_filename] = self.load_file_contents(just_filename, filename)
        except Exception as excep:
            YLogger.exception(self, "Failed to load file contents for file [%s]"%filename, excep)

        return collection

    def get_just_filename_from_filepath(self, filepath):

        if os.sep in filepath:
            pathsplits = filepath.split(os.sep)
            filename_ext = pathsplits[-1]
        else:
            filename_ext = filepath

        if "." in filename_ext:
            filesplits = filename_ext.split(".")
            filename = filesplits[0]
        else:
            filename = filename_ext

        return filename
