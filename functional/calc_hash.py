import hashlib
import os
import sys

from app_strings.app_strings import win_platform


class Hash:
    def __init__(self, path, callback):
        self.path = path
        self._callback = callback
        self._chunk = 64
        self._platform = sys.platform
        self.hash_sum = {}

    def calc_hash(self):
        if os.path.isfile(self.path):
            hash_file = self._calc_hash_file(self.path)
            filepath = '/' + self.path.split('/')[-1]
            self.hash_sum[filepath] = hash_file
            info = f'{hash_file}\t\t\t\t{filepath}\n'
            self._callback(info)
        else:
            for root, _, files in os.walk(self.path):
                for file in files:
                    root = root.replace('\\', '/')
                    filepath = '/'.join((root, file))
                    hash_file = self._calc_hash_file(filepath)
                    filepath = filepath.replace(self.path, '')
                    info = f'{hash_file}\t\t\t\t{filepath}\n'
                    self._callback(info)
                    self.hash_sum[filepath] = hash_file

    def _calc_hash_file(self, filepath):
        with open(filepath, 'rb') as file:
            hash_file = self._get_hash_object()
            while data := file.read(self._chunk):
                hash_file.update(data)
            return hash_file.hexdigest()

    def get_hash(self):
        return self.hash_sum

    def _get_hash_object(self):
        return hashlib.md5() if self._platform == win_platform else hashlib.sha1()
