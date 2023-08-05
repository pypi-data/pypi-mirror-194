from pathlib import Path
import json


class Fopen:
    def __init__(
        self,
        path:Path,
        delimiter:str=',',
        enc:str='utf-8'
    ):
        self.path = path
        self.delimiter = delimiter
        self.enc = enc

    @property
    def file_type(self):    
        return self.path.rsplit('.', 1)[1]

    @property
    def content(self):
        f = open(self.path, 'r', encoding=self.enc)
        content = f.read()
        f.close()
        return content

    def clear(self):
        open(self.path, 'w').close()

    def to_json_array(self):
        f = open(self.path, 'r', encoding=self.enc)
        dict_list = []
        for line in f.readlines():
            dict_list.append(json.loads(line))
        f.close()
        return json.dumps(dict_list) 

    def read_lines(self):
        ftype = self.file_type
        if  ftype == 'csv':
            return self._csv_read_lines()
        elif ftype == 'jsonl':
            return self._jsonlines_read_lines()
        else:
            return self._txt_read_lines()

    def append_line(self, text):
        ftype = self.file_type
        if ftype == 'csv':
            return self._csv_append_line(text)
        elif ftype == 'jsonl':
            return self._jsonlines_append_line(text)
        else:
            return self._txt_append_line(text)

    def _jsonlines_read_lines(self):
        f = open(self.path, 'r', encoding=self.enc)
        for line in f.readlines():
            yield json.loads(line)
        f.close()

    def _csv_read_lines(self):
        f = open(self.path, 'r', encoding=self.enc)
        for line in f.readlines():
            stripped = line.strip()
            if len(stripped) == 0: continue
            yield stripped.split(self.delimiter)
        f.close()

    def _txt_read_lines(self):
        f = open(self.path, 'r', encoding=self.enc)
        for line in f.readlines():
            stripped = line.strip()
            yield stripped
        f.close()

    def _csv_append_line(self, word_list:list):
        f = open(self.path, 'a', encoding=self.enc)
        f.write('\n')
        for index, word in enumerate(word_list):
            if index == len(word_list) - 1:
                f.write(word)
            else:
                f.write(f'{word}{self.delimiter}')
        f.close()

    def _txt_append_line(self, text:str):
        f = open(self.path, 'a', encoding=self.enc)
        f.write(f'\n{text}')
        f.close()

    def _jsonlines_append_line(self, text):
        f = open(self.path, 'a', encoding=self.enc)
        f.write('\n')
        json.dump(text, f)
        f.close()
        