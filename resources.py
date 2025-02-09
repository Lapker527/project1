
import os
import json

def print_with_indent(value, indent=4):
    indentation = '\t' * indent
    print(f'{indentation}{value}')

class Entry:
    def __init__(self, title, entries=None, parent=None):
        self.title = title
        if entries is None:
            entries = []
        self.entries = entries
        self.parent = parent

    @classmethod
    def from_json(cls, value):
        entry = cls(value['title'])
        for sub_entry in value.get('entries', []):
            entry.add_entry(cls.from_json(sub_entry))
        return entry

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as f:
            content = json.load(f)
            return cls.from_json(content)

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent=indent + 1)

    def json(self):
        res = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]
        }
        return res

    def save(self, path):
        filename = os.path.join(path, self.title)
        content = self.json()
        with open(f'{filename}.json', 'w') as f:
            json.dump(content, f)
    #def save(self, path):
    #    filename = f'{self.title}.json'
    #    full_path = os.path.join(path, filename)

    #    with open(full_path, 'w', encoding='utf-8') as f:
    #        json.dump(self.json(), f, ensure_ascii=False, indent=4)
    def __str__(self):
        return self.title

grocery_list = {
    "title": "Продукты",
    "entries": [
        {
            "title": "Молочные",
            "entries": [
                {
                    "title": "Йогурт",
                    "entries": []
                },
                {
                    "title": "Сыр",
                    "entries": []
                }
            ]
        }
    ]
}
if __name__ == '__main__':
    entry = Entry('Продукты')
    entry.add_entry(Entry('Молоко'))
    entry.add_entry(Entry('Кофе'))
    entry.add_entry(Entry('Хлеб'))
    entry.add_entry(Entry('Яйца'))
    entry.print_entries()
entry = Entry.from_json(grocery_list)

entry.save('C:\\Users\\avosa\\PycharmProjects')
loaded_entry = Entry.load('C:\\Users\\avosa\\PycharmProjects\\Продукты.json')

if loaded_entry:
    print(f'Загружено: {loaded_entry.title}')
    for sub_entry in loaded_entry.entries:
        print(f' - {sub_entry.title}')


import os

class EntryManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.entries = []

    def load(self):
        if not os.path.isdir(self.data_path):
            os.makedirs(self.data_path)
        else:
            for filename in os.listdir(self.data_path):
                if filename.endswith('json'):
                    entry = Entry.load(os.path.join(self.data_path, filename))
                    self.entries.append(entry)
        return self

    def add_entry(self, title):
        self.entries.append(Entry(title))
    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

