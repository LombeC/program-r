from programr.utils.logging.ylogger import YLogger

from programr.utils.files.filefinder import FileFinder


class MapLoader(FileFinder):

    def __init__(self, split_char=":", eol="\n"):
        self._split_char = split_char
        self._eol = eol
        FileFinder.__init__(self)

    def load_file_contents(self, id, filename, userid="*"):
        YLogger.debug(self, "Loading map [%s]", filename)
        the_map = {}
        try:
            with open(filename, 'r', encoding='utf8') as my_file:
                for line in my_file:
                    self.process_line(line, the_map)
        except Exception as excep:
            YLogger.error(self, "Failed to load map [%s] - %s", filename, excep)
        return the_map

    def load_from_text(self, text):
        the_map = {}
        lines = text.split(self._eol)
        for line in lines:
            self.process_line(line, the_map)
        return the_map

    def process_line(self, line, the_map):
        text = line.strip()
        if text is not None and text:
            splits = text.split(self._split_char)
            name = splits[0].upper()
            the_map[name] = self._split_char.join(splits[1:])


class MapCollection(object):

    def __init__(self, split_char=":", eol="\n"):
        self._split_char = split_char
        self._eol = eol
        self._maps = {}
        self._files = {}

    def empty(self):
        self._maps.clear()
        self._files.clear()

    def map(self, name):
        map_name = name.upper()
        return self._maps[map_name]

    def filename(self, mapname):
        return self._files[mapname]

    def add_map(self, name, values):
        self._maps[name.upper()] = values

    def contains(self, name):
        map_name = name.upper()
        return bool(map_name in self._maps)

    def load(self, configuration):
        loader = MapLoader(split_char=self._split_char, eol=self._eol)
        if configuration.files is not None:
            self._maps = {}
            for file in configuration.files:
                maps, file_maps = loader.load_dir_contents(file, configuration.directories, configuration.extension)
                for key in maps.keys():
                    if key in self._maps:
                        YLogger.error(self, "Duplicate map [%s] found in [%s]", key, file)
                    self._maps[key] = maps[key]
                for key in file_maps.keys():
                    self._files[key] = file_maps[key]
        else:
            self._maps = {}
        return len(self._maps)

    def reload_file(self, filename):
        loader = MapLoader(split_char=self._split_char, eol=self._eol)
        just_filename = loader.get_just_filename_from_filepath(filename)
        new_map = loader.load_file_contents(just_filename, filename)
        map_name = just_filename.upper()
        del self._maps[map_name]
        self._maps[map_name] = new_map
