class StrUtil:
    @classmethod
    def get_base(cls, basename):
        index = basename.find('?')
        if index != -1:
            return basename[0:index]
        return basename

    @classmethod
    def filter(cls, folder_name):
        invalid_chars = set("\\/:*?\"<>|")
        return "".join(filter(lambda x: x not in invalid_chars, folder_name))

