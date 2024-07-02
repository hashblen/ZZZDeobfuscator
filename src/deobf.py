import tools


class Deobf:
    def __init__(self, name):
        self.name = name
        self.obfuscated = tools.read_obfuscated(self.name + ".json")
        self.example = tools.read_example(self.name + "Example.json")
        self.deobfuscated = None
        self.key_mapping = None

    def create_key_mapping(self):
        key_mapping = {}
        for obfuscated_item in self.obfuscated[next(iter(self.obfuscated.keys()))]:
            for obfuscated_key, deobfuscated_key in zip(obfuscated_item.keys(), self.example.keys()):
                key_mapping[obfuscated_key] = deobfuscated_key
        self.key_mapping = key_mapping

    def deobfuscate(self, makeID=None):
        if self.key_mapping is None:
            self.create_key_mapping()
        deobfuscated_data = {}
        for item in self.obfuscated[next(iter(self.obfuscated.keys()))]:
            deobfuscated_item = {}
            id = None
            for obfuscated_key, value in item.items():
                if makeID is not None and self.key_mapping[obfuscated_key] == makeID:
                    id = str(value)
                deobfuscated_item[self.key_mapping[obfuscated_key]] = value
            if makeID is not None and id is None:
                raise ValueError("ID was not found!")
            deobfuscated_data[id] = deobfuscated_item
        self.deobfuscated = deobfuscated_data

    def save_deobfuscated(self, makeID=None):
        if self.deobfuscated is None:
            self.deobfuscate(makeID=makeID)
        tools.write_deobfuscated(self.deobfuscated, self.name + ".json")