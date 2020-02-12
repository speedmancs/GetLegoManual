import math

class FileUtil:
    @classmethod
    def writelines(cls, lines, output_file, newline=True):
        with open(output_file, mode='w', encoding='utf-8') as file:
            if newline:
                file.writelines('\n'.join(lines))
            else:
                file.writelines(lines)

    @classmethod
    def load_csv(cls, input_file):
        results = []
        with open(input_file, mode='r', encoding='utf-8') as file:
            for item in file.readlines():
                results.append(tuple(item.rstrip().split(',')))
        return results

    @classmethod
    def split(cls, input_file, parts):
        with open(input_file, mode='r', encoding='utf-8') as file:
            lines = file.readlines()
        count = math.floor(len(lines) / parts)
        index = 0
        for i in range(0, parts):
            if i == parts - 1:
                count = len(lines) - index
            FileUtil.writelines(lines[index:count + index], output_file=f'{input_file}.{i}', newline=False)
