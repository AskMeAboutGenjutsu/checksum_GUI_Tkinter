import csv

from app_strings.app_strings import file_csv_title, files_csv_title


class CSVSaver:
    def __init__(self, filepath, info):
        self.filepath = filepath
        self.dict_info = info
        self.diff = False
        self._type_values()

    def _type_values(self):
        if isinstance(list(self.dict_info.items())[0][1], list):
            self.diff = True

    def save(self):
        with open(self.filepath, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            if self.diff:
                self._write_diff(writer)
            else:
                self._write(writer)

    def _write(self, writer):
        writer.writerow(file_csv_title)
        for i, (key, val) in enumerate(self.dict_info.items()):
            writer.writerow([i + 1, val, key])

    def _write_diff(self, writer):
        writer.writerow(files_csv_title)
        for i, (key, val) in enumerate(self.dict_info.items()):
            if val[0] == val[1]:
                writer.writerow([i + 1, val[0], val[1], key, True])
            else:
                writer.writerow([i + 1, val[0], val[1], key, False])


class CSVParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.info = {}

    def parse(self):
        with open(self.filepath, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in list(reader)[1:]:
                filename = row[2]
                filehash = row[1]
                self.info[filename] = filehash

    def get_hash(self):
        return self.info
